"""
A basic XCP interface to send commands and interpret responses.

@copyright
    Copyright 2024, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
    All rights reserved.
"""
import enum
import logging
import socket
import struct


class XCPError(enum.IntEnum):
    # Command processor synchronization.
    ERR_CMD_SYNCH = 0x00
    # Command was not executed.
    ERR_CMD_BUSY = 0x10
    # Command rejected because DAQ is running.
    ERR_DAQ_ACTIVE = 0x11
    # Command rejected because PGM is running.
    ERR_PGM_ACTIVE = 0x12
    # Unknown command or not implemented optional command.
    ERR_CMD_UNKNOWN = 0x20
    # Command syntax invalid
    ERR_CMD_SYNTAX = 0x21
    # Command syntax valid but command parameter(s) out of range.
    ERR_OUT_OF_RANGE = 0x22
    # The memory location is write protected. S2
    ERR_WRITE_PROTECTED = 0x23
    # The memory location is not accessible. S2
    ERR_ACCESS_DENIED = 0x24
    # Access denied, Seed & Key is required
    ERR_ACCESS_LOCKED = 0x25
    # Selected page not available.
    ERR_PAGE_NOT_VALID = 0x26
    # Selected page mode not available.
    ERR_MODE_NOT_VALID = 0x27
    # Selected segment not valid.
    ERR_SEGMENT_NOT_VALID = 0x28
    # Sequence error.
    ERR_SEQUENCE = 0x29
    # DAQ configuration not valid.
    ERR_DAQ_CONFIG = 0x2A
    # Memory overflow error.
    ERR_MEMORY_OVERFLOW = 0x30
    # Generic error.
    ERR_GENERIC = 0x31
    # The slave internal program verify routine detects an error.
    ERR_VERIFY = 0x32


class _DataTypeImpl:
    def __init__(self, fmt):
        self._fmt = f'<{fmt}'

    def to_bytes(self, value):
        return struct.pack(self._fmt, value)

    def from_bytes(self, value):
        return struct.unpack(self._fmt, value)[0]

    def __len__(self):
        return struct.calcsize(self._fmt)


class DataType(enum.Enum):
    SBYTE = _DataTypeImpl('b')
    UBYTE = _DataTypeImpl('B')
    SWORD = _DataTypeImpl('h')
    UWORD = _DataTypeImpl('H')
    SLONG = _DataTypeImpl('l')
    ULONG = _DataTypeImpl('L')
    A_SINT64 = _DataTypeImpl('q')
    A_UINT64 = _DataTypeImpl('Q')
    FLOAT32_IEEE = _DataTypeImpl('f')
    FLOAT64_IEEE = _DataTypeImpl('d')

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


class XCPAddressExtension(enum.IntEnum):
    FREE = 0
    ODT = 1
    DAQ = 3


class XCPResponseType(enum.IntEnum):
    RESPONSE = 0xFF
    ERROR = 0xFE
    EVENT = 0xFD
    SERVICE = 0xFC


class XCPResponseBase:
    def __new__(cls, data):
        resp_type = XCPResponseType(data[0])
        if resp_type == XCPResponseType.RESPONSE:
            obj = super().__new__(cls)
        elif resp_type == XCPResponseType.ERROR:
            obj = super().__new__(XCPResponseError)
        else:
            raise NotImplementedError(resp_type)
        obj.__type = resp_type
        return obj

    @property
    def type(self):
        return self.__type


class XCPResponseError(XCPResponseBase):
    def __init__(self, data):
        self._data = data

    @property
    def error_code(self):
        return XCPError(self._data[1])


class XCPCommandBase:
    def __init__(self, data):
        self._data = data

    @property
    def size(self):
        return DataType.UWORD.value.to_bytes(len(self._data))

    def serialize(self):
        return bytes(self._data)


class XCPCommandConnect(XCPCommandBase):
    def __init__(self):
        super().__init__([0xFF, 0x00])

    class Response(XCPResponseBase):
        size = 8
        # We don't care much about the content of the response at the moment,
        # just that it's a response, not an error.


class XCPCommandDisconnect(XCPCommandBase):
    def __init__(self):
        super().__init__([0xFE])

    class Response(XCPResponseBase):
        size = 1


class XCPCommandShortUpload(XCPCommandBase):
    def __init__(self, address, datatype):
        super().__init__(
            [0xF4,
             len(datatype.value),
             0,
             XCPAddressExtension.FREE,
             *list(DataType.ULONG.value.to_bytes(address))
             ],
        )

        class _Response(XCPResponseBase):
            size = 1 + len(datatype.value)

            def __init__(self, data):
                super().__init__()
                self._data = data

            @property
            def value(self):
                return datatype.value.from_bytes(self._data[1:])

        self.Response = _Response


class XCPCommand(enum.Enum):
    CONNECT = XCPCommandConnect
    DISCONNECT = XCPCommandDisconnect
    SHORT_UPLOAD = XCPCommandShortUpload


class XCPInterface:
    def __init__(self, ip, port, logger=None):
        if logger is None:
            logger = logging.getLogger()
        self._logger = logger.getChild(f'{self.__class__.__name__}')
        self._ip = ip
        self._port = port
        self._communicator = None

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((self._ip, self._port))
        self._communicator = self._Communicator(
            sock,
            self._logger.getChild(self._ip.replace(".", "_")),
        )
        return self._communicator

    def __exit__(self, exc_type, exc_value, traceback):
        if self._communicator is not None:
            self._communicator.close()

    class _Communicator:
        def __init__(self, socket, logger):
            self._socket = socket
            self._logger = logger
            self._counter = 0

        def __del__(self):
            self.close()

        def close(self):
            self._socket.close()

        @property
        def counter(self):
            self._counter += 1
            return DataType.UWORD.value.to_bytes(self._counter)

        def send(self, cmd, *args, **kwargs):
            if isinstance(cmd, XCPCommand):
                cmd = cmd.value(*args, **kwargs)
            elif not isinstance(cmd, XCPCommandBase):
                raise TypeError(cmd)

            cmd_bytes = cmd.size + self.counter + cmd.serialize()
            self._logger.debug('Sending command: %s', cmd_bytes)
            self._socket.send(cmd_bytes)

            response_bytes = self._socket.recv(cmd.Response.size + 4)
            self._logger.debug('Received response: %s', response_bytes)
            response_size = DataType.UWORD.value.from_bytes(response_bytes[0:2])
            return cmd.Response(response_bytes[4: 4 + response_size])
