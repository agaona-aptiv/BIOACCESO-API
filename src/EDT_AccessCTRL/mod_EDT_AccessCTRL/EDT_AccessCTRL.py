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
#          Module: EDT_AccessCTRL
#          Description: Main script for Access Control
#          Enterprise: Condumex
#          SW Developer: Jonatan Uresti
#          
#          File: EDT_ImageProcess.py
#          Feature: EDT_AccessCTRL
#          Design:  Diagrama_Secuencia_EDT_AccessCTRL_v1.pptx
#          Deviations: **Por aclarar con Calidad
#########################################################################################

# All imported modules must be added after config file
# Avoid use of 'cfg' as alias because all modules contain a config file


import mod_EDT_AccessCTRL.EDT_AccessCTRL_cfg as ac_cfg         #import EDT_AccessCTRL_cfg as ac_cfg
import mod_Temperature.ST_Temperature_cfg as temp_cfg         #import ST_Temperature_cfg as temp_cfg 

import os
import time
import shelve
import numpy as np
import tkinter as tk
import math

from os import path
from datetime import datetime as dt
from datetime import timedelta as tdelta 
from inspect import currentframe
from mod_FaceID.ST_FaceID import *
import mod_GPIOInterfaces.ST_GPIOInterfaces as gpioDriver
from POST_Test.POST_Service import *
from mod_Temperature.ST_Temperature import *
from main_HMI.EDT_HMI_cfg import BOX_COLOR as HMI_BOX_COLOR
from main_HMI.EDT_HMI_cfg import HMI_MESSAGES
from random import *

from Config_Test.EDT_Debug import EDT_Logger, Images_Logger
#root = tk.Tk()
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()
#SCREEN_SIZE = (screen_width,screen_height) #1024 * 600

def Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('edt', debug_line, text)

def TLogger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('temperature', debug_line, text)

def Save_User_Suspicious_Temp_Image(image, user, event):
    Images_Logger(image,user,event)


