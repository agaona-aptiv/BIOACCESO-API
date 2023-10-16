# ==============================================================================
#
# @file Proteus_Definitions.py
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
#          Description: This file contains the response code and parameters size of the Proteus message.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#
#          File: Proteus_Definitions.py
#          Feature: Proteus
#          Design: PROTEUS_en_Dispositivo_de_Acceso_Biometrico.vsdx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
from enum import Enum
import logging
from sys import platform
from logging.handlers import RotatingFileHandler
import os


# -----------------------------------------------
#  Exported Type Declarations
# -----------------------------------------------
# Minimum parameters supported to be received in PROTEUS' requests
MINIMUM_PARAMETERS = 3
# Maximum bytes to be received in PROTEUS' requests
MAX_BUFFER_SIZE = 258
# Maximum hexadecimal bytes to be received in PROTEUS' requests
MAX_DATA_SIZE = MAX_BUFFER_SIZE - MINIMUM_PARAMETERS


#  ---------- Supported Response ------------
class ProteusResponseCode(Enum):
    SERVICE_NOT_SUPPORTED = 0x00
    SUBSERVICE_NOT_SUPPORTED = 0x01
    NO_ERROR = 0x02
    GENERAL_FAILURE = 0x03
    INCORRECT_LENGTH = 0x04
    DATA_OUT_OF_RANGE = 0x05
    DATA_NOT_WRITEABLE = 0x06
    COMMAND_NOT_SUPPORTED = 0x07
    NOT_ACTIVE_IN_CURRENT_SESSION = 0x08
    SECURITY_ACCESS_DENIED = 0x09
    INVALID_KEY = 0X0A
    RESPONSE_MAX = 0x0B


#  ---------- SubService Structure ------------
class SubServiceStructure(Enum):
    REQ_LEN = 0
    RESP_LEN = 1
    SECURITY = 2
    SESSION = 3
    FUNCTION_NAME = 4

#  ----------- Custom logger -----------
MAX_LOG_FILE_SIZE = 20971520  # 20 MB
MAX_NUMBER_OF_LOG_FILES = 4
LOG_FILES_PATH_AND_NAME = os.getcwd() + "/mod_ProTeUS/log/proteus.log"

# Creating a rotating logger
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)

# Add a rotating handler
handler = RotatingFileHandler(LOG_FILES_PATH_AND_NAME, maxBytes=MAX_LOG_FILE_SIZE, backupCount=MAX_NUMBER_OF_LOG_FILES)
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(f_format)
logger.addHandler(handler)

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
# Nov-30-2020   Edgar Hernandez
#   + DBL_154
#      - Rotating file handler created, in order to log debug, info, warnings and errors
#        to file, instead of printing out to console.
#
# Jan-14-2021 Edgar Hdz Meraz
#   + DBL_175
#      - Change added to write the log file name according to the platform where Proteus
#        is running.
#
# Jan-14-2021 Edgar Hdz Meraz
#   + DBL_201
#      - Update path for proteus log.
#
#########################################################################################
