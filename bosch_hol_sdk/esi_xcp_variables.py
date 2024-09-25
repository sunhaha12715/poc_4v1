#!/usr/bin/env python3.9
"""
!!!DO NOT MODIFY BY HAND!!!

An automatically generated Python script containing the XCP variables of ESI
devices.

Generated on: 2024-09-19 16:13:35.032047
A2L Files:
    esi1: ESIKitDrive.a2l(2024-09-19 15:17:53.876339)
    esi2: ESIKitDrive.a2l(2024-09-06 10:29:45.600498)

@copyright
    Copyright 2024, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
    All rights reserved.
"""
import dataclasses
import enum

from dspace.bosch_hol_sdk.xcpinterface import (
    XCPInterface, XCPCommand, DataType, XCPResponseType,
)


@dataclasses.dataclass
class Variable:
    type: DataType
    address: int


@dataclasses.dataclass
class EsiInfo:
    name: str
    version: str
    version_address: int
    variables: enum.Enum


class _Esi1Variables(enum.Enum):
    Replay_Application_OutputValue = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000000,
    )
    Replay_Application_VDC0_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000008,
    )
    Replay_Application_VDC0_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000010,
    )
    Replay_Application_VDC0_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000018,
    )
    Replay_Application_VDC0_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000020,
    )
    Replay_Application_VDC0_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000028,
    )
    Replay_Application_VDC0_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000030,
    )
    Replay_Application_VDC0_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000038,
    )
    Replay_Application_VDC1_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000040,
    )
    Replay_Application_VDC1_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000048,
    )
    Replay_Application_VDC1_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000050,
    )
    Replay_Application_VDC1_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000058,
    )
    Replay_Application_VDC1_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000060,
    )
    Replay_Application_VDC1_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000068,
    )
    Replay_Application_VDC1_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000070,
    )
    Replay_Application_VDC2_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000078,
    )
    Replay_Application_VDC2_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000080,
    )
    Replay_Application_VDC2_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000088,
    )
    Replay_Application_VDC2_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000090,
    )
    Replay_Application_VDC2_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000098,
    )
    Replay_Application_VDC2_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0000A0,
    )
    Replay_Application_VDC2_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0000A8,
    )
    Replay_Application_VDC3_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD0000B0,
    )
    Replay_Application_VDC3_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD0000B8,
    )
    Replay_Application_VDC3_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0000C0,
    )
    Replay_Application_VDC3_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0000C8,
    )
    Replay_Application_VDC3_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD0000D0,
    )
    Replay_Application_VDC3_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0000D8,
    )
    Replay_Application_VDC3_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0000E0,
    )
    Replay_Application_VDC4_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD0000E8,
    )
    Replay_Application_VDC4_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD0000F0,
    )
    Replay_Application_VDC4_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0000F8,
    )
    Replay_Application_VDC4_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000100,
    )
    Replay_Application_VDC4_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000108,
    )
    Replay_Application_VDC4_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000110,
    )
    Replay_Application_VDC4_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000118,
    )
    Replay_Application_VDC5_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000120,
    )
    Replay_Application_VDC5_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000128,
    )
    Replay_Application_VDC5_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000130,
    )
    Replay_Application_VDC5_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000138,
    )
    Replay_Application_VDC5_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000140,
    )
    Replay_Application_VDC5_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000148,
    )
    Replay_Application_VDC5_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000150,
    )
    Replay_Application_VDC6_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000158,
    )
    Replay_Application_VDC6_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000160,
    )
    Replay_Application_VDC6_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000168,
    )
    Replay_Application_VDC6_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000170,
    )
    Replay_Application_VDC6_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000178,
    )
    Replay_Application_VDC6_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000180,
    )
    Replay_Application_VDC6_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000188,
    )
    Replay_Application_VDC7_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000190,
    )
    Replay_Application_VDC7_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000198,
    )
    Replay_Application_VDC7_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0001A0,
    )
    Replay_Application_VDC7_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001A8,
    )
    Replay_Application_VDC7_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD0001B0,
    )
    Replay_Application_VDC7_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0001B8,
    )
    Replay_Application_VDC7_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0001C0,
    )
    Replay_Application_ch0fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001C8,
    )
    Replay_Application_ch1fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001D0,
    )
    Replay_Application_ch2fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001D8,
    )
    Replay_Application_ch3fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001E0,
    )
    Replay_Application_ch4fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001E8,
    )
    Replay_Application_ch5fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001F0,
    )
    Replay_Application_ch6fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001F8,
    )
    Replay_Application_ch7fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000200,
    )
    Replay_Application_daqTime = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000208,
    )
    replay_subsystem_0_channel_0_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000210,
    )
    replay_subsystem_0_channel_0_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000218,
    )
    replay_subsystem_0_channel_0_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000220,
    )
    replay_subsystem_0_channel_0_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000228,
    )
    replay_subsystem_0_channel_0_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000230,
    )
    replay_subsystem_0_channel_0_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000238,
    )
    replay_subsystem_0_channel_0_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000240,
    )
    replay_subsystem_0_channel_0_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000248,
    )
    replay_subsystem_0_channel_0_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000250,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000258,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000260,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000268,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000270,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000278,
    )
    replay_subsystem_0_channel_0_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000280,
    )
    replay_subsystem_0_channel_0_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000288,
    )
    replay_subsystem_0_channel_0_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000290,
    )
    replay_subsystem_0_channel_0_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000298,
    )
    replay_subsystem_0_channel_0_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0002A0,
    )
    replay_subsystem_0_channel_0_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0002A8,
    )
    replay_subsystem_0_channel_0_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0002B0,
    )
    replay_subsystem_0_channel_0_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0002B8,
    )
    replay_subsystem_0_channel_0_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0002C0,
    )
    replay_subsystem_0_channel_0_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002C8,
    )
    replay_subsystem_0_channel_0_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002D0,
    )
    replay_subsystem_0_channel_0_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0002D8,
    )
    replay_subsystem_0_channel_0_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0002E0,
    )
    replay_subsystem_0_channel_0_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0002E8,
    )
    replay_subsystem_0_channel_1_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0002F0,
    )
    replay_subsystem_0_channel_1_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002F8,
    )
    replay_subsystem_0_channel_1_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000300,
    )
    replay_subsystem_0_channel_1_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000308,
    )
    replay_subsystem_0_channel_1_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000310,
    )
    replay_subsystem_0_channel_1_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000318,
    )
    replay_subsystem_0_channel_1_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000320,
    )
    replay_subsystem_0_channel_1_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000328,
    )
    replay_subsystem_0_channel_1_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000330,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000338,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000340,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000348,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000350,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000358,
    )
    replay_subsystem_0_channel_1_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000360,
    )
    replay_subsystem_0_channel_1_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000368,
    )
    replay_subsystem_0_channel_1_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000370,
    )
    replay_subsystem_0_channel_1_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000378,
    )
    replay_subsystem_0_channel_1_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000380,
    )
    replay_subsystem_0_channel_1_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000388,
    )
    replay_subsystem_0_channel_1_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000390,
    )
    replay_subsystem_0_channel_1_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000398,
    )
    replay_subsystem_0_channel_1_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0003A0,
    )
    replay_subsystem_0_channel_1_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003A8,
    )
    replay_subsystem_0_channel_1_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003B0,
    )
    replay_subsystem_0_channel_1_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0003B8,
    )
    replay_subsystem_0_channel_1_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0003C0,
    )
    replay_subsystem_0_channel_1_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0003C8,
    )
    replay_subsystem_0_channel_2_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0003D0,
    )
    replay_subsystem_0_channel_2_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003D8,
    )
    replay_subsystem_0_channel_2_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003E0,
    )
    replay_subsystem_0_channel_2_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003E8,
    )
    replay_subsystem_0_channel_2_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003F0,
    )
    replay_subsystem_0_channel_2_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003F8,
    )
    replay_subsystem_0_channel_2_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000400,
    )
    replay_subsystem_0_channel_2_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000408,
    )
    replay_subsystem_0_channel_2_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000410,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000418,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000420,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000428,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000430,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000438,
    )
    replay_subsystem_0_channel_2_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000440,
    )
    replay_subsystem_0_channel_2_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000448,
    )
    replay_subsystem_0_channel_2_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000450,
    )
    replay_subsystem_0_channel_2_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000458,
    )
    replay_subsystem_0_channel_2_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000460,
    )
    replay_subsystem_0_channel_2_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000468,
    )
    replay_subsystem_0_channel_2_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000470,
    )
    replay_subsystem_0_channel_2_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000478,
    )
    replay_subsystem_0_channel_2_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000480,
    )
    replay_subsystem_0_channel_2_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000488,
    )
    replay_subsystem_0_channel_2_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000490,
    )
    replay_subsystem_0_channel_2_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000498,
    )
    replay_subsystem_0_channel_2_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0004A0,
    )
    replay_subsystem_0_channel_2_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0004A8,
    )
    replay_subsystem_0_channel_3_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0004B0,
    )
    replay_subsystem_0_channel_3_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004B8,
    )
    replay_subsystem_0_channel_3_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004C0,
    )
    replay_subsystem_0_channel_3_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004C8,
    )
    replay_subsystem_0_channel_3_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004D0,
    )
    replay_subsystem_0_channel_3_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004D8,
    )
    replay_subsystem_0_channel_3_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004E0,
    )
    replay_subsystem_0_channel_3_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004E8,
    )
    replay_subsystem_0_channel_3_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004F0,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004F8,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000500,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000508,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000510,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000518,
    )
    replay_subsystem_0_channel_3_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000520,
    )
    replay_subsystem_0_channel_3_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000528,
    )
    replay_subsystem_0_channel_3_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000530,
    )
    replay_subsystem_0_channel_3_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000538,
    )
    replay_subsystem_0_channel_3_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000540,
    )
    replay_subsystem_0_channel_3_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000548,
    )
    replay_subsystem_0_channel_3_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000550,
    )
    replay_subsystem_0_channel_3_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000558,
    )
    replay_subsystem_0_channel_3_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000560,
    )
    replay_subsystem_0_channel_3_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000568,
    )
    replay_subsystem_0_channel_3_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000570,
    )
    replay_subsystem_0_channel_3_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000578,
    )
    replay_subsystem_0_channel_3_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000580,
    )
    replay_subsystem_0_channel_3_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000588,
    )
    replay_subsystem_0_channel_4_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000590,
    )
    replay_subsystem_0_channel_4_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000598,
    )
    replay_subsystem_0_channel_4_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005A0,
    )
    replay_subsystem_0_channel_4_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005A8,
    )
    replay_subsystem_0_channel_4_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005B0,
    )
    replay_subsystem_0_channel_4_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005B8,
    )
    replay_subsystem_0_channel_4_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005C0,
    )
    replay_subsystem_0_channel_4_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005C8,
    )
    replay_subsystem_0_channel_4_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005D0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005D8,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0005E0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0005E8,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0005F0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0005F8,
    )
    replay_subsystem_0_channel_4_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000600,
    )
    replay_subsystem_0_channel_4_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000608,
    )
    replay_subsystem_0_channel_4_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000610,
    )
    replay_subsystem_0_channel_4_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000618,
    )
    replay_subsystem_0_channel_4_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000620,
    )
    replay_subsystem_0_channel_4_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000628,
    )
    replay_subsystem_0_channel_4_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000630,
    )
    replay_subsystem_0_channel_4_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000638,
    )
    replay_subsystem_0_channel_4_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000640,
    )
    replay_subsystem_0_channel_4_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000648,
    )
    replay_subsystem_0_channel_4_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000650,
    )
    replay_subsystem_0_channel_4_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000658,
    )
    replay_subsystem_0_channel_4_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000660,
    )
    replay_subsystem_0_channel_4_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000668,
    )
    replay_subsystem_0_channel_5_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000670,
    )
    replay_subsystem_0_channel_5_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000678,
    )
    replay_subsystem_0_channel_5_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000680,
    )
    replay_subsystem_0_channel_5_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000688,
    )
    replay_subsystem_0_channel_5_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000690,
    )
    replay_subsystem_0_channel_5_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000698,
    )
    replay_subsystem_0_channel_5_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0006A0,
    )
    replay_subsystem_0_channel_5_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006A8,
    )
    replay_subsystem_0_channel_5_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006B0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006B8,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0006C0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0006C8,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0006D0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0006D8,
    )
    replay_subsystem_0_channel_5_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0006E0,
    )
    replay_subsystem_0_channel_5_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0006E8,
    )
    replay_subsystem_0_channel_5_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0006F0,
    )
    replay_subsystem_0_channel_5_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0006F8,
    )
    replay_subsystem_0_channel_5_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000700,
    )
    replay_subsystem_0_channel_5_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000708,
    )
    replay_subsystem_0_channel_5_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000710,
    )
    replay_subsystem_0_channel_5_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000718,
    )
    replay_subsystem_0_channel_5_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000720,
    )
    replay_subsystem_0_channel_5_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000728,
    )
    replay_subsystem_0_channel_5_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000730,
    )
    replay_subsystem_0_channel_5_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000738,
    )
    replay_subsystem_0_channel_5_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000740,
    )
    replay_subsystem_0_channel_5_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000748,
    )
    replay_subsystem_0_channel_6_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000750,
    )
    replay_subsystem_0_channel_6_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000758,
    )
    replay_subsystem_0_channel_6_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000760,
    )
    replay_subsystem_0_channel_6_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000768,
    )
    replay_subsystem_0_channel_6_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000770,
    )
    replay_subsystem_0_channel_6_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000778,
    )
    replay_subsystem_0_channel_6_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000780,
    )
    replay_subsystem_0_channel_6_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000788,
    )
    replay_subsystem_0_channel_6_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000790,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000798,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0007A0,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0007A8,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0007B0,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0007B8,
    )
    replay_subsystem_0_channel_6_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0007C0,
    )
    replay_subsystem_0_channel_6_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0007C8,
    )
    replay_subsystem_0_channel_6_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0007D0,
    )
    replay_subsystem_0_channel_6_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0007D8,
    )
    replay_subsystem_0_channel_6_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0007E0,
    )
    replay_subsystem_0_channel_6_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0007E8,
    )
    replay_subsystem_0_channel_6_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0007F0,
    )
    replay_subsystem_0_channel_6_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0007F8,
    )
    replay_subsystem_0_channel_6_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000800,
    )
    replay_subsystem_0_channel_6_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000808,
    )
    replay_subsystem_0_channel_6_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000810,
    )
    replay_subsystem_0_channel_6_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000818,
    )
    replay_subsystem_0_channel_6_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000820,
    )
    replay_subsystem_0_channel_6_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000828,
    )
    replay_subsystem_0_channel_7_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000830,
    )
    replay_subsystem_0_channel_7_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000838,
    )
    replay_subsystem_0_channel_7_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000840,
    )
    replay_subsystem_0_channel_7_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000848,
    )
    replay_subsystem_0_channel_7_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000850,
    )
    replay_subsystem_0_channel_7_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000858,
    )
    replay_subsystem_0_channel_7_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000860,
    )
    replay_subsystem_0_channel_7_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000868,
    )
    replay_subsystem_0_channel_7_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000870,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000878,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000880,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000888,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000890,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000898,
    )
    replay_subsystem_0_channel_7_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0008A0,
    )
    replay_subsystem_0_channel_7_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0008A8,
    )
    replay_subsystem_0_channel_7_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0008B0,
    )
    replay_subsystem_0_channel_7_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0008B8,
    )
    replay_subsystem_0_channel_7_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0008C0,
    )
    replay_subsystem_0_channel_7_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0008C8,
    )
    replay_subsystem_0_channel_7_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0008D0,
    )
    replay_subsystem_0_channel_7_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0008D8,
    )
    replay_subsystem_0_channel_7_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0008E0,
    )
    replay_subsystem_0_channel_7_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0008E8,
    )
    replay_subsystem_0_channel_7_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0008F0,
    )
    replay_subsystem_0_channel_7_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0008F8,
    )
    replay_subsystem_0_channel_7_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000900,
    )
    replay_subsystem_0_channel_7_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000908,
    )
    replay_subsystem_0_current_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000910,
    )
    replay_subsystem_0_numChannels = Variable(
        type=DataType.ULONG,
        address=0XFD000918,
    )
    replay_subsystem_0_ptp_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000920,
    )


