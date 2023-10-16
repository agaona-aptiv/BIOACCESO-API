'''
Created on February 2021
@author: Lucia Chavez
'''
#########################################################################################
#  COPYRIGHT 2021
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: EDT_AccessCTRL/mod_Temperature
#          Program: Static interface to manage IIC and read temperature from sensor
#          Enterprise: Condumex
#          SW Developer: Lucia Chavez
#
#          File: MLX641_data.py
#          Feature: Temperature
#          Design: NA
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################

import ST_Temperature_cfg as temp_cfg
import numpy as np

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
    #print('Object temperature: ' + str(temperature))
    background_temperature = np.average(area[:,1]) + 1.6     # Average from accurate sensor area   
    print('Background temperature: ' + str(background_temperature))
    cloth_temperature = np.average(area[:,-1]) + 1.6     # Min from accurate sensor area   
    print('Cloth temperature: ' + str(cloth_temperature))
    np.savetxt('mlx9064x-dump-test.csv', image, delimiter=',', fmt='%f')