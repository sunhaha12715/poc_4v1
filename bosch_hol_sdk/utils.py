'''
Random utilities and helper functions.

@copyright
    Copyright 2023, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
    All rights reserved.
'''
import logging
import pathlib
import shlex
import subprocess
import time
import typing

import paramiko

from dspace.bosch_hol_sdk import defaults


PathLikeType = typing.Union[pathlib.PurePosixPath, str]


def ping(ip, logger=None):
    if logger is None:
        root_logger = logging.getLogger()
    else:
        root_logger = logger
    logger = root_logger.getChild(f"ping_{ip}")

    try:
        subprocess.check_output(['ping', '-c', '1', ip], text=True)
    except subprocess.CalledProcessError as exc:
        # Attempt to extract the failure reason if it exists.
        reason = ""
        if exc.stdout:
            for line in exc.stdout.splitlines():
                if line.startswith('From'):
                    try:
                        *_, reason = line.split(" ", 3)
                    except IndexError:
                        continue
                    else:
                        reason = f': {reason}'
                        break
        logger.info(f"Ping statistics for {ip}: Lost=100%{reason}")
        return False
    else:
        logger.info(f"Ping statistics for {ip}: Lost=0%")
        return True


def run_file_remotely(
    file,
    *args,
    remote_ip,
    username,
    password,
    sudo_password=None,
    paramiko_log_level=logging.INFO,
) -> tuple[str, str]:
    """ Copies a file to a remote host, executes it and then deletes it. """
    file = pathlib.Path(file)

    # Limit paramiko's logs.
    logging.getLogger('paramiko').setLevel(paramiko_log_level)

    with paramiko.SSHClient() as ssh:
        # Open connect to remote.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=remote_ip,
            username=username,
            password=password,
        )

        remote_path = f'/tmp/{file.name}'
        # Copy the file to the remote host and make it executable.
        sftp = ssh.open_sftp()
        sftp.put(file, remote_path)
        sftp.chmod(remote_path, 0o755)

        # Make sure we have unix line endings (dos2unix is not installed).
        _, _, stderr = ssh.exec_command(f"sed -i 's/\\r$//' {remote_path}")
        exit_status = stderr.channel.recv_exit_status()
        if exit_status != 0:
            error = stderr.read().decode('utf-8')
            raise RuntimeError(f'Failed to run sed: {error}')

        # Run the file.
        cmd = [remote_path, *args]
        if sudo_password is None:
            _, stdout, stderr = ssh.exec_command(shlex.join(cmd))
            outputs = (
                stdout.read().decode('utf-8'),
                stderr.read().decode('utf-8'),
            )
        else:
            cmd_str = f'echo {sudo_password} | sudo --stdin {shlex.join(cmd)}'
            _, stdout, stderr = ssh.exec_command(cmd_str)
            stderr.read().decode('utf-8')
            if stderr.startswith('[sudo]'):
                if 'incorrect password attemp' in stderr:
                    raise ValueError('Wrong sudo password')
                else:
                    _, stderr = stderr.split(':', 1)
            outputs = (
                stdout.read().decode('utf-8'),
                stderr,
            )

        # Delete the file.
        ssh.exec_command(f'rm -f {remote_path}')

        return outputs


def execute_command(
    cmd: list,
    logger: typing.Optional[logging.Logger] = None,
    **kwargs: typing.Any
) -> bool:
    logger = logger or logging.getLogger('DRAPI.utils.execute_command')
    result = subprocess.run(cmd, text=True, capture_output=True, **kwargs)

    err_msgs = False
    stderr = result.stderr.strip().splitlines()
    for line in stderr:
        err_msgs = True
        logger.error(line)

    stdout = result.stdout.strip().splitlines()
    for line in stdout:
        logger.info(line)

    logger.info(f'Command "{cmd}" finished with code {result.returncode}')

    # With error -> return False,  no error -> return True
    return result.returncode == 0 and not err_msgs


def download_sclx_app(
    sdf_path: str,
    scalexios: list = [],
    cmdloader: PathLikeType = defaults.CMDLOADER_PATH,
    platform: str = defaults.PLATFORM,
    on_error: str = 'unload',
    logger: typing.Optional[logging.Logger] = None,
):
    logger = logger or logging.getLogger('DRAPI.utils.download_sclx_app')
    # Register platform and download application in one step.
    logger.info(f'Loading the real-time application: {sdf_path}')
    register_cmd = [
        cmdloader,
        '-ra'
    ]

    if not execute_command(register_cmd, logger=logger):
        logger.error('Failed to register platform "{platform}"')
        # There is no point of restarting the SCALEXIO or trying to load.
        return False

    load_cmd = [
        cmdloader,
        '-p', platform,
        sdf_path
    ]

    if not execute_command(load_cmd, logger=logger):
        if not scalexios:
            # There is not point of retrying anything if we have no instances
            # of the used SCALEXIO systems.
            return False

        if on_error == 'unload':
            logger.info('Failed to load application.')
            logger.info(
                'Attempting to unload previous applications and trying again.'
            )
            for sclx in scalexios:
                try:
                    sclx.unload()
                except Exception:
                    logger.exception('Failed to unload the application')
            # Try again.
            return download_sclx_app(
                sdf_path=sdf_path,
                scalexios=scalexios,
                cmdloader=cmdloader,
                platform=platform,
                on_error='reboot',
                logger=logger,
            )
        elif on_error == 'reboot':
            logger.info(
                'Failed to load application. Rebooting HIL and trying again.'
            )
            for sclx in scalexios:
                sclx.reboot()
            # Sleep 10 seconds first. There is no point of starting pinging
            # right away and it might even repsond if it's pinged too soon.
            time.sleep(10)
            for sclx in scalexios:
                sclx.wait_till_online(60)
            # Now try one last time.
            return download_sclx_app(
                sdf_path=sdf_path,
                scalexios=scalexios,
                cmdloader=cmdloader,
                platform=platform,
                on_error='fail',
                logger=logger,
            )
        else:
            logger.error('Downloading application failed!')
            return False

    logger.info('Downloading application finished successfully')
    return True


def unload_sclx_app(
    cmdloader: PathLikeType = defaults.CMDLOADER_PATH,
    platform: str = defaults.PLATFORM,
    logger: typing.Optional[logging.Logger] = None,
):
    logger = logger or logging.getLogger('DRAPI.utils.unload_sclx_app')
    # control desk application unload
    logger.info('Unloading the real-time application.')
    ret = execute_command(
        [cmdloader, '-unload', '-p', platform, '-ol', '2'],
        logger=logger,
    )
    if not ret:
        logger.error('Unloading application failed!')
        return False

    logger.info('Unloading application finished successfully')
    return True
