'''
Created on October, 2020
@author: Ernesto Ulises Beltran
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: Stubs
#          Description: This script provides stubs for host.
#          Enterprise: Condumex
#          SW Developer: Ernesto Ulises Beltran
#
#          File: ST_Temperature_cfg.py
#          Feature: Stubs
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################

_debugTest = False

TEMPERATURE = 36.6
EMISSIVITY = 1.0

I2C_BUS = 8	# TODO: Consider configuration for Jetson Nano (1) and Xavier (8)
SENSOR_ADDRESS = 0x5A

# SMBus commands
EEPROM_ACCESS_COMMAND = 0x20

# EEPROM registers
EMISSIVITY_REG_ADDRESS = 0x24
SMBUS_REG_ADDRESS = 0x2E
EMISSIVITY_LOCK_REG_ADDRESS = 0x2F

EEPROM_SIZE = 32
CLEAR_EEPROM = 0x00
WRITE_CELL_TIME = 0.01  # 10ms

# Error IDs
INVALID_TEMPERATURE = -273
ERROR_INVALID_PARAMETER = -1
ERROR_SENSOR_NOT_CONNECTED = -2
ERROR_READ_FAILED = -3
ERROR_WRITE_FAILED = -4

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
#########################################################################################