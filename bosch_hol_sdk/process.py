import logging
import paramiko
import shlex
import subprocess
import time


class Process(object):
    def __new__(
            cls,
            args,
            *extra_args,
            sudo=None,
            logger=None,
            remote_credentials=None,
            **kwargs,
    ):
        if remote_credentials is None:
            return super().__new__(LocalProcess, *extra_args, **kwargs)
        else:
            return super().__new__(RemoteProcess, *extra_args, **kwargs)

    def __init__(self, *args, logger=None, remote_credentials=None, **kwargs):
        super().__init__(*args, **kwargs)
        logger = logger or logging.getLogger()
        self._logger = logger.getChild(self.__class__.__name__)

    def start(self):
        raise NotImplementedError('start()')

    def stop(self):
        raise NotImplementedError('stop()')

    @property
    def running(self):
        raise NotImplementedError('running')

    @property
    def output(self):
        raise NotImplementedError('output')

    @property
    def exit_code(self):
        raise NotImplementedError('exit_code')


class LocalProcess(Process):
    def __init__(self, args, *extra_args, sudo=None, **kwargs):
        super().__init__(*extra_args, **kwargs)
        if sudo is not None:
            args = ['sudo', '--stdin', *args]
            if isinstance(sudo, str):
                sudo = sudo.encode()
            if not sudo.endswith(b'\n'):
                sudo += b'\n'
        self._args = args
        self._sudo = sudo
        self._proc = None
        self._stopped = False

    def start(self):
        if self._proc is not None:
            raise RuntimeError('Process already started')
        self._proc = subprocess.Popen(
            self._args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        # We expect the timeout-exception from communcate. if not it means
        # The process died!
        try:
            self._proc.communicate(self._sudo, 0.5)
        except subprocess.TimeoutExpired:
            pass

    def stop(self):
        if self._proc is None:
            raise RuntimeError('Process not started')
        if self._stopped:
            return

        if not self.running:
            self._logger.info('The process is already dead')
            self._stopped = True
            return

        self._logger.info('Terminating the process')
        try:
            self._proc.terminate()
            self._proc.wait(2)
        except (subprocess.TimeoutExpired, PermissionError):
            pass
        else:
            self._stopped = True
            return

        self._logger.info('Killing the process')
        try:
            self._proc.kill()
            self._proc.wait(1)
        except (subprocess.TimeoutExpired, PermissionError):
            pass
        else:
            self._stopped = True
            return

        self._logger.info('Starting a kill process!')
        LocalProcess(['kill', str(self._proc.pid)], sudo=self._sudo).start()
        try:
            self._proc.wait(1)
        except subprocess.TimeoutExpired:
            self._logger.error('Failed to terminate process')
        else:
            self._stopped = True

    @property
    def running(self):
        if self._proc is None:
            return False
        return self._proc.poll() is None

    @property
    def output(self):
        if self._proc is None:
            raise RuntimeError('Process not started')
        if self.running:
            return None
        return self._proc.stdout.readlines()

    @property
    def exit_code(self):
        if self._proc is None:
            raise RuntimeError('Process not started')
        return self._proc.returncode


class RemoteProcess(Process):
    def __init__(
            self,
            args,
            *extra_args,
            remote_credentials,
            sudo=None,
            **kwargs,
    ):
        super().__init__(*extra_args, **kwargs)
        if sudo is not None:
            args = ['sudo', '--stdin', *args]
            if isinstance(sudo, str):
                sudo = sudo.encode()
            if not sudo.endswith(b'\n'):
                sudo += b'\n'
        self._cmd = shlex.join(args)
        self._credentials = remote_credentials
        self._sudo = sudo
        self._stdio = None
        self._stopped = False

    def start(self):
        self._logger.debug(f'Running remote process: {self._cmd}')
        self._ssh = paramiko.SSHClient()
        # Open connect to remote.
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(**self._credentials)
        self._stdio = self._ssh.exec_command(self._cmd, get_pty=True)

        if self._sudo:
            self._stdio[0].write(self._sudo)

    def stop(self):
        if self._stdio is None:
            raise RuntimeError('Process not started')
        if self._stopped:
            return

        if not self.running:
            self._logger.info('The process is already dead')
            self._stopped = True
            return

        ch = self._stdio[0].channel

        self._logger.info('Interrupting the remote process (CTRL+C)')
        ch.send(u'\x03')

        for _ in range(10):
            time.sleep(0.02)
            if not self.running:
                self._logger.info('The process is stopped.')
                self._stopped = True
                break
        else:
            self._logger.warning('Failed to stop remote tcpdump!')

        self._ssh.close()

    @property
    def running(self):
        if self._stdio is None:
            return False
        return not self._stdio[0].channel.exit_status_ready()

    @property
    def output(self):
        if self._stdio is None:
            raise RuntimeError('Process not started')
        return self._stdio[1].channel.recv(-1).splitlines()

    @property
    def exit_code(self):
        if self._stdio is None:
            raise RuntimeError('Process not started')
        if self.running:
            return None
        return self._stdio[1].channel.recv_exit_status()
