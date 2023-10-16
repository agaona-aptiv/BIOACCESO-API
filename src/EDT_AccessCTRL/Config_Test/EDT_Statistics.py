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
#          Module: Statistics
#          Description: Script for saving statistics logs
#          Enterprise: Condumex
#          SW Developer: Leobardo N Hernandez
#          
#          File: EDT_Statistics.py
#          Feature: Statistics
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
from enum import Enum
from Config_Test.EDT_Debug import EDT_Logger

DEBUG = True
log_to_file = True

statistic_line = 0

LOGS_PATH = '/home/edt/Documents/Share/_Logs/'
# STATISTICS
class EDT_STATISTIC(Enum):
    ID_ATTEMPT = 0
    COMPLETED_ID = 1
    SUCCESSFUL_ID = 2
    ALTERNATIVE_ID = 3
    UNSUCCESSFUL_ID = 4
    ABORTED_ID = 5

TOTAL_ID_ATTEMPTS = 'Total Intentos de Identificacion'
COMPLETED_EVAL = 'Evaluaciones Completadas'
SUCCESSFUL_IDENT = 'Identificaciones'
ALTERNATIVE_IDENT = 'Identificaciones Metodo Alterno'
UNSUCCESSFUL_IDENT = 'Identificaciones No Exitosas'
ABORTED_IDENT = 'Identificaciones Abortadas'

def Statistics_Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('stats', debug_line, text)

def Update_Statistics(stat, userId):
    global statistic_line

    try:
        if DEBUG:
            today = date.today()
            statistics_file = LOGS_PATH + 'bioaccesso_stats_' + str(today) + '.log'

            if log_to_file:
                # Create the folder to store statistics log in case it does not exist
                if not os.path.exists(LOGS_PATH):
                    os.makedirs(LOGS_PATH)
        
                # Create the statistics log file in case it does not exist
                if not os.path.exists(statistics_file):
                    if EDT_STATISTIC.COMPLETED_ID != stat:
                        attempts = 1
                        completed_eval = 0
                        if EDT_STATISTIC.SUCCESSFUL_ID == stat:
                            successful_id = 1
                            id_event = 'IDENTIFICATION EXITOSA (' + str(userId) + ')'
                        elif EDT_STATISTIC.ALTERNATIVE_ID == stat:
                            alternative_id = 1
                            id_event = 'IDENTIFICATION METODO ALTERNATO (' + str(userId) + ')'
                        elif EDT_STATISTIC.UNSUCCESSFUL_ID == stat:
                            unsuccessful_id = 1
                            id_event = 'IDENTIFICATION NO EXITOSA'
                        elif EDT_STATISTIC.ABORTED_ID == stat:
                            aborted_id = 1
                            id_event = 'IDENTIFICATION ABORTADA'
                        else:
                            successful_id = 0
                            alternative_id = 0
                            unsuccessful_id = 0
                            aborted_id = 0


                        file = open(statistics_file, 'a+')
                        file.write('*************** ESTADISTICAS BIOACCESO - ' + str(today) + ' ***************\n\n')
                        file.write('- ' + TOTAL_ID_ATTEMPTS + ' = ' + str(attempts) + '\n')
                        file.write('- ' + COMPLETED_EVAL + ' = ' + str(completed_eval) + '\n')
                        file.write('- ' + SUCCESSFUL_IDENT + ' = ' + str(successful_id) + '\n')
                        file.write('- ' + ALTERNATIVE_IDENT + ' = ' + str(alternative_id) + '\n')
                        file.write('- ' + UNSUCCESSFUL_IDENT + ' = ' + str(unsuccessful_id) + '\n')
                        file.write('- ' + ABORTED_IDENT + ' = ' + str(aborted_id) + '\n\n')
                        file.write('******************** DETALLE DE ESTADISTICAS **********************\n')

                        if successful_id == 1 or alternative_id == 1 or unsuccessful_id == 1:
                            statistic_line = 1
                            dt_string = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                            stat_number = '{:0>6}'.format(statistic_line)
                            record = 'Id ' + str(stat_number) + ' = ' + dt_string[:-3] + ' ' + str(id_event)
                            file.write(record)
                        file.close()
                else:
                    # Statistics file already exists, update it.
                    row_stat = 0
                    col_data = 0
                    if EDT_STATISTIC.ID_ATTEMPT == stat:
                        row_stat = 2
                        col_data = 6
                    elif EDT_STATISTIC.COMPLETED_ID == stat:
                        row_stat = 3
                        col_data = 4
                    elif EDT_STATISTIC.SUCCESSFUL_ID == stat:
                        row_stat = 4
                        col_data = 3
                        id_event = 'IDENTIFICATION EXITOSA (' + str(userId) + ')\n'
                    elif EDT_STATISTIC.ALTERNATIVE_ID == stat:
                        row_stat = 5
                        col_data = 5
                        id_event = 'IDENTIFICATION METODO ALTERNATO (' + str(userId) + ')\n'
                    elif EDT_STATISTIC.UNSUCCESSFUL_ID == stat:
                        row_stat = 6
                        col_data = 5
                        id_event = 'IDENTIFICATION NO EXITOSA\n'
                    elif EDT_STATISTIC.ABORTED_ID == stat:
                        row_stat = 7
                        col_data = 4
                        id_event = 'IDENTIFICATION NO EXITOSA\n'
                    else:
                        pass

                    #Statistics_Logger('ROW: ' + str(row_stat) + ' - COL_DATA: ' + str(col_data))
                    if row_stat != 0 and row_stat != 0:
                        total_lines = 1
                        current_stats = list()
                        with open(statistics_file,'r+') as stats_file:
                            current_stats = stats_file.readlines()
                            total_lines = len(current_stats)
                            
                            stat_to_be_updated = current_stats[row_stat].split(' ')
                            stat_to_be_updated[col_data] = str(int(stat_to_be_updated[col_data].replace('\n','')) + 1)
                            current_stats[row_stat] = ' '.join(stat_to_be_updated) + '\n'
                        with open(statistics_file,'w') as stats_file:
                            stats_file.writelines(current_stats)

                        if row_stat == 4 or row_stat == 5 or row_stat == 6:
                            statistic_line = (total_lines - 9) + 1
                            dt_string = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                            stat_number = '{:0>6}'.format(statistic_line)
                            record = 'Id ' + str(stat_number) + ' = ' + dt_string[:-3] + ' ' + str(id_event)
                            file = open(statistics_file, 'a+')
                            file.write(record)
                            file.close()
    except Exception as e:
        Statistics_Logger('ERROR AL ACTUALIZAR LAS ESTADISTICAS DE BIOACCESO: ' + str(e))

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_230
#      -Created initial file.
#
# Mar-26-2021 Lucia B Chavez
#   + DBL_247
#      -Added event for ABORTED_ID.
#
#########################################################################################