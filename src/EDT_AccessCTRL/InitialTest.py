'''
Created on 01-Nov-2020
@author: José Arturo Gaona
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: **InitialTest
#          Description: **This module provide simple test for HW verifications
#          Enterprise: Condumex
#          SW Developer: **José Arturo Gaona Cuadra
#          
#          File: **InitialTest.py
#          Feature: **Diagnostics
#          Design:  **NA
#          Deviations: **NA
#   
#  **Information that must change according to the script
#########################################################################################
import cv2
import numpy as np
import tkinter as tk
import os.path
import time
from os import path
import configparser
from uuid import getnode as get_mac
try:
    from mod_Temperature.MLX90641.mlx90641 import *
    from mod_Temperature.ST_Temperature import *
    import mod_Temperature.ST_Temperature_cfg as temp_cfg
    import mod_GPIOInterfaces.ST_GPIOInterfaces as gpioDriver
    from Config_Test.Manufacturing.API_MAN_Config_Cal import *    
    from Config_Test.SpecificServices.API_SS_Config_Cal import *    
except Exception as e:
    pass
from io import open
import datetime

MANUF_CONFIG_PATH = os.getcwd() + '/Config_Test/Manufacturing/'
MANUF_CONFIG_FILE_NAME = 'MAN_CFG.txt'

SS_CONFIG_PATH = os.getcwd() + '/Config_Test/SpecificServices/'
SS_CONFIG_FILE_NAME = 'SS_CFG.txt'

RELEASE_INFO_PATH = '../_Release/'
RELEASE_INFO_FILE_NAME = 'release_info.txt'

DELAY_DISPLAY_TIME = 10000
TEST_LOG_FILE = 'InitialTest.log'

manuf_enabled = True
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
SCREEN_SIZE = (screen_width,screen_height) #1024 * 600
cv2.namedWindow('Dispositivo Biometrico de Acceso Test inicial', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Dispositivo Biometrico de Acceso Test inicial',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def SaveLog(reportList):
    global manuf_enabled
	
    try:
        #if (not path.exists('AbsPathForConfigurationfile.cfg')):   # Update for configuration info
        if manuf_enabled:
            now = datetime.datetime.now()
            archivoTexto = open(TEST_LOG_FILE,"a")
            archivoTexto.write("\n" + "Test Executed: " +  now.strftime("%Y-%m-%d %H:%M:%S"))
            for element in reportList:
                archivoTexto.write("\n" + element)
            archivoTexto.close()
    except Exception as e:
        print('Exception:' + str(e))

def create_blank(width, height):
    red = (255, 0, 0)
    green = (0,255, 0)
    image = np.zeros((height, width, 3), np.uint8)
    color_red = tuple(reversed(red))
    color_green = tuple(reversed(green))

    reportList = []
    #Check for Camera connections
    if (path.exists("/dev/video0")):
        color_result = color_green
        text_result = 'PASSED'
        print('**** Video 0 Interface TEST PASSED: /dev/video0 was found')
        reportList.append('Video 0 Interface TEST PASSED: /dev/video0 was found')
    else:
        color_result = color_red
        text_result = 'FAILED'
        print('***** Video 0 Interface TEST FAILED: /dev/video0 was NOT found')
        reportList.append('Video 0 Interface TEST FAILED: /dev/video0 was NOT found')

    image[:int(height*1/4)] = color_result
    image = cv2.putText(image,'Video Camera 0 Test: '+text_result,(int(width/2*0.3),int((height*2)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'Video Camera 0 Test: '+text_result,(int(width/2*0.3),int((height*2)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)

    if (path.exists("/dev/video1")):
        color_result = color_green
        text_result = 'PASSED'
        print('***** Video 1 Interface TEST PASSED: /dev/video1 was found')
        reportList.append('Video 1 Interface TEST PASSED: /dev/video1 was found')
    else:
        color_result = color_red
        text_result = 'FAILED'
        print('**** Video 1 Interface TEST FAILED: /dev/video1 was NOT found')  
        reportList.append('Video 1 Interface TEST FAILED: /dev/video1 was NOT found')

    image[int(height*1/4):int(height*2/4)] = color_result
    image = cv2.putText(image,'Video Camera 1 Test: '+text_result,(int(width/2*0.3),int((height*4)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'Video Camera 1 Test: '+text_result,(int(width/2*0.3),int((height*4)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)

    try:
        gpioControl = gpioDriver.ST_GPIOInterfaces.getInstance()
        gpioControl.Init_GPIO_Ports()
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.RELAY1, gpio_state=0)
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.RELAY2, gpio_state=0)
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.BUZZER, gpio_state=1)  #1
        time.sleep(0.2)  #0.2
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.RELAY1, gpio_state=1)
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.RELAY2, gpio_state=1)
        gpioControl.Set_GPIO_State(gpio_pin=gpioDriver.BUZZER, gpio_state=0)   #0
        gpioControl.Clean_GPIO_Ports()
        color_result = color_green
        text_result = 'PASSED'
        print('**** GPIO Interfaces TEST PASSED:')
        reportList.append('GPIO Interfaces TEST PASSED')
    except Exception as e:
        color_result = color_red
        text_result = 'FAILED'
        print('**** GPIO Interfaces TEST FAILED: Exception'+ str(Exception))
        reportList.append('GPIO Interfaces TEST FAILED: Exception'+ str(Exception))

    image[int(height*2/4):int(height*3/4)] = color_result
    image = cv2.putText(image,'GPIO Test: '+text_result,(int(width/2*0.3),int((height*6)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'GPIO Test: '+text_result,(int(width/2*0.3),int((height*6)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)

    try:
        temperatureDevice = ST_Temperature.getInstance()
        temperatureDevice.Connect()
        temperature = temperatureDevice.GetObjectTemperature()
        if temperature == -273:
            color_result = color_red
            text_result = 'FAILED'
            print('**** Device Temperature TEST FAILED:')
            reportList.append('Device Temperature TEST FAILED')
        else:
            color_result = color_green
            text_result = 'PASSED'        
            print('**** Device Temperature TEST PASSED:' + str(temperature))
            reportList.append('Device Temperature TEST PASSED:' + str(temperature))
        temperatureDevice.Disconnect()

    except Exception as e:
        color_result = color_red
        text_result = 'FAILED'
        print('****Device Temperature TEST FAILED: Exception'+ str(Exception))
        reportList.append('****Device Temperature TEST FAILED: Exception'+ str(Exception))
    image[int(height*3/4):height] = color_result
    image = cv2.putText(image,'Temperature Test: '+text_result,(int(width/2*0.3),int((height*8)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'Temperature Test: '+text_result,(int(width/2*0.3),int((height*8)/10)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)


    #LOCAL_IP = ''
    #LOCAL_IP = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
    #if LOCAL_IP == '':
    #    LOCAL_IP = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
    #if (len(LOCAL_IP)==13):
    #    print('****LOCAL_IP TEST PASSED:' + str(LOCAL_IP))
    #else:
    #    print('****LOCAL_IP TEST FAILED:  No IP Address was defined')

    #Write tittle
    image = cv2.putText(image,'Dispositivo  Biometrico  de  Acceso  Test  inicial',(int(width/2*0.3),int((height*1)/20)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'Dispositivo  Biometrico  de  Acceso  Test  inicial',(int(width/2*0.3),int((height*1)/20)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)
    image = cv2.putText(image,'El Dispositivo de Acceso Biometrico esta iniciando...',(int(width/2*0.3),int((height*18)/20)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0), 2)
    image = cv2.putText(image,'El Dispositivo de Acceso Biometrico esta iniciando...',(int(width/2*0.3),int((height*18)/20)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255), 1)
    SaveLog(reportList)
    return image

def Create_Device_Config_Information():
    global manuf_enabled

    try:
        # Create manufacturing configuration file
        if not path.exists(MANUF_CONFIG_PATH + MANUF_CONFIG_FILE_NAME):
            manuf_conf = API_MAN_Config_Cal.getInstance()
            cfgParser = configparser.RawConfigParser()
            cfgParser.read(MANUF_CONFIG_PATH + MANUF_CONFIG_FILE_NAME)

            # Read SW Id from /_Release/release_info.txt
            if path.exists(RELEASE_INFO_PATH + RELEASE_INFO_FILE_NAME):
                print('Updating man_sw_version in new MAN_CFG.txt')
                relParser = configparser.RawConfigParser()
                relParser.read(RELEASE_INFO_PATH + RELEASE_INFO_FILE_NAME)
                sw_version = relParser.get('SW_RELEASE_INFORMATION', 'sw_version')
                print('sw_version: ' + str(sw_version))
                cfgParser.set('MAN_Configuration', 'sw_id', sw_version.replace('.',''))

            # Read MAC Address from system
            jetson_mac_str = str(':'.join(['{:02x}'.format((get_mac()>>ele) & 0xff) for ele in range(0,8*6,8)][::-1]))
            cfgParser.set('MAN_Configuration', 'mac_address', jetson_mac_str.upper())

            with open(MANUF_CONFIG_PATH + MANUF_CONFIG_FILE_NAME, 'w') as manconfigfile:
                cfgParser.write(manconfigfile)
        else:
            if path.exists(RELEASE_INFO_PATH + RELEASE_INFO_FILE_NAME):
                cfgParser = configparser.RawConfigParser()
                cfgParser.read(MANUF_CONFIG_PATH + MANUF_CONFIG_FILE_NAME)
                relParser = configparser.RawConfigParser()
                relParser.read(RELEASE_INFO_PATH + RELEASE_INFO_FILE_NAME)
                sw_version = relParser.get('SW_RELEASE_INFORMATION', 'sw_version')
                sw_version = sw_version.replace('.','')
                man_sw_version = cfgParser.get('MAN_Configuration', 'sw_id')
                man_serial_number = cfgParser.get('MAN_Configuration', 'serial_number')
                print('sw_version: ' + str(sw_version))
                print('man_sw_version: ' + str(man_sw_version))
                print('man_serial_number: ' + str(man_serial_number))

                # Check for a software version 
                if sw_version != man_sw_version:
                    print('Updating man_sw_version...')
                    cfgParser.set('MAN_Configuration', 'sw_id', sw_version.replace('.',''))

                    with open(MANUF_CONFIG_PATH + MANUF_CONFIG_FILE_NAME, 'w') as manconfigfile:
                        cfgParser.write(manconfigfile)

                # Check if the device has already completed the manufacturing process
                if man_serial_number != 'B0000':
                    manuf_enabled = False

        # Create specific services configuration file
        if not path.exists(SS_CONFIG_PATH + SS_CONFIG_FILE_NAME):
            ss_conf = API_SS_Config_Cal.getInstance()
            ssParser = configparser.RawConfigParser()
            ssParser.read(SS_CONFIG_PATH + SS_CONFIG_FILE_NAME)
            jetson_ip = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
            if jetson_ip == '':
                jetson_ip = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()

            print('Jetson IP: ' + str(jetson_ip))
            ssParser.set('SS_Configuration', 'dba_ip', jetson_ip)

            with open(SS_CONFIG_PATH + SS_CONFIG_FILE_NAME, 'w') as ssconfigfile:
                ssParser.write(ssconfigfile)
        else:
            ssParser = configparser.RawConfigParser()
            ssParser.read(SS_CONFIG_PATH + SS_CONFIG_FILE_NAME)
            ss_ip = ssParser.get('SS_Configuration', 'dba_ip')

            jetson_ip = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
            if jetson_ip == '':
                jetson_ip = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()

            print('SS_CFG IP = ' + str(ss_ip))
            print('Jetson IP = ' + str(jetson_ip))
            if ss_ip != jetson_ip:
                print('Updating Jetson IP...')
                ssParser.set('SS_Configuration', 'dba_ip', jetson_ip)

                with open(SS_CONFIG_PATH + SS_CONFIG_FILE_NAME, 'w') as ssconfigfile:
                    ssParser.write(ssconfigfile)

    except Exception as SetDeviceEx:
        print('[Initial Test]: Error while trying to set the MAC ADDRESS into the Manufacturing Information file!')
        print('[Exception]: ' + str(SetDeviceEx))
        pass

    print('MANUFACTURING PROCESS STATUS: ' + str(manuf_enabled))


# Create new blank 300x300 red image
width1, height1 = screen_width, screen_height

Create_Device_Config_Information()
image = create_blank(width1, height1)
cv2.imshow('Dispositivo Biometrico de Acceso Test inicial', image)
cv2.waitKey(DELAY_DISPLAY_TIME)   #10 seg
cv2.destroyAllWindows()

######################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
#
# Date          userid          Description                                   
# 01-Nov-2020   Arturo Gaona    first release of the design implementation    
#                                       
# Oct-21-2020 nzddvp
#   DBL_63:
#       - Updated GPIO Interfaces
#
# Jan-22-2021 Leobardo N Hernandez
#   DBL_201:
#       - Added implementation to create initial device configuration information.
#
# Jan-26-2021 Arturo Gaona / Leobardo N Hernandez
#   DBL_204:
#       - Save initial test report in a log file while the device serial number has not
#         been written.
#
# Feb-03-2021 Leobardo N Hernandez
#   DBL_209:
#       - Updated Create_Device_Config_Information() to save IP in SS_CFG.txt
#
#########################################################################################
