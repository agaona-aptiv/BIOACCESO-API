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
#          Module: EDT_AccessCTRL
#          Program: Configuration file for Access CTRL module
#          Enterprise: Condumex
#          SW Developer: Jonatan Uresti
#          FILE DESCRIPTION
#          File: EDT_AccessCTRL_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################

import uuid
import sys
import os
import cv2
#import gi
#gi.require_version('Gst', '1.0')
#from gi.repository import Gst

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
UNKNOWN_USER_ID = '0000'
MAC = str(hex(uuid.getnode()))
DEVICE_ID = MAC.upper().replace('0X', '')
USER_ID = "user_id"
MONITOR_ID = "monitor_id"
NAME = "name"
LAST_NAME = "last_name"
TEMPERATURE = "temperature"
MASK_STATUS = "mask_status"
BOX_POSITION = "box_position"
BOX_COLOR = "box_color"
AUTHORIZED = "authorized"

# Camera definitions
IN_WIDTH=864 #1280
IN_HEIGHT=486 #720
OUT_WIDTH=864 #640
OUT_HEIGHT=486 #360
FRAMERATE=21
#FLIP_METHOD = 4  #Beta1
FLIP_METHOD= 6 #Beta2
#wbmode = white balance mode 
#tnr-mode = temporal noise reduction mode
#tnr-strength = level [-1,1]
#ee-mode = 2
#tnr-strength=1
#videobalance contrast=1.5 brightness=-.3 saturation=1.2

#Gst.debug_set_active(True)
#Gst.debug_set_default_threshold(3)
#wbmode=1 sensor-id=0 tnr-mode=2 ee-mode=2 aeantibanding=1
#VIDEO_INPUT_DEVICE = 'nvarguscamerasrc wbmode=1 sensor-id=0 tnr-mode=2 ee-mode=2 aeantibanding=1 !' \
#                     ' video/x-raw(memory:NVMM), framerate=21/1, width=1280, height=720, format=NV12 !' \
#                     ' nvvidconv flip-method=2 ! video/x-raw, width=400, height=240, format=BGRx !' \
#                     ' videoconvert ! video/x-raw, format=BGR ! appsink'
#VIDEO_INPUT_DEVICE = 0 #'IMG_3658_small.mov' #'/home/edt/Code/VideoExample.mp4"
                        #0 
                        #'VideoExample.mp4'  
                        #Camera number, rtsp string format, or video path file gstreame format

# Algorithm definitions
CASCADE_FILE_PATH = './cascades/data/haarcascade_frontalface_alt2.xml'
DATA_FACE_PATH = 'UserFaceIDs'
MODEL_FILE_PATH = 'UserFaceIDs.pkl'
FACE_MIN_HEIGHT_FACTOR = 1 / 3
FACE_MIN_WIDTH_FACTOR = 3 / 16

# Display definitions
CAMERA_WIDTH_RESOLUTION = 640  # 640
CAMERA_HEIGHT_RESOLUTION = 480  # 480
FONT = cv2.FONT_HERSHEY_SIMPLEX #cv2.FONT_HERSHEY_DUPLEX # ImageFont.truetype("calibrii.ttf", 80)
FONT_SCALE = 0.7
LINE_THICKNESS = 3
TRAIN_EXT = ['jpg']
WINDOWS_TITLE = 'EDT Access CTRL CIDEC Ver 1.0'

# Users DB definitions
USERS_DB_PATH = os.getcwd() + '/Users_Database/'
USERS_DB_NAME = 'Users_Database'

######################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
#
# Date          userid          Description                                
# 29-Sep-2020   xznmw9_Agaona}
#   - Initial version
#   - Line 70 Provide capabiliti to configure webcam
#                                       
# Oct-15-2020 Ernesto Ulises Beltran
#   + DBL_93:
#      -Updated data flow for hmi.
#
# Oct-21-2020 Pablo Mejia
#   + DBL_97:
#      -Add Users DB definitions
#
# Oct-30-2020 Cinthia Valdez / Jonatan Uresti
#   DBL_54:
#       - Redisign of Access Control
#       - Includes DBL_13, DBL_23, DBL_75, DBL_83, DBL_84, DBL_86, DBL_89, DBL_91,
#          DBL_92, DBL_102*, DBL_103, DBL_104, DBL_107
#
#########################################################################################
