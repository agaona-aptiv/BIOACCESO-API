'''
Created on July, 2020
@author: Jonatan Uresti
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: EDT_AccessCTRL/mod_Temperature
#          Program: Configuration file for Temperature module
#          Enterprise: Condumex
#          SW Developer: Cinthia Valdez
#
#          File: ST_Temperature_cfg.py
#          Feature: Temperature
#          Design: ST_Temperature.pptx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################

_debugTest = False

I2C_BUS = 8 # TODO: Consider configuration for Jetson Nano (1) and Xavier (8)
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

# Emissivity configuration
EMISSIVITY_DEFAULT = 0.98

#Default area   DBL_249, DBL_263
POSICION = [225,275]
DIMENSION = [273,402]

# Temperature conversion and compensation stages
'''
These values are specific to the MLX90614ESF-DCI
'''
SUPPLY_VOLTAGE = 3.3
BASE_DISTANCE = 15  # cm
DISTANCE_COMPENSATION_FACTOR = 0.0243
#BODY_TEMPERATURE_CONVERSION_OFFSET = 2.0
#BODY_TEMPERATURE_CONVERSION_OFFSET = 3.3 # 16 Dic 2020
BODY_TEMPERATURE_CONVERSION_OFFSET = 0 # 18 Ene 2021 mlx90614

FACTOR_PLANTA = 0.94   #Default value 1.00
#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Sep-10-2020 sjkk9h
#   + Created initial file.
#
# Oct-06-2020 sjkk9h
#   + DBL_27
#       - Added temperature compensation and conversion stages.
#   + Added temporal default emissivity configuration.
#
# Dec-16-2020 zzn3y2
#   + DBL_131
#       - Update temperature compensation.
#
# Ene-27-2021 zzn3y2
#   +DBL_197
#      - Implementacion de ecuacion para compensacion por temp ambiente
#
#   + DBL_61
#      - MLX9064x implementation.
#
# Mar-12-2021 zzn3y2
#   + DBL_237
#      - Agregar el factor de la planta cuya funcionalidad es simular un opturador
#
# Abril 2021 lj05rj
#   + DBL_249
#      - Cambiar datos por default para obtencion de temperatura cuando no existe un rostro
# Abril 2021 lj05rj
#   + DBL_253
#      - Ajuste en datos por default para obtencion de temperatura cuando no existe un rostro
#Mayo 2021 lj05rj
#   + DBL_263
#      - Ajuste en datos por default para obtencion de temperatura cuando no existe un rostro
#
#Julio 2021 lj05rj
#         DBL_273 Ajuste de coordenadas por default
#########################################################################################