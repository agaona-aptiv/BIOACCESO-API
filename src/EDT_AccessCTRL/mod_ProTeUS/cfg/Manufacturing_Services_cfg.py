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
#          Description: Configuration file for the manufacturing services.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#          FILE DESCRIPTION
#          File: Manufacturing_Services_cfg.py
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
MAX_LAST_DIGITS_SERIAL_NUMBER = 999
MAX_HW_TYPE = 1
MAX_SENSOR_TYPE = 1

# -----------------------------------------------
#  Exported Type Declarations
# -----------------------------------------------

Manufacturing_SubServices_List = {
    # ServiceID | Properties
    # -------------------------------------------------------------------
    #           | Req_Len | Resp_Len | Security | Session | Function Name
    0x02: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_0.value, 'self.Enter_Session_1'),
    0x04: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'self.Enter_Session_0'),
    0x06: (3, 0, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'self.Unlock_Security_Access_Level_1'),
    0x08: (3, 4, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'Get_SW_Version'),
    0x0A: (3, 3, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'Get_HW_Type'),
    0x0C: (6, 0, SC_cfg.SecurityLevel.SEC_LEVEL_1.value, SC_cfg.SessionLevel.SESSION_1.value, 'Set_HW_Type'),
    0x0E: (3, 5, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'Get_Serial_Number'),
    0x10: (8, 0, SC_cfg.SecurityLevel.SEC_LEVEL_1.value, SC_cfg.SessionLevel.SESSION_1.value, 'Set_Serial_Number'),
    0x12: (3, 17, SC_cfg.SecurityLevel.SEC_LEVEL_0.value, SC_cfg.SessionLevel.SESSION_1.value, 'Get_Mac_Address')
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
#
# Jan-22-2021   Edgar Hdz Meraz
#   + DBL_201
#      - Changes to support sub-service 0x12, in order to read Mac Address value
#########################################################################################
