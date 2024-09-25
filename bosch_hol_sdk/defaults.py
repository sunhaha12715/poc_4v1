"""
A collection of default values used in different places.

@copyright
    Copyright 2024, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
    All rights reserved.
"""
import pathlib


CMDLOADER_PATH = pathlib.PurePosixPath(
    r'/opt/dspace/xilapi.net4.0/MAPort/Main/bin/CmdLoader'
)

PLATFORM = 'SCALEXIO_2'

TEST_RTAPP_PATH = pathlib.Path(__file__).parent / 'system_reset' / 'reset_test_app'
TEST_RTAPP_SDF = TEST_RTAPP_PATH / 'DummyApp_XILAPI_ESI_Testing.sdf'
