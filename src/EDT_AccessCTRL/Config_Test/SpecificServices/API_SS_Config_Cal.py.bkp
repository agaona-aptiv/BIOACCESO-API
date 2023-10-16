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
#          File: API_SS_Config_Cal.py
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
CONFIG_DB_NAME = 'SS_CFG'
CONFIG_DB_EXT = '.txt'
STR_DEF_CFG_SECTION = 'SS_Configuration'
MODULE_FILE_NAME = "API_SS_Config_Cal.py"
# -----------------------------------------------
# Initial Configuration (Specific Services)
# -----------------------------------------------
STR_HW_COMPATIBILITY = 'hw_compatibility'
STR_FACIAL_RECOGNITION = 'facial_recognition'
STR_TEMP_DETECTION = 'temp_detection'
STR_DOOR_ACCESS = 'door_access'
STR_FACEMASK = 'facemask'
STR_SEND_INFO_TO_HUB = 'send_info_to_hub'
# -----------------------------------------------
# Calibration (Specific Services)
# -----------------------------------------------
STR_WHITE_BALANCE = 'white_balance'
STR_UPPER_TEMP_LIMIT = 'upper_temp_limit'
STR_LOWER_TEMP_LIMIT = 'lower_temp_limit'
STR_DBA_IP = 'dba_ip'
STR_HUB_URL = 'hub_url'
STR_FACE_RECOGNITION_RATE = 'face_recognition_rate'
STR_ACCESS_CODE = 'access_code'

ACCESS_CODE_SIZE = 64

#   Variable name | Value
SSDefaultsVar = {
    STR_HW_COMPATIBILITY: '99', #Versión Sensor MLX90614 - Pantalla 104990343
    STR_FACIAL_RECOGNITION: '1',
    STR_TEMP_DETECTION: '1',
    STR_DOOR_ACCESS : '1',
    STR_FACEMASK : '1',
    STR_SEND_INFO_TO_HUB: '1',
    STR_WHITE_BALANCE: '1',
    STR_UPPER_TEMP_LIMIT: '37.5',
    STR_LOWER_TEMP_LIMIT: '34.5',
    STR_DBA_IP: '255.255.255.255',
    STR_HUB_URL: 'http://misaplicaciones.cidec.com.mx/sba_hub/API/public/index.php/api/v1/hubapi',
    STR_FACE_RECOGNITION_RATE: '0.0',
    STR_ACCESS_CODE: 'A'*ACCESS_CODE_SIZE
}

# -----------------------------------------------
#  Class and Functions Definitions
# -----------------------------------------------

class API_SS_Config_Cal:
    __instance = None

    @staticmethod
    def getInstance():
        if API_SS_Config_Cal.__instance == None:
            API_SS_Config_Cal()
        return API_SS_Config_Cal.__instance

    def __init__(self):
        if API_SS_Config_Cal.__instance != None:
            raise Exception("This class is a singleton! another instance already exists")
        else:
            print("Created SS_Config class")
            API_SS_Config_Cal.__instance = self

            self.cfgObj = Config_cfg("", MODULE_FILE_NAME, STR_DEF_CFG_SECTION, SSDefaultsVar)

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

    def Get_HWCompatibility(self):
        result, data = self.cfgObj.Get_CalValue(STR_HW_COMPATIBILITY)
        return result, data

    def Set_HWCompatibility(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_HW_COMPATIBILITY)
        return result


    def Get_FacialRecognition(self):
        result, data = self.cfgObj.Get_CalValue(STR_FACIAL_RECOGNITION)
        return result, data

    def Set_FacialRecognition(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_FACIAL_RECOGNITION)
        return result


    def Get_TempDetection(self):
        result, data = self.cfgObj.Get_CalValue(STR_TEMP_DETECTION)
        return result, data

    def Set_TempDetection(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_TEMP_DETECTION)
        return result


    def Get_DoorAccess(self):
        result, data = self.cfgObj.Get_CalValue(STR_DOOR_ACCESS)
        return result, data

    def Set_DoorAccess(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_DOOR_ACCESS)
        return result


    def Get_FaceMask(self):
        result, data = self.cfgObj.Get_CalValue(STR_FACEMASK)
        return result, data

    def Set_FaceMask(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_FACEMASK)
        return result


    def Get_SendInfoToHub(self):
        result, data = self.cfgObj.Get_CalValue(STR_SEND_INFO_TO_HUB)
        return result, data

    def Set_SendInfoToHub(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_SEND_INFO_TO_HUB)
        return result


    def Get_WhiteBalance(self):
        result, data = self.cfgObj.Get_CalValue(STR_WHITE_BALANCE)
        return result, data

    def Set_WhiteBalance(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_WHITE_BALANCE)
        return result


    def Get_UpperTempLimit(self):
        result, data = self.cfgObj.Get_CalValue(STR_UPPER_TEMP_LIMIT)
        return result, data

    def Set_UpperTempLimit(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_UPPER_TEMP_LIMIT)
        return result


    def Get_LowerTempLimit(self):
        result, data = self.cfgObj.Get_CalValue(STR_LOWER_TEMP_LIMIT)
        return result, data

    def Set_LowerTempLimit(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_LOWER_TEMP_LIMIT)
        return result


    def Get_DBAIP(self):
        result, data = self.cfgObj.Get_CalValue(STR_DBA_IP)
        return result, data

    def Set_DBAIP(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_DBA_IP)
        return result


    def Get_HUBURL(self):
        result, data = self.cfgObj.Get_CalValue(STR_HUB_URL)
        return result, data

    def Set_HUBURL(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_HUB_URL)
        return result

    def Get_FaceRecognitionRate(self):
        result, data = self.cfgObj.Get_CalValue(STR_FACE_RECOGNITION_RATE)
        return result, data

    def Set_FaceRecognitionRate(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_FACE_RECOGNITION_RATE)
        return result

    def Get_AccessCode(self):
        result, data = self.cfgObj.Get_CalValue(STR_ACCESS_CODE)
        return result, data

    def Set_AccessCode(self, data):
        result = self.cfgObj.Set_CalValue(data, STR_ACCESS_CODE)
        return result



# ==============================================================================
# File Revision History (top to bottom: last revision to first revision)
# ==============================================================================
#
# Date             Name             Description
# ------------------------------------------------------------------------------
# 10-Dec-2020   Edgar Hdz Meraz      Created initial File (API_SS_Config_Cal.py)
# to implement ticket DBL_175.
# ==============================================================================