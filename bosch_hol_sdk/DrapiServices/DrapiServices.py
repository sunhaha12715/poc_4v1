#!/usr/bin/env python3.9
import argparse
from concurrent import futures
import json
import logging
import signal
import sys
import time

import grpc

from dspace.bosch_hol_sdk import defaults
from dspace.bosch_hol_sdk import DrapiServices_pb2, DrapiServices_pb2_grpc
from dspace.bosch_hol_sdk import get_version_tuple
from dspace.bosch_hol_sdk import utils
from dspace.bosch_hol_sdk import version_management
from dspace.bosch_hol_sdk.netio_api_json_via_http import NetioState
from dspace.bosch_hol_sdk.replaydevicecontrol import (
    get_replay_device, ReplayDevice,
)
from dspace.bosch_hol_sdk.shmem import ReplayJobSharedMemory
from dspace.bosch_hol_sdk.system_reset import kill_runtime


DEVICE_MAP = {
    DrapiServices_pb2.Device.ESI: ReplayDevice.ESI,
    DrapiServices_pb2.Device.SCALEXIO1: ReplayDevice.SCALEXIO1,
    DrapiServices_pb2.Device.SCALEXIO2: ReplayDevice.SCALEXIO2,
}

POWER_STATE_MAP = {
    NetioState.unknown: DrapiServices_pb2.PowerStatus.POWER_STATUS_UNKNOWN,
    NetioState.on: DrapiServices_pb2.PowerStatus.ON,
    NetioState.off: DrapiServices_pb2.PowerStatus.OFF,
}

PC2_IP = '192.168.140.102'
PC2_USERNAME = 'dspace'
PC2_PASSWORD = 'dspace'


