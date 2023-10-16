# Created on July 2020
# Author Lucero Buenrostro

#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: Config_Cal
#          Program: Configuration file for Config module
#          Enterprise: Condumex
#          SW Developer: Lucero Buenrostro
#          FILE DESCRIPTION
#          File: ConfigL_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################

import os
import configparser


# -----------------------------------------------
# Definitions
# -----------------------------------------------
ROOT_DIR_NAME = "EDT_AccessCTRL"
ROOT_DIR_NAME_SIZE = len(ROOT_DIR_NAME)


class Config_cfg:

    def __init__(self, fileNameAndPath, moduleFileName, configSection, defaults):
        self.fileNameAndPath = fileNameAndPath
        self.configSection = configSection
        self.defaults = defaults
        self.moduleFileName = moduleFileName

    def getModulePath(self):
        file_dir = os.getcwd()
        current_path = file_dir
        try:
            # Find POST Service Path , If module is not found , db is created in POST_Config_folder
            path_index = current_path.find(ROOT_DIR_NAME)
            search_path = current_path[:path_index + ROOT_DIR_NAME_SIZE]
            for dirpath, dirnames, filenames in os.walk(search_path):
                for filename in filenames:
                    if filename == self.moduleFileName:
                        file_dir = dirpath
                        print(file_dir)
                        break
                # only executed if the inner loop did NOT break
                else:
                    continue
                break  # only executed if the inner loop Did break
        except Exception as e:
            print(e)
            pass
        return file_dir

    def Configure_With_Defaults(self):
        result = False
        # If Config file does not exists, create a set config values to default
        try:
            config = configparser.RawConfigParser()
            config.add_section(self.configSection)
            for key in self.defaults:
                config.set(self.configSection, key, self.defaults[key])
            with open(self.fileNameAndPath, 'w') as configfile:
                config.write(configfile)
            result = True

        except Exception as e:
            print(e)

        print("result conf" + str(result))
        return result

    def Module_Configuration_Successful(self):
        pass
        return True

    def Get_CalValue(self, strCalName):
        result = False
        data= None
        try:
            cfgParser = configparser.RawConfigParser()
            cfgParser.read(self.fileNameAndPath)
            data = cfgParser.get(self.configSection, strCalName)
            result = True
        except Exception as e:
            print(e)
        return result, data

    def Set_CalValue(self, data, strCalName, isRW = 1):
        result = False
        #Verify r/w is allowed
        if isRW:
            try:
                data = str(data)
                print(data)

                config = configparser.RawConfigParser()
                config.read(self.fileNameAndPath)
                config.set(self.configSection, strCalName, data)
                with open(self.fileNameAndPath, 'w') as configfile:
                    config.write(configfile)
                result = True
            except Exception as e:
                print(e)
        else:
            print("Not able to write for key: {0}".format(strCalName))
        return result
#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-15-2020 Lucero Buenrostro
#   + Created initial file.
#
# Dec-10-2020 Edgar Hdz Meraz
#   + DBL_175
#   + Added cal constants and generic functions to read and write cal values in a single
#     place.
#########################################################################################
