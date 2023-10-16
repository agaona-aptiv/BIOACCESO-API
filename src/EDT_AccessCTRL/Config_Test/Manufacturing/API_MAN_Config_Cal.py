# Created on Dec 2020
# Author Edgar Hernandez Meraz

#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: Configuration
#          Program: Configurations POST API
#          Enterprise: Condumex
#          SW Developer: Edgar Hernandez Meraz
#          FILE DESCRIPTION
#          File: API_MAN_Config_Cal.py
#          Project: EDT_AccessCTRL
#          Delivery:
#########################################################################################


# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
from Config_Test.Config_cfg import Config_cfg
from sys import platform
import os

# -----------------------------------------------
# Definitions
# -----------------------------------------------
STR_SW_ID = 'sw_id'
STR_HW_TYPE = 'hw_type'
STR_SERIAL_NUMBER = 'serial_number'
STR_MAC_ADDRESS = 'mac_address'

CONFIG_DB_NAME = 'MAN_CFG'
CONFIG_DB_EXT = '.txt'
STR_DEF_CFG_SECTION = 'MAN_Configuration'
MODULE_FILE_NAME = "API_MAN_Config_Cal.py"

#   Variable name | Value
MANDefaultsVar = {
    STR_SW_ID: '0000',
    STR_HW_TYPE: '999', # Xavier, Sensor MLX90614, Pantalla modelo 104990343
    STR_SERIAL_NUMBER: 'B0000',
    STR_MAC_ADDRESS: '00:00:00:00:00:00'
}

# -----------------------------------------------
#  Class and Functions Definitions
# -----------------------------------------------

class API_MAN_Config_Cal:
    __instance = None

    @staticmethod
    def getInstance():
        if API_MAN_Config_Cal.__instance == None:
            API_MAN_Config_Cal()
        return API_MAN_Config_Cal.__instance

    def __init__(self):
        if API_MAN_Config_Cal.__instance != None:
            raise Exception("This class is a singleton! another instance already exists")
        else:
            print("Created MAN_Config class")

            API_MAN_Config_Cal.__instance = self

            self.cfgObj = Config_cfg("", MODULE_FILE_NAME, STR_DEF_CFG_SECTION, MANDefaultsVar)

            # Assign the path to the document based on the platform running the script
            if 'linux' == platform or 'linux2' == platform:
                CONFIG_DB_PATH = self.cfgObj.getModulePath() + '/'
            elif 'win32' == platform:
                CONFIG_DB_PATH = self.cfgObj.getModulePath() + '\\'

            CONFIG_DB_PATH_T = CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT
            print(CONFIG_DB_PATH_T)

            self.cfgObj.fileNameAndPath = CONFIG_DB_PATH_T;

            if not os.path.exists(CONFIG_DB_PATH_T):
                self.cfgObj.Configure_With_Defaults()

    def Get_SWID(self):
        result, data = self.cfgObj.Get_CalValue(STR_SW_ID)
        return result, data


    def Get_HWType(self):
        result, data = self.cfgObj.Get_CalValue(STR_HW_TYPE)
        return result, data

    def Set_HWType(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_HW_TYPE)
        return result


    def Get_SerialNumber(self):
        result, data = self.cfgObj.Get_CalValue(STR_SERIAL_NUMBER)
        return result, data

    def Set_SerialNumber(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_SERIAL_NUMBER)
        return result


    def Get_MacAddress(self):
        result, data = self.cfgObj.Get_CalValue(STR_MAC_ADDRESS)
        return result, data


# ==============================================================================
# File Revision History (top to bottom: last revision to first revision)
# ==============================================================================
#
# Date             Name             Description
# ------------------------------------------------------------------------------
# 14-Dec-2020   Edgar Hdz Meraz      Created initial File (API_SS_Config_Cal.py)
# to implement ticket DBL_175.
#
# Jan-22-2021   Edgar Hdz Meraz
#   + DBL_201
#      - Changes to Get the Mac Address value
#
# Jan-22-2021   Leobardo N Hernandez
#   + DBL_201
#      - Updated the default value of the Mac Address
#
# ==============================================================================