class _Esi2Variables(enum.Enum):
    Replay_Application_OutputValue = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000000,
    )
    Replay_Application_VDC0_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000008,
    )
    Replay_Application_VDC0_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000010,
    )
    Replay_Application_VDC0_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000018,
    )
    Replay_Application_VDC0_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000020,
    )
    Replay_Application_VDC0_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000028,
    )
    Replay_Application_VDC0_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000030,
    )
    Replay_Application_VDC0_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000038,
    )
    Replay_Application_VDC1_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000040,
    )
    Replay_Application_VDC1_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000048,
    )
    Replay_Application_VDC1_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000050,
    )
    Replay_Application_VDC1_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000058,
    )
    Replay_Application_VDC1_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000060,
    )
    Replay_Application_VDC1_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000068,
    )
    Replay_Application_VDC1_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000070,
    )
    Replay_Application_VDC2_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000078,
    )
    Replay_Application_VDC2_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000080,
    )
    Replay_Application_VDC2_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000088,
    )
    Replay_Application_VDC2_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000090,
    )
    Replay_Application_VDC2_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000098,
    )
    Replay_Application_VDC2_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0000A0,
    )
    Replay_Application_VDC2_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0000A8,
    )
    Replay_Application_VDC3_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD0000B0,
    )
    Replay_Application_VDC3_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD0000B8,
    )
    Replay_Application_VDC3_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0000C0,
    )
    Replay_Application_VDC3_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0000C8,
    )
    Replay_Application_VDC3_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD0000D0,
    )
    Replay_Application_VDC3_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0000D8,
    )
    Replay_Application_VDC3_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0000E0,
    )
    Replay_Application_VDC4_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD0000E8,
    )
    Replay_Application_VDC4_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD0000F0,
    )
    Replay_Application_VDC4_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0000F8,
    )
    Replay_Application_VDC4_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000100,
    )
    Replay_Application_VDC4_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000108,
    )
    Replay_Application_VDC4_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000110,
    )
    Replay_Application_VDC4_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000118,
    )
    Replay_Application_VDC5_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000120,
    )
    Replay_Application_VDC5_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000128,
    )
    Replay_Application_VDC5_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000130,
    )
    Replay_Application_VDC5_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000138,
    )
    Replay_Application_VDC5_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000140,
    )
    Replay_Application_VDC5_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000148,
    )
    Replay_Application_VDC5_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000150,
    )
    Replay_Application_VDC6_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000158,
    )
    Replay_Application_VDC6_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000160,
    )
    Replay_Application_VDC6_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD000168,
    )
    Replay_Application_VDC6_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000170,
    )
    Replay_Application_VDC6_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD000178,
    )
    Replay_Application_VDC6_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD000180,
    )
    Replay_Application_VDC6_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD000188,
    )
    Replay_Application_VDC7_frameCounter = Variable(
        type=DataType.ULONG,
        address=0XFD000190,
    )
    Replay_Application_VDC7_frameCurLine = Variable(
        type=DataType.ULONG,
        address=0XFD000198,
    )
    Replay_Application_VDC7_frameCurPixel = Variable(
        type=DataType.ULONG,
        address=0XFD0001A0,
    )
    Replay_Application_VDC7_frameFrequency = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001A8,
    )
    Replay_Application_VDC7_inputSizeX = Variable(
        type=DataType.ULONG,
        address=0XFD0001B0,
    )
    Replay_Application_VDC7_inputSizeY = Variable(
        type=DataType.ULONG,
        address=0XFD0001B8,
    )
    Replay_Application_VDC7_operationMode = Variable(
        type=DataType.UBYTE,
        address=0XFD0001C0,
    )
    Replay_Application_ch0fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001C8,
    )
    Replay_Application_ch1fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001D0,
    )
    Replay_Application_ch2fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001D8,
    )
    Replay_Application_ch3fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001E0,
    )
    Replay_Application_ch4fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001E8,
    )
    Replay_Application_ch5fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001F0,
    )
    Replay_Application_ch6fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0001F8,
    )
    Replay_Application_ch7fps = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000200,
    )
    Replay_Application_daqTime = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000208,
    )
    replay_subsystem_0_channel_0_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000210,
    )
    replay_subsystem_0_channel_0_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000218,
    )
    replay_subsystem_0_channel_0_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000220,
    )
    replay_subsystem_0_channel_0_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000228,
    )
    replay_subsystem_0_channel_0_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000230,
    )
    replay_subsystem_0_channel_0_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000238,
    )
    replay_subsystem_0_channel_0_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000240,
    )
    replay_subsystem_0_channel_0_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000248,
    )
    replay_subsystem_0_channel_0_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000250,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000258,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000260,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000268,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000270,
    )
    replay_subsystem_0_channel_0_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000278,
    )
    replay_subsystem_0_channel_0_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000280,
    )
    replay_subsystem_0_channel_0_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000288,
    )
    replay_subsystem_0_channel_0_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000290,
    )
    replay_subsystem_0_channel_0_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000298,
    )
    replay_subsystem_0_channel_0_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0002A0,
    )
    replay_subsystem_0_channel_0_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0002A8,
    )
    replay_subsystem_0_channel_0_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0002B0,
    )
    replay_subsystem_0_channel_0_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0002B8,
    )
    replay_subsystem_0_channel_0_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0002C0,
    )
    replay_subsystem_0_channel_0_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002C8,
    )
    replay_subsystem_0_channel_0_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002D0,
    )
    replay_subsystem_0_channel_0_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0002D8,
    )
    replay_subsystem_0_channel_0_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0002E0,
    )
    replay_subsystem_0_channel_0_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0002E8,
    )
    replay_subsystem_0_channel_1_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0002F0,
    )
    replay_subsystem_0_channel_1_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0002F8,
    )
    replay_subsystem_0_channel_1_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000300,
    )
    replay_subsystem_0_channel_1_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000308,
    )
    replay_subsystem_0_channel_1_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000310,
    )
    replay_subsystem_0_channel_1_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000318,
    )
    replay_subsystem_0_channel_1_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000320,
    )
    replay_subsystem_0_channel_1_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000328,
    )
    replay_subsystem_0_channel_1_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000330,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000338,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000340,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000348,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000350,
    )
    replay_subsystem_0_channel_1_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000358,
    )
    replay_subsystem_0_channel_1_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000360,
    )
    replay_subsystem_0_channel_1_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000368,
    )
    replay_subsystem_0_channel_1_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000370,
    )
    replay_subsystem_0_channel_1_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000378,
    )
    replay_subsystem_0_channel_1_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000380,
    )
    replay_subsystem_0_channel_1_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000388,
    )
    replay_subsystem_0_channel_1_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000390,
    )
    replay_subsystem_0_channel_1_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000398,
    )
    replay_subsystem_0_channel_1_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0003A0,
    )
    replay_subsystem_0_channel_1_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003A8,
    )
    replay_subsystem_0_channel_1_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003B0,
    )
    replay_subsystem_0_channel_1_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0003B8,
    )
    replay_subsystem_0_channel_1_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0003C0,
    )
    replay_subsystem_0_channel_1_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0003C8,
    )
    replay_subsystem_0_channel_2_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0003D0,
    )
    replay_subsystem_0_channel_2_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003D8,
    )
    replay_subsystem_0_channel_2_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003E0,
    )
    replay_subsystem_0_channel_2_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003E8,
    )
    replay_subsystem_0_channel_2_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003F0,
    )
    replay_subsystem_0_channel_2_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0003F8,
    )
    replay_subsystem_0_channel_2_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000400,
    )
    replay_subsystem_0_channel_2_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000408,
    )
    replay_subsystem_0_channel_2_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000410,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000418,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000420,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000428,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000430,
    )
    replay_subsystem_0_channel_2_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000438,
    )
    replay_subsystem_0_channel_2_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000440,
    )
    replay_subsystem_0_channel_2_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000448,
    )
    replay_subsystem_0_channel_2_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000450,
    )
    replay_subsystem_0_channel_2_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000458,
    )
    replay_subsystem_0_channel_2_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000460,
    )
    replay_subsystem_0_channel_2_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000468,
    )
    replay_subsystem_0_channel_2_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000470,
    )
    replay_subsystem_0_channel_2_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000478,
    )
    replay_subsystem_0_channel_2_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000480,
    )
    replay_subsystem_0_channel_2_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000488,
    )
    replay_subsystem_0_channel_2_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000490,
    )
    replay_subsystem_0_channel_2_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000498,
    )
    replay_subsystem_0_channel_2_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD0004A0,
    )
    replay_subsystem_0_channel_2_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD0004A8,
    )
    replay_subsystem_0_channel_3_active = Variable(
        type=DataType.UBYTE,
        address=0XFD0004B0,
    )
    replay_subsystem_0_channel_3_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004B8,
    )
    replay_subsystem_0_channel_3_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004C0,
    )
    replay_subsystem_0_channel_3_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004C8,
    )
    replay_subsystem_0_channel_3_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004D0,
    )
    replay_subsystem_0_channel_3_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004D8,
    )
    replay_subsystem_0_channel_3_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0004E0,
    )
    replay_subsystem_0_channel_3_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004E8,
    )
    replay_subsystem_0_channel_3_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004F0,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0004F8,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000500,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000508,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000510,
    )
    replay_subsystem_0_channel_3_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000518,
    )
    replay_subsystem_0_channel_3_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000520,
    )
    replay_subsystem_0_channel_3_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000528,
    )
    replay_subsystem_0_channel_3_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000530,
    )
    replay_subsystem_0_channel_3_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000538,
    )
    replay_subsystem_0_channel_3_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000540,
    )
    replay_subsystem_0_channel_3_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000548,
    )
    replay_subsystem_0_channel_3_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000550,
    )
    replay_subsystem_0_channel_3_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000558,
    )
    replay_subsystem_0_channel_3_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000560,
    )
    replay_subsystem_0_channel_3_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000568,
    )
    replay_subsystem_0_channel_3_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000570,
    )
    replay_subsystem_0_channel_3_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000578,
    )
    replay_subsystem_0_channel_3_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000580,
    )
    replay_subsystem_0_channel_3_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000588,
    )
    replay_subsystem_0_channel_4_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000590,
    )
    replay_subsystem_0_channel_4_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000598,
    )
    replay_subsystem_0_channel_4_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005A0,
    )
    replay_subsystem_0_channel_4_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005A8,
    )
    replay_subsystem_0_channel_4_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005B0,
    )
    replay_subsystem_0_channel_4_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005B8,
    )
    replay_subsystem_0_channel_4_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0005C0,
    )
    replay_subsystem_0_channel_4_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005C8,
    )
    replay_subsystem_0_channel_4_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005D0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0005D8,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0005E0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0005E8,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0005F0,
    )
    replay_subsystem_0_channel_4_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0005F8,
    )
    replay_subsystem_0_channel_4_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000600,
    )
    replay_subsystem_0_channel_4_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD000608,
    )
    replay_subsystem_0_channel_4_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD000610,
    )
    replay_subsystem_0_channel_4_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD000618,
    )
    replay_subsystem_0_channel_4_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000620,
    )
    replay_subsystem_0_channel_4_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000628,
    )
    replay_subsystem_0_channel_4_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000630,
    )
    replay_subsystem_0_channel_4_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000638,
    )
    replay_subsystem_0_channel_4_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000640,
    )
    replay_subsystem_0_channel_4_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000648,
    )
    replay_subsystem_0_channel_4_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000650,
    )
    replay_subsystem_0_channel_4_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000658,
    )
    replay_subsystem_0_channel_4_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000660,
    )
    replay_subsystem_0_channel_4_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000668,
    )
    replay_subsystem_0_channel_5_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000670,
    )
    replay_subsystem_0_channel_5_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000678,
    )
    replay_subsystem_0_channel_5_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000680,
    )
    replay_subsystem_0_channel_5_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000688,
    )
    replay_subsystem_0_channel_5_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000690,
    )
    replay_subsystem_0_channel_5_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000698,
    )
    replay_subsystem_0_channel_5_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0006A0,
    )
    replay_subsystem_0_channel_5_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006A8,
    )
    replay_subsystem_0_channel_5_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006B0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD0006B8,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0006C0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0006C8,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0006D0,
    )
    replay_subsystem_0_channel_5_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0006D8,
    )
    replay_subsystem_0_channel_5_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0006E0,
    )
    replay_subsystem_0_channel_5_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0006E8,
    )
    replay_subsystem_0_channel_5_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0006F0,
    )
    replay_subsystem_0_channel_5_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0006F8,
    )
    replay_subsystem_0_channel_5_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD000700,
    )
    replay_subsystem_0_channel_5_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000708,
    )
    replay_subsystem_0_channel_5_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD000710,
    )
    replay_subsystem_0_channel_5_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000718,
    )
    replay_subsystem_0_channel_5_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000720,
    )
    replay_subsystem_0_channel_5_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000728,
    )
    replay_subsystem_0_channel_5_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000730,
    )
    replay_subsystem_0_channel_5_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000738,
    )
    replay_subsystem_0_channel_5_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000740,
    )
    replay_subsystem_0_channel_5_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000748,
    )
    replay_subsystem_0_channel_6_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000750,
    )
    replay_subsystem_0_channel_6_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000758,
    )
    replay_subsystem_0_channel_6_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000760,
    )
    replay_subsystem_0_channel_6_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000768,
    )
    replay_subsystem_0_channel_6_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000770,
    )
    replay_subsystem_0_channel_6_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000778,
    )
    replay_subsystem_0_channel_6_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000780,
    )
    replay_subsystem_0_channel_6_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000788,
    )
    replay_subsystem_0_channel_6_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000790,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000798,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD0007A0,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD0007A8,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD0007B0,
    )
    replay_subsystem_0_channel_6_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD0007B8,
    )
    replay_subsystem_0_channel_6_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0007C0,
    )
    replay_subsystem_0_channel_6_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0007C8,
    )
    replay_subsystem_0_channel_6_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0007D0,
    )
    replay_subsystem_0_channel_6_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0007D8,
    )
    replay_subsystem_0_channel_6_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0007E0,
    )
    replay_subsystem_0_channel_6_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0007E8,
    )
    replay_subsystem_0_channel_6_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0007F0,
    )
    replay_subsystem_0_channel_6_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0007F8,
    )
    replay_subsystem_0_channel_6_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD000800,
    )
    replay_subsystem_0_channel_6_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000808,
    )
    replay_subsystem_0_channel_6_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000810,
    )
    replay_subsystem_0_channel_6_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD000818,
    )
    replay_subsystem_0_channel_6_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000820,
    )
    replay_subsystem_0_channel_6_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000828,
    )
    replay_subsystem_0_channel_7_active = Variable(
        type=DataType.UBYTE,
        address=0XFD000830,
    )
    replay_subsystem_0_channel_7_current_offset_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000838,
    )
    replay_subsystem_0_channel_7_current_start_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000840,
    )
    replay_subsystem_0_channel_7_current_stop_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000848,
    )
    replay_subsystem_0_channel_7_debug_current_offset_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000850,
    )
    replay_subsystem_0_channel_7_debug_current_start_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000858,
    )
    replay_subsystem_0_channel_7_debug_current_stop_time_age = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000860,
    )
    replay_subsystem_0_channel_7_debug_eth_dropped_pkt_count = Variable(
        type=DataType.ULONG,
        address=0XFD000868,
    )
    replay_subsystem_0_channel_7_debug_eth_image_frame_count = Variable(
        type=DataType.ULONG,
        address=0XFD000870,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_count = Variable(
        type=DataType.ULONG,
        address=0XFD000878,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_first = Variable(
        type=DataType.UBYTE,
        address=0XFD000880,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_intermediate = Variable(
        type=DataType.UBYTE,
        address=0XFD000888,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_last = Variable(
        type=DataType.UBYTE,
        address=0XFD000890,
    )
    replay_subsystem_0_channel_7_debug_eth_packet_loss_partial = Variable(
        type=DataType.UBYTE,
        address=0XFD000898,
    )
    replay_subsystem_0_channel_7_debug_status_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0008A0,
    )
    replay_subsystem_0_channel_7_debug_status_m_axis_tready = Variable(
        type=DataType.UBYTE,
        address=0XFD0008A8,
    )
    replay_subsystem_0_channel_7_debug_status_replaydata_valid = Variable(
        type=DataType.UBYTE,
        address=0XFD0008B0,
    )
    replay_subsystem_0_channel_7_debug_status_s_axis_tvalid = Variable(
        type=DataType.UBYTE,
        address=0XFD0008B8,
    )
    replay_subsystem_0_channel_7_debug_status_schd_debug_word = Variable(
        type=DataType.ULONG,
        address=0XFD0008C0,
    )
    replay_subsystem_0_channel_7_debug_status_start_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0008C8,
    )
    replay_subsystem_0_channel_7_debug_status_stop_time_reached = Variable(
        type=DataType.UBYTE,
        address=0XFD0008D0,
    )
    replay_subsystem_0_channel_7_fifo_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0008D8,
    )
    replay_subsystem_0_channel_7_fifo_buffer_free_entries = Variable(
        type=DataType.ULONG,
        address=0XFD0008E0,
    )
    replay_subsystem_0_channel_7_next_relative_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0008E8,
    )
    replay_subsystem_0_channel_7_next_scheduled_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD0008F0,
    )
    replay_subsystem_0_channel_7_ram_buffer_fill_percent = Variable(
        type=DataType.FLOAT32_IEEE,
        address=0XFD0008F8,
    )
    replay_subsystem_0_channel_7_ram_buffer_free_bytes = Variable(
        type=DataType.A_UINT64,
        address=0XFD000900,
    )
    replay_subsystem_0_channel_7_status_ts_tl_fifo_empty = Variable(
        type=DataType.UBYTE,
        address=0XFD000908,
    )
    replay_subsystem_0_current_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000910,
    )
    replay_subsystem_0_numChannels = Variable(
        type=DataType.ULONG,
        address=0XFD000918,
    )
    replay_subsystem_0_ptp_time = Variable(
        type=DataType.FLOAT64_IEEE,
        address=0XFD000920,
    )


