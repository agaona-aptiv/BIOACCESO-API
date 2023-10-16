'''
Created on July, 2020
@author: Leobardo N Hernandez
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: GPIO Driver
#          Description: This script provides control of the GPIO ports.
#          Enterprise: Condumex
#          SW Developer: Leobardo N Hernandez
#
#          File: ST_GPIOInterfaces.py
#          Feature: GPIO driver
#          Design: Driagrama_Secuencia_DB_GPIO_Driver.pptx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################
from enum import Enum


class GPIOHardware(Enum):
    JETSON_NANO = 0
    JETSON_XAVIER_NX = 1


class DBValueError(ValueError):
    def __init__(self,message, *args):
        super(DBValueError, self).__init__(message, *args)


_debugTest = False
_gpioTarget = GPIOHardware.JETSON_XAVIER_NX


#----------------------------------------------------------------------------
# Jetson Nano J41 Header (Pin definition)
#----------------------------------------------------------------------------
JETSON_NANO_GPIO216 = 4 # BCM pin 4, BOARD pin 7
JETSON_NANO_GPIO50 = 17 # BCM pin 17, BOARD pin 11
JETSON_NANO_GPIO79 = 18 # BCM pin 18, BOARD pin 12
JETSON_NANO_GPIO14 = 27 # BCM pin 27, BOARD pin 13
JETSON_NANO_GPIO194 = 22 # BCM pin 22, BOARD pin 15
JETSON_NANO_GPIO232 = 23 # BCM pin 23, BOARD pin 16
JETSON_NANO_GPIO15 = 24 # BCM pin 24, BOARD pin 18
JETSON_NANO_GPIO16 = 10 # BCM pin 10, BOARD pin 19
JETSON_NANO_GPIO17 = 9 # BCM pin 9, BOARD pin 21
JETSON_NANO_GPIO13 = 25 # BCM pin 25, BOARD pin 22
JETSON_NANO_GPIO18 = 11 # BCM pin 11, BOARD pin 23
JETSON_NANO_GPIO19 = 8 # BCM pin 8, BOARD pin 24
JETSON_NANO_GPIO20 = 7 # BCM pin 7, BOARD pin 26
JETSON_NANO_GPIO149 = 5 # BCM pin 5, BOARD pin 29
JETSON_NANO_GPIO200 = 6 # BCM pin 6, BOARD pin 31
JETSON_NANO_GPIO168 = 12 # BCM pin 12, BOARD pin 32
JETSON_NANO_GPIO38 = 13 # BCM pin 13, BOARD pin 33
JETSON_NANO_GPIO76 = 19 # BCM pin 19, BOARD pin 35
JETSON_NANO_GPIO51 = 16 # BCM pin 16, BOARD pin 36
JETSON_NANO_GPIO12 = 26 # BCM pin 26, BOARD pin 37
JETSON_NANO_GPIO77 = 20 # BCM pin 20, BOARD pin 38
JETSON_NANO_GPIO78 = 21 # BCM pin 21, BOARD pin 40


#----------------------------------------------------------------------------------------
# Jetson Xavier NX J41 Header (Pin definition)
#----------------------------------------------------------------------------------------
JETSON_XAVIER_NX_GPIO436 = 4     # BCM pin 4,  BOARD pin 7
JETSON_XAVIER_NX_GPIO428 = 17    # BCM pin 17, BOARD pin 11
JETSON_XAVIER_NX_GPIO445 = 18    # BCM pin 18, BOARD pin 12
JETSON_XAVIER_NX_GPIO480 = 27    # BCM pin 27, BOARD pin 13
JETSON_XAVIER_NX_GPIO268 = 22    # BCM pin 22, BOARD pin 15
JETSON_XAVIER_NX_GPIO484 = 23    # BCM pin 23, BOARD pin 16
JETSON_XAVIER_NX_GPIO483 = 24    # BCM pin 24, BOARD pin 18
JETSON_XAVIER_NX_GPIO493 = 10    # BCM pin 10, BOARD pin 19
JETSON_XAVIER_NX_GPIO492 = 9     # BCM pin 9,  BOARD pin 21
JETSON_XAVIER_NX_GPIO481 = 25    # BCM pin 25, BOARD pin 22
JETSON_XAVIER_NX_GPIO491 = 11    # BCM pin 11, BOARD pin 23
JETSON_XAVIER_NX_GPIO494 = 8     # BCM pin 8,  BOARD pin 24
JETSON_XAVIER_NX_GPIO495 = 7     # BCM pin 7,  BOARD pin 26
JETSON_XAVIER_NX_GPIO421 = 5     # BCM pin 5,  BOARD pin 29
JETSON_XAVIER_NX_GPIO422 = 6     # BCM pin 6,  BOARD pin 31
JETSON_XAVIER_NX_GPIO424 = 12    # BCM pin 12, BOARD pin 32
JETSON_XAVIER_NX_GPIO393 = 13    # BCM pin 13, BOARD pin 33
JETSON_XAVIER_NX_GPIO448 = 19    # BCM pin 19, BOARD pin 35
JETSON_XAVIER_NX_GPIO429 = 16    # BCM pin 16, BOARD pin 36
JETSON_XAVIER_NX_GPIO482 = 26    # BCM pin 26, BOARD pin 37
JETSON_XAVIER_NX_GPIO447 = 20    # BCM pin 20, BOARD pin 38
JETSON_XAVIER_NX_GPIO446 = 21    # BCM pin 21, BOARD pin 40


#----------------------------------------------------------------------------------------
# Jetson AGX Xavier J41 Header (Pin definition)
#----------------------------------------------------------------------------------------
JETSON_AGX_XAVIER_GPIO422 = 4     # BCM pin 4,  BOARD pin 7
JETSON_AGX_XAVIER_GPIO428 = 17    # BCM pin 17, BOARD pin 11
JETSON_AGX_XAVIER_GPIO351 = 18    # BCM pin 18, BOARD pin 12
JETSON_AGX_XAVIER_GPIO424 = 27    # BCM pin 27, BOARD pin 13
JETSON_AGX_XAVIER_GPIO393 = 22    # BCM pin 22, BOARD pin 15
JETSON_AGX_XAVIER_GPIO256 = 23    # BCM pin 23, BOARD pin 16
JETSON_AGX_XAVIER_GPIO344 = 24    # BCM pin 24, BOARD pin 18
JETSON_AGX_XAVIER_GPIO493 = 10    # BCM pin 10, BOARD pin 19
JETSON_AGX_XAVIER_GPIO492 = 9     # BCM pin 9,  BOARD pin 21
JETSON_AGX_XAVIER_GPIO417 = 25    # BCM pin 25, BOARD pin 22
JETSON_AGX_XAVIER_GPIO491 = 11    # BCM pin 11, BOARD pin 23
JETSON_AGX_XAVIER_GPIO494 = 8     # BCM pin 8,  BOARD pin 24
JETSON_AGX_XAVIER_GPIO495 = 7     # BCM pin 7,  BOARD pin 26
JETSON_AGX_XAVIER_GPIO251 = 5     # BCM pin 5,  BOARD pin 29
JETSON_AGX_XAVIER_GPIO250 = 6     # BCM pin 6,  BOARD pin 31
JETSON_AGX_XAVIER_GPIO257 = 12    # BCM pin 12, BOARD pin 32
JETSON_AGX_XAVIER_GPIO248 = 13    # BCM pin 13, BOARD pin 33
JETSON_AGX_XAVIER_GPIO354 = 19    # BCM pin 19, BOARD pin 35
JETSON_AGX_XAVIER_GPIO429 = 16    # BCM pin 16, BOARD pin 36
JETSON_AGX_XAVIER_GPIO249 = 26    # BCM pin 26, BOARD pin 37
JETSON_AGX_XAVIER_GPIO353 = 20    # BCM pin 20, BOARD pin 38
JETSON_AGX_XAVIER_GPIO352 = 21    # BCM pin 21, BOARD pin 40


#----------------------------------------------------------------------------------------
# GPIO INTERFACES FOR THE EXTERNAL DEVICES
#----------------------------------------------------------------------------------------
if GPIOHardware.JETSON_NANO == _gpioTarget:
    RELAY1_GPIO_INTERFACE = JETSON_NANO_GPIO149
    RELAY2_GPIO_INTERFACE = JETSON_NANO_GPIO200
    BUZZER_GPIO_INTERFACE = JETSON_NANO_GPIO38
elif GPIOHardware.JETSON_XAVIER_NX == _gpioTarget:
    RELAY1_GPIO_INTERFACE = JETSON_XAVIER_NX_GPIO421
    RELAY2_GPIO_INTERFACE = JETSON_XAVIER_NX_GPIO422
    BUZZER_GPIO_INTERFACE = JETSON_XAVIER_NX_GPIO393
else:
    raise DBValueError("GPIO Config Error [000] - The Jetson Hardware is not Supported!")

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Aug-07-2020 nzddvp
#   + Created initial file.
#
# Sep-08-2020 nzddvp
#   Description:
#       - Added RELAY2 interface.
#
# Oct-21-2020 nzddvp
#   DBL_63:
#       - Updated GPIO configuration to add Jetson Xavier NX and Jetson AGX Xavier
#         definitions.
#
#########################################################################################
