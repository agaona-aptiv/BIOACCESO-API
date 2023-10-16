# Created on Sep 2020
# Author Maria A Colin

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
#          SW Developer: Lucero Buenrostro
#          FILE DESCRIPTION
#          File: POST_Config_CAL.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################


# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
import shelve
import os
from sys import platform
import Config_Test.Config_cfg as cf_cfg
import configparser

# -----------------------------------------------
# Definitions
# -----------------------------------------------
# Config Definitions
ROOT_DIR_NAME = cf_cfg.ROOT_DIR_NAME
ROOT_DIR_NAME_SIZE = cf_cfg.ROOT_DIR_NAME_SIZE

# POST Config Definitions
ACCESS_CODE_SIZE = 64
MODULE_FILE_NAME = "POST_Service.py"

# -----------------------------------------------
# POST String Keys
# -----------------------------------------------
STR_POST_CFG_SECTION = 'POST_Configuration'
STR_ACCESS_CODE = 'access_code'
STR_POST_CONFIGURED = 'POST_Configured'
STR_MAC_ADDRESS = 'mac_address'

# -----------------------------------------------
#  Variables Definitions
# -----------------------------------------------
#   Variable name | R/W, Value
#                   R = 0, R/W = 1
IsRW_var = {
    STR_POST_CONFIGURED: 1,
    STR_ACCESS_CODE: 1,
    STR_MAC_ADDRESS:1
}

#   Variable name | Value
Defaults_var = {
    STR_POST_CONFIGURED: False,
    STR_ACCESS_CODE: "A"*ACCESS_CODE_SIZE,
    STR_MAC_ADDRESS: '12:B3:07:76:D6:22'
}


def getModulePath():
    file_dir = os.getcwd()
    current_path = file_dir
    try:
        # Find POST Service Path , If module is not found , db is created in POST_Config_folder
        path_index = current_path.find(ROOT_DIR_NAME)
        search_path = current_path[:path_index + ROOT_DIR_NAME_SIZE]
        for dirpath, dirnames, filenames in os.walk(search_path):
            for filename in filenames:
                if filename == MODULE_FILE_NAME:
                    file_dir = dirpath
                    print(file_dir)
    except Exception as e:
        print(e)
        pass
    return file_dir


# Assign the path to the document based on the platform running the script
if 'linux' == platform or 'linux2' == platform:

    CONFIG_DB_PATH = getModulePath() + '/'
    CONFIG_DB_NAME = 'POST_CFG'
    CONFIG_DB_EXT = '.txt'
    CONFIG_DB_PATH_T = CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT
    print(CONFIG_DB_PATH_T)

elif 'win32' == platform:

    CONFIG_DB_PATH = getModulePath() + '\\'
    CONFIG_DB_NAME = 'POST_CFG'
    CONFIG_DB_EXT = '.txt'
    CONFIG_DB_PATH_T = CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT
    print(CONFIG_DB_PATH_T)

# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------
class POST_Config_CAL:
    __instance = None

    @staticmethod
    def getInstance():
        if POST_Config_CAL.__instance == None:
            POST_Config_CAL()
        return POST_Config_CAL.__instance

    def __init__(self):
        if POST_Config_CAL.__instance != None:
            raise Exception("This class is a singleton! another instance already exists")
        else:
            print("Created POST_Config class")
            POST_Config_CAL.__instance = self
            if not os.path.exists(CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT):
                POST_Config_CAL.Configure_With_Defaults()

    @staticmethod
    def Configure_With_Defaults():
        result = False
        # If Config file does not exists, create a set config values to default
        try:
            if not os.path.isdir(CONFIG_DB_PATH):
                os.makedirs(CONFIG_DB_PATH)

            config = configparser.RawConfigParser()
            config.add_section(STR_POST_CFG_SECTION)
            for key in Defaults_var:
                config.set(STR_POST_CFG_SECTION, key, Defaults_var[key])
            with open(CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT, 'w') as configfile:
                config.write(configfile)
            """with shelve.open(CONFIG_DB_PATH + CONFIG_DB_NAME, flag='c') as configDatabase:
                for key in Defaults_var:
                    configDatabase[key] = Defaults_var[key]"""
            result = True


        except Exception as e:
            print(e)

        print("result conf" + str(result))
        return result
    #Conservar para módulos configurables (esta es general)#
    def Is_The_Module_Configured(self):
        return Defaults_var[STR_POST_CONFIGURED]

    def Module_Configuration_Successful(self):
        pass
        return True

    def Get_AccessCode(self):
        result = False
        data= None
        try:

            cfgParser = configparser.RawConfigParser()
            cfgParser.read(CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT)
            Access_Code = cfgParser.get(STR_POST_CFG_SECTION, STR_ACCESS_CODE)
            b_data = Access_Code.encode('utf-8')
            data = [byte for byte in b_data]
            result = True

            """with shelve.open(CONFIG_DB_PATH + CONFIG_DB_NAME, 'r') as configDatabase:
                # Obtain access code and format as binary
                print(configDatabase[STR_ACCESS_CODE])
                b_data = configDatabase[STR_ACCESS_CODE].encode('utf-8')
                data = [byte for byte in b_data]
                result = True"""

        except Exception as e:
            print(e)
        return result, data

    def Set_AccessCode(self, data_list):
        result = False
        #Verify r/w is allowed
        if IsRW_var[STR_ACCESS_CODE]:
            try:

                string_data= ''.join([chr(elem) for elem in data_list])
                print(string_data)
                # Verify access code has 64 characters TODO: Verify type of char
                if len(string_data) == ACCESS_CODE_SIZE:
                    config = configparser.RawConfigParser()
                    config.read(CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT)
                    config.set(STR_POST_CFG_SECTION, STR_ACCESS_CODE, string_data)
                    with open(CONFIG_DB_PATH + CONFIG_DB_NAME + CONFIG_DB_EXT, 'w') as configfile:
                        config.write(configfile)
                    """with shelve.open(CONFIG_DB_PATH + CONFIG_DB_NAME, flag='w', writeback=True) as configDatabase:
                        # Obtain access code
                        configDatabase[STR_ACCESS_CODE] = string_data"""
                    result = True
                    #configDatabase.close()
            except Exception as e:
                print(e)
        else:
            print("Not able to write for key: {0}".format(STR_ACCESS_CODE))
        return result

if __name__ == "__main__":
    int_data = [52, 52, 52, 52, 52, 52, 52, 52, 49, 54, 51, 101, 99, 49, 99, 54, 51, 52, 52, 102, 48, 102, 50, 52, 50, 54, 54, 102, 50, 52, 102, 52, 49, 57, 56, 98, 48, 102, 57, 55, 51, 101, 98, 57, 102, 97, 50, 102, 52, 48, 101, 48, 57, 101, 54, 100, 51, 48, 53, 52, 97, 99, 53, 101]
    POSTConf = POST_Config_CAL.getInstance()
    result, data = POSTConf.Get_AccessCode()
    print(result)
    print(data)
    #print(type(data))
    result = POSTConf.Set_AccessCode(int_data)
    print(result)
    result, data = POSTConf.Get_AccessCode()
    print(result)
    print(data)
    #print(type(data))




# ==============================================================================
# File Revision History (top to bottom: last revision to first revision)
# ==============================================================================
#
# Date             Name             Description
# ------------------------------------------------------------------------------
# 21-Sep-2020   Maria A Colin      Created initial File (DBA_Config_CAL.py)
# 13-Oct-2020   Lucero Buenrostro   Initial file modified for specific POST configuration APIs (POST_Config_CAL.py)
# ==============================================================================