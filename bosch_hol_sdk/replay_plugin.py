"""
The script configure the rtmaps diagram and control desk model for data replay
Requirements: Python3, Replay_pc1
by QianweiY, DSC, 2023/8/14

v2.0:
-The second demo version
- Ubuntu 20.04
-Test data:
    copy7-pc1:"/mnt/ext_ssd/auto/20230809_155456_DSU1_auto@20230809_155456973558/DSU1_auto_20230809_155456@20230809_155456973558.rec"
    copy7-pc2:"/mnt/ext_ssd/auto/20230809_155456_DSU0_auto@20230809_155456809596/DSU0_auto_20230809_155456@20230809_155456809596.rec"
-Test rtmaps diagram:
    copy7-pc1: "/home/dspace/workspace/replay_test/Complete_DSU1_Chery_API.rtd"
    copy7-pc2: "/home/dspace/workspace/replay_test/Complete_DSU0_Chery_API.rtd"
-Main package version:
    esi-unit-encoder-v2.pck(2.0)
    fillterCAN.pck(1.0.0)
    rtmaps_custom_data.pck(1.11.0)
    CANContainer.pck(0.999)
    DDRP.pck(2.0)
    EthernetContainer.pck(2.1.0)
    rtmaps_get_timestamp.pck(1.0)
    rtmaps_pcap.pck (3.0.0)
-Main component version:
    Image2ESI 2.0.12
    MAPS_ToStream8 1.1.1
    dDRP_Offset_Sender 1.0
    dDrp_Frame_Encoder 1.1
    filter_CAN_1.0.1
    get_timestamp 1.0
    pcap_filter 2.0.0
"""
import dataclasses
import enum
from pathlib import Path
import time
from datetime import datetime
import logging
import json
import re
import shutil
import tarfile
import typing
import requests
import json

# "third-party" modules.
from ASAM.XIL.Interfaces.Testbench.Common.Error.TestbenchPortException import TestbenchPortException
import Pyro5.api

from dspace.bosch_hol_sdk import get_version_tuple
from dspace.bosch_hol_sdk import __version__ as full_version_str
from dspace.bosch_hol_sdk.bus_manipulation import (
    DataManipulation, reload_xil_paths, XilManipulationBase,
)
from dspace.bosch_hol_sdk.configuration import (
    deserialize_data_manipulation, check_data_manipulation_objects,
    ReplayTimeConfiguration,
)
from dspace.bosch_hol_sdk.DataReplayAPI.drapi.helper.xilapi_maport import XILAPIMAPort
from dspace.bosch_hol_sdk.DataReplayAPI.drapi import datareplay_pb2
from dspace.bosch_hol_sdk.dsmessagereader import (
    DsMessagesReader, DsMessageType,
)
from dspace.bosch_hol_sdk.esi_ftp_client import esi_ftp_client
from dspace.bosch_hol_sdk import esi_telnet
from dspace.bosch_hol_sdk import idx_rec_compare
from dspace.bosch_hol_sdk.netio_api_json_via_http import NetioState
from dspace.bosch_hol_sdk.port_connection_config import (
    PortConnectionManager, PlayerLocation,
)
from dspace.bosch_hol_sdk.prepare_connection import RtmapsConnection
from dspace.bosch_hol_sdk.replay_plugin_exceptions import (
    RTAppDownloadError, ESIRestartTimeoutError, XilApiError, RTMapsError,
    ECURestartedError, ReplayFrozenError, RTAppUnloadError,
    BadManipulationConfigurationError, IncompatibleRTAppsError,
    IncompatibleRTAppApiError, ESIError, RealtimeApplicationError,
    ReplayDataTimeTimeout, BadXilPathError,
)
from dspace.bosch_hol_sdk.replaydevicecontrol import (
    get_replay_device, ReplayDevice,
)
from dspace.bosch_hol_sdk.shmem import ReplayJobSharedMemory
from dspace.bosch_hol_sdk.system_reset import kill_runtime
from dspace.bosch_hol_sdk.utils import (
    run_file_remotely, download_sclx_app, unload_sclx_app,
)
from dspace.bosch_hol_sdk.xcpinterface import (
    XCPInterface, XCPCommand, XCPResponseType, DataType,
)
from dspace.bosch_hol_sdk import xil_variables

NETIO_URL = "http://192.168.140.51/netio.json"
# Port on which the Pyro API is listening
PYRO_PORT = 33033
# IP of the secondary server
REMOTE_IP = "192.168.140.102"  # remote ip of device that slave diagram in
# RTMaps Port (can be choosen freely), used for the "master/slave" mechanism in RTMaps
RTMAPS_PORT = 11118  # rtmaps should be standalone, port can not be the same port in rtmaps

ESI_CHECK_INTERVAL = 5  # seconds.
PROGRESS_PRINT_INTERVAL = 1  # seconds.

cwd = Path(__file__).resolve().parent

DEFAULT_REPLAY_DATA_TIMEOUT = 20  # seconds
COUNTER_SUM_PROP_NAME = "Sum_Count"
PLAYER_PROP_NAME = ["percentage", "time"]

FRAME_SKIPPERS = {
    PlayerLocation.PC1: (
        "frame_skipper_SideFrontCam01",
        "frame_skipper_SideFrontCam02",
        "frame_skipper_SideRearCam01",
        "frame_skipper_SideRearCam02",
        "frame_skipper_SurCam02",
        "frame_skipper_SurCam04",
        "frame_skipper_SurCam01",
        "frame_skipper_SurCam03",
    ),
    PlayerLocation.PC2: (
        "frame_skipper_FrontCam02",
        "frame_skipper_FrontCam01",
        "frame_skipper_RearCam01",
    ),
}

SOMEIP_ROOT_PATTERN = (
    r'.*'  # Platform
    r'BusSystems/'
    r'Ethernet/'
    r'(?P<ECU>[^/]+)/'
    r'[CP]SIs/'
    r'ROOT_PACKAGE/'
    r'Service_(?P<ServiceID>[^/]+)_1/'
)

SOMEIP_SUBSCRIPTION_STATUS_PATTERN = SOMEIP_ROOT_PATTERN + (
    r'.*/'  # We ignore some parts of the path.
    r'Event_Group_(?P<GroupId>\d+)/'
    r'ADCC/'
    r'Subscription Status'
)

SOMEIP_COUNTER_PATTERN = SOMEIP_ROOT_PATTERN + (
    r'(?P<Type>Methods|Events)/'  # Matche both but we want to know which.
    r'(?P<Name>[^/]+)/'  # Method or event name
    r'(?:Response_RX/)?'  # Only exists in the case of Methods
    r'Status/'
    r'Data\s(?P<Counter>\S+\sCounter)'  # Both transmitted and received.
)

SOMEIP_SUBSCRIPTION_REGEX = re.compile(SOMEIP_SUBSCRIPTION_STATUS_PATTERN)
SOMEIP_COUNTER_REGEX = re.compile(SOMEIP_COUNTER_PATTERN)