_devices = {
    "ESI1": EsiInfo(
        name="ESI1",
        version="ESI_E09597B4",
        version_address=0XFB000000,
        variables=_Esi2Variables,
    ),
    "ESI2": EsiInfo(
        name="ESI2",
        version="ESI_E09597B4",
        version_address=0XFB000000,
        variables=_Esi2Variables,
    ),
}


def get_esi_info(esi_name):
    return _devices[esi_name]


def _test():
    IP = {
        'ESI1': "192.168.141.21",
        'ESI2': "192.168.141.22",
    }

    for device in _devices.values():
        print()
        print(f'{device.name} (at {IP[device.name]})')
        with XCPInterface(IP[device.name], 30303) as xcp_comm:
            # Connect
            resp = xcp_comm.send(XCPCommand.CONNECT)
            assert resp.type == XCPResponseType.RESPONSE

            # Check the version
            print(f'Excepted version: {device.version}')
            chars = ""
            for position, character in enumerate(device.version):
                resp = xcp_comm.send(
                    XCPCommand.SHORT_UPLOAD,
                    device.version_address + position,
                    DataType.UBYTE,
                )
                chars += chr(resp.value)
                if character != chr(resp.value):
                    raise ValueError(chars)

            # Read the variables
            for variable in device.variables:
                resp = xcp_comm.send(
                    XCPCommand.SHORT_UPLOAD,
                    variable.value.address,
                    variable.value.type,
                )
                print(f'	{variable.name}: {resp.value}')

            # Disconnect
            resp = xcp_comm.send(XCPCommand.DISCONNECT)
            assert resp.type == XCPResponseType.RESPONSE


if __name__ == "__main__":
    _test()
