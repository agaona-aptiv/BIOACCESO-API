'''
Created on March, 2021
@author: Leobardo N Hernandez
'''
#########################################################################################
#  COPYRIGHT 2021
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: Throughput
#          Description: Script for saving performance
#          Enterprise: Condumex
#          SW Developer: Leobardo N Hernandez
#          
#          File: EDT_Thruput.py
#          Feature: Throughput
#          Design:  NA
#          Deviations: **Por aclarar con Calidad
#########################################################################################
import os
from io import open
from inspect import currentframe
from datetime import date
from datetime import datetime as dt
import cv2
import configparser
from Config_Test.EDT_Debug import EDT_Logger

DEBUG = True
log_to_file = True

statistic_line = 0

LOGS_PATH = '/home/edt/Documents/Share/_Logs/'

IDENTIFICATION_THRUPUT = 'thr_id'
ALTERNATIVE_THRUPUT = 'thr_alt'
TEMPERATURE_THRUPUT = 'thr_temp'
MASK_THRUPUT = 'thr_mask'
EVALUATION_THRUPUT = 'thr_eval'
TOTAL_THRUPUT = 'thr_total'

THRUPUT_INIT = 'init_time'
THRUPUT_END =  'end_time'
THRUPUT = 'thr_time'

# This dictionary is used to save the thruput statistics
EdtThruput = {
IDENTIFICATION_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0},
ALTERNATIVE_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0},
TEMPERATURE_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0},
MASK_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0},
EVALUATION_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0},
TOTAL_THRUPUT : {THRUPUT_INIT : 0, THRUPUT_END : 0, THRUPUT : 0}
}

def Thruput_Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('thruput', debug_line, text)

def Set_Thruput_Time(edt_state, event, thr_time):
    global EdtThruput
    global statistic_line

    try:
        if DEBUG:
            EdtThruput[edt_state][event] = thr_time
        pass
    except Exception as e:
        Thruput_Logger('ERROR AL INTENTAR ALMACENAR TIEMPO PARA CALCULO DE THRUPUT: ' + str(e))

def Save_Thruput():
    global EdtThruput
    global statistic_line

    try:
        if DEBUG:
            today = date.today()
            thruput_file = LOGS_PATH + 'bioaccesso_perf_' + str(today) + '.log'

            if log_to_file:
                # Create the folder to store statistics log in case it does not exist
                if not os.path.exists(LOGS_PATH):
                    os.makedirs(LOGS_PATH)

                if not os.path.exists(thruput_file):
                    file = open(thruput_file, 'a+')
                    file.write('***** BIOACCESO - HISTORIAL DE RENDIMIENTO DEL DISPOSITIVO *****\n')
                    file.write('Fecha: ' + str(today) + '\n')
                    file.close()

                for key in EdtThruput:
                    EdtThruput[key][THRUPUT] = EdtThruput[key][THRUPUT_END] - EdtThruput[key][THRUPUT_INIT]

                rec_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                file = open(thruput_file, 'a+')
                file.write('TIEMPO TOTAL DE IDENTIFICACI0N: ' + str(EdtThruput[TOTAL_THRUPUT][THRUPUT]) + 's - (' + rec_time[:-3] + ')\n')
                file.write('\t- TIEMPO IDENTIFICANDO: ' + str(EdtThruput[IDENTIFICATION_THRUPUT][THRUPUT]) + 's\n')
                file.write('\t- TIEMPO IDENTIFICANDO METODO ALTERNO: ' + str(EdtThruput[ALTERNATIVE_THRUPUT][THRUPUT]) + 's\n')
                file.write('\t- TIEMPO TOMA DE TEMPERATURA: ' + str(EdtThruput[TEMPERATURE_THRUPUT][THRUPUT]) + 's\n')
                file.write('\t- TIEMPO DETECCION MASCARA: ' + str(EdtThruput[MASK_THRUPUT][THRUPUT]) + 's\n')
                file.write('\t- TIEMPO EVALUACION: ' + str(EdtThruput[EVALUATION_THRUPUT][THRUPUT]) + 's\n\n')
                file.close()

            else:
                print("THRUPUT DISABLED")

            Reset_Thruput()

    except Exception as e:
        Thruput_Logger('ERROR AL INTENTAR GUARDAR LA INFORMACION DEL THRUPUT: ' + str(e))

def Reset_Thruput():
    global EdtThruput

    try:
        # Set thruput variables to default value
        for key in EdtThruput:
            EdtThruput[key][THRUPUT_INIT] = 0
            EdtThruput[key][THRUPUT_END] = 0
            EdtThruput[key][THRUPUT] = 0
    except Exception as e:
        Thruput_Logger('ERROR AL INTENTAR REINICIALIZAR LA INFORMACION DEL THRUPUT: ' + str(e))

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_230
#      -Created initial file.
#
#########################################################################################