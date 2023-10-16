'''
Created on October, 2020
@author: Felipe Martinez
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: Proteus
#          Description: Configuration file for the specific services.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#          FILE DESCRIPTION
#          File: Specific_Services_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
import mod_ProTeUS.cfg.Session_ctrl_cfg as SC_cfg

# -----------------------------------------------
#  Exported Preprocessor #define Constants
# -----------------------------------------------
#To manage combination of version and pantalla
MAX_HW_VERSION = 5
MAX_WHITE_BALANCE_VALUES = 9
MAX_DBL_CONFIG = 1  # 0/1: Disable/Enable
UPPER_TEMP_LIMIT_MIN_INTEGER = 37  # 37.5°C
UPPER_TEMP_LIMIT_MIN_DECIMALS = 5
UPPER_TEMP_LIMIT_MAX_INTEGER = 38  # 38.9°C
UPPER_TEMP_LIMIT_MAX_DECIMALS = 9
LOWER_TEMP_LIMIT_MIN_INTEGER = 34  # 34.0°C
LOWER_TEMP_LIMIT_MIN_DECIMALS = 0
LOWER_TEMP_LIMIT_MAX_INTEGER = 35  # 35.0C
LOWER_TEMP_LIMIT_MAX_DECIMALS = 0
MAX_ADDRESS_VALUE = 255  # 0xFF
MIN_ADDRESS_VALUE = 0
UPPER_LIMIT_FACE_RECOGNITION = 99
LOWER_LIMIT_FACE_RECOGNITION = 0
FACE_RECOGNITION_RESOLUTION = 5
MAX_URL_LENGTH = 255

# -----------------------------------------------
#  Exported Type Declarations
# -----------------------------------------------


Specific_Subservices_List = {
    # ServiceID | Properties
    # -------------------------------------------------------------------
    #           | Req_Len | Resp_Len | Security | Session | Function Name
    0x02: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_0.value, 'self.Enter_Session_2'),
    0x04: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_0.value, 'self.Enter_Session_0'),
    # 0x06: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_0.value, 'self.Enter_Session_3'),
    0x08: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'self.Unlock_Security_Access_Level_2'),
    0x0A: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'self.Unlock_Security_Access_Level_3'),
    0x0C: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_HW_Compatibility'),
    0x0E: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_HW_Compatibility'),
    0x10: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Facial_Recognition'),
    0x12: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Facial_Recognition'),
    0x14: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Temp_Detection'),
    0x16: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Temp_Detection'),
    0x18: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Door_Access'),
    0x1A: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Door_Access'),
    0x1C: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Facemask'),
    0x1E: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Facemask'),
    0x20: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Send_Info_To_HUB'),
    0x22: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Send_Info_To_HUB'),
    0x24: (3, 1, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_White_Balance'),
    0x26: (4, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_White_Balance'),
    0x28: (3, 2, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Upper_Temp_Limit'),
    0x2A: (5, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Upper_Temp_Limit'),
    0x2C: (3, 2, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Lower_Temp_Limit'),
    0x2E: (5, 0, SC_cfg.SecurityLevel.SEC_LEVEL_2.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Lower_Temp_Limit'),
    0x30: (3, 4, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_DBA_IP'),
    0x32: (7, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_DBA_IP'),
    0x34: (3, 255, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_HUB_URL'),
    0x36: (258, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_HUB_URL'),
    0x38: (3, 2, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Face_Recognition_Rate'),
    0x3A: (5, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Face_Recognition_Rate'),
    0x3C: (3, 64, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_2.value, 'Get_Access_Code'),
    0x3E: (67, 0, SC_cfg.SecurityLevel.SEC_LEVEL_3.value, SC_cfg.SessionLevel.SESSION_2.value, 'Set_Access_Code'),
}

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
# Dec-23-2020   Edgar Hdz Meraz
#   + DBL_175
#      - Changes to define/modify constants and to modify number of requested response
#        length for some calibrations
#########################################################################################