ESI_XCP_ALLOW_LIST = [
    'replay_subsystem_0_current_time',
    'replay_subsystem_0_ptp_time',
    '_current_offset_time',
    '_current_start_time',
    '_current_stop_time',
    '_next_scheduled_time',
    '_next_relative_time',
    '_ram_buffer_fill_percent',
    '_debug_eth_image_frame_count',
    '_active',
    '_debug_status_start_time_reached',
    '_debug_status_stop_time_reached',
    '_debug_eth_dropped_pkt_count',
    '_operationMode',
    '_frameFrequency',
]


def get_instance(*args, **kwargs):
    return DemoReplayPlugin(*args, **kwargs)


@dataclasses.dataclass
class CounterData:
    name: str
    # NOTE: Bad type-hinting but currently no generic solution to import both
    # RTMaps objects for type hinting only.
    rtmaps: object
    component_id: str
    last_count: int = 0
    timestamp: float = 0

@dataclasses.dataclass
class PlayerData:
    name: str
    rtmaps: object
    component_id: str
    skip_frozen_check: bool
    last_percentage: int = 0
    last_player_time: int = 0
    timestamp: float = 0

class RTMapsLogError(enum.Enum):
    NoError = enum.auto()
    GenericError = enum.auto()
    Image2EsiError = enum.auto()
    RTMapsZombie = enum.auto()


@dataclasses.dataclass(frozen=True)
class LogMessage:
    level: int
    text: str

    def __post_init__(self):
        # To understand the following magic formula see the following
        # mapping table between the numeric values of the log-levels of RTMaps
        # and of the Python logging module:
        # ________________________________
        # | Level     | RTMaps | logging |
        # |-----------|--------|---------|
        # | debug     | 3      | 10      |
        # | info      | 0      | 20      |
        # | warning   | 1      | 30      |
        # | error     | 2      | 40      |
        # | exception | N/A    | 50      |
        # --------------------------------
        # logging.DEBUG has a level of 10. Anything less, is most likely RTMaps
        # style logging level, so we need to map it.
        # RTMaps has the debug-level as the highest value, we solve this by
        # adding 1 and then taking modulo 4. This puts the debug-level at 0,
        # info at 1, warning at 2 and error at 3.
        # Now all that is missing is an offset of 1 and a factor of 10 to get
        # the same levels as the logging module of Python.
        if self.level < 10:
            object.__setattr__(
                self,
                'level',
                (((self.level + 1) % 4) + 1) * 10,
            )


@dataclasses.dataclass(frozen=True)
class RTMapsErrorHandler:
    regex: typing.Union[str, re.Pattern]
    error_type: RTMapsLogError
    level: int = logging.ERROR

    def __post_init__(self):
        if isinstance(self.regex, str):
            object.__setattr__(self, 'regex', re.compile(f'.*{self.regex}.*'))

    def __eq__(self, other: LogMessage) -> bool:
        if not isinstance(other, LogMessage):
            raise TypeError(type(other))

        if self.level != other.level:
            return False

        return self.regex.match(other.text) is not None


class RTMapsErrorHandlersList(list):
    def __getitem__(self, key):
        for handler in self:
            if key == handler:
                return handler
        raise IndexError(key)


