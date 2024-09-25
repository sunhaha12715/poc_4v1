import abc
from collections.abc import Iterable
import logging

from dspace.bosch_hol_sdk.port_connection_config import PortConnectionManager
from dspace.bosch_hol_sdk.replay_plugin_exceptions import (
    BadXilPathError, XilWriteVerificationError,
)


class ManipulationBase(abc.ABC):
    def __init__(self, *args, configuration, logger=None, **kwargs):
        super().__init__(*args, **kwargs)
        parent_logger = logger or logging.getLogger('DRAPI.data_manipulation')
        self._logger = parent_logger.getChild(self.__class__.__name__)
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    @abc.abstractmethod
    def apply(self) -> None:
        """ Apply the manipulation configuration. """
        raise NotImplementedError()


class RTMapsManipulationBase(ManipulationBase):
    _connection_manager = PortConnectionManager()

    def __init__(self, *args, access_objects, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self._connection_manager.get_port_connection(
            self.configuration.name
        )
        self._rtmaps = access_objects['rtmaps'][conn.player.location]


class XilManipulationBase(ManipulationBase):
    _known_paths = None

    def __init__(self, *args, access_objects, **kwargs):
        super().__init__(*args, **kwargs)
        self._maport = access_objects['maport']

    @staticmethod
    def reload_known_paths(maport):
        XilManipulationBase._known_paths = maport.get_variables()

    @staticmethod
    def get_known_paths():
        return XilManipulationBase._known_paths

    def _check_variable_path(self, paths: Iterable[str]) -> None:
        # If no one loaded the data in advance, load now.
        if XilManipulationBase._known_paths is None:
            self.reload_known_paths(self._maport)

        for path in paths:
            if path in XilManipulationBase._known_paths:
                self._logger.debug(f'The path {path} is known.')
            else:
                raise BadXilPathError(path, self.configuration)

    def _write_variable(self, path, value, name=None):
        """ Write a value in a XIL path (Can raise XIL-Exceptions """
        name = name or path  # Use the path if no name is provided.
        value_before = self._maport.read_variable(path)
        self._logger.debug(f'{name} before write: {value_before}')

        if isinstance(value, Iterable):
            for idx, subvalue in enumerate(value):
                self._maport.write_variable(f'{path}[{idx}]', subvalue)
        else:
            self._maport.write_variable(path, value)

        value_after = self._maport.read_variable(path)
        self._logger.debug(f'{name} after write: {value_after}')

        # Throw away the irrelevant values.
        if isinstance(value, Iterable):
            if not isinstance(value_after, Iterable) or \
                    len(value_after) < len(value):
                raise XilWriteVerificationError(
                    path,
                    self.configuration,
                    value,
                    value_after,
                )
            del value_after[len(value):]

        # Check the read-back value.
        if value_after != value:
            raise XilWriteVerificationError(
                path,
                self.configuration,
                value,
                value_after,
            )
