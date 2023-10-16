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
#          Module: ST_FaceID
#          Program: Configuration file for Face ID module
#          Enterprise: Condumex
#          SW Developer: Arturo Gaona
#          FILE DESCRIPTION
#          File: ST_FaceID_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################
import os

_debugTest = False
FACE_RECOG_TOLERANCE_MASK = 0.43	#Face Recognition Tolerance with face mask     DBL_9, DBL_21, DBL_12, DBL_165
FACE_RECOG_TOLERANCE_NO_MASK = 0.43	#Face Recognition Tolerance with no face mask  DBL_9, DBL_21, DBL_12, DBL_165
UNKNOWN_USERID = '12636_12636'
FACE_IMAGE_FORMAT = ['jpg']

#DEPTH Methods   DBL_241
MIN_DISPARITY = 50		#M in disparity
BASE_DISTANCE = 6 		# Distance between cameras 6 cm
TEST_POINT = 65 		# Distance cm of the mark position to camera calibration
CURRENT_MEASURE = 37.1 # Distance cm displayed on Initial while the face is on test point		
FOCAL_PIXEL_FACTOR = TEST_POINT/CURRENT_MEASURE  # Calibration Factor 
FOCAL_PIXEL = FOCAL_PIXEL_FACTOR*432.454   #(640 * 0.5)/np.tan(alpha *0.5 * np.pi/180)

#>>>>>>  DBL_262  Facemask training
FACEMASKMODEL1 = os.path.dirname(__file__) + "/Models/KN95-Medical-Face-Masks-5.png"
FACEMASKMODEL2 = os.path.dirname(__file__) + "/Models/FaceMaskblue.png"
FACEMASKMODEL3 = os.path.dirname(__file__) + "/Models/FaceMaskBlack.png"
FACEMASK_PREDICTOR = os.path.dirname(__file__) + "/Models/shape_predictor_68_face_landmarks.dat"
#<<<<<<<


#MODEL String TAGS
MASK_MODEL = os.path.dirname(__file__) + '/Models/mask_recog_ver8.h5'              
CASCADE_MODEL = os.path.dirname(__file__) + '/Models/haarcascade_frontalface_alt6.xml'
CASCADE_PROFILE_MODEL = os.path.dirname(__file__) + "/Models/haarcascade_profileface.xml"
CASCADE_LEYE_MODEL = os.path.dirname(__file__) + "/Models/haarcascade_lefteye_2splits.xml"  
CASCADE_REYE_MODEL = os.path.dirname(__file__) + "/Models/haarcascade_righteye_2splits.xml"

NO_MODEL_EXCEPTION = 'Mask Model NOT found: '
MODEL_FACE_LIST = 'faceIDList'
MODEL_FACE_ENCODE_LIST = 'faceEncodeList'


#Exceptions string TAGS
SINGLETONE_MODEL_EXCEPTION = 'This class is a singleton!'

#General status string TAGS
GENERAL_RESULT_STATUS = 'status'
GENERAL_RESULT_COMMNENT = 'comment'
GENERAL_RESULT_EXCEPTION = 'Exception: '
GENERAL_RESULT_USER_ID = 'sap_number' #@TODO: change to string user_id when correct implementation is done in REST server
GENERAL_RESULT_HUB_PATH = 'HUB_photo_path'

# Objects to Train Keys
KEY_HUB_PHOTO_PATH = 'HUB_photo_path'

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# 26-Aug-2020   Arturo Gaona
#   + First release of the design implementation  
#
# 20-Sep-2020   Arturo Gaona
#    -Include capability to train images from url
#    -Implement solution for issues: 
#        * DBL_9, DBL_12,DBL_21
#
# Sep-25-2020 Pablo Mejia
#   + DBL_43
#      - Created initial file.
#      - Adapt POST & PATCH to work with current ST_FACE_ID
#
# Oct-30-2020 Arturo Gaona
#   DBL_113:
#       - Added models for face detection
# Dic-01-2020 Arturo Gaona
#   DBL_162:
#       - model Updated mask_recog_ver7.h5
#
# Dic-01-2020 Arturo Gaona
#   DBL_164:
#       - Model Updated to mask_recog_ver7.h5
#
# Dic-02-2020 Arturo Gaona
#   DBL_165:
#       - Update Tolerance
#
# Dic-15-2020 Arturo Gaona
#   DBL_178:
#       - Update Model to recognize facemask vs beard
# Apr-08-2021 Arturo Gaona
#   DBL_238:
#       - Update Model to recognize white facemask
#
# Mar-31-2021 Pablo Mejia
#   DBL_243:
#       - Add KEY_HUB_PHOTO_PATH.
#       - Add GENERAL_RESULT_HUB_PATH.
#
# 09-Apr-2021   Arturo Gaona    Change  Remove Virtual facemask
#                                   * # DBL_252 Remove Virtual FaceID
#
# Mar-24-2021 Arturo Gaona
#   DBL_241:
#       - Implement methods for distance and depth
#
# 30-Apr-2021 Arturo Gaona      Implement methods for distance and depth on Initial Test
#                                   * DBL_257: Implemented on Initial Test
#
# 25-May-2021 Arturo Gaona
#   DBL_262:
#       - Added models for virtual facemask process
#
#########################################################################################