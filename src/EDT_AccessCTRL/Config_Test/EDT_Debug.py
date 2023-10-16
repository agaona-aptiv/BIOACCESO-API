'''
Created on February, 2021
@author: Leobardo N Hernandez
'''
#########################################################################################
#  COPYRIGHT 2021
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: Debug
#          Description: Script for saving debugging logs
#          Enterprise: Condumex
#          SW Developer: Leobardo N Hernandez
#          
#          File: EDT_Debug.py
#          Feature: Debug
#          Design:  NA
#          Deviations: **Por aclarar con Calidad
#########################################################################################
import os
from io import open
from inspect import currentframe
from datetime import date
from datetime import datetime as dt
import cv2

DEBUG = True
log_to_file = True
log_image_to_file = True

LOGS_PATH = '/home/edt/Documents/Share/_Logs/'
IMAGES_LOG_PATH = '/home/edt/Documents/Share/_ImagesLog/'

def EDT_Logger(log_file, debug_line, text):
    try:
        if DEBUG:
            today = date.today()
            dt_string = ' ln ' + debug_line + ' - ' + dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if log_to_file:
                if not os.path.exists(LOGS_PATH):
                    os.makedirs(LOGS_PATH)

                with open(LOGS_PATH + log_file + '_log_' + str(today) + '.log', "a+") as file:
                    file.write(dt_string[:-3] + ': ' + str(text) + '\n')
            else:
                print(dt_string[:-3] + ':', str(text))
    except Exception as e:
        print("ERROR AL ESCRIBIR EN EL NUEVO LOG: " + str(e))

def Images_Logger(image, userid, event):
    try:
        if DEBUG:
            dt_string = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            today = (dt_string[:-3]).replace(':','_')
            #today = date.today()
            if log_image_to_file:
                if not os.path.exists(IMAGES_LOG_PATH):
                    os.makedirs(IMAGES_LOG_PATH)

                image_name = event + '_' + userid + '_' + str(today)
                cv2.imwrite(IMAGES_LOG_PATH + image_name + '.jpg', image)
            else:
                print(dt_string[:-3] + ':', str(text))
    except Exception as e:
        print("ERROR AL INTENTAR GUARDAR LA IMAGEN EN EL DIRECTORIO DE IMAGES_LOG: " + str(e))

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225:
#      -Created initial file.
#
# Feb-19-2021 Leobardo N Hernandez
#   + DBL_226
#      - Created function Images_Logger to save images for debugging purposes.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_230
#      - Updated Images_Logger.
#
# Mar-09-2022 Arturo Gaona
#   + DBL_324
#      - Fix too many files opened issue, update to system log.
#
#########################################################################################