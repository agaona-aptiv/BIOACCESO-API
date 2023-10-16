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
#          Module: HMI
#          Description: This script provides control of HMI.
#          Enterprise: Condumex
#          SW Developer: Ernesto Ulises Beltran
#
#          File: EDT_HMI_cfg.py
#          Feature: HMI
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################

import uuid
import sys
import os
import cv2
from enum import Enum

# Add to path modules located in different folders
sys.path.append(os.getcwd())
# modules_list = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, f))]
# modules_list = [os.path.join(cwd, f) for f in modules_list if f.startswith('mod_')]
# sys.path.append(modules_list)
# print('----- sys.path start -----')
# print(sys.path)
# print('------ sys.path end ------')

################################################################################
# Start definition of constants from here
################################################################################

# General definitions
DEBUG = True
DEFAULT_USERID = '0000_0000'
MAC = str(hex(uuid.getnode()))
DEVICE_ID = MAC.upper().replace('0X', '')
width=640
height=480
flip=4

class BOX_COLOR(Enum):
    GREEN = "green"
    RED = "red"
    BLUE = "blue"

class HMI_MESSAGES(Enum):
    ACCESO_AUTORIZADO = 1
    ACCESO_NEGADO_COLOCAR_CUBREBOCAS = 2
    ACUDIR_SERVICIO_MEDICO = 3
    REMOVE_MASK = 4
    PUT_MASK = 5
    ACCESO_NEGADO_CONTACTAR_RH = 6
    NO_RECONOCIDO_CENTRAR_ROSTRO = 7
    ACERCAR_ROSTRO_PARA_TEMPERATURA = 8
    ACCESO_NEGADO_PASAR_VIGILANCIA = 9
    ERROR_LECTURA_PASAR_VIGILANCIA = 10
    ACERCAR_A_ZONA_DE_ID = 11
    IDENTIFICANDO = 12
    IDENTIFICANDO_METODO_ALTERNO = 13    #DBL_186

#wbmode = white balance mode 
#tnr-mode = temporal noise reduction mode
#tnr-strength = level [-1,1]
#ee-mode = 2
#tnr-strength=1
#videobalance contrast=1.5 brightness=-.3 saturation=1.2
pipeSensor    = 'nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode = 2 tnr-strength=1 sensor-id=0 !video/x-raw(memory:NVMM), width=640, height=480, framerate=21/1, '
pipeConverter = 'format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width) +', height='+str(height)+', '
pipeformat    = 'format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 !appsink'
VIDEO_INPUT_DEVICE = pipeSensor + pipeConverter + pipeformat
#VIDEO_INPUT_DEVICE = 0  #'IMG_3658_small.mov' #'/home/edt/Code/VideoExample.mp4'
                        #0 
                        #'VideoExample.mp4'  
                        #Camera number, rtsp string format, or video path file gstreame format

# Algorithm definitions
CASCADE_FILE_PATH = './cascades/data/haarcascade_frontalface_alt2.xml'
DATA_FACE_PATH = 'UserFaceIDs'
FACE_MIN_HEIGHT = 144  # 144            #85 centimeters from Camera with 640*480
FACE_MIN_WIDTH = 144  # 144         #85 centimeters from Camera with 640*480

# Display definitions
CAMERA_WIDTH_RESOLUTION = 320  # 640
CAMERA_HEIGHT_RESOLUTION = 240  # 480
FONT = cv2.FONT_HERSHEY_SIMPLEX #cv2.FONT_HERSHEY_DUPLEX # ImageFont.truetype("calibrii.ttf", 80)
FONT_SCALE = 0.5
LINE_THICKNESS = 2
TRAIN_EXT = 'jpg'
WINDOWS_TITLE = 'EDT Access CTRL CIDEC Ver 1.0'

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
# Oct-30-2020 Cinthia Valdez / Jonatan Uresti
#   DBL_54:
#       - Redisign of Access Control
#       - Includes DBL_13, DBL_23, DBL_75, DBL_83, DBL_84, DBL_86, DBL_89, DBL_91,
#          DBL_92, DBL_102*, DBL_103, DBL_104, DBL_107
#13-11-2020 Lucia Chavez
#      -Change thicknes 
#
# Jan-04-2021 Leobardo N Hernandez
#   + DBL_186
#      - Added IDENTIFICANDO_METODO_ALTERNO to HMI_MESSAGES.
#
#########################################################################################