class EDT_AccessCTRL:
    def __init__(self):
        # Frame related variables
        self._frame = None
        #@todo: should these values be in cfg?
        self._widthResolution = 640
        self._heightResolution = 480
        self._widthCentre = self._widthResolution / 2
        self._heightCentre = self._heightResolution / 2
        self._detMinSize = 95  # Min size of face in pixels at 1.5m
        self._roi1MinSize = 160  # Min size of face in pixels at 0.85m
        self._roi1MaxSize = 360  # Max size of face in pixels at 0.85m
        self._roi2MinSize = 360  # Min size of face in pixels at 0.35m
        self._tolerance = fid_cfg.FACE_RECOG_TOLERANCE_NO_MASK
        self._knownUserMaskAccuracy = 85.0
        self._unknownUserMaskAccuracy = 40.0 #@TODO: Check correct value to remove mask
        self._maxDistFromUser = 25  # Max distance in pixels to move between frames
        self._xEyeFactor = 1.7
        self._wEyeFactor = 3.2
        self._hEyeFactor = 4
        self._tempUpperLimit = 40
        self._tempFeverLimit = 37.5
        self._tempLowerLimit = 35
        self._faceIdSize = 224
        #End @TODO

        '''
        [FSM Redesign]
        '''
        # Instead of considering a face is in ROI2 when it is outside ROI1, make ROI2 wider
        # and use the distance to classify it
        self._roiWidth = 400                     
        self._roiLeftLimit = self._widthCentre - self._roiWidth / 2
        self._roiRigthLimit = self._widthCentre + self._roiWidth / 2
        '''
        [FSM Redesign] end
        '''

        # EDT modules variables
        self._faces = []
        self._highlightFace = []
        self._facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        self._faceProfileCascade = cv2.CascadeClassifier(fid_cfg.CASCADE_PROFILE_MODEL)
        self._eyeCascadeL = cv2.CascadeClassifier(fid_cfg.CASCADE_LEYE_MODEL)
        self._eyeCascadeR = cv2.CascadeClassifier(fid_cfg.CASCADE_REYE_MODEL)
        self._faceIdentification = ST_FaceID.getInstance()
        self._temperatureDevice = ST_Temperature.getInstance()
        self._externalDevices = gpioDriver.ST_ExternalDevices.getInstance()
        self._temperatureDevice.Connect()
        self._externalDevices.Connect_External_Devices()
        PostProcessHandler.Init()
        Logger('Loading faceIdentification model from: ' + ac_cfg.DATA_FACE_PATH)
        train_res = self._faceIdentification.Train(ac_cfg.DATA_FACE_PATH,ac_cfg.MODEL_FILE_PATH, ac_cfg.TRAIN_EXT)
        Logger('type:' + str(type(train_res)) + str(train_res))
        self._updateModelTS = dt.now()
        self._modelFileTS = os.path.getmtime(ac_cfg.MODEL_FILE_PATH)

        # Timestamps Limits in seconds
        self._updateModelTSLimit = 5 # @TODO: Check correct time to verify model file

        self.ResetValues()

    def Shutdown(self):
        PostProcessHandler.Shutdown()
        self._temperatureDevice.Disconnect()
        self._externalDevices.Disconnect_External_Devices()
        Logger('EDT_AccessCTRL Shutdown')

    def ResetValues(self):
        # Main flags
        Logger("Reset Values")
        self._knownUserFlag = False
        self._maskOnFlag = False
        self._temperatureFlag = False

        # User Info
        self._temperature = 0.0
        self._messages = None
        self._userInfo = {ac_cfg.USER_ID: None,
                          ac_cfg.MONITOR_ID: None,
                          ac_cfg.NAME: None,
                          ac_cfg.LAST_NAME: None,
                          ac_cfg.TEMPERATURE: 0.0,
                          ac_cfg.MASK_STATUS: None,
                          ac_cfg.BOX_POSITION: None,
                          ac_cfg.BOX_COLOR: None,
                          ac_cfg.AUTHORIZED: None}
        self._userIndex = -1

        # Response to POST_Service
        self._dataToSend = {'userID': None,
                            'monitorID': None,
                            'userType': None,
                            'temp': None,
                            'mask': None,
                            'authorizedAccess': None}

    def CreateResponseToHMI(self):
        # Fill response to HMI
        userAccStatus = False
        hmi_user_info = None
        if self._userInfo[ac_cfg.AUTHORIZED] is not None and self._userInfo[ac_cfg.USER_ID] is not None:
            # @TODO: Remove when POST, HMI and Access Control keys are standard
            userAccStatus = True
            hmi_user_info = {'aut': self._userInfo[ac_cfg.AUTHORIZED],
                             ac_cfg.NAME: self._userInfo[ac_cfg.NAME],
                             ac_cfg.LAST_NAME: self._userInfo[ac_cfg.LAST_NAME],
                             'usrID': self._userInfo[ac_cfg.USER_ID],
                             'monID': self._userInfo[ac_cfg.MONITOR_ID],
                             'temp': self._userInfo[ac_cfg.TEMPERATURE],
                             'mask': self._userInfo[ac_cfg.MASK_STATUS]}
            Logger(str(hmi_user_info))
            Logger("faces: " + str(self._faces))
            Logger("user_info[BOX_POSITION]: " + str(self._userInfo[ac_cfg.BOX_POSITION]))
        message = self._messages.value if self._messages is not None else None
        return self._faces, userAccStatus, hmi_user_info, message

    def HasFacesToDetect(self):
        return len(self._faces) > 0

    def HasFaceToIdentify(self):
        #DBL_Inprove_Recognition_Speed
        result = False
        if self._userInfo[ac_cfg.BOX_POSITION] is not None:
            distance = 80.0 - 0.35294*(self._userInfo[ac_cfg.BOX_POSITION][3]-170)
            if (distance > 35 and distance < 85):
                result = True
        return result

    def GetFaces(self, frame):
        self._frame = frame
        self._faces = []
        self._highlightFace = []
        self._userIndex = -1
        self._userInfo[ac_cfg.BOX_POSITION] = None
        if self._frame is not None:
            frameContrast = self._faceIdentification.Contrast(self._frame)  #DBL_251
            frameGray = cv2.cvtColor(frameContrast, cv2.COLOR_BGR2GRAY)     #DBL_251
            faces = self._facecascade.detectMultiScale(frameGray, scaleFactor=1.07,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
            if len(faces)==0:
                faces = self._faceProfileCascade.detectMultiScale(frameGray,scaleFactor=1.07,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
            if (len(faces)==0):
                leftEyes = self._eyeCascadeL.detectMultiScale(frameGray,scaleFactor=1.07,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
                rightEyes = self._eyeCascadeR.detectMultiScale(frameGray,scaleFactor=1.07,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
                if (len(leftEyes)==1 and len(rightEyes) == 1):
                    faces = []
                    for (x, y, w, h) in leftEyes:
                        x = int(x -self._xEyeFactor * w)
                        if (x < 0):
                            x = 0
                        y = y - h
                        if (y < 0):
                            y = 0
                        w = int(w * self._wEyeFactor)
                        if w > self._widthResolution:
                            w = self._widthResolution
                        h = h * self._hEyeFactor
                        if h > self._heightResolution:
                            w = self._heightResolution
                        face = (x, y, w, h)
                        faces.append(face)

            if len(faces) > 0:
                self.ClassifyFaces(faces)
        # Logger("Found {0} faces".format(len(faces)))
         
    def ClassifyFaces(self, faces):
        '''
        Faces will be added to a list as long as they are at a distance less than or equal 
        to the detection distance.
         
        This function analyzes the detected faces and selects a face to be identified based on the following criteria:
           - It must be within the identification region.
           - It should be the closest to the device.
        The selected face will be added at the end of the list.
        '''
   
        # minDistance = 9999
        for (x, y, w, h) in faces:
            # @TODO: restrict blue rectangles when face is in identification area according to systems feedback
            if w > self._detMinSize:   # @TODO: Change to distance less than 150 cm
                self._faces.append([x, y, w, h, HMI_BOX_COLOR.BLUE])
            else:
                # Do nothing
                pass

        maxWidth = 0
        userIndex = -1
        currentIndex = 0
        for (x, y, w, h, c) in self._faces:
            if x > self._roiLeftLimit and (x + w) < self._roiRigthLimit:
                if w > self._roi1MaxSize:   # TODO: Change to distance less than 35 cm
                    # If there is a face inside identification region at this distance, 
                    # there is no way another face exists within.
                    maxWidth = w
                    userIndex = currentIndex
                elif w > self._roi1MinSize:   # TODO: Change to distance less than 85 cm
                    if w > maxWidth:   # TODO: Change to distance less than minDistance
                        # The new face is the first one to meet this criteria (selectedFaceValues will be empty)
                        # or is closer so is the new candidate to be used in the identification process.
                        maxWidth = w
                        userIndex = currentIndex
                    else:
                        #Do nothing
                        pass
                else:
                    # Do nothing
                    pass
            else:
                # Face out of identification area
                # Do nothing
                pass

            currentIndex += 1

        if userIndex > -1:
            self._userIndex = userIndex
            self._userInfo[ac_cfg.BOX_POSITION] = [self._faces[userIndex][0], self._faces[userIndex][1], 
                                                   self._faces[userIndex][2], self._faces[userIndex][3]]
            self._highlightFace.append([self._faces[userIndex][0], self._faces[userIndex][1],
                                        self._faces[userIndex][2], self._faces[userIndex][3], self._faces[userIndex][4]])


    def GetUserKnown(self):
        #return self._userInfo[ac_cfg.USER_ID] is not None
        return self._knownUserFlag

    #DBL_323_PostServiceProcess improve resize procedure
    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def IdentifyUser(self):
        userID = ac_cfg.UNKNOWN_USER_ID
        if self._userInfo[ac_cfg.BOX_POSITION] is not None:
            x = self._userInfo[ac_cfg.BOX_POSITION][0]
            y = self._userInfo[ac_cfg.BOX_POSITION][1]
            w = self._userInfo[ac_cfg.BOX_POSITION][2]
            h = self._userInfo[ac_cfg.BOX_POSITION][3]
            face = self._frame[y:y+h, x:x+w]
            #face = cv2.resize(face, (self._faceIdSize, self._faceIdSize))
            face = self.image_resize(face, self._faceIdSize)  #DBL_323_PostServiceProcess improve resize procedure
            
            #face_encoding = face_recognition.face_encodings(face, [(0, self._faceIdSize, self._faceIdSize,0)])
            face_encoding = face_recognition.face_encodings(face) #DBL_323_PostServicess
            #DBL_Inprove_Recognition_Speed  Avoid to get distance when is not used
            #TLogger("IdentifyUser. self._userInfo[ac_cfg.BOX_POSITION]: "+ str(self._userInfo[ac_cfg.BOX_POSITION]))          #DBL_Add_Distance_Measure            
            #dis = 80-0.35294(h-170)
            #distance = 80.0 - 0.35294*(self._userInfo[ac_cfg.BOX_POSITION][3]-170)
            #if (distance<40.0):
            #    distance=40
            #if (distance>85):
            #    distance=85
            #TLogger("distance: "+ str(distance))          #DBL_Add_Distance_Measure

            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]
                result = self._faceIdentification.IdentifyFace(face_encoding, str(ac_cfg.UNKNOWN_USER_ID), tolerance=self._tolerance)
                userID = result['faceID']
                if userID != ac_cfg.UNKNOWN_USER_ID:
                    print("userID: " + str(userID))
                    self._userInfo[ac_cfg.USER_ID] = userID
                    self._knownUserFlag = True #False
                    #self._identificationTS = None   # [FSM Redesign]
                # @TODO: Define if "IDENTIFICANDO" message should be send and when

            else:
                # Do something?
                Logger("face_encodings returned None")
        else:
            #Logger("IdentifyUser - No face position")
            pass
        return userID

    def GetMask(self, mask_accuracy):
        self._maskOnFlag = False
        # localMaskOn = False   # [FSM Redesign]
        if self._userInfo[ac_cfg.BOX_POSITION] is not None:
            #x = self._userInfo[ac_cfg.BOX_POSITION][0]
            #y = self._userInfo[ac_cfg.BOX_POSITION][1]
            #w = self._userInfo[ac_cfg.BOX_POSITION][2]
            #h = self._userInfo[ac_cfg.BOX_POSITION][3]
            #face = self._frame[y:y+h, x:x+w]
            #result = self._faceIdentification.GetMaskStatus(face)
            '''
            [FSM Redesign]
            '''
            #if result['maskStatus'] and result['accuracy'] > mask_accuracy:
            #    print("Mask on!")
            self._userInfo[ac_cfg.MASK_STATUS] = True
            self._maskOnFlag = True
        else:
            #Logger("GetMask - No face position")
            pass
        return self._maskOnFlag

    def GetTemperature(self, user_id_evaluated):
        '''self._temperature = 34.8 + 0.1*(randrange(0, 30, 1))
        self._temperatureFlag = True'''
        '''
        [FSM Redesign]
        '''
        distance = 60
        user_position = temp_cfg.POSICION   #DBL_249 
        user_dimension = temp_cfg.DIMENSION

        if self._userInfo[ac_cfg.BOX_POSITION] is not None:
            user_position = [self._userInfo[ac_cfg.BOX_POSITION][1], self._userInfo[ac_cfg.BOX_POSITION][0]]
            user_dimension = [self._userInfo[ac_cfg.BOX_POSITION][3], self._userInfo[ac_cfg.BOX_POSITION][2]]

            w = self._userInfo[ac_cfg.BOX_POSITION][2]   # @TODO: Change for distance
            if w > self._roi2MinSize:   # @TODO: Change to distance less than or equal to 35 cm
                #self._temperature = 36.0
                self._temperature = self._temperatureDevice.GetObjectTemperature(distance, user_position, user_dimension, user_id_evaluated)   # @TODO: Pass distance to temp function
                self._temperatureFlag = True
                # self._temperatureTS = None   # [FSM Redesign]
            else:
                #temp = 35.0
                temp = self._temperatureDevice.GetObjectTemperature(distance, user_position, user_dimension, user_id_evaluated)   # @TODO: Pass distance to temp function
                self._temperature = temp if temp > self._temperature else self._temperature
        else:   # @TODO: Remove or change for elif distance less than or equal to 35 cm
            # @TODO: Set self._temperatureFlag to True if distance less than or equal to 35????
            #temp = 34.0
            TLogger("Temperature position Defaulf")
            temp = self._temperatureDevice.GetObjectTemperature(distance, user_position, user_dimension, user_id_evaluated)   # @TODO: Pass distance to temp function
            self._temperature = temp if temp > self._temperature else self._temperature
        Logger("temp: " + str(self._temperature))
        Logger("Puse el flag")
        return self._temperatureFlag

    #def EvaluateAccess(self):
    def EvaluateAccess(self, user_id_evaluated):

        self._userInfo[ac_cfg.BOX_COLOR] = HMI_BOX_COLOR.RED.value
        self._userInfo[ac_cfg.AUTHORIZED] = False
        gpioTempStatus = False
        self._temperature = round(self._temperature, 1)
        Logger("Temperature: " + str(self._temperature))
        TLogger("Temperature to HUB: " + str(self._temperature) + "   User ID: " + str(user_id_evaluated))
        # if user was identified:
        #if self._knownUserFlag:
        if user_id_evaluated != ac_cfg.UNKNOWN_USER_ID:
            # if temperature is within min and max limits
            if self._tempLowerLimit < self._temperature < self._tempUpperLimit:
                self._userInfo[ac_cfg.TEMPERATURE] = self._temperature
                # If temperature is within normal range
                if self._temperature < self._tempFeverLimit:
                    self._userInfo[ac_cfg.AUTHORIZED] = True
                    self._userInfo[ac_cfg.BOX_COLOR] = HMI_BOX_COLOR.GREEN.value
                    if self._maskOnFlag:
                        self._messages = HMI_MESSAGES.ACCESO_AUTORIZADO
                        self._userInfo[ac_cfg.MASK_STATUS] = True
                    else:
                        self._messages = HMI_MESSAGES.PUT_MASK
                        self._userInfo[ac_cfg.MASK_STATUS] = False
                    Logger("messages: " + str(self._messages))
                else:
                    self._messages = HMI_MESSAGES.ACUDIR_SERVICIO_MEDICO
                    Logger("messages: " + str(self._messages))
                    Save_User_Suspicious_Temp_Image(self._frame, user_id_evaluated, 'fever_temp')
                    gpioTempStatus = True
            else:
                # either temperature timeout expired with no correct measurement or temperature is out of limits
                self._messages = HMI_MESSAGES.ERROR_LECTURA_PASAR_VIGILANCIA
                Logger("messages: " + str(self._messages))
                Save_User_Suspicious_Temp_Image(self._frame, user_id_evaluated, 'suspicious_temp')

            if self._userInfo[ac_cfg.BOX_POSITION] is None:
                # Temperature timeout expired
                # At this point there are not faces in ROI2, take the one closest to the center
                currentFace = []
                index = 0
                minDistanceIndex = -1
                distance = self._widthResolution  # Start with an invalid distance
                for (x, y, w, h, c) in self._faces:
                    faceCentre_x = x + int(w / 2)
                    faceCentre_y = y + int(h / 2)
                    distanceFromCentre = math.sqrt(
                        (faceCentre_x - self._widthCentre) ** 2 + (faceCentre_y - self._heightCentre) ** 2)
                    if distanceFromCentre < distance:
                        distance = distanceFromCentre
                        minDistanceIndex = index
                    index += 1
                if minDistanceIndex > -1:
                    # @TODO: Update _userIndex??
                    self._userInfo[ac_cfg.BOX_POSITION] = self._faces[minDistanceIndex]

            if not self._maskOnFlag:
            #    # Called when user was not wearing a mask
            #    self._messages = HMI_MESSAGES.ACCESO_NEGADO_COLOCAR_CUBREBOCAS
                 self._userInfo[ac_cfg.MASK_STATUS] = False #DBL_276
            else:
            #    # Error in evaluate access
                Logger("Access could not be determined")
        else:
            # User was not identified or User not in DB
            self._messages = HMI_MESSAGES.ACCESO_NEGADO_CONTACTAR_RH
        Logger("messages: " + str(self._messages))

        if len(self._faces) > 0 and self._userIndex > -1:
            self._faces[self._userIndex][4] = self._userInfo[ac_cfg.BOX_COLOR]
        else:
            Logger("userIndex: {0}, len(faces): {1}".format(self._userIndex, len(self._faces)))

        # Fill response to POST Services
        #if self._knownUserFlag:
        if user_id_evaluated != ac_cfg.UNKNOWN_USER_ID:
            #self.GetUserInfoFromDB()
            self.GetUserInfoFromDB(user_id_evaluated)
            self._userInfo[ac_cfg.USER_ID] = user_id_evaluated
            Logger("Post user: " + str(self._userInfo[ac_cfg.USER_ID]))
            self._dataToSend['userID'] = self._userInfo[ac_cfg.USER_ID]
            self._dataToSend['monitorID'] = self._userInfo[ac_cfg.MONITOR_ID]
            self._dataToSend['temp'] = int(self._temperature * 10)
            self._dataToSend['mask'] = self._userInfo[ac_cfg.MASK_STATUS]
            self._dataToSend['authorizedAccess'] = self._userInfo[ac_cfg.AUTHORIZED]
            try:
                if (not PostProcessHandler.is_alive()):           # DBL_323_PostServiceProcess if not initialize it again
                    Logger("PostProcessHandler is NOT alive re-starting")
                    PostProcessHandler.Init()
                PostProcessHandler.dataQueue.put(self._dataToSend)
            except Exception as e:
                Logger("Post Exception" + str(e))
            

        # Enable buzzer
        if self._userInfo[ac_cfg.AUTHORIZED]:
            self._externalDevices.Activate_Relay1()
            self._externalDevices.Activate_Buzzer(gpioDriver.BUZZER_SOUNDS.ACCESS_GRANTED)
        elif gpioTempStatus:
            self._externalDevices.Activate_Buzzer(gpioDriver.BUZZER_SOUNDS.ACCESS_GRANTED)
        else:
            self._externalDevices.Activate_Buzzer(gpioDriver.BUZZER_SOUNDS.ACCESS_GRANTED)
        return self._messages

    #def GetUserInfoFromDB(self):
    def GetUserInfoFromDB(self, user_id_evaluated):
        #userID = self._userInfo[ac_cfg.USER_ID]
        userID = user_id_evaluated
        monitorID = userID
        name = 'Usuario'
        last_name = 'Sin_Registro'
        try:
            # @TODO: Remove keys when they are standard
            with shelve.open(ac_cfg.USERS_DB_PATH + ac_cfg.USERS_DB_NAME, 'r') as userDatabase:
                self._dataToSend['userType'] = userDatabase[userID]['user_type']
                name = userDatabase[userID][ac_cfg.NAME]
                last_name = userDatabase[userID][ac_cfg.LAST_NAME]
                monitorID = userDatabase[userID]['monitor_id']
        except Exception as exp:  # @todo: Decide if the information has to be sent if not found on DB
            self._dataToSend['userType'] = '1'
        if name == 'Usuario' or userID == '12636_12636':
            self._userInfo[ac_cfg.MONITOR_ID] = '-----'
            self._userInfo[ac_cfg.NAME] = name
            self._userInfo[ac_cfg.LAST_NAME] = last_name
            self._userInfo[ac_cfg.USER_ID] = '------' # @TODO: To confirm if this information is needed
        else:
            self._userInfo[ac_cfg.MONITOR_ID] = monitorID
            self._userInfo[ac_cfg.NAME] = name
            self._userInfo[ac_cfg.LAST_NAME] = last_name
            self._userInfo[ac_cfg.USER_ID] = user_id_evaluated # @TODO: To confirm if this information is needed

    def FollowUpUser(self):
        # Distance between previous user centre and new faces centre should not excede a delta to
        # consider it as the same face.
        #if self._followUpTS is None:
        #    self._followUpTS = dt.now()

        if self._userInfo[ac_cfg.BOX_POSITION] is not None:
            x = self._userInfo[ac_cfg.BOX_POSITION][0]
            y = self._userInfo[ac_cfg.BOX_POSITION][1]
            w = self._userInfo[ac_cfg.BOX_POSITION][2]
            h = self._userInfo[ac_cfg.BOX_POSITION][3]
            userCentre = (int(x + (w / 2)), (y + int(h / 2)))
            index = 0
            foundUser =  False
            for (x, y, w, h, c) in self._faces:
                newCentre = (int(x + (w / 2)), (y + int(h / 2)))
                distanceFromUser = math.sqrt((newCentre[0] - userCentre[0]) ** 2 + (newCentre[1] - userCentre[1]) ** 2)
                Logger("Distance: " + str(distanceFromUser))
                if distanceFromUser < self._maxDistFromUser:
                    if (newCentre[0] > int(self._widthCentre - (self._roi2MinSize / 2)) and 
                        newCentre[0] < int(self._widthCentre + (self._roi2MinSize / 2))):
                        self._userInfo[ac_cfg.BOX_POSITION] = [x, y, w, h]
                        self._faces[index][4] = self._userInfo[ac_cfg.BOX_COLOR]
                        foundUser = True
                        break
                index += 1
            if not foundUser and self._followUpTS is not None and (dt.now() - self._followUpTS) > tdelta(seconds=self._followUpTSLimit):
                Logger("User not found and FollowUp timeout")
                self.ResetValues()
        else:
            Logger("FollowUpUser - No face position")

    def TurnOnAuxiliaryLamp(self):
        self._externalDevices.Activate_Relay2()

    def TurnOffAuxiliaryLamp(self):
        self._externalDevices.Deactivate_Relay2()

    def UpdateIdentificationModel(self):
        try:
            new_model_TS = os.path.getmtime(ac_cfg.MODEL_FILE_PATH)
            if self._modelFileTS != new_model_TS:
                res = self._faceIdentification.Load(ac_cfg.MODEL_FILE_PATH)
                self._modelFileTS = new_model_TS
        except Exception as e:
            Logger('ERROR AL INTENTAR ACTUALIZAR EL MODELO DE IDENTIFICACION: ' + str(e))

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Sep-18-2020   Jonatan Uresti
#   + Created initial file.
#
# Sep-25-2020   Jonatan Uresti
#   + DBL_42
#      - Cleaned initial code.
#
# 29-Sep-2020   xznmw9_Agaona
#   + DBL_39
#      - Cascade model file path 
#   + DBL_24
#      - First face identification
#
# 06-Oct-2020   Nestor Hernandez / Jonatan Uresti
#   + DBL_17
#      - Information of first identified user is updated
#         when a second user enter detection area.
#   + DBL_26
#      - Screen should turn black after 5 seconds without detecting faces.
#
# Oct-09-2020 Jonatan Uresti
#   + DBL_70:
#      -Updated identification area.
#
# Oct-15-2020 Ernesto Ulises Beltran
#   + DBL_93:
#      -Updated data flow for hmi.
#
# Oct-20-2020 Ernesto Ulises Beltran, Eduardo Gunter
#   + DBL_99:
#      -Disable tracker and update data flow.
#
# Oct-21-2020 Pablo Mejia
#   + DBL_97:
#      -Extract user info from local DB
#
# Oct-21-2020 nzddvp
#   DBL_63:
#       - Updated GPIO Interfaces
#
# Oct-30-2020 Cinthia Valdez / Jonatan Uresti
#   DBL_54:
#       - Redisign of Access Control
#       - Includes DBL_13, DBL_23, DBL_75, DBL_83, DBL_84, DBL_86, DBL_89, DBL_91,
#          DBL_92, DBL_102*, DBL_103, DBL_104, DBL_107
#
# Oct-30-2020 Arturo Gaona
#   DBL_113:
#       - Added models for face detection
#
# Nov-06-2020 Cinthia Valdez
#   DBL_117:
#       - Report reading error if temperature if above upper limit
#
# Nov-11-2020 Jonatan Uresti
#   DBL_121 DBL_124:
#       - Display info for at least 2 seconds
#       - Set display off limit to 60 seconds
#       - Changed 'Not Found' to 'Usuario Desconocido'
#
# Dec-01-2020 Leobardo N Hernandez / Lucero Buenrostro / Jonatan Uresti
#   + DBL_196:
#      - Implementation was changed due to access control redesign.
#
# Jan-28-2021 Leobardo N Hernandez
#   + DBL_205:
#      - Added TurnOnAuxiliaryLamp and TurnOffAuxiliaryLamp functions.
#
# Feb-17-2021 Leobardo N Hernandez
#   + DBL_222:
#      - Updated GetTemperature funtion to provide the location of the identified user
#        to the temperature module.
#
# Feb-17-2021 Leobardo N Hernandez
#   + DBL_223:
#      - Updated the detectMultiScale parameters to improve the faces detection.
#
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225
#      - Updated function Logger().
#
# Feb-19-2021 Leobardo N Hernandez
#   + DBL_226
#      - Created function Save_User_Suspicious_Temp_Image to save the frame when the 
#        temperature is outside of the expected thresholds.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_231
#      - Added _highlightFace to save the face to which the blue rectangle be shown.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_232
#      - Added UpdateIdentificationModel function.
#
# Abril 2021 Lucia Chavez
#   + DBL_249
#      - Change position/dimension by default when GetTemperature without a face
# Abril 2021 Lucia Chavez/Arturo Gaona
#   + DBL_251
#      - Add contrast on GetFaces in principal Frame
# Mar-24-2021 Leobardo N Hernandez/Lucia Chavez
#   + DBL_244
#      - Updated EvaluateAccess function.
#
# Julio-2021 Lucia Chavez
#   + DBL_276
#      - Updated EvaluateAccess Function adding a status of MaskDetection when the flag is NONE.
#
# Diciembre-2021 Arturo Gaona
#   + DBL_Improve_Recognition_Speed
#       - Updated to improve recognition speed by sending to identify only the faces that are closer    
#
# Febrero-2022 Arturo Gaona
#   + DBL_323_PostServiceProcess Is_alive issue
#       - Check that PostServiceProcess is alive to send the post
#       - Improve resize method considering isometric projection
#
#########################################################################################