class DemoReplayPlugin():
    PYRO_ADDRESS = (REMOTE_IP, PYRO_PORT)

    def __init__(self, rtmaps, logger):
        self._rtmaps = rtmaps
        self._logger = logger
        self._user_data = {}
        self._pending_exception = None
        self._set_print = 0
        self._counters = []
        self._players = []
        self._replay_data_timeout = DEFAULT_REPLAY_DATA_TIMEOUT
        self._remote_rtmaps = None
        self._rt_app_download = False
        self._restart_service_pending = False
        self._last_esi_check = 0
        self._last_progress_print = 0
        self._esi_restart_count = 0
        self._someip_monitor_list = []
        self._ecu = None
        self._esi = None
        self._sclx = None
        self._sclx2 = None
        self._sclx2_reader = None
        self._sclx_reader = None
        self._esi_xcp_vars = []
        self.replayState = None
        self._rtmaps_error_handlers = RTMapsErrorHandlersList([
            # The order implies precedence!
            RTMapsErrorHandler(
                regex=r'component.*is still alive',
                error_type=RTMapsLogError.RTMapsZombie,
            ),
            RTMapsErrorHandler(
                regex=r'component.*refuses to die',
                error_type=RTMapsLogError.RTMapsZombie,
                level=logging.WARNING,
            ),
            RTMapsErrorHandler(
                regex=r"component Image2Esi",
                error_type=RTMapsLogError.Image2EsiError,
            ),
        ])

        # XIL
        self._xil_api_maport = None
        self._start_offset = float(15)   # change Start offset
        self._stop_offset = float(3600)  # change stop offset

        self._logger.info(
            f'Creating replay-plugin instance with version {full_version_str}'
        )

        self._debug = False
        self._started = False
        self._start_time = 0
        self._data_time_transmitted = False
        self._shmem = None
        self._too_late_count = 0
        self._DsCanMsg_count = 0
        self._replay_length = -1

        # Not really the most reliable way to get the job name but it's the
        # only one with minimal changes. An alternative solution would be
        # to redundantly write the job-name in the replay_data in the
        # job-configuration object (or modify drapi to pass the jobname to the
        # plugin).
        self._job_name = self._logger.name.split('.')[-2]

        # NETIO configuration
        self.netio_init()

    def _connect_to_remote_rtmaps(self):
        ip, port = self.PYRO_ADDRESS
        uri = f"PYRO:RTMapsService@{ip}:{port}"
        self._logger.info(f"Connecting to remote RTMaps at {uri}")
        self._remote_rtmaps = Pyro5.api.Proxy(uri)
        # Clear any old logs.
        self._remote_rtmaps.clear_log()

    def download_SCLX_APP(self, sdf_path: str, CMDLOADER: str, platform: str):
        if not download_sclx_app(
            sdf_path=sdf_path,
            cmdloader=CMDLOADER,
            platform=platform,
            scalexios=[self._sclx, self._sclx2],
            logger=self._logger,
        ):
            raise RTAppDownloadError()
        self._rt_app_download = True

    def unload_SCLX_APP(self, CMDLOADER: str, platform: str):
        if not unload_sclx_app(
            cmdloader=CMDLOADER,
            platform=platform,
            logger=self._logger,
        ):
            raise RTAppUnloadError()

    def _ensure_version_compatibility(self, maport):
        # Read versions
        api_version = get_version_tuple()
        rtapp_versions = self._get_rt_app_versions(maport)

        # Report versions
        self._logger.info(f'Detected Replay API version: {api_version}')
        for rtpc, version in enumerate(rtapp_versions, 1):
            self._logger.info(
                f'Detected RT App version on RTPC{rtpc}: {version}'
            )

        # Check compatibilities
        if rtapp_versions[0][:2] != rtapp_versions[1][:2]:
            raise IncompatibleRTAppsError(
                rtapp_versions[0],
                rtapp_versions[1],
            )

        for rtpc, version in enumerate(rtapp_versions, 1):
            if api_version[:2] != version[:2]:
                if version[:2]==(1.0,9.0) or version[:2]==(1.0,8.0):
                    self._logger.info(
                        f'Detected RT App version on RTPC{rtpc}:{version} is compatible with api version:{api_version}')
                else:
                    raise IncompatibleRTAppApiError(
                        api_version=api_version,
                        rtapp_version=version,
                        rtpc=rtpc,
                    )

    def _get_rt_app_version_paths(self):
        pc_roots = [
            'SCALEXIO Real-Time PC()://Replay_MP_Chery_BM',
            'SCALEXIO Real-Time PC_2()://Replay_MP_SOMEIP',
        ]
        return (f'{root}/Model Root/ModelVersion/Out1' for root in pc_roots)

    def _get_rt_app_versions(self, maport):
        versions = []
        for i, path in enumerate(self._get_rt_app_version_paths(), 1):
            try:
                version = maport.read_variable(path)
                version = tuple(version[:3])
            except Exception:
                self._logger.exception(
                    f'Failed to read the RT App version of PC{i}'
                )
                version = (0, 0, 0)
            finally:
                versions.append(version)

        return versions

    def netio_init(self) -> None:
        self._ecu = get_replay_device(ReplayDevice.ECU)
        self._esi = get_replay_device(ReplayDevice.ESI)
        self._sclx = get_replay_device(ReplayDevice.SCALEXIO1)
        self._sclx2 = get_replay_device(ReplayDevice.SCALEXIO2)
        self._sclx2_reader = DsMessagesReader(self._sclx2, logger=self._logger)
        self._sclx_reader = DsMessagesReader(self._sclx, logger=self._logger)

    def ecu_on(self) -> None:
        self._logger.info("Turning ECU on.")
        self._ecu.netio_socket.turn_on()
        self._logger.info("Waiting 10s for ECU to be ON.")
        time.sleep(10)

    def ecu_off(self) -> None:
        self._logger.info("Turning ECU off.")
        self._ecu.netio_socket.turn_off()

    def ESI_check(self, reboot_on_error=True) -> None:
        self._logger.info('Checking connection to the ESI units.')
        if not self._esi.is_ready():
            self._logger.warning('ESI units not ready!')
            if reboot_on_error:
                self._reset_esis()

    def _esi_check_xcp_version(self) -> None:
        for esi in self._esi.devices:
            self._logger.info(f'Checking firmware version of {esi}.')
            with XCPInterface(esi.ip, esi.port, self._logger) as xcp_comm:
                try:
                    resp = xcp_comm.send(XCPCommand.CONNECT)
                    if resp.type != XCPResponseType.RESPONSE:
                        raise Exception(f'Failed to connect to {esi}')

                    version = esi.xcp_infos.version
                    self._logger.debug(f'Excepted version: {version}')
                    read_version = ""
                    for offset in range(len(version)):
                        resp = xcp_comm.send(
                            XCPCommand.SHORT_UPLOAD,
                            esi.xcp_infos.version_address + offset,
                            DataType.UBYTE,
                        )
                        read_version += chr(resp.value)

                    if read_version != version:
                        xcp_comm.send(XCPCommand.DISCONNECT)
                        raise ValueError(read_version, version)

                    xcp_comm.send(XCPCommand.DISCONNECT)
                except Exception:
                    self._logger.exception(f'Disabling XCP variables for {esi}.')
                else:
                    self._esi_xcp_vars.append(esi)

    def SCLX_model_config_StartStop(self) -> None:
        xil_paths = xil_variables.Enable

        ReplayModeEnabled = self._xil_api_maport.read_variable(xil_paths['EnableReplayMode'])
        self._logger.info(f'ReplayModeEnabled: {ReplayModeEnabled}')
        if ReplayModeEnabled == 0.0:
            self._xil_api_maport.write_variable(xil_paths['EnableReplayMode'], float(1))

        Enable_StartStopSetFromSCLX = self._xil_api_maport.read_variable(xil_paths['Enable_StartStopSetFromSCLX'])
        self._logger.info(f'Enable_StartStopSetFromSCLX: {Enable_StartStopSetFromSCLX}')
        if Enable_StartStopSetFromSCLX is False:
            self._xil_api_maport.write_variable(xil_paths['Enable_StartStopSetFromSCLX'], True)

    def SCLX_model_config_startReplay(self) -> None:
        xil_paths = xil_variables.Enable

        # start Relplay !!!!!!
        EnableReplay = self._xil_api_maport.read_variable(xil_paths['StartReplay'])
        self._logger.info(f'EnableReplay: {EnableReplay}')
        if EnableReplay == 0:
            self._xil_api_maport.write_variable(xil_paths['StartReplay'], int(1))
            startReplay = self._xil_api_maport.read_variable(xil_paths['StartReplay'])
            self._logger.info(f'set EnableReplay: {startReplay}')

    def SCLX_model_read_ptpMaster(self) -> None:
        # gPTP_Master
        self._debug_xil_var_list(
            xil_variables.gPTP_Master.items(),
            self._logger,
        )

    def DuTSyncStartCalc(self, logger) -> None:
        # DuTSyncStartCalc
        if self._set_print == 2:
            self._debug_xil_var_list(
                xil_variables.DuTSyncStartCalc.items(),
                logger,
            )
        self._set_print += 1

    def _check_sclx_time(self, logger):
        if self._data_time_transmitted:
            return

        values = self._debug_xil_var_list(
            xil_variables.ReplayDataTime.items(),
            logger,
        )

        BytesReceived = values['BytesReceived']
        if not BytesReceived and time.perf_counter() - self._start_time > 11:
            raise ReplayDataTimeTimeout()

        self._data_time_transmitted = BytesReceived

    def get_replay_state(self, replay_state, logger) -> None:
        xil_paths = xil_variables.ReplayStateMonitor

        # Write the eplapsed time back to drapi.
        replay_duration = self._xil_api_maport.read_variable(xil_paths["replayDuration"])
        replay_state.elapsed_time = replay_duration

        # Write the progress back to drapi.
        replay_progress = self._xil_api_maport.read_variable(xil_paths["replayProgress"])
        replay_state.progress = round(replay_progress * 100)

        old_replay_state = self.replayState
        self.replayState = self._xil_api_maport.read_variable(xil_paths["replayState"])
        if old_replay_state != self.replayState and self.replayState == 2:
            self._replay_length = self._xil_api_maport.read_variable(xil_paths["replayLength"])

        if logger:
            logger.info(f'replay Duration: {replay_duration}')
            logger.info(f'progress: {replay_state.progress}%')
            logger.info(f'replayState for model: {self.replayState}')
            logger.info(f'replayLength: {self._replay_length}')
            
    def monitor_replaypc_load(self, url, logger):
        try:
            # set timeout 0.5s
            response = requests.get(url, timeout=1)
            response.raise_for_status()  # if response a error value, raise a exception

            # get json
            data = response.json()

            # get load value of ID1 and ID2
            load_id1 = next((output['Load'] for output in data['Outputs'] if output['ID'] == 1), None)
            load_id2 = next((output['Load'] for output in data['Outputs'] if output['ID'] == 2), None)
            logger.debug(f'RTPC2 & replayPC1 load: {load_id1}w')
            logger.debug(f'replayPC2 load: {load_id2}w')
            
            return load_id1, load_id2

        except requests.RequestException as e:
            logger.error(f"An error occured: {e}")
            return None, None

    def monitor_ESI1(self, logger) -> None:
        # ESI1
        self._debug_xil_var_list(
            xil_variables.ReplayDisgnostic_ESI1.items(),
            logger,
        )

    def monitor_ESI2(self, logger) -> None:
        # ESI2
        self._debug_xil_var_list(
            xil_variables.ReplayDisgnostic_ESI2.items(),
            logger,
        )

    def monitor_RTPC(self, logger) -> None:
        # RTPC1
        self._debug_xil_var_list(
            xil_variables.ReplayDisgnostic_RTPC1.items(),
            logger,
        )

    def monitor_someip(self, logger) -> None:
        self._debug_xil_var_list(self._someip_monitor_list, logger)

    def monitor_time_calc(self, logger) -> None:
        return self._debug_xil_var_list(
            xil_variables.ReplayTimeCalc.items(),
            logger,
        )

    def _debug_xil_var_list(self, lst, logger) -> dict:
        values = {}
        for name, path in lst:
            value = self._xil_api_maport.read_variable(path)
            logger.debug(f'{name}: {value}')
            values[name] = value
        return values

    def _configure_data_manipulation(self, configuration_string):
        try:
            config_units = deserialize_data_manipulation(configuration_string)
            check_data_manipulation_objects(config_units)
        except Exception as exc:
            # Ideally should never happen because we check the data also
            # before serialization.
            raise BadManipulationConfigurationError() from exc

        access_objects = {
            'maport': self._xil_api_maport,
            'rtmaps': {
                PlayerLocation.PC1: self._rtmaps,
                PlayerLocation.PC2: self._remote_rtmaps,
            },
        }
        for unit in config_units:
            manipulation_object = DataManipulation(
                configuration=unit,
                access_objects=access_objects,
                logger=self._logger.getChild('data_manipulation'),
            )
            manipulation_object.apply()

    def _check_replay_data_files(self, connection_manager, pc1_path, pc2_path):
        available = {}
        pc1_sensors = {
            'camera': [],
            'can': [],
            'lidar': [],
        }
        pc2_args = [pc2_path, '-vvv']

        for connection in connection_manager.get_port_connections():
            if connection.player.location == PlayerLocation.PC1:
                pc1_sensors[connection.type].append(connection.name)
            else:
                pc2_args.extend((f'--{connection.type}', connection.name))

        # Running check on PC1.
        logger = self._logger.getChild('IdxRecCompare')
        compare_obj = idx_rec_compare.IdxRecCompare(
            pc1_path,
            pc1_sensors,
            logger,
        )
        available[PlayerLocation.PC1], timestamp1 = compare_obj.data_check()

        # Running check on PC2.
        serialized_output, stderr = run_file_remotely(
            idx_rec_compare.__file__,
            *pc2_args,
            remote_ip=REMOTE_IP,
            username='dspace',
            password='dspace',
        )

        if stderr.strip():
            for line in stderr.splitlines():
                try:
                    level, msg = line.split(':', 1)
                    log_func = getattr(self._logger, level.lower())
                except (ValueError, AttributeError):
                    self._logger.error(line)
                else:
                    log_func(f'Remote IdxRecCompare: {msg}')

        output = json.loads(serialized_output)
        available[PlayerLocation.PC2] = output['sensors']
        timestamp2 = int(output['ts_end'])

        for location, sensors in available.items():
            self._logger.debug(f'Data analysis results on {location}:')
            for name, data in sensors.items():
                self._logger.debug(f'\t{name}: {data}')

        self._logger.debug(f'End time PC1: {timestamp1}')
        self._logger.debug(f'End time PC2: {timestamp2}')

        found = []
        missing = []

        for connection in connection_manager.get_port_connections():
            if available[connection.player.location][connection.name][1] > 0:
                found.append(connection)
            else:
                missing.append(connection)

        self._logger.info(
            f'Connections considered: {[conn.name for conn in found]}'
        )
        if missing:
            self._logger.warning(
                f'Missing connections: {[conn.name for conn in missing]}'
            )
            # Tolerate errors regarding those possibly missing.
            for conn in missing:
                self._rtmaps_error_handlers.append(
                    RTMapsErrorHandler(
                        regex=f"{conn.name}: couldn't find stream file",
                        error_type=RTMapsLogError.NoError,
                    )
                )

        return found, min(timestamp1, timestamp2)

    def _prepare_someip_monitor_list(self):
        var_list = []
        for entry in XilManipulationBase.get_known_paths():
            m = SOMEIP_SUBSCRIPTION_REGEX.match(entry)
            if m:
                name = (
                    f'ECU {m.group("ECU"):<16} / '
                    f'Service {m.group("ServiceID")} '
                    f'({hex(int(m.group("ServiceID")))})'
                    '  Subscription status'
                )
                var_list.append((name, entry))
                continue

            m = SOMEIP_COUNTER_REGEX.match(entry)
            if m:
                name = (
                    f'ECU {m.group("ECU"):<16} / '
                    f'Service {m.group("ServiceID")} '
                    f'({hex(int(m.group("ServiceID")))}) /   '
                    f'{m.group("Type")[:-1]} {m.group("Name")} / '
                    f'{m.group("Counter")}'
                )
                var_list.append((name, entry))
                continue

        var_list.sort()
        self._someip_monitor_list = var_list

    def _check_someip_subscriptions(self, logger):
        for name, path in self._someip_monitor_list:
            # ignore counters.
            if not 'Subscription status' in name:
                continue
            value = self._xil_api_maport.read_variable(path)
            if value == 0:
                logger.info(f'Unsubscribed service: {name}')

    def configure(self, replay_data, log_files, additional_properties=None):
        tic = time.perf_counter()

        self._user_data['config_time'] = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        # Read the debug flag.
        self._debug = replay_data.get('debug', 'false').lower() == 'true'
        if self._debug:
            self._logger.warning('Debug mode activated!')

        try:
            # First try!
            self._real_configure(
                replay_data=replay_data,
                log_files=log_files,
                additional_properties=additional_properties,
            )
        # The follwoing errors should end the job right away with no retry!
        except (
            # Configuration errors:
            BadManipulationConfigurationError, IncompatibleRTAppsError,
            IncompatibleRTAppApiError, BadXilPathError,
            # ESI Errors:
            ECURestartedError, ESIError, ESIRestartTimeoutError,
        ):
            raise
        except Exception:
            self._logger.exception(
                'First configuration attempt failed. Trying again...'
            )
            master_diagram = self._rtmaps.diagram

            self._remote_rtmaps = None
            self._rtmaps.shutdown()
            self._rtmaps.reset()

            self.cleanup(
                datareplay_pb2.ERROR,
                replay_data,
                final=False,
            )

            time.sleep(3)
            self._pending_exception = None

            # Second try
            self._rtmaps.load_diagram(master_diagram)
            self._real_configure(
                replay_data=replay_data,
                log_files=log_files,
                additional_properties=additional_properties,
            )

        # Start the replay.
        try:
            # Start stop replay.
            self.SCLX_model_config_StartStop()
        except TestbenchPortException as ex:
            self._logger.exception(
                f'VendorCodeDescription: {ex.VendorCodeDescription}'
            )
            raise XilApiError(ex.CodeDescription)

        autostart = replay_data.get('autostart', 'true').lower() == 'true'
        if autostart:
            self._start_replay()
        else:
            self._create_start_shmem()

        toc = time.perf_counter()
        self._user_data['configuration_duration'] = str(toc - tic)

    def _real_configure(self, replay_data, log_files, additional_properties=None):
        self._replay_data_timeout = float(replay_data.get(
            'replay_data_timeout',
            DEFAULT_REPLAY_DATA_TIMEOUT,
        ))

        # Check if there were already errors during the initialization.
        if self._pending_exception is not None:
            tmp_exception = self._pending_exception
            self._pending_exception = None
            raise tmp_exception

        # Connect to Pyro server.
        self._connect_to_remote_rtmaps()

        # Download control desk app (Raises the apropriate exception if failed).
        if not self._rt_app_download:
            self.download_SCLX_APP(
                replay_data['sdf_path'],
                replay_data['CMDLOADER'],
                replay_data['platform_name'],
            )

        # initialize xil api
        self._logger.info('Initializing XIL API access.')
        if self._xil_api_maport is None:
            self._xil_api_maport = XILAPIMAPort(
                replay_data['platform_name'],
                replay_data['sdf_path'],
                directory='.',
                logger=None,
            )

        # reload all the known XIL path in the cache.
        self._logger.info('Reloading XIL variables.')
        reload_xil_paths(self._xil_api_maport)
        self._prepare_someip_monitor_list()

        self._ensure_version_compatibility(self._xil_api_maport)

        # check ESI connection (it raises an exception if not reachable).
        self.ESI_check()
        self._esi_check_xcp_version()
        self._last_esi_check = time.perf_counter()

        data_path_pc1 = replay_data['path1']
        data_path_pc2 = replay_data['path2']
        connection_manager = PortConnectionManager()

        connections, end_time = self._check_replay_data_files(
            connection_manager,
            data_path_pc1,
            data_path_pc2,
        )

        replay_time = None
        try:
            if replay_data['replay_time_flag'].lower() == 'true':
                replay_time = ReplayTimeConfiguration(
                    start=int(replay_data['replay_start_time']),
                    end=int(replay_data['replay_end_time']),
                )
        except Exception as exc:
            self._logger.error(
                f'Failed to parse replay-time configuration: {exc}'
            )

        # prepare connection
        connection_logger = self._logger.getChild("RTMapsConnection")
        rtmaps_connection = RtmapsConnection(
            self._rtmaps,
            self._remote_rtmaps,
            end_time,
            connection_logger,
        )

        # Enable the "slave" mechanism on the secondary server
        rtmaps_connection.configure_diagrams(
            replay_data['slave_diagram'],
            REMOTE_IP,
            RTMAPS_PORT,
        )

        data_lengths = {}
        for player in connection_manager.get_players():
            if player.location == PlayerLocation.PC1:
                data_path = data_path_pc1
            else:
                data_path = data_path_pc2

            data_lengths[player.location] = rtmaps_connection.configure_player(
                player=player,
                data_path=data_path,
                replay_time=replay_time,
            )

        for location, length in data_lengths.items():
            self._user_data[f'{location}_data_length'] = str(length)

        for connection in connections:
            rtmaps_connection.connect_port(connection)

        self._fetch_diagram_counters()

        # Check for any errors from the remote rtmaps.
        time.sleep(3)
        self._process_remote_rtmaps_logs()
        # Check if there were already errors during the initialization.
        if self._pending_exception is not None:
            tmp_exception = self._pending_exception
            self._pending_exception = None
            raise tmp_exception

        # Apply data manipualtion
        try:
            self._configure_data_manipulation(replay_data['data_manipulation'])
        except TestbenchPortException as ex:
            self._logger.exception(
                f'VendorCodeDescription: {ex.VendorCodeDescription}'
            )
            raise XilApiError(ex.CodeDescription)

        self._fetch_diagram_players()

    def _start_replay(self):
        try:
            # Start relplay.
            self.SCLX_model_config_startReplay()
            self._logger.info("Replay started!")
            # Check time calculations.
            values = self.monitor_time_calc(self._logger)
        except TestbenchPortException as ex:
            self._logger.exception(
                f'VendorCodeDescription: {ex.VendorCodeDescription}'
            )
            raise XilApiError(ex.CodeDescription)

        self._rtmaps.run()
        self._started = True
        self._logger.debug("RTMaps diagram started")
        self._user_data['start_time'] = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        self._start_time = time.perf_counter()

    def _create_start_shmem(self):
        self._shmem = ReplayJobSharedMemory(self._job_name, create=True)

    def _process_scalexio_messages(self, logger):
        logger = logger.getChild('ScalexioMessages')

        for message in self._sclx2_reader.get_messages():
            self._process_scalexio_message(logger, message)

        for message in self._sclx_reader.get_messages():
            self._process_scalexio_message(logger, message)

    def _process_scalexio_message(self, logger, message):
        # Generally, only print warnings and errors if debug is not set.
        do_print = (
            self._debug
            or (message.type in (DsMessageType.WARNING, DsMessageType.ERROR))
        )

        # Only count messages about the DsCanMsg timestamp.
        if "Timestamp of DsCanMsg" in message.message:
            # Print this message only once if the debug mode is not set!
            do_print = self._debug or (self._DsCanMsg_count == 0)
            self._DsCanMsg_count += 1
        elif 'DEBUG_REPLAY: to late id' in message.message:
            # Print this message only once if the debug mode is not set!
            do_print = self._debug or (self._too_late_count == 0)
            self._too_late_count += 1

        if do_print:
            logger.log(message.type.logging_level, message.message)

        if 'The sending buffers might be blocked' in message.message:
            raise RealtimeApplicationError(message.message)

    def _fetch_diagram_counters(self):
        self._logger.info("Getting the replay counters in each diagram")
        counters_to_check = [
            ("remote diagram", self._remote_rtmaps, "data_counter_dsu0_1"),
            ("local diagram", self._rtmaps, "data_counter_dsu1_1"),
        ]
        for name, rtmaps, component_id in counters_to_check:
            try:
                rtmaps.check_component_availability(component_id)
                rtmaps.check_property_availability(
                    component_id,
                    COUNTER_SUM_PROP_NAME,
                )
            except Exception:
                self._logger.warning(
                    f"Component {component_id} is missing in the {name}!"
                )
                self._logger.warning(f"Replay timeout disabled for {name}!")
            else:
                self._logger.info(
                    f"Registering counter {component_id} for {name}."
                )
                self._counters.append(
                    CounterData(
                        name=name,
                        rtmaps=rtmaps,
                        component_id=component_id,
                    )
                )

    def _check_real_replay_progress(self, logger=None):
        logger = logger or self._logger
        for data in self._counters:
            try:
                count = data.rtmaps.get_integer_property(
                    data.component_id,
                    COUNTER_SUM_PROP_NAME,
                )
            except Exception:
                logger.exception(
                    f"Failed to read replay count on {data.name}!"
                )
                count = data.last_count
            logger.debug(
                f"Count of {data.component_id} in {data.name}: {count}"
            )

            # This converts None to the last count.
            # Usually Nones are only returned when the component has not
            # finished starting (but what if it was dead?). We use last_count,
            # just to be safe to invoke a timeout.
            count = count or data.last_count

            if count > data.last_count or data.timestamp == 0:
                data.last_count = count
                data.timestamp = time.perf_counter()
            else:
                elapsed_time = time.perf_counter() - data.timestamp
                if elapsed_time >= self._replay_data_timeout:
                    raise ReplayFrozenError(
                        f"{data.name} is stale for {elapsed_time} seconds"
                    )

    def _fetch_diagram_players(self):
        self._logger.info("Getting the replay players in each diagram")
        for player in PortConnectionManager().get_players():
            if player.location == PlayerLocation.PC1:
                diagram = "local diagram"
                rtmaps = self._rtmaps
            else:
                diagram = "remote diagram"
                rtmaps = self._remote_rtmaps

            skip_frozen_check = self._check_frame_skipper(
                FRAME_SKIPPERS[player.location],
                rtmaps,
            )
            if skip_frozen_check:
                self._logger.info(
                    f"Frozen error detection is disabled on {player.location}"
                )

            try:
                rtmaps.check_component_availability(player.name)
                for prop in PLAYER_PROP_NAME:
                    rtmaps.check_property_availability(
                        player.name,
                        prop,
                    )
            except Exception as e:
                self._logger.warning(
                    f"Component {player.name} is missing in the {diagram}!"
                )
                self._logger.warning(
                    f"warning message: {e} ")
                self._logger.warning(f"Replay timeout disabled for {diagram}!")
            else:
                self._logger.info(
                    f"Registering player {player.name} for {diagram}."
                )
                self._players.append(
                    PlayerData(
                        name=diagram,
                        rtmaps=rtmaps,
                        component_id=player.name,
                        skip_frozen_check=skip_frozen_check,
                    )
                )

    def _check_frame_skipper(self, component_frame_skipper, rtmaps):
        for frame_skipper in component_frame_skipper:
            cam_suspend_duration = rtmaps.get_string_property(
                frame_skipper,
                "duration"
            )
            cam_suspend_starttime = rtmaps.get_string_property(
                frame_skipper,
                "start_time"
            )

            if "-1" in cam_suspend_duration.strip() and "-1" in cam_suspend_starttime.strip():
                return False

        return True

    def _check_player_percentage(self, logger=None):
        logger = logger or self._logger
        for data in self._players:
            # Skip if all the camera streams are suspended.
            if data.skip_frozen_check:
                continue

            try:
                percentage = data.rtmaps.get_integer_property(
                    data.component_id,
                    PLAYER_PROP_NAME[0],
                )
            except Exception:
                logger.exception(
                    f"Failed to read player percentage on {data.name}!"
                )
            try:
                  player_time = data.rtmaps.get_integer_property(
                    data.component_id,
                    PLAYER_PROP_NAME[1],
                )
            except:
                logger.exception(
                    f"Failed to read player player_time on {data.name}!"
                )

            logger.debug(
                f"percentage of {data.component_id} in {data.name}: {percentage}%"
            )
            logger.debug(
                f"player_time of {data.component_id} in {data.name}: {player_time}"
            )

            player_time = player_time or data.last_player_time

            if 0 <= percentage < 100:
                if player_time > data.last_player_time or data.timestamp == 0:
                    data.last_player_time = player_time
                    data.timestamp = time.perf_counter()
                else:
                    elapsed_time = time.perf_counter() - data.timestamp
                    if elapsed_time > 3:
                        raise ReplayFrozenError(
                                f"{data.name} is stale for {elapsed_time} seconds"
                            )

    def _check_esi_variables(self, logger):
        logger.debug(f'Reading ESI variables from {self._esi.devices}')
        for esi in self._esi_xcp_vars:
            logger.info(f'Getting XCP variables from {esi}')
            try:
                with XCPInterface(esi.ip, esi.port, logger) as xcp_comm:
                    resp = xcp_comm.send(XCPCommand.CONNECT)
                    if resp.type != XCPResponseType.RESPONSE:
                        logger.error(f'Failed to connect to {esi}')
                        return

                    for variable in esi.xcp_infos.variables:
                        if any(map(
                            variable.name.endswith,
                            ESI_XCP_ALLOW_LIST,
                        )):
                            try:
                                resp = xcp_comm.send(
                                    XCPCommand.SHORT_UPLOAD,
                                    variable.value.address,
                                    variable.value.type,
                                )
                            except Exception:
                                logger.exception(
                                    f'Failed to read XCP variable: {variable}'
                                )
                            else:
                                logger.info(f'    {variable.name}: {resp.value}')
                    xcp_comm.send(XCPCommand.DISCONNECT)
            except Exception:
                logger.exception(
                    'Failed to communicate with the ESI over XCP'
                )

    def get_progress(self, replay_state):
        # Fill user data:
        for key, value in self._user_data.items():
            replay_state.user_data[key] = value

        replay_state.user_data['update_time'] = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        if not self._started:
            if self._shmem is None:
                # This would be an implementation error! Should never happen!
                raise RuntimeError(
                    'Replay job not started and no shared memory object found.'
                )

            if self._shmem.start:
                self._start_replay()
            else:
                return

        # check ESI connection (it raises an exception if not reachable).
        if time.perf_counter() - self._last_esi_check >= ESI_CHECK_INTERVAL:
            self.ESI_check()
            self._last_esi_check = time.perf_counter()

        # Check if there are any pending exceptions (mostly form the rtmaps logs).
        if self._pending_exception is not None:
            tmp_exception = self._pending_exception
            self._pending_exception = None
            raise tmp_exception

        self._process_remote_rtmaps_logs()

        if self._xil_api_maport is None:
            # There is nothing to read anyway.
            replay_state.state = datareplay_pb2.ERROR
            return

        progress_logger = self._logger.getChild("getProgress")

        try:
            # Check if the RTPC has received the first and last time values.
            self._check_sclx_time(progress_logger)

            # DuTSyncStartCalc
            self.DuTSyncStartCalc(progress_logger)

            if time.perf_counter() - self._last_progress_print < PROGRESS_PRINT_INTERVAL:
                progress_logger = None
            else:
                self._last_progress_print = time.perf_counter()

            # get Progress
            self.get_replay_state(replay_state, progress_logger)

            # Replay System Monitoring
            if progress_logger:
                self.monitor_ESI1(progress_logger)
                self.monitor_ESI2(progress_logger)
                self.monitor_RTPC(progress_logger)
                self.monitor_replaypc_load(NETIO_URL, progress_logger)
                if self._debug:
                    self.monitor_someip(progress_logger)
                else:
                    self._check_someip_subscriptions(progress_logger)

        except TestbenchPortException as ex:
            self._logger.exception(f'CodeDescription: {ex.CodeDescription}')
            self._logger.error(
                f'VendorCodeDescription: {ex.VendorCodeDescription}'
            )

        if progress_logger:
            self._check_real_replay_progress(progress_logger)
            self._process_scalexio_messages(progress_logger)

            # if self.replayState == 1 and self._debug:
            if self.replayState == 1:
                self._check_esi_variables(progress_logger)
            elif self.replayState == 2:
                self._check_player_percentage(progress_logger)

        if replay_state.progress == 100:
            self._logger.info("Waiting for data transmission in 2s")
            time.sleep(2)

            # get finish time
            replay_state.user_data['end_time'] = datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
            )

            self._logger.info(f"start_time: {replay_state.user_data['start_time']}")
            self._logger.info(f"end_time: {replay_state.user_data['end_time']}")

            # XXX: Only for testing purpose! SHOULD NOT BE RELEASED!
            if self._too_late_count > 0:
                raise Exception('ETHCP too late error occured!')

            replay_state.state = datareplay_pb2.FINISHED

    def cleanup(self, reason, replay_data, final=True):
        self._logger.info(f"Starting cleanup process with reason {reason}.")

        # Read the ESI logs.
        if final and self._esi is not None:
            if reason != 2:
                try:
                    self._check_esi_variables(self._logger)
                except Exception:
                    self._logger.exception('Failed to read ESI variables.')
            else:
                # Check ESI connection (just for logging purposes).
                try:
                    self.ESI_check(reboot_on_error=False)
                except Exception:
                    self._logger.exception('Failed to check ESI status.')

                self._logger.info("Reading ESI logs...")
                for esi in self._esi.devices:
                    try:
                        self._create_esi_support(esi)
                    except Exception:
                        self._logger.exception(
                            f'Error while creating support tarball for {esi.name}'
                        )
        else:
            self._logger.info("Skipping ESI logs creation.")

        # Delete the shared memory if it exists:
        if self._shmem is not None:
            try:
                self._shmem.destroy()
            except Exception:
                self._logger.exception('Failed to destroy the shared memory.')
            finally:
                self._shmem = None

        if self._rt_app_download and self._xil_api_maport is not None:
            try:
                self._debug_xil_var_list(
                    xil_variables.OverrunCounters.items(),
                    self._logger,
                )
            except Exception:
                self._logger.exception('Failed to read the overrun counters.')

        # xil api clean up
        if final and self._xil_api_maport is not None:
            self._logger.info("Cleaning-up the XIL MAPort object.")
            try:
                self._xil_api_maport.cleanup()
            except Exception:
                self._logger.exception('Failed to cleanup XIL MAPort.')
            finally:
                self._xil_api_maport = None

        # SCALEXIO unload
        if final and self._rt_app_download:
            try:
                self.unload_SCLX_APP(
                    replay_data['CMDLOADER'],
                    replay_data['platform_name'],
                )
            except Exception:
                self._logger.exception('Failed to unload application.')
            finally:
                self._rt_app_download = False

        # Read any available logs in the remote rtmaps without exceptions.
        try:
            self._process_remote_rtmaps_logs(
                handle_errors=False,
                wait_till_shutdown=True,
            )
        except Exception:
            self._logger.exception('Failed to process remote RTMaps logs.')

        if self._too_late_count > 0:
            self._logger.warning(
                f'ETHCP too late error occured {self._too_late_count} times!'
            )
        if self._DsCanMsg_count > 0:
            self._logger.warning(
                f'DsCanMsg error occured {self._DsCanMsg_count} times!'
            )

        if self._restart_service_pending:
            # We raise an ESIError exception to communicate the necessity
            # to restart both the ESI units and the services.
            # But first reset the flag to avoid a second exception in case
            # of a second cleanup.
            self._restart_service_pending = False
            raise ESIError()

            # The auto-restart mechanism is disabled!
            try:
                self._restart_services()
            except Exception:
                self._logger.exception('Failed to restart services.')
            finally:
                self._restart_service_pending = False

        self._logger.info("Cleanup process finished.")

    def _restart_services(self):
        self._logger.warning(
            'An RTMaps error requiring a restart has been detected! '
            'Both services will be restarted now!'
        )
        kill_runtime.pc_ssh_restart(REMOTE_IP, "dspace", "dspace")
        kill_runtime.restart_replay_api_service()

    def _process_rtmaps_log(self, log_message):
        try:
            handler = self._rtmaps_error_handlers[log_message]
        except IndexError:
            # If no handlers and not an error message, ignore.
            if log_message.level < logging.ERROR:
                return RTMapsLogError.NoError

            self._logger.warning(f'Unknown RTMaps error: {log_message}')
            return RTMapsLogError.GenericError

        self._logger.info(
            f'RTMaps error "{log_message}" resolved to {handler.error_type}'
        )
        return handler.error_type

    def _create_esi_support(self, esi):
        self._logger.info(f"Reading ESI logs from {esi.name}...")
        # basedir = Path("/var/log/dspace")
        basedir = Path("/tmp")
        username = r"root"
        password = r"100%esiu"
        try:
            now = datetime.now().isoformat().replace(":", "_")
            tmp_dir = basedir / f"{now}_{self._job_name}_{esi.name}_{esi.ip}"
            tmp_dir.mkdir(parents=True, exist_ok=True)

            # Job log file.
            file_handlers = list(filter(
                lambda x: isinstance(x, logging.FileHandler),
                self._logger.parent.handlers,
            ))
            if file_handlers:
                # We assume the last file in the list is always the one
                # belonging to the job only (last one added) (a bit hacky).
                logfile = Path(file_handlers[-1].baseFilename)
                if logfile.exists():
                    self._logger.info(
                        f"Collecting the job's log file: {logfile}"
                    )
                    shutil.copy2(logfile, tmp_dir)
            else:
                self._logger.info("Failed to find the job's log file.")

            # FTP files.
            ftp_cred = {
                "id": esi.name,
                "addr": esi.ip,
                "usr": username,
                "passwd": password,
            }
            self._logger.info("Getting logs per FTP.")
            ftp_handle = esi_ftp_client(ftp_cred, self._logger)
            if ftp_handle.ftp_ready:
                ftp_handle.download_logs(save_dir=tmp_dir)
                coredump = Path('/tmp') / 'generic_app.elf.core'
                self._logger.info(
                    f'Attempting to download a coredump from {coredump}'
                )
                try:
                    ftp_handle.download_binary(
                        coredump,
                        tmp_dir / coredump.name,
                    )
                except Exception as exc:
                    self._logger.info(f'No coredump downloaded: {exc}!')
                else:
                    self._logger.warning('ESI coredump downloaded!')
                ftp_handle.quit()
            else:
                self._logger.error(f'Failed to connent to {esi} per FTP!')

            # Telnet stats.
            self._logger.info("Getting system stats per Telnet.")
            with esi_telnet.Telnet(esi.ip, 23, timeout=10) as tn:
                tn.login(username, password)
                esi_telnet.get_esi_stats(tn, tmp_dir)
        finally:
            # Zip the content.
            tmp_tarball_name = Path.home() / tmp_dir.with_suffix(".tgz").name
            ds_log_dir = Path('/var/log/dspace/')
            self._logger.info(f"Creating tarball file at {tmp_tarball_name}")
            with tarfile.TarFile.gzopen(tmp_tarball_name, mode="x") as tarball:
                tarball.add(tmp_dir)
            self._logger.info(
                f"ESI logs of {esi.name} written to {tmp_tarball_name}."
            )
            shutil.rmtree(tmp_dir, ignore_errors=True)
            try:
                shutil.move(tmp_tarball_name, ds_log_dir)
            except Exception as exc:
                self._logger.warning(
                    f'Failed to move tarball to {ds_log_dir}: {exc}'
                )
                self._logger.info(f'The file is left at {tmp_tarball_name}')
            else:
                self._logger.info(
                    f'Tarball moved to {ds_log_dir / tmp_tarball_name.name}'
                )

    def _reset_esis(self, force=False):
        self._logger.warning("Attempting to restart ESI units!")
        if not force and self._esi_restart_count > 0:
            self._logger.warning("Suppressing a second ESI reset!")
            return

        self._esi_restart_count += 1

        if self._esi is None:
            self._logger.error('No ESI units device instances created!')
            return

        # Disable the resetting before reading the ESI logs because we always
        # read logs now in cleanup.
        self._logger.warning("Resetting ESI units is disabled!")
        raise ESIError()

        self._logger.info("Reading ESI logs...")
        for esi in self._esi.devices:
            try:
                self._create_esi_support(esi)
            except Exception:
                self._logger.exception(
                    f'Error while creating support tarball for {esi.name}'
                )

        self._logger.warning("Resetting ESI units!")

        ecu_is_on = self._ecu.power_state == NetioState.on
        if ecu_is_on:
            # Turning ECU off.
            self.ecu_off()

        retries = 3
        reset_failed = False
        for i in range(retries, 0, -1):
            # Since both ESIs are connected to the same socket, it's enough to
            # reboot only one of them.
            self._esi.reboot()

            try:
                # Wait for both ESIs to finish booting.
                self._logger.info('Waiting for the ESI units.')
                self._esi.wait_till_online()
                self._logger.info('ESI units ready.')
            except TimeoutError as exc:
                # The raised TimeoutError has the device as its argument.
                dev = exc.args[0]
                c = retries - i + 1
                self._logger.error(
                    f"{dev.name} failed to boot properly ({c}/{retries})."
                )
                continue
            else:
                break
        else:
            self._logger.error(
                f"Failed to reset ESI units! (tried {retries} times)"
            )
            reset_failed = True

        if ecu_is_on:
            # Turning ECU back on.
            self.ecu_on()
            # ECU was restarted. Abort the test and notify the job.
            raise ECURestartedError()

        if reset_failed:
            raise ESIRestartTimeoutError()

    def _process_remote_rtmaps_logs(self, handle_errors=True, wait_till_shutdown=False):
        # Get the rtmaps console log output from the secondary server.
        # Currently simply log them again on the main machine
        if self._remote_rtmaps is None:
            return

        rtmaps_logger = self._logger.getChild("RemoteRTMaps")

        shutdown_msg_received = False
        shutdown_timeout = time.perf_counter() + 30  # seconds

        while True:
            # Read the logs and clear right away to make sure we are consistent
            try:
                rtmaps_logs = self._remote_rtmaps.get_log()
                self._remote_rtmaps.clear_log()
            except Exception:
                self._logger.warning('Failed to read remote RTMaps logs!')
                return

            exception_to_raise = None
            while rtmaps_logs:
                level, message = rtmaps_logs.pop(0)

                log_message = LogMessage(level=level, text=message)

                rtmaps_logger.log(log_message.level, log_message.text)

                error = self._process_rtmaps_log(log_message)

                if 'Shutdown OK' in message:
                    shutdown_msg_received = True

                # Error handling.
                if error != RTMapsLogError.NoError:
                    # We catch any possible exception and don't raise it right
                    # away because we want to print all messages first!
                    try:
                        self._handle_rtmaps_error(error, message)
                    except Exception as exc:
                        # We only store the first one for raising at the end.
                        exception_to_raise = exception_to_raise or exc

            # Break the loop already if we are not waiting for the shutdown or
            # if the shutdown message was received
            if not wait_till_shutdown or shutdown_msg_received:
                break

            # Break if we exceed the timeout.
            if time.perf_counter() > shutdown_timeout:
                self._logger.warning(
                    'Timeout while waiting for a successful timeout of RTMaps'
                )
                break

            # Wait one second before we try to read the logs again.
            time.sleep(1)

        if handle_errors and exception_to_raise is not None:
            raise exception_to_raise

    def _handle_rtmaps_error(self, error, message):
        self._logger.error(message)
        # Handling ESI Problems.
        if error == RTMapsLogError.Image2EsiError:
            # This method will raise its own exception if needed.
            self._reset_esis()
        else:
            if error == RTMapsLogError.RTMapsZombie:
                self._restart_service_pending = True
            raise RTMapsError(message)

    def get_callback(self):
        """
        Optional: If defined, it must return a function that accepts two
        arguments (level and message) or None. The function is called each time
        an RTMaps log event occurs. Must be non blocking.
        """
        def rtmaps_callback(level, message):
            log_message = LogMessage(level=level, text=message)

            error = self._process_rtmaps_log(log_message)

            # Generic error handling.
            if error != RTMapsLogError.NoError:
                self._logger.error(message)

                # Strictly speaking, we can let the exceptions get raised here,
                # because the replay_executor catches those exceptions and
                # stores them anyway. But we might want to handle our own
                # exceptions internally to be on the safe side.
                new_exception = None
                try:
                    self._handle_rtmaps_error(error, message)
                except Exception as exc:
                    new_exception = exc

                # Store the new exception only if there isn't one pending already.
                self._pending_exception = self._pending_exception or new_exception

        return rtmaps_callback
