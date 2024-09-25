"""
The paths of the XIL variables used to start the replay and to read the
diagnostics

@copyright
    Copyright 2024, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
    All rights reserved.
"""

# Set_StartStop and start replay
Enable = {
    "StartReplay":                 "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/EnableReplay/Value",
    "EnableReplayMode":            "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/EnableReplayMode/Value",
    "Enable_StartStopSetFromSCLX": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/Enable_StartStopSetFromSCLX/Value",
}

# The time caluclation variables.
ReplayTimeCalc = {
    "StartOffset":                 "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/Time Calc/StartOffset/Value",
    "StopOffset":                  "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/Time Calc/StopOffset/Value",
    "startTime_RTPC":              "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_StartStop_ESI/Time Calc/startTime_RTPC",
}

# Replay monitoring
ReplayStateMonitor = {
    "replayDuration": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayStateMonitor/replayTime",
    "replayProgress": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayStateMonitor/replayProgress",
    "replayState":    "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayStateMonitor/replayState",
    "replayLength":   "SCAELXIO()://Replay_MP_Chery_BM/Model Root/Set_OffsetTime_CANETH/replayLength",
}

# gPTP_Master
gPTP_Master = {
    "BaseTimeVector_DuT": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/gPTP_Master/BaseTimeVector_DuT/Value",
    "UpdateBaseTime_DuT": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/gPTP_Master/UpdateBaseTime_DuT/Value",
}

# DuTSyncStartCalc
DuTSyncStartCalc = {
    "firsttTs_Lidar":           "SCALEXIO()://Replay_MP_Chery_BM/Model Root/DuTSyncStartCalc/CalcSyncStart/Gain/Out1[1]",
    "firstTimestamp_LidarMSOP": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/DuTSyncStartCalc/CalcSyncStart/Gain/Out1[0]",
    "firstTs":                  "SCALEXIO()://Replay_MP_Chery_BM/Model Root/DuTSyncStartCalc/CalcSyncStart/DTC_firstTs/Out1",
    "AdditionalOffset":         "SCALEXIO()://Replay_MP_Chery_BM/Model Root/DuTSyncStartCalc/CalcSyncStart/AdditionalOffset/Value",
    "syncStartTime_DuT":        "SCALEXIO()://Replay_MP_Chery_BM/Model Root/DuTSyncStartCalc/syncStartTime_DuT",
}

# Replay System Monitoring---ESI1
ReplayDisgnostic_ESI1 = {
    "ESI1_FMC4_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[0]",
    "ESI1_FMC4_Ch2_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[1]",
    "ESI1_FMC4_Ch3_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[2]",
    "ESI1_FMC4_Ch4_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[3]",
}

#Replay System Monitoring---ESI2
ReplayDisgnostic_ESI2 = {
    "ESI2_FMC3_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[00]",
    "ESI2_FMC3_Ch2_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[01]",
    "ESI2_FMC3_Ch4_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[02]",
    "ESI2_FMC4_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[4]",
    "ESI2_FMC4_Ch2_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[5]",
    "ESI2_FMC4_Ch3_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[6]",
    "ESI2_FMC4_Ch4_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC1/decoded_val[7]",
}

# Replay System Monitoring---RTPC1
ReplayDisgnostic_RTPC1 = {
    "RTPC1_DS6333_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[03]",
    "RTPC1_DS6333_Ch1_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayStreams/UDP_Stream_1/State [UltraFastUDPReplay - DS6333_Ch1]/Frames Transmited",
    "RTPC1_DS6341_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[10]",
    "RTPC1_DS6341_Ch1_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6341_Ch1/Out1",
    "RTPC1_DS6341_Ch2_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[11]",
    "RTPC1_DS6341_Ch2_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6341_Ch2/Out1",
    "RTPC1_DS6341_Ch3_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[12]",
    "RTPC1_DS6341_Ch3_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6341_Ch3/Out1",
    "RTPC1_DS6341_Ch4_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[13]",
    "RTPC1_DS6341_Ch4_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6341_Ch4/Out1",
    "RTPC1_DS6342_Ch1_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[04]",
    "RTPC1_DS6342_Ch1_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch1/Out1",
    "RTPC1_DS6342_Ch2_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[05]",
    "RTPC1_DS6342_Ch2_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch2/Out1",
    "RTPC1_DS6342_Ch3_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[06]",
    "RTPC1_DS6342_Ch3_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch3/Out1",
    "RTPC1_DS6342_Ch4_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[07]",
    "RTPC1_DS6342_Ch4_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch4/Out1",
    "RTPC1_DS6342_Ch5_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[08]",
    "RTPC1_DS6342_Ch5_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch5/Out1",
    "RTPC1_DS6342_Ch6_Buffered": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/BufferedFrames/Decode_FrameCnt_PC2/decoded_val[09]",
    "RTPC1_DS6342_Ch6_Replayed": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/ReplayDisgnostic/ReplayedFrames/CAN/ReplayedFrames_DS6342_Ch6/Out1",
}

# Replay Data time sent from RTMaps to SCALEXIO
ReplayDataTime = {
    "firstTs":       "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_OffsetTime_CANETH/ddrp_offset_receiver_firstTs/Out1",
    "lastTs PC1":    "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_OffsetTime_CANETH/ddrp_offset_receiver_lastTs_PC1/Out1",
    "lastTs PC2":    "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_OffsetTime_CANETH/ddrp_offset_receiver_lastTs_PC2/Out1",
    "BytesReceived": "SCALEXIO()://Replay_MP_Chery_BM/Model Root/Set_OffsetTime_CANETH/ByteFromRTMapsReceived/y",
}

OverrunCounters = {
    "Overrun Count RTPC1":   "SCALEXIO()://Replay_MP_Chery_BM/Simulation and RTOS/Task Information Variables/Periodic Task 1/Overrun Count",
    "Task Turnaround RTPC1": "SCALEXIO()://Replay_MP_Chery_BM/Simulation and RTOS/Task Information Variables/Periodic Task 1/Max Task Turnaround Time",
    "Overrun Count RTPC2":   "SCALEXIO()://Replay_MP_SOMEIP/Simulation and RTOS/Task Information Variables/Periodic Task 1/Overrun Count",
    "Task Turnaround RTPC2": "SCALEXIO()://Replay_MP_SOMEIP/Simulation and RTOS/Task Information Variables/Periodic Task 1/Max Task Turnaround Time",
}
