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
#          File: ST_Temperature.py
#          Feature: Stubs
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################
#sudo -H pip3 install smbus2
#sudo -H pip3 install PyMLX90614

# All imported modules must be added after config file
# Avoid use of 'cfg' as alias because all modules contain a config file
import mod_UserServices.ST_Temperature_cfg as temp_cfg

import os
from inspect import currentframe
from datetime import datetime as dt

log_to_file_t = False

def TLogger(text):
    if True:
        dt_string = os.path.basename(__file__) + ' ln ' + str(currentframe().f_back.f_lineno) + ' - ' + dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if log_to_file_t:
            file = open('edt_log.log', 'a+')
            file.write(dt_string[:-3] + ': ' + str(text) + '\n')
            file.close()
        else:
            print(dt_string[:-3] + ':', str(text))

import os
import unittest
import sys

class ST_Temperature:
   __instance = None

   @staticmethod
   def getInstance():
      """ Static access method. """
      if ST_Temperature.__instance == None:
         ST_Temperature()
      return ST_Temperature.__instance

   #Class Constructor
   def __init__(self):
      """ Virtually private constructor. """
      if ST_Temperature.__instance != None:
         raise Exception('This class is a singleton!')
      else:
         ST_Temperature.__instance = self
         ST_Temperature._isConnected = False
         ST_Temperature._bus = None
         ST_Temperature._sensor = None
         ST_Temperature._busId = 0
         ST_Temperature._sensorAddress = 0

   @staticmethod
   def Connect(i2cBus = temp_cfg.I2C_BUS, address = temp_cfg.SENSOR_ADDRESS):
      '''
         Connect to the Temperature Device
      '''
      ST_Temperature._isConnected = True
      return ST_Temperature._isConnected

   @staticmethod
   def Disconnect():
      '''
         Disconnect form the Device
      '''
      ST_Temperature._isConnected = False
      return not ST_Temperature._isConnected

   @staticmethod
   def GetTemperature(ambient = False):
      '''
         Get Temperature from the Device
            Get Temperature from and object or the ambient
            return -273 in case on error
      '''
      temperature = temp_cfg.INVALID_TEMPERATURE
      if ST_Temperature._isConnected:
         temperature = temp_cfg.TEMPERATURE
      else:
         TLogger('Sensor not connected!')
      return temperature

   @staticmethod
   def GetEmissivity():
      '''
         Get emissivity
      '''
      if ST_Temperature._isConnected:
         emissivity = temp_cfg.EMISSIVITY
      else:
         TLogger('Sensor not connected!')
         emissivity = temp_cfg.ERROR_SENSOR_NOT_CONNECTED
      return emissivity

   @staticmethod
   def SetEmissivity(emissivity = 1.0, address = temp_cfg.SENSOR_ADDRESS):
      '''
         Set emissivity

         Based on procedure described in:
         MLX90614-Changing-Emissivity-Unlocking-Key-Application-Note-Melexis
      '''
      if ST_Temperature._isConnected:
         try:
           if ((emissivity > 1.0) or (emissivity < 0.1)):
               result = temp_cfg.ERROR_INVALID_PARAMETER
           else:
               result = ST_Temperature.GetEmissivity()
         except Exception as e:
           result = temp_cfg.ERROR_WRITE_FAILED
           TLogger('Temperature sensor failed:' + str(e))
      else:
         TLogger('Sensor not connected!')
         result = temp_cfg.ERROR_SENSOR_NOT_CONNECTED
      return result

      @staticmethod
      def DumpEEPROM():
         if ST_Temperature._isConnected:
            pass
         else:
            TLogger('Sensor not connected!')

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
#########################################################################################