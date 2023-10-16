'''
Created on July, 2020
@author: Arturo Gaona
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: EDT_AccessCTRL/mod_Temperature
#          Program: Static interface to manage IIC and read temperature from sensor
#          Enterprise: Condumex
#          SW Developer: Marco Magana
#
#          File: ST_Temperature.py
#          Feature: Temperature
#          Design: ST_Temperature.pptx <-Update>
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################
#sudo -H pip3 install smbus2

# All imported modules must be added after config file
# Avoid use of 'cfg' as alias because all modules contain a config file
if __name__ == '__main__':
    import ST_Temperature_cfg as temp_cfg
else:
    import mod_Temperature.ST_Temperature_cfg as temp_cfg

import os
from inspect import currentframe
from datetime import datetime as dt
from datetime import timedelta as timedelta
import numpy as np
from Config_Test.EDT_Debug import EDT_Logger

timestamp_ok = False
termografias = True

#***********************
#from bmp280 import BMP280
#from smbus2 import SMBus
#from time import sleep
#******************

def TLogger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('temperature', debug_line, text)

try:
   from smbus2 import SMBus
   #Temporal import for demo below
   #from mod_Temperature.ST_Temperature.MLX90641.mlx90641 import *
   from mod_Temperature.MLX90641.mlx90641 import *
   from time import sleep
except Exception as e:
   TLogger('Temperature module failed: Could not load modules'+str(e))
   pass

import configparser
import unittest
import sys

class ST_Temperature:
   __instance = None

   @staticmethod
   def getInstance():
      """ Static access method. """
      if ST_Temperature.__instance == None:
         TLogger('Starting Initialization')
         ST_Temperature()
         TLogger('ST_Temperature ended')
         ''' Saved for melexis driver
         ST_Temperature._sensor = mlx.Mlx9064x('I2C-8', i2c_addr=0x33, frame_rate=2.0)  # establish communication between EVB90640 and
                                                                                        # PC, the I2C address of the MLX90640 sensor is
                                                                                        # 0x33 and change the frame rate to 2Hz
         ST_Temperature._sensor.init()  # read EEPROM and pre-compute calibration parameters.
         '''
         try:
             slaveAddr = 0x33
             ST_Temperature._sensor = MLX90641()

             ST_Temperature._sensor.i2cInit()
             ST_Temperature._sensor.setRefreshRate(slaveAddr, 0)

             RR = ST_Temperature._sensor.getRefreshRate(slaveAddr)

             eepromdata = (ctypes.c_uint16*832)()
             frameData = (ctypes.c_uint16*834)()
             params = paramsMLX90641()
             mlx90641To = (ctypes.c_float * 192)()

             ST_Temperature._sensor.dumpEE(slaveAddr, ctypes.cast(eepromdata, ctypes.POINTER(ctypes.c_uint16)))
             ST_Temperature._sensor.extractParameters(eepromdata, ctypes.byref(params))
             TLogger('Initialization ended')
             ST_Temperature._sensor.getFrameData(slaveAddr, ctypes.cast(frameData, ctypes.POINTER(ctypes.c_uint16)))
             Ta = ST_Temperature._sensor.getTa(frameData, params)-5.0
             ST_Temperature._sensor.calculateTo(frameData, params, 1, Ta, mlx90641To)
             Tf = max(mlx90641To)
             TLogger('Ta: ' + str(Ta) + ' Tf: ' + str(Tf))
         except Exception as e:
             TLogger('ST_Temperature intance failed: '+str(e))
         pass 
         #Temporal Initialization ---end---

      return ST_Temperature.__instance

   #Class Constructor
   def __init__(self):
      """ Virtually private constructor. """
      if ST_Temperature.__instance != None:
         raise Exception('This class is a singleton!')
      else:
         ST_Temperature.__instance = self
         ST_Temperature._isConnected = False
         #ST_Temperature._bus = None
         ST_Temperature._sensor = None
         #ST_Temperature._busId = 0
         ST_Temperature._sensorAddress = 0

   @staticmethod
   def Connect(i2cBus = temp_cfg.I2C_BUS, address = temp_cfg.SENSOR_ADDRESS):
      '''
         Connect the temperature device
            Opens the I2C bus and creates the sensor instance
      '''
      return True

   @staticmethod
   def Disconnect():
      '''
         Disconnect the temperature device
            Closes the I2C bus and deletes the sensor instance
      '''
      return True
   @staticmethod
   def CompensateVDDError(temperature):
      '''
         Voltage compensation

         MLX90614-Datasheet:
         10.1.3 Temperature reading dependence on VDD
            The typical VDD dependence of the ambient and object temperature is 0.6 C/V
            t_compensated = temperature - (vdd - 3) * 0.6
      '''
      tempCompensated = temperature #- (temp_cfg.SUPPLY_VOLTAGE - 3) * 0.6 #To be reviewed
      return tempCompensated

   @staticmethod
   def CompensateDistanceError(temperature, distance):
      '''
         Distance compensation
            Applies a compensation factor based on the distance
      '''
      #TODO: Verify distance is greater than base distance?
      tempCompensated = temperature + temp_cfg.DISTANCE_COMPENSATION_FACTOR * (distance - temp_cfg.BASE_DISTANCE)
      return tempCompensated

   @staticmethod
   def ConvertSurfaceToBody(temperature, ta, surface_temperature):
      '''
         Biophysical Conversion Formula
         ta = Ambient temperature read from FIR sensor
         tf = Forehead temperature read from FIR sensor, known as TO; Object Temperature
      '''
      low = 35.0
      high = 37.5
      tcore_body = 36.0
      tf = temperature * temp_cfg.FACTOR_PLANTA

      # compute thresholds
      if ta <= 25:
         low = 32.66 + 0.186 * (ta - 25)
         high = 34.84 + 0.148 * (ta - 25)
      elif ta > 25:
         low = 32.66 + 0.086 * (ta - 25)
         high = 34.84 + 0.100 * (ta - 25)

      #compute core body temperature
      if tf < low:
         tcore_body = 36.3 + (0.551658273 + 0.021525068 * ta) * (tf - low)
      elif low < tf < high:
         tcore_body = 36.3 + (0.5 / (high - low)) * (tf - low)
      elif tf > high:
         tcore_body = 36.8 + (0.829320618 + 0.002364434 * ta) * (tf - high)

      return tcore_body

   @staticmethod
   def GetAmbientTemperature():
      '''
         Get the ambient temperature
            Reads the ambient temperature (package temperature) and
            applies the corresponding compensation functions.
            Returns -273 in case on error
      '''
      temperature = temp_cfg.INVALID_TEMPERATURE
      ''' Saved for the driver
      frame = dev.read_frame()        # Read a frame from MLX9064x
                                    # In case EVB90640 hw is used, the EVB will buffer up to 4 frames, so possibly you get a cached frame.
      f = dev.do_compensation(frame)  # calculates the temperatures for each pixel
      #print('f: ',f)
      ta = f.pop() # pop ambient temperature from the array.
      '''
      # Temporal implementation
      slaveAddr = 0x33
      eepromdata = (ctypes.c_uint16*832)()
      frameData = (ctypes.c_uint16*834)()
      params = paramsMLX90641()
      mlx90641To = (ctypes.c_float * 192)()
      
      ST_Temperature._sensor.dumpEE(slaveAddr, ctypes.cast(eepromdata, ctypes.POINTER(ctypes.c_uint16)))
      ST_Temperature._sensor.extractParameters(eepromdata, ctypes.byref(params))

      ST_Temperature._sensor.getFrameData(0x33, ctypes.cast(frameData, ctypes.POINTER(ctypes.c_uint16)))
      ta = ST_Temperature._sensor.getTa(frameData, params)-5.0
      print('MLX ambient temperature: ' + str(ta))
      return ta

   @staticmethod
   def GetWeatherTemperature():

      ROOM_TEMP_DB_PATH = os.getcwd() + '/mod_Temperature/'
      ROOM_TEMP_DB_NAME = 'Room_Temperature.txt'
      HUB_RoomTemp={
      'region':'unknown',
      'temperature': 0.0,
      'feels_like' : 0.0,
      'humidity' : 0,
      'timestamp' : 0
      }
      room_temperature = 21.05    # Default value

      if os.path.exists(ROOM_TEMP_DB_PATH + ROOM_TEMP_DB_NAME):
          TLogger('Reading temperature file')

          cfgParser = configparser.RawConfigParser()
          cfgParser.read(ROOM_TEMP_DB_PATH + ROOM_TEMP_DB_NAME)

          for key in HUB_RoomTemp:
              HUB_RoomTemp[key] = cfgParser.get('Room Temperature', key)
              if key == 'temperature':
                  room_temperature = float(cfgParser.get('Room Temperature', key))
              if key == 'timestamp':
                  timestamp = dt.fromtimestamp(int(cfgParser.get('Room Temperature', key)))
                  if(timestamp >= (dt.now() - timedelta(minutes=15))):
                      timestamp_ok = True
                  else:
                      timestamp_ok = False
          TLogger('The information in the file is:' + str(HUB_RoomTemp))
      else:
          TLogger('The temperature file does not exist!')

      print('Room temperature', room_temperature)

      return room_temperature,timestamp_ok

   @staticmethod
   def GetObjectTemperature(distance = 60, posicion=temp_cfg.POSICION, dimension = temp_cfg.DIMENSION, sap_id='0000'):  #DBL_249
      '''
         Get the object temperature
            Reads the object temperature and applies the corresponding
            conversion and compensation functions.
            Returns -273 in case on error
      '''
      body_temperature = temp_cfg.INVALID_TEMPERATURE
      log_temp = "DATA," 
      if True:
         try:
            # DBL_322 Freee Issue correct Distance_Measure
            # dis = 80-0.35294(h-170)
            distance = 80.0 - 0.35294 * (dimension[0] - 170)
            if (distance < 35.0):
               distance = 35
            if (distance > 85):
               distance = 85
            '''
            frame = ST_Temperature._sensor.read_frame()        # Read a frame from MLX90640
                                                               # In case EVB90640 hw is used, the EVB will buffer up to 4 frames, so possibly you get a cached frame.
            f = ST_Temperature._sensor.do_compensation(frame)  # calculates the temperatures for each pixel
            '''
            RESOLUCION_CAMARA_Y = 480 #de 486 pixeles
            RESOLUCION_CAMARA_X = 640 #de 864 pixeles
            DIMENSION_CAMARA_Y = 309.1358 #de 313 mm
            DIMENSION_CAMARA_X = 367.4074 #de 496 mm
            DISTANCIAOFFSET_SENVSCAM_Y = 70 #de  70 mm
            DISTANCIAOFFSET_SENVSCAM_X = -65.8148 #de -168 mm
            DIMENSION_SENSOR_Y = 365 #pixels a 60 cm
            DIMENSION_SENSOR_X = 220 #pixels a 60 cm
            RESOLUCION_SENSOR_Y = 16 #indice de matriz del mlx90641
            RESOLUCION_SENSOR_X = 12 #indice de matriz del mlx90641
            
            slaveAddr = 0x33
            eepromdata = (ctypes.c_uint16*832)()
            frameData = (ctypes.c_uint16*834)()
            params = paramsMLX90641()
            mlx90641To = (ctypes.c_float * 192)()

            ST_Temperature._sensor.dumpEE(slaveAddr, ctypes.cast(eepromdata, ctypes.POINTER(ctypes.c_uint16)))
            ST_Temperature._sensor.extractParameters(eepromdata, ctypes.byref(params))

            ST_Temperature._sensor.getFrameData(slaveAddr, ctypes.cast(frameData, ctypes.POINTER(ctypes.c_uint16)))
            tb = ST_Temperature._sensor.getTa(frameData, params)-5.0
            ST_Temperature._sensor.calculateTo(frameData, params, 1, tb, mlx90641To)
            
            if len(mlx90641To) == 768:
                image = np.reshape(mlx90641To, (24, 32)) # Vector to matrix for mlx90640
            else:
                image = np.reshape(mlx90641To, (12, 16)) # Vector to matrix for mlx90641

            image = np.rot90(image,1)       # Sensor is rotated 90 deg
            if termografias:
                dump_name = "{0}-{1}-{2}{3}".format('/home/edt/Documents/Share/_Termografias/mlx9064x-dump',dt.now().strftime("%Y-%m-%d-%H-%M-%S-%f"),sap_id,'.csv')
                np.savetxt(dump_name, image, delimiter=',', fmt='%f')
            #Coordenadas del rostro en pixeles
            PosicionPixelCamY = posicion[0]
            PosicionPixelCamX = posicion[1]
            PosicionPixelCamY2 = posicion[0]+dimension[0]
            PosicionPixelCamX2 = posicion[1]+dimension[1]
            TLogger('PosicionPixelCamY: '+str(PosicionPixelCamY)+' PosicionPixelCamX: '+str(PosicionPixelCamX)+' PosicionPixelCamY2: '+str(PosicionPixelCamY2)+' PosicionPixelCamX2: '+str(PosicionPixelCamX2))
            #Formula para Y
            ProporcionCamY = PosicionPixelCamY / RESOLUCION_CAMARA_Y
            DistanciaCamaraY = ProporcionCamY * DIMENSION_CAMARA_Y
            DistanciaSensorY = DistanciaCamaraY + DISTANCIAOFFSET_SENVSCAM_Y
            ProporcionSensY = DistanciaSensorY / DIMENSION_SENSOR_Y
            PosicionPixelSensor_Y = np.int(np.floor(ProporcionSensY * RESOLUCION_SENSOR_Y)) + 1 # Recorta 1 en la parte superior
            TLogger('ProporcionCamY: '+str(ProporcionCamY)+' DistanciaCamaraY: '+str(DistanciaCamaraY)+' DistanciaSensorY: '+str(DistanciaSensorY)+' ProporcionSensY: '+str(ProporcionSensY)+' PosicionPixelSensor_Y: '+str(PosicionPixelSensor_Y))
            ProporcionCamY2 = PosicionPixelCamY2 / RESOLUCION_CAMARA_Y
            DistanciaCamaraY2 = ProporcionCamY2 * DIMENSION_CAMARA_Y
            DistanciaSensorY2 = DistanciaCamaraY2 + DISTANCIAOFFSET_SENVSCAM_Y
            ProporcionSensY2 = DistanciaSensorY2 / DIMENSION_SENSOR_Y
            PosicionPixelSensor_Y2 = np.int(np.ceil((ProporcionSensY2 * RESOLUCION_SENSOR_Y) - 0.5))
            PosicionPixelSensor_Y2 = np.int((PosicionPixelSensor_Y+PosicionPixelSensor_Y2)/2) - 1 #Usa la mitad superior del cuadro azul, Recorta 1 de la parte inferior
            TLogger('ProporcionCamY2: '+str(ProporcionCamY2)+' DistanciaCamaraY2: '+str(DistanciaCamaraY2)+' DistanciaSensorY2: '+str(DistanciaSensorY2)+' ProporcionSensY2: '+str(ProporcionSensY2)+' PosicionPixelSensor_Y2: '+str(PosicionPixelSensor_Y2))
            #Formula para X
            ProporcionCamX = PosicionPixelCamX / RESOLUCION_CAMARA_X
            DistanciaCamaraX = ProporcionCamX * DIMENSION_CAMARA_X
            DistanciaSensorX = DistanciaCamaraX + DISTANCIAOFFSET_SENVSCAM_X
            ProporcionSensX = DistanciaSensorX / DIMENSION_SENSOR_X
            PosicionPixelSensor_X = np.int(np.floor(ProporcionSensX * RESOLUCION_SENSOR_X)) + 1 # Recorta 1 a la izquierda 
            TLogger('ProporcionCamX: '+str(ProporcionCamX)+' DistanciaCamaraX: '+str(DistanciaCamaraX)+' DistanciaSensorX: '+str(DistanciaSensorX)+' ProporcionSensX: '+str(ProporcionSensX)+' PosicionPixelSensor_X: '+str(PosicionPixelSensor_X))
            ProporcionCamX2 =PosicionPixelCamX2 / RESOLUCION_CAMARA_X
            DistanciaCamaraX2 =ProporcionCamX2 * DIMENSION_CAMARA_X
            DistanciaSensorX2 =DistanciaCamaraX2 + DISTANCIAOFFSET_SENVSCAM_X
            ProporcionSensX2 = DistanciaSensorX2 / DIMENSION_SENSOR_X
            PosicionPixelSensor_X2 = np.int(np.ceil((ProporcionSensX2 * RESOLUCION_SENSOR_X) -0.5)) - 1 # Recorta 1 a la derecha
            TLogger('ProporcionCamX2: '+str(ProporcionCamX2)+' DistanciaCamaraX2: '+str(DistanciaCamaraX2)+' DistanciaSensorX2: '+str(DistanciaSensorX2)+' ProporcionSensX2: '+str(ProporcionSensX2)+' PosicionPixelSensor_X2: '+str(PosicionPixelSensor_X2))

            TLogger('Area utilizada: '+str(PosicionPixelSensor_Y+1)+","+str(PosicionPixelSensor_Y2+1)+","+str(PosicionPixelSensor_X+1)+","+str(PosicionPixelSensor_X2+1))
            area = image[PosicionPixelSensor_Y:PosicionPixelSensor_Y2, PosicionPixelSensor_X:PosicionPixelSensor_X2]
            if termografias:
                dump_name = "{0}-{1}-{2}-{3}-{4}-{5}-{6}{7}".format('/home/edt/Documents/Share/_Termografias/mlx9064x-dump',dt.now().strftime("%Y-%m-%d-%H-%M-%S-%f"),PosicionPixelSensor_Y+1,PosicionPixelSensor_Y2+1,PosicionPixelSensor_X+1,PosicionPixelSensor_X2+1,sap_id,'.csv')
                np.savetxt(dump_name, area, delimiter=',', fmt='%f')

            surface_temperature = np.max(area)      # Max from accurate sensor area
            tmin = np.min(image)                      # Min temperature used for ta
            tw,timestamp_ok = ST_Temperature.GetWeatherTemperature()

            #****************BMP 280*********************************
           # bus = SMBus(1)
            #bmp280 = BMP280(i2c_dev=bus)
            #tbmp = bmp280.get_temperature()
            #ta = tbmp
            #************************************************
            #ta = tbmp #default tbmp
            if timestamp_ok == True:
                ta = tw
            else:
                ta = tmin
            TLogger('Surface temperature: ' + str(surface_temperature))
            log_temp = log_temp + str(surface_temperature)+","

            # Voltage compensation
            vdd_temperature = ST_Temperature.CompensateVDDError(surface_temperature)
            TLogger('VDD compensated temperature: ' + str(vdd_temperature))
            log_temp = log_temp + str(vdd_temperature)+","

            # Distance compenstion
            distance_temperature = ST_Temperature.CompensateDistanceError(vdd_temperature, distance)
            TLogger('Distance compensated temperature: ' + str(distance_temperature))
            log_temp = log_temp + str(distance_temperature)+","

            # Skin temperature to body temperature conversion
            body_temperature = ST_Temperature.ConvertSurfaceToBody(distance_temperature, ta, surface_temperature)
            TLogger('Body temperature: ' + str(round(body_temperature,1)))
            

            log_temp = log_temp + str(round(body_temperature,1))+","
            log_temp = log_temp + str(tw)+","         
            log_temp = log_temp + str(tb)+","
            log_temp = log_temp + str(tmin)+ ","
            log_temp = log_temp + str(ta)+ ","
            #log_temp = log_temp + str(tbmp)+ "," #tbmp
            log_temp = log_temp + str(sap_id) 

            TLogger(str(log_temp))

         except IOError as e:
            ST_Temperature._isConnected = False
            # TODO: Send error to POSTServices?
            TLogger('Temperature sensor failed - No response: ' + str(e))
         except Exception as e:
            #TODO: Send error to POSTServices?
            TLogger('Temperature sensor failed:' + str(e))
      else:
         #TODO: Send error to POSTServices?
         TLogger('Sensor not connected!')
      #DBL_325_Limit_Low_hihg_Temperature
      if (body_temperature < 35.0):
         body_temperature = 35.0 + body_temperature/100.0   #To keep traceability of the low temperature

      #DBL_325_Limit_Low_high_Temperature
      if (body_temperature > 39.0):
         body_temperature = 39.0 + body_temperature/100.0   #To keep traceability of the hihg temperature         
                  
      return body_temperature



'''
**********************************
********* Unit Test **************
*** https://docs.python.org/2/library/unittest.html#assert-methods *****
**********************************
'''
class TC001_Test_SingleTone(unittest.TestCase):
   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test001_1_TestSingletoneException(self):
      print('******************** test001_TestSingletone ************************')
      print('-------------------- test001_TestSingletoneException ---------------')
      instance1 = ST_Temperature()
      exceptionFlag = False 
      try:
         instance2 = ST_Temperature()
      except Exception as e:
         exceptionFlag = True
      else:
         pass
      self.assertTrue(exceptionFlag,True)

   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test001_2_TestMultipleGetInstances(self):
      print('-------------------- test002_TestMultipleGetInstances ---------------')
      instance1 = ST_Temperature.getInstance()
      instance2 = ST_Temperature.getInstance()
      self.assertEqual(instance1, instance2)

class TC002_Test_GetTemperature(unittest.TestCase):
   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test002_1_TestConnect(self):
      print('******************** test002_1_TestConnect ************************')
      sensor = ST_Temperature.getInstance()
      connected = sensor.Connect()
      self.assertEqual(connected, True)

      sensor.Disconnect()

   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test002_2_TestGetObjectTemperature(self):
      print('******************** test002_2_TestGetObjectTemperature *****************')
      sensor = ST_Temperature.getInstance()
      sensor.Connect()

      temperature = sensor.GetObjectTemperature(35)
      print('obj temp: ' + str(temperature))
      self.assertGreater(temperature, 0.0)

      sensor.Disconnect()

   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test002_3_TestGetAmbientTemperature(self):
      print('******************** test002_3_TestGetAmbientTemperature ***********')
      sensor = ST_Temperature.getInstance()
      sensor.Connect()

      temprerature = sensor.GetAmbientTemperature()
      print('ambient temp: ' + str(temprerature))
      self.assertGreater(temprerature, 0.0)

      sensor.Disconnect()

   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test002_5_TestEmissivity(self):
      print('******************** test002_4_TestEmissivity ***********')
      sensor = ST_Temperature.getInstance()
      sensor.Connect()

      emissivity = sensor.GetEmissivity()
      print('current emissivity: ', emissivity)
      self.assertGreaterEqual(emissivity, 0.1)
      self.assertLessEqual(emissivity, 1.0)

      reqEmissivity = temp_cfg.EMISSIVITY_DEFAULT
      newEmissivity = sensor.SetEmissivity(reqEmissivity)
      print('new emissivity: ', newEmissivity)
      self.assertLessEqual(newEmissivity, reqEmissivity * 1.001)
      self.assertGreaterEqual(newEmissivity, reqEmissivity * .999)

      sensor.Disconnect()

   @unittest.skipIf(temp_cfg._debugTest==True,"DebugMode")
   def test002_6_TestDisconnect(self):
      print('******************** test002_6_TestDisconnect **********************')
      sensor = ST_Temperature.getInstance()
      sensor.Connect()

      disconnected = sensor.Disconnect()
      self.assertEqual(disconnected, True)


if __name__ == '__main__':
    #Temporal import for demo below
    from MLX90641.mlx90641 import *
    import numpy as np
    #unittest.main()
    low = 35.0
    high = 37.5
    tcore_body = 36.0

    ''' Saved for melexis driver
    dev = mlx.Mlx9064x('I2C-8', i2c_addr=0x33, frame_rate=2.0) # establish communication between EVB90640 and
                                                               # PC, the I2C address of the MLX90640 sensor is
                                                               # 0x33 and change the frame rate to 2Hz
    dev.init()                      # read EEPROM and pre-compute calibration parameters.
    frame = dev.read_frame()        # Read a frame from MLX90640
                                    # In case EVB90640 hw is used, the EVB will buffer up to 4 frames, so possibly you get a cached frame.
    f = dev.do_compensation(frame)  # calculates the temperatures for each pixel
    print('f: ',f)
    f = dev.do_handle_bad_pixels(f)
    print('fbad:',f)
    '''

    #Temporal Initialisation ---start---
    slaveAddr = 0x33
    dev = MLX90641()

    dev.i2cInit()
    dev.setRefreshRate(slaveAddr, 0)

    RR = dev.getRefreshRate(slaveAddr)
    #print ("refresh rate: {}".format (RR))

    eepromdata = (ctypes.c_uint16*832)()
    frameData = (ctypes.c_uint16*834)()
    params = paramsMLX90641()
    mlx90641To = (ctypes.c_float * 192)()

    dev.dumpEE(slaveAddr, ctypes.cast(eepromdata, ctypes.POINTER(ctypes.c_uint16)))
    dev.extractParameters(eepromdata, ctypes.byref(params))
    #Temporal Initialization ---end---
    dev.getFrameData(slaveAddr, ctypes.cast(frameData, ctypes.POINTER(ctypes.c_uint16)))
    Ta = dev.getTa(frameData, params)-5.0
    dev.calculateTo(frameData, params, 1, Ta, mlx90641To)
    Tf = max(mlx90641To)
    if len(mlx90641To) == 768:
        image = np.reshape(mlx90641To, (24, 32)) # Vector to matrix for mlx90640

    else:
        image = np.reshape(mlx90641To, (12, 16)) # Vector to matrix for mlx90641

    image = np.rot90(image,1)       # Sensor is rotated 90 deg
    area = image#[2:10, 4:12]        # cuts 2 rows at the top and bottom, cuts 4 rows at the left and right
    surface_temperature = np.max(area)      # Max from accurate sensor area
    tf = surface_temperature
    #temperature = surface_temperature + 0.25*(surface_temperature-ambient_temperature) + 1.6
    #ta = ambient_temperature()
    #ta = f.pop() # pop ambient temperature from the array.
    ta = Ta
    print('MLX ambient temperature: ' + str(ta))

    # compute thresholds
    if ta <= 25:
       low = 32.66 + 0.186 * (ta - 25)
       high = 34.84 + 0.148 * (ta - 25)
    elif ta > 25:
       low = 32.66 + 0.086 * (ta - 25)
       high = 34.84 + 0.100 * (ta - 25)

    #compute core body temperature
    if tf < low:
       tcore_body = 36.3 + (0.551658273 + 0.021525068 * ta) * (tf - low)
    elif low < tf < high:
       tcore_body = 36.3 + (0.5 / (high - low)) * (tf - low)
    elif tf > high:
       tcore_body = 36.8 + (0.829320618 + 0.002364434 * ta) * (tf - high)
    print('Core temperature: ' + str(tcore_body))
    background_temperature = np.average(area[1,:])     # Average from top row   
    print('Background temperature: ' + str(background_temperature))
    cloth_temperature = np.average(area[-1,:])    # Average from bottom row
    print('Cloth temperature: ' + str(cloth_temperature))
    np.savetxt('mlx9064x-dump-test.csv', image, delimiter=',', fmt='%f')


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
# Oct-08-2020 sjkk9h
#   + DBL_62
#      - Added connection validation
#
# Nov-13-2020 zzn3y2
#   + DBL_51
#      - Change MLX90614 for MLX90640 implementation.
#
# Ene-27-2021 zzn3y2
#   + DBL_61
#      - MLX9064x implementation.
#
# Feb-05-2021 zzn3y2
#   + DBL_61
#      - MLX90641 driver module implementation.
#
# Feb-09-2021 zzn3y2
#   + DBL_213
#      - DBL_Temperatura: Agregar temperatura base del sensor al log
#
# Feb-09-2021 zzn3y2
#   + DBL_214
#      - DBL_Log: Matriz de temperaturas
#
# Feb-12-2021 zzn3y2
#   + DBL_215
#      - DBL_Temperatura: Limitar la matriz de termografia
#
# Feb-17-2021 zzn3y2
#   + DBL_222
#      - DBL: Ajuste de temperatura con cuadro azul
#
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225
#      - Updated function Logger().
#
# Mar-01-2021 zzn3y2
#   + DBL_228
#      - Agregar a los logs Tmin de la termografia antes del SAP ID
#
# Mar-12-2021 zzn3y2
#   + DBL_237
#      - Agregar el factor de la planta cuya funcionalidad es simular un opturador
#
# Mar-18-2021 zzn3y2
#   + DBL_239
#      - Recorte de Imagen a la mitad del cuadro azul
#
# Mar-26-2021 zzn3y2
#   + DBL_246
#      - Eliminar una linea alrededor de la termografia

# Abr-06-2021 zzn3y2
#   + DBL_245
#      - Agregar Timestamp a Temperatura. Realizar una comparacion de timestamp, y decidir
#        si se utiliza el servicio weather o la temperatura minima de la termografia
# Abr-28-2021 
#    DBL_256
#          Considerar la temeperatura ambiente para discriminar temperaturas superficiales
#           altas	
#    DBL_253
#       Add bmp DBL_286
#
# Ene-10-2022 Arturo Gaona
#   + DBL_322: Comment BMP 280 to avoid Temperature freeze Issue
#      -Comment BMP280
#
# Mar-18-2022 Arturo Gaona
#   + DBL_325: Limit low and hihg temperatures to 35.XXX and 39.XXX
#      -Limit low and hihg temperatures when tem is less than 35 degress set as 35.XXX where XXX is temperature value
#
#########################################################################################