class DrapiServicesImpl(DrapiServices_pb2_grpc.DrapiServicesServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger('DrapiServices.Server')

    def _reset_hw(self, device, parameters):
        self._logger.debug('Resetting the hardware device.')
        ret_val = DrapiServices_pb2.FAIL

        try:
            self._logger.debug(f'Translating chosen device: {device}.')
            drapi_device = DEVICE_MAP[device]
        except KeyError:
            self._logger.exception('Failed to find the device.')
            return DrapiServices_pb2.FAIL, 'Unknown device.'

        try:
            if device == DrapiServices_pb2.Device.ESI:
                # In the case of the ESI, make sure the ECU is not powered on!
                self._logger.debug('ESI reboot: checking if the ECU is on.')
                ecu = get_replay_device(ReplayDevice.ECU)
                if ecu.KL15.state != NetioState.off:
                    raise RuntimeError(
                        'Cannot restart the ESI units while the ECU is on'
                    )

            self._logger.debug(f'Getting control device for {drapi_device}.')
            replay_device = get_replay_device(drapi_device)

            self._logger.info(f'Rebooting {replay_device}')
            replay_device.reboot()
            # Wait an extra second to make sure the device doesn't respond to
            # ping before it is restarted.
            time.sleep(1)
            self._logger.info(f'Waiting till {replay_device} is online')
            replay_device.wait_till_online()
        except KeyError:
            self._logger.exception('Failed to find the device.')
            status = 'Unknown device.'
        except TimeoutError:
            self._logger.exception('Waiting for device failed.')
            status = "The device didn't boot in time."
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            status = f'{exc}'
        else:
            self._logger.info('Device rebooting was successful.')
            ret_val = DrapiServices_pb2.SUCCESS
            status = 'OK.'

        return ret_val, status

    def _reset_service(self, device, parameters):
        self._logger.info(f'Restarting services with parameters {parameters}.')
        EParameter = DrapiServices_pb2.SystemResetConfiguration.ResetParameter
        ret_val = DrapiServices_pb2.SUCCESS
        status = ''
        if EParameter.PC2 in parameters:
            self._logger.info('Restarting service on PC2.')
            try:
                restart_result = kill_runtime.pc_ssh_restart(
                        PC2_IP,
                        PC2_USERNAME,
                        PC2_PASSWORD,
                )
            except Exception as exc:
                self._logger.exception('Unexpected error occured.')
                status = f'PC2 Service: {exc}\n'
                ret_val = DrapiServices_pb2.FAIL
            else:
                if restart_result:
                    self._logger.info(
                        'Pyro-server service on pc2 successfully restarted.'
                    )
                else:
                    self._logger.error(
                        'Restarting Pyro-server service on pc2 failed.'
                    )
                    status += 'Restarting Pyro-server service on pc2 failed.\n'
                    ret_val = DrapiServices_pb2.FAIL

        if EParameter.PC1 in parameters:
            self._logger.info('Restarting service on PC1.')
            try:
                restart_result = kill_runtime.restart_replay_api_service()
            except Exception as exc:
                self._logger.exception('Unexpected error occured.')
                status = f'PC1 Service: {exc}\n'
                ret_val = DrapiServices_pb2.FAIL
            else:
                if restart_result:
                    self._logger.info(
                        'Replay API service on pc1 successfully restarted.'
                    )
                else:
                    self._logger.error(
                        'Restarting replay API service on pc1 failed.'
                    )
                    status += 'Restarting replay API service on pc1 failed.\n'
                    ret_val = DrapiServices_pb2.FAIL

        return ret_val, (status or 'OK.')

    def _reset_full_system(self, device, parameters):
        self._logger.debug('Resetting the full replay system.')
        ret_val = DrapiServices_pb2.FAIL
        error = False
        status = ''

        EParameter = DrapiServices_pb2.SystemResetConfiguration.ResetParameter
        try:
            self._logger.debug('Getting the device instances.')
            ecu = get_replay_device(ReplayDevice.ECU)
            esi = get_replay_device(ReplayDevice.ESI)
            rtpc_1 = get_replay_device(ReplayDevice.SCALEXIO1)
            rtpc_2 = get_replay_device(ReplayDevice.SCALEXIO2)

            self._logger.info('Turning off the ECU (KL15).')
            ecu.KL15.turn_off()

            self._logger.info('Turning off the ECU (KL30).')
            ecu.KL30.turn_off()

            self._logger.info('Rebooting the ESI units.')
            esi.reboot()

            self._logger.info('Rebooting the services.')
            self._reset_service(device, [EParameter.PC1, EParameter.PC2])

            self._logger.info('Rebooting RTPC 1.')
            rtpc_1.reboot()

            self._logger.info('Rebooting RTPC 2.')
            rtpc_2.reboot()

            # Sleep 10 seconds first. There is no point of starting pinging
            # right away and it might even repsond if it's pinged too soon.
            self._logger.info(
                'Waiting 10 seconds for a software reboot to take effect.'
            )
            time.sleep(10)

            self._logger.info('Waiting for RTPC 1.')
            rtpc_1.wait_till_online()

            self._logger.info('Waiting for RTPC 2.')
            rtpc_2.wait_till_online()

            self._logger.info('Testing downloading a real-time application.')
            if utils.download_sclx_app(sdf_path=defaults.TEST_RTAPP_SDF):
                self._logger.info('Unloading the real-time application.')
                if not utils.unload_sclx_app():
                    status += 'Failed to unload real-time application.\n'
                    error = True
            else:
                status += 'Failed to load real-time application.\n'
                error = True

            self._logger.info('Waiting for the ESI units.')
            esi.wait_till_online()
        except KeyError:
            self._logger.exception('Failed to find the device.')
            status += 'Unknown device.\n'
        except TimeoutError:
            self._logger.exception('Waiting for device failed.')
            status += "The device didn't boot in time.\n"
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            status += f'{exc}\n'
        else:
            self._logger.info('Rebooting process finished.')
            if not error:
                ret_val = DrapiServices_pb2.SUCCESS

        return ret_val, (status or 'OK.')

    def ResetSystem(self, request, context):
        self._logger.debug('Received ResetSystem request')
        response = DrapiServices_pb2.Response()
        response.return_value = DrapiServices_pb2.FAIL
        response.text = 'Not executed.'
        reset_func_map = {
            DrapiServices_pb2.Device.ESI: self._reset_hw,
            DrapiServices_pb2.Device.SERVICE: self._reset_service,
            DrapiServices_pb2.Device.SCALEXIO1: self._reset_hw,
            DrapiServices_pb2.Device.SCALEXIO2: self._reset_hw,
            DrapiServices_pb2.Device.FULL_SYSTEM: self._reset_full_system,
        }
        try:
            reset_func = reset_func_map[request.device]
        except KeyError:
            self._logger.exception(f'Unsupported device "{request.device}".')
            response.text = f'Unsupported device "{request.device}" to reset.'
            return response

        try:
            ret_val, status = reset_func(request.device, request.parameters)
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            response.text = str(exc)
        else:
            response.return_value = ret_val
            response.text = status

        return response

    def GetDeviceStatus(self, request, context):
        self._logger.debug('Received ResetSystem request')
        response = DrapiServices_pb2.DeviceStatus()
        response.device = request.device
        response.power_status = DrapiServices_pb2.PowerStatus.POWER_STATUS_UNKNOWN
        response.device_status = response.DeviceSystemStatus.DEVICE_STATUS_UNKNOWN
        response.text = 'Not executed.'
        try:
            self._logger.debug(f'Translating chosen device {request.device}.')
            device = DEVICE_MAP[request.device]

            self._logger.debug(f'Getting control device for {device}.')
            device_control = get_replay_device(device)

            self._logger.info(
                f'Reading the power state of {device_control}'
            )
            power_state = device_control.power_state
            if device_control.is_ready():
                response.device_status = DrapiServices_pb2.DeviceStatus.READY
            else:
                response.device_status = DrapiServices_pb2.DeviceStatus.ERROR
        except KeyError:
            self._logger.exception('Failed to find the device.')
            response.text = 'Unknown device.'
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            response.text = f'{exc}'
        else:
            self._logger.info(
                'Reading device status was successful '
                f'({power_state}/{POWER_STATE_MAP[power_state]}).'
            )
            response.power_status = POWER_STATE_MAP[power_state]
            response.text = 'OK.'

        return response

    def _read_api_version(self, version_obj):
        try:
            (
                version_obj.major,
                version_obj.minor,
                version_obj.patch,
            ) = get_version_tuple()
        except Exception as exc:
            self._logger.exception('Error while reading the API version.')
            status = str(exc)
            ret_val = DrapiServices_pb2.FAIL
        else:
            status = 'OK'
            ret_val = DrapiServices_pb2.SUCCESS

        return ret_val, status

    def _read_sdf_version(self, sdf_file, version_obj):
        if not sdf_file:
            status = 'No SDF file provided.'
            ret_val = DrapiServices_pb2.SUCCESS
        else:
            try:
                (
                    version_obj.major,
                    version_obj.minor,
                    version_obj.patch,
                ) = version_management.get_sdf_version(sdf_file)
            except FileNotFoundError as exc:
                file = exc.args[0]
                self._logger.error(f'Failed to find {file}.')
                status = f"File '{file}' does not exist"
                ret_val = DrapiServices_pb2.FAIL
            except Exception as exc:
                self._logger.exception(
                    f'Error while reading the version of {sdf_file}.'
                )
                status = str(exc)
                ret_val = DrapiServices_pb2.FAIL
            else:
                status = 'OK'
                ret_val = DrapiServices_pb2.SUCCESS
        return ret_val, status

    def _read_pc1_diagram_version(self, diagram, version_obj):
        if not diagram:
            status = 'No diagram file for PC1 provided.'
            ret_val = DrapiServices_pb2.SUCCESS
        else:
            try:
                (
                    version_obj.major,
                    version_obj.minor,
                    version_obj.patch,
                ) = version_management.get_diagram_version(diagram)
            except Exception as exc:
                self._logger.exception(
                    f'Error while reading the version of {diagram}.'
                )
                status = str(exc)
                ret_val = DrapiServices_pb2.FAIL
            else:
                status = 'OK'
                ret_val = DrapiServices_pb2.SUCCESS
        return ret_val, status

    def _read_pc2_diagram_version(self, diagram, version_obj):
        if not diagram:
            status = 'No diagram file for PC2 provided.'
            ret_val = DrapiServices_pb2.SUCCESS
        else:
            try:
                serialized_output, stderr = utils.run_file_remotely(
                    version_management.__file__,
                    '--diagram',
                    diagram,
                    remote_ip=PC2_IP,
                    username=PC2_USERNAME,
                    password=PC2_PASSWORD,
                )

                if stderr.strip():
                    for line in stderr.splitlines():
                        # version_management doesn't use the logging module
                        # so we assume anything in stderr means it was an
                        # exception. We take the last line of it for the
                        # response-text.
                        self._logger.error(line)
                    raise RuntimeError(line)

                (
                    version_obj.major,
                    version_obj.minor,
                    version_obj.patch,
                ) = json.loads(serialized_output)
            except Exception as exc:
                self._logger.exception(
                    f'Error while reading the version of {diagram}.'
                )
                status = str(exc)
                ret_val = DrapiServices_pb2.FAIL
            else:
                status = 'OK'
                ret_val = DrapiServices_pb2.SUCCESS
        return ret_val, status

    def GetVersions(self, request, context):
        self._logger.debug('Received GetVersions request')
        version_info = DrapiServices_pb2.VersionInformation()
        # We assume success now and set it to failed if something goes wrong.
        version_info.response.return_value = DrapiServices_pb2.SUCCESS
        version_info.response.text = ''
        try:
            # API version.
            ret_val, status = self._read_api_version(version_info.api)
            version_info.response.text += f'API version: {status}\n'
            if ret_val == DrapiServices_pb2.FAIL:
                version_info.response.return_value = DrapiServices_pb2.FAIL

            # RT-APP version.
            ret_val, status = self._read_sdf_version(
                request.sdf_path,
                version_info.realtime_application,
            )
            version_info.response.text += f'RT-APP version: {status}\n'
            if ret_val == DrapiServices_pb2.FAIL:
                version_info.response.return_value = DrapiServices_pb2.FAIL

            # PC1 diagram version.
            ret_val, status = self._read_pc1_diagram_version(
                request.pc1_diagram_path,
                version_info.pc1_diagram,
            )
            version_info.response.text += f'PC1 diagram version: {status}\n'
            if ret_val == DrapiServices_pb2.FAIL:
                version_info.response.return_value = DrapiServices_pb2.FAIL

            # PC2 diagram version.
            ret_val, status = self._read_pc2_diagram_version(
                request.pc2_diagram_path,
                version_info.pc2_diagram,
            )
            version_info.response.text += f'PC2 diagram version: {status}\n'
            if ret_val == DrapiServices_pb2.FAIL:
                version_info.response.return_value = DrapiServices_pb2.FAIL
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            version_info.response.return_value = DrapiServices_pb2.FAIL
            version_info.response.text += str(exc)

        return version_info

    def StartReplayJob(self, request, context):
        self._logger.debug('Received StartReplayJob request')
        # Prepare the response object.
        response = DrapiServices_pb2.StartReplayJobResponse()
        response.response.return_value = DrapiServices_pb2.FAIL
        response.response.text = 'Not executed.'
        # Get the job name.
        job_name = request.job.name
        self._logger.info(f'Starting replay-job: {job_name}')
        try:
            # Attempt to send the start trigger through shared-memory.
            with ReplayJobSharedMemory(job_name, create=False) as shmem:
                shmem.start = 1
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            response.response.return_value = DrapiServices_pb2.FAIL
            response.response.text = str(exc)
        else:
            response.response.return_value = DrapiServices_pb2.SUCCESS
            response.response.text = 'OK.'

        return response
    
    def DownloadApplication(self, request, context):
        response = DrapiServices_pb2.DownloadAppResponse()
        response.response.return_value = DrapiServices_pb2.FAIL
        response.response.text = 'Not executed.'

        sdf_path = request.sdf_path
        try:
            if utils.download_sclx_app(sdf_path):
                response.response.return_value = DrapiServices_pb2.SUCCESS
                response.response.text = 'OK.'
            else:
                response.response.text = 'Failed to download application.'
        except Exception as exc:
            self._logger.exception('Unexpected error occured.')
            response.response.return_value = DrapiServices_pb2.FAIL
            response.response.text = str(exc)
        return response

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host',
        default='[::]',
        type=str,
        help='the hostname to listen on',
    )
    parser.add_argument(
        '--port',
        default=50061,
        type=int,
        help='the port to listen on',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help='Increase the output verbosity',
    )
    args = vars(parser.parse_args(argv))
    # Pop the arguments that are not passed to the instance.
    host = args.pop('host')
    port = args.pop('port')
    verbosity = args.pop('verbose')

    # Initialize logging.
    log_level = max(logging.DEBUG, logging.ERROR - verbosity*10)
    logging.basicConfig(
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
        level=log_level,
    )
    logger = logging.getLogger('DrapiServices.Main')

    address = f'{host}:{port}'
    logger.info(f'Creating service instance at {address}')
    instance = DrapiServicesImpl(**args)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DrapiServices_pb2_grpc.add_DrapiServicesServicer_to_server(
        instance,
        server,
    )
    server.add_insecure_port(address)

    # Configure signal handler for graceful shutdown
    original_handlers = {}

    def signal_handler(sig, frame):
        logger.info(f'Received signal {sig}.')
        # Install original handler to allow for a second CTRL+C to forcefully
        # abort the execution.
        logger.info('Restoring the original signal handler.')
        signal.signal(sig, original_handlers.get(sig, signal.SIG_DFL))

        logger.info('Stopping gRPC server.')
        server.stop(None)

    logger.info('Installing signal handlers.')
    for sig in [signal.SIGINT, signal.SIGTERM]:
        original_handlers[sig] = signal.signal(sig, signal_handler)

    logger.info('Starting gRPC server.')
    server.start()
    server.wait_for_termination()
    logger.info('gRPC server terminated.')


if __name__ == '__main__':
    sys.exit(main())
