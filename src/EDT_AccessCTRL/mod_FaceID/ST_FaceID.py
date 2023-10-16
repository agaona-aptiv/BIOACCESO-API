'''
Created on 26-Aug-2020
@author: José Arturo Gaona
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: **EDT_AccessCTRL/Gateway
#          Description: **This module provide all methods to train, add, remove or identify faceIDs from a givem model file path
#          Enterprise: Condumex
#          SW Developer: **José Arturo Gaona Cuadra
#          
#          File: **ST_FaceID.py
#          Feature: **EDT_AccessCTRL
#          Design:  **Diagrama_Clases_ST_FaceID_v1.0.ppt
#          Deviations: **Por aclarar con Calidad
#   
#  **Information that must change according to the script
#########################################################################################
_debugTest=False
_TestWithTensorFlow = False   #DBL_40
import os
if (os.path.isdir('mod_FaceID')):
    import mod_FaceID.ST_FaceID_cfg as fid_cfg
    parentFolder =  '/mod_FaceID/'
else:
    import ST_FaceID_cfg as fid_cfg
    parentFolder =  '/'

import unittest
import face_recognition
import cv2
import os
import pickle
import numpy as np
import urllib.request                       # DBL_41
from urllib.request import Request, urlopen # DBL_41
from PIL import Image

import dlib                                 # DBL_262
from math import hypot                      # DBL_262

class ST_FaceID:
    '''
    Static interface for Image recognition
    '''
    __instance = None
    UseTensorFlow = True

    @staticmethod
    def getInstance():
        """ 
            Static access method.
        """
        if ST_FaceID.__instance is None:
            ST_FaceID()
        return ST_FaceID.__instance

    def __init__(self,useTensorFlow=True):  #DBL_40
        """ 
            Virtually private constructor. 
        """
        ST_FaceID.UseTensorFlow=useTensorFlow
        if ST_FaceID.__instance != None:
            raise Exception(fid_cfg.SINGLETONE_MODEL_EXCEPTION)
        else:
            ST_FaceID.__instance = self
            #DBL_262  Facemask Models and images
            ST_FaceID.__kn95_facemask = cv2.imread(fid_cfg.FACEMASKMODEL1)
            ST_FaceID.__blue_facemask = cv2.imread(fid_cfg.FACEMASKMODEL2)
            ST_FaceID.__black_facemask = cv2.imread(fid_cfg.FACEMASKMODEL3)
            ST_FaceID.__detector = dlib.get_frontal_face_detector()
            ST_FaceID.__predictor = dlib.shape_predictor(fid_cfg.FACEMASK_PREDICTOR)   #DBL_262  Facemask Model
            #DBL_262
            ST_FaceID.Model = {fid_cfg.MODEL_FACE_LIST:[], fid_cfg.MODEL_FACE_ENCODE_LIST:[]}
            ST_FaceID.FirstIdentifyFace()   # DBL_24

            if (ST_FaceID.UseTensorFlow==True):    #DBL_40
                ST_FaceID.tensorflow = __import__('tensorflow')
                modelPath = fid_cfg.MASK_MODEL
                if (os.path.exists(modelPath)):
                    ST_FaceID.MaskModel = ST_FaceID.tensorflow.keras.models.load_model(modelPath)
                    ST_FaceID.FirstMaskDetection()   # DBL_24
                else:
                    raise Exception(fid_cfg.NO_MODEL_EXCEPTION + fid_cfg.MASK_MODEL)

    @staticmethod   # DBL_24
    def FirstIdentifyFace():
        if (os.path.isdir('mod_FaceID')):
            test_path = os.path.dirname(__file__) + '/UnitTestImages/TestMeganFox.jpg'
        else:            
            test_path = './UnitTestImages/TestMeganFox.jpg'
        frame = face_recognition.load_image_file(test_path)
        face_encoding = face_recognition.face_encodings(frame)[0]
        result = ST_FaceID.IdentifyFace(face_encoding)

    @staticmethod # DBL_24
    def FirstMaskDetection():
        if (os.path.isdir('mod_FaceID')):
            test_path = os.path.dirname(__file__) + '/UnitTestImages/TestMeganFox.jpg'
        else:            
            test_path = './UnitTestImages/TestMeganFox.jpg'
        frame = face_recognition.load_image_file(test_path)
        result = ST_FaceID.GetMaskStatus(frame)
           
    @staticmethod
    def Load(modelFilePath):
        '''
            Loads the model from a file path
            usage example: 

            import ST_FaceID
            faceIdentification = ST_FaceID.getInstance()
            result = faceIdentification.Load('unitestModel.pkl')
        '''
        result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Model was loaded on ST_FaceID.Model'}
        try:
            with open(modelFilePath, 'rb') as f:
                ST_FaceID.Model = pickle.load(f)
        except Exception as e:
            result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:fid_cfg.GENERAL_RESULT_EXCEPTION + str(e)}
        return result

    @staticmethod
    def SaveModel(modelFilePath):
        '''
            Save ST_FaceID.Model to a file
        '''
        result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Model was saved on ' + modelFilePath}
        try:
            with open(modelFilePath, 'wb') as f:
                pickle.dump(ST_FaceID.Model, f)
        except Exception as e:
            result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT: fid_cfg.GENERAL_RESULT_EXCEPTION + str(e)}
        return result

    @staticmethod
    def AddFaceIDs(modelFilePath,objectsToTrainList):
        '''
            How to use:
            faceIdentification = ST_FaceID.getInstance()
            objectsToTrainList = []
            objectsToTrainList.append({'faceID':'MeganFox','path':'./TestCaseImages/MeganFox.jpg'})
            result = faceIdentification.AddFaceIDs('modelFilePath.pkl',objectsToTrainList)
            
            result--> [{fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'MeganFox was added to ST_FaceID.Model'}]
        '''
        resultList = []
        for objectsToTrain in objectsToTrainList:
            try:
                #result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT: objectsToTrain['faceID'] + ' was added to ST_FaceID.Model'}
                result = {fid_cfg.GENERAL_RESULT_USER_ID: objectsToTrain['faceID'],
                            fid_cfg.GENERAL_RESULT_STATUS:True,
                            fid_cfg.GENERAL_RESULT_COMMNENT: objectsToTrain['faceID'] + ' was added to ST_FaceID.Model'}
                
                # DBL_41
                if (('https:' in str(objectsToTrain['path'])) or ('http:' in str(objectsToTrain['path']))):
                    url = str(objectsToTrain['path'])
                    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
                    image = Image.open(urllib.request.urlopen(req, timeout=10))
                    image = np.asarray(image)
                else:
                    # DBL_41
                    image = face_recognition.load_image_file(objectsToTrain['path'])
                    image = image[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

                # >>>>>>>  DBL_262
                if (objectsToTrain['faceID'].endswith('_1')):
                    faceID_List,imageWithFaceMaskList = ST_FaceID.GetFaceMasksImages(image,objectsToTrain['faceID'])
                else:
                    faceID_List = []
                    imageWithFaceMaskList = []
                    faceID_List.append(objectsToTrain['faceID'])
                    imageWithFaceMaskList.append(image)

                for (facemaskFaceID,image) in zip(faceID_List,imageWithFaceMaskList):
                    face_locations = face_recognition.face_locations(image)  # DBL_21  improve accuracy using CNN model instead of HUG
                    if (len(face_locations)>0):
                        face_encode = face_recognition.face_encodings(image)[0]
                    else:
                        result = {fid_cfg.GENERAL_RESULT_USER_ID: facemaskFaceID,
                        fid_cfg.GENERAL_RESULT_STATUS:False,
                        fid_cfg.GENERAL_RESULT_COMMNENT: fid_cfg.GENERAL_RESULT_EXCEPTION + ' It was not possible to locate a face on this image'}

                    ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST].append(facemaskFaceID)
                    ST_FaceID.Model[fid_cfg.MODEL_FACE_ENCODE_LIST].append(face_encode)

            except Exception as e:
                objectsToTrain['faceID'] = objectsToTrain['faceID'].split('_')[0]    #DBL_265
                result = {fid_cfg.GENERAL_RESULT_USER_ID: objectsToTrain['faceID'],
                            fid_cfg.GENERAL_RESULT_STATUS:False,
                            fid_cfg.GENERAL_RESULT_COMMNENT: fid_cfg.GENERAL_RESULT_EXCEPTION + str(e)}

            # DBL_243
            if fid_cfg.KEY_HUB_PHOTO_PATH in objectsToTrain:
                result[fid_cfg.GENERAL_RESULT_HUB_PATH] = objectsToTrain[fid_cfg.KEY_HUB_PHOTO_PATH]

            resultList.append(result)
        if len(resultList)>0:
            ST_FaceID.SaveModel(modelFilePath)
        return resultList

    @staticmethod
    def Train(pathImages,modelFilePath,extension=fid_cfg.FACE_IMAGE_FORMAT):
        '''
            Train the Face Racognition model 
                pathImages = Path where the faces are placed
                modelFilePath = Model file path where the new updated model will be saved
                Extension = types  list of file to be used on filter []
                Returns the result status list 
            Usage example: 

            import ST_FaceID

            faceIdentification = ST_FaceID.getInstance()
            result = faceIdentification.Train('./TestCaseImages','unitestModel.pkl',['jpg'])
        '''
        result = [{fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Model was trained from:'+ pathImages +' and saved on ' + modelFilePath}]
        if not os.path.exists(modelFilePath):
            ST_FaceID.SaveModel(modelFilePath)
        loadResult = ST_FaceID.Load(modelFilePath)

        if loadResult[fid_cfg.GENERAL_RESULT_STATUS]:
            faceIDList = []
            faceEncodeList = []
            objectsToTrainList = []
            for root, dirs, files in os.walk(pathImages):
                for file in files:
                    if (file.endswith(extension[0])):
                        path = os.path.join(root, file)
                        faceID = os.path.basename(path).replace('.' + extension[0], '')
                        if (faceID not in ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST]):
                            objectsToTrainList.append({'faceID':faceID,'path':path})
            if (len(objectsToTrainList)>0):
                result = ST_FaceID.AddFaceIDs(modelFilePath,objectsToTrainList)
        else:
            result = loadResult
        return result

    @staticmethod
    def GetMaskStatus(crop_image):
        '''
            Determina if the face image parameter is using a face-mask or not
            How to use it:
            faceIdentification = ST_FaceID.getInstance()
            frame = face_recognition.load_image_file('./UnitTestImages/Mask.jpg')
            result = face_recognition.GetMaskStatus(frame)
            result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Mask status was determied as ' + label,'maskStatus':False,'accuracy':100.0}
        '''
        if (ST_FaceID.UseTensorFlow==True):   #DBL_40
            label = "No_Mask"
            result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Mask status was determied as ' + label,'maskStatus':False,'accuracy':100.0}
            face_frame = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            face_frame = cv2.resize(face_frame, (224, 224))
            face_frame = ST_FaceID.tensorflow.keras.preprocessing.image.img_to_array(face_frame)
            face_frame = np.expand_dims(face_frame, axis=0)
            face_frame =  ST_FaceID.tensorflow.keras.applications.mobilenet_v2.preprocess_input(face_frame)
            faces_list=[]
            faces_list.append(face_frame)
            if len(faces_list)>0:
                preds = ST_FaceID.MaskModel.predict(faces_list)
            #mask contain probabily of wearing a mask and vice versa
            for pred in preds:
                (mask, withoutMask) = pred

            accuracy = max(mask, withoutMask) * 100

            if mask > withoutMask:
                label = "Mask"
                result['maskStatus'] = True
                result[fid_cfg.GENERAL_RESULT_COMMNENT] = 'Mask status was determied as ' + label
            result['accuracy'] = accuracy
        else:  #DBL_40
            result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:'Use tensorflow is not supported for this time','maskStatus':False,'accuracy':0.0}
        return result

    @staticmethod
    def IdentifyFace(face_encoding,unknown=fid_cfg.UNKNOWN_USERID,tolerance=fid_cfg.FACE_RECOG_TOLERANCE_NO_MASK):
        '''
            Identify only one face in the frame face encoded
            how to use it:

            faceIdentification = ST_FaceID.getInstance()
            faceIdentification.Load('unitestModel.pkl')
            frame = face_recognition.load_image_file('./UnitTestImages/TestMeganFox.jpg')
            face_encoding = face_recognition.face_encodings(frame)[0]
            result = faceIdentification.IdentifyFace(face_encoding)
            #result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was found on ST_FaceID.Model','faceID':faceID}

        '''
        try:
            result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was NOT found on ST_FaceID.Model','faceID':unknown}
            #DBL_321_Use_euclidean_distance for face identification
            distance = face_recognition.face_distance(ST_FaceID.Model[fid_cfg.MODEL_FACE_ENCODE_LIST],face_encoding)
            min_distance = float(np.amin(distance))
            min_distance_index = np.argmin(distance)
            tolerance = float(np.float64(tolerance))
            if (min_distance < tolerance):
                faceID = ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST][min_distance_index].split('_')[0] 
                result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was found on ST_FaceID.Model','faceID':faceID}
            else:
                result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was not found on ST_FaceID.Model','faceID':'12636_12636'}

        except Exception as e:
            result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:fid_cfg.GENERAL_RESULT_EXCEPTION+ str(e),'faceID':unknown}        
        return result

    @staticmethod
    def RemoveFaceID(modelFilePath,faceID):
        '''
            How to use:
            faceIdentification = ST_FaceID.getInstance()
            result = faceIdentification.RemoveFaceID('modelFilePath.pkl','MeganFox')
            result--> {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'MeganFox was removed from ST_FaceID.Model'}]
        '''
        try:
            result = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT: faceID + ' was removed from the ST_FaceID.Model'}
            deleteSuccess = False
            for currentFaceID in ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST]:  # DBL_134, ensuere to remove all incidences
                if faceID in ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST]:
                    faceID_index = ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST].index(faceID)
                    ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST].remove(faceID)
                    del(ST_FaceID.Model[fid_cfg.MODEL_FACE_ENCODE_LIST][faceID_index])

                    if (faceID.endswith('_1')):             #DBL_262
                        for cnt in range(1,5):
                            faceID_index = ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST].index(faceID+str(cnt))
                            ST_FaceID.Model[fid_cfg.MODEL_FACE_LIST].remove(faceID+str(cnt))
                            del(ST_FaceID.Model[fid_cfg.MODEL_FACE_ENCODE_LIST][faceID_index])
                        
                    
                    ST_FaceID.SaveModel(modelFilePath)

                    deleteSuccess = True                    
            if (deleteSuccess == False):
                result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT: faceID + ' was not found on the ST_FaceID.Model'}
        except Exception as e:
            result = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:fid_cfg.GENERAL_RESULT_EXCEPTION+ str(e),'faceID':unknown}        
        return result

    @staticmethod
    def UpdateFaceIDs(modelFilePath,objectsToTrainList):
        '''
            How to use:
            faceIdentification = ST_FaceID.getInstance()
            objectsToTrainList = []
            objectsToTrainList.append({'faceID':'MeganFox','path':'./TestCaseImages/MeganFox.jpg'})
            result = faceIdentification.UpdateFaceIDs('modelFilePath.pkl',objectsToTrainList)
            result--> [{fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'MeganFox was added on ST_FaceID.Model'}]
        '''
        resultList = []
        try:
            #Delete all FaceIDs from the model
            for objectsToTrain in objectsToTrainList:
                ST_FaceID.RemoveFaceID(modelFilePath,objectsToTrain['faceID'])
            resultList = ST_FaceID.AddFaceIDs(modelFilePath,objectsToTrainList)
        except Exception as e:
            resultList.append({fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:fid_cfg.GENERAL_RESULT_EXCEPTION+ str(e),'faceID':unknown})
        return resultList

    @staticmethod
    def getRefPoints(test_L, test_R,x_L,x_R):           #DBL_241
        x_eyecenter_L = []
        x_eyecenter_R = []
        x_coord_L = None
        x_coord_R = None
        for (xl, yl, wl, hl) in test_L:
            # L: Get x coordinate of each eye center
            x_eyecenter_L.append(x_L+xl+int(wl/2))
        # L: Get x coordinate of point between eye centers
        if len(x_eyecenter_L) == 2:
            x_coord_L = ((x_eyecenter_L[0] + x_eyecenter_L[1])/2)

        for (xl, yl, wl, hl) in test_R:
            # R: Get x coordinate of each eye center
            x_eyecenter_R.append(x_R+xl+int(wl/2))
        # R: Get x coordinate of point between eye centers
        if len(x_eyecenter_R) == 2:
            x_coord_R = ((x_eyecenter_R[0] + x_eyecenter_R[1])/2)
        return x_coord_L, x_coord_R
            
    @staticmethod
    def getRefPoints(test_L, test_R,x_L,x_R):           #DBL_241
        x_eyecenter_L = []
        x_eyecenter_R = []
        x_coord_L = None
        x_coord_R = None
        for (xl, yl, wl, hl) in test_L:
            # L: Get x coordinate of each eye center
            x_eyecenter_L.append(x_L+xl+int(wl/2))
        # L: Get x coordinate of point between eye centers
        if len(x_eyecenter_L) == 2:
            x_coord_L = ((x_eyecenter_L[0] + x_eyecenter_L[1])/2)

        for (xl, yl, wl, hl) in test_R:
            # R: Get x coordinate of each eye center
            x_eyecenter_R.append(x_R+xl+int(wl/2))
        # R: Get x coordinate of point between eye centers
        if len(x_eyecenter_R) == 2:
            x_coord_R = ((x_eyecenter_R[0] + x_eyecenter_R[1])/2)
        return x_coord_L, x_coord_R

    @staticmethod
    def getRefPointsFI(face_L, face_R,face_x_L,face_x_R):           #DBL_241
        '''
        Get the center between eyes
        Parameter example: 
        face_L = [{'nose_tip': [(264, 363)], 'left_eye': [(131, 222), (207, 222)], 'right_eye': [(407, 219), (329, 220)]}]
        '''
        x1_L = face_L[0]['left_eye'][1][1] # left eye left()   point 
        y1_L = face_L[0]['left_eye'][0][0] # left eye top()    point
        x2_L = face_L[0]['left_eye'][0][1] # left eye right()  point
        y2_L = face_L[0]['left_eye'][1][0] # left eye botton() point

        x_L = face_x_L + x1_L + int((x2_L-x1_L)/2)
        y_L = y1_L + int((y2_L-y1_L)/2)

        eyecenter_L = (x_L,y_L)

        x1_R = face_R[0]['left_eye'][1][1] # right eye left()   point 
        y1_R = face_R[0]['left_eye'][0][0] # right eye top()    point
        x2_R = face_R[0]['left_eye'][0][1] # right eye right()  point
        y2_R = face_R[0]['left_eye'][1][0] # right eye botton() point

        x_R = face_x_R  + x1_R + int((x2_R-x1_R)/2)
        y_R = y1_R + int((y2_R-y1_R)/2)

        eyecenter_R = (x_R,y_R)

        #X coord from L and R
        x_coord_L =  eyecenter_L[0]
        x_coord_R =  eyecenter_R[0]

        return x_coord_L, x_coord_R

    @staticmethod
    def getDepth(coordinate_L, coordinate_R):           #DBL_241
        '''
            Get distance between camera and reference point
        '''
        z_RL = None
        if (coordinate_L != None) and (coordinate_R != None):
            # Calculate disparity
            d_RL = abs(coordinate_L - coordinate_R)
            # Get depth in cm
            if d_RL != 0:
                z_RL = round(fid_cfg.FOCAL_PIXEL * fid_cfg.BASE_DISTANCE / d_RL,1)
            else:
                z_RL = 0
        return z_RL

    @staticmethod
    def getHumanity(coordinate_L, coordinate_R, width_L, min_disparity = fid_cfg.MIN_DISPARITY):        #DBL_241
        '''
            Determine Humanity from coordinate reference point and face width
        '''
        retVal = False
        # Calculate disparity
        if (coordinate_L != None) and (coordinate_R != None):
            d_RL = abs(coordinate_L - coordinate_R)
            if (d_RL > fid_cfg.MIN_DISPARITY ) and (width_L > d_RL):
                # It is a person
                retVal = True
        return retVal

    @staticmethod
    def Contrast(image,clipLimit=3.,tileGridSize=(8,8)):
        '''
       This method  implementes CLAHE (Contrast Limited Adaptive Histogram Equalization)
        https://stackoverflow.com/questions/19363293/whats-the-fastest-way-to-increase-color-image-contrast-with-opencv-in-python-c

        '''
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)

        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2,a,b))  # merge channels
        new_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
        return new_image

    @staticmethod
    def GetFaceMasksImages(frame,faceID,face_mask_size=0.60):              #DBL_262
        faceIDList=[]
        facemaskList=[]
        faceIDList.append(faceID)
        facemaskList.append(frame)
        rows, cols, _ = frame.shape
        facemask = np.zeros((rows, cols), np.uint8)
        facemask.fill(0)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = ST_FaceID.__detector(frame)
        for face in faces:
            landmarks = ST_FaceID.__predictor(gray_frame, face)
            #landmarks = face_recognition.face_landmarks(gray_frame, face_locations=face, model = 'small')

            # Fasecamsk coordinates
            top_faceMask = (landmarks.part(30).x, landmarks.part(30).y)       #30 Nose point check presentation
            center_facemask = (landmarks.part(62).x, landmarks.part(62).y)    #30 
            left_facemask = (landmarks.part(3).x, landmarks.part(3).y)        #31
            right_facemask = (landmarks.part(13).x, landmarks.part(13).y)     #35

            facemask_width = int(hypot(left_facemask[0] - right_facemask[0],left_facemask[1] - right_facemask[1]) * face_mask_size)
            facemask_height = int(facemask_width *face_mask_size)  # Try and test size

            # New facemask position
            top_left = (int(center_facemask[0] - facemask_width / 2),int(center_facemask[1] - facemask_height / 2))
            bottom_right = (int(center_facemask[0] + facemask_width / 2),int(center_facemask[1] + facemask_height / 2))

            # Adding the new facemask
            add_facemask1 = cv2.resize(ST_FaceID.__kn95_facemask, (facemask_width, facemask_height))
            add_facemask2 = cv2.resize(ST_FaceID.__blue_facemask, (facemask_width, facemask_height))
            add_facemask3 = cv2.resize(ST_FaceID.__black_facemask, (facemask_width, facemask_height))
            
            add_facemask_gray1 = cv2.cvtColor(add_facemask1, cv2.COLOR_BGR2GRAY)
            _, facemask1 = cv2.threshold(add_facemask_gray1, 25, 255, cv2.THRESH_BINARY_INV)

            add_facemask_gray2 = cv2.cvtColor(add_facemask2, cv2.COLOR_BGR2GRAY)
            _, facemask2 = cv2.threshold(add_facemask_gray2, 25, 255, cv2.THRESH_BINARY_INV)

            add_facemask_gray3 = cv2.cvtColor(add_facemask3, cv2.COLOR_BGR2GRAY)
            _, facemask3 = cv2.threshold(add_facemask_gray3, 25, 255, cv2.THRESH_BINARY_INV)

            facemask_area = frame[top_left[1]: top_left[1] + facemask_height,top_left[0]: top_left[0] + facemask_width]

            facemask_area_no_facemask1 = cv2.bitwise_and(facemask_area, facemask_area, mask=facemask1)
            facemask_area_no_facemask2 = cv2.bitwise_and(facemask_area, facemask_area, mask=facemask2)
            facemask_area_no_facemask3 = cv2.bitwise_and(facemask_area, facemask_area, mask=facemask3)
            final_facemask1 = cv2.add(facemask_area_no_facemask1, add_facemask1)
            final_facemask2 = cv2.add(facemask_area_no_facemask2, add_facemask2)
            final_facemask3 = cv2.add(facemask_area_no_facemask3, add_facemask3)

            #-Insert facemask on the original image
            framekn95 = frame.copy()
            frameBlue = frame.copy()
            frameBlack = frame.copy()
            framekn95[top_left[1]: top_left[1] + facemask_height,top_left[0]: top_left[0] + facemask_width] = final_facemask1
            frameBlue[top_left[1]: top_left[1] + facemask_height,top_left[0]: top_left[0] + facemask_width] = final_facemask2
            frameBlack[top_left[1]: top_left[1] + facemask_height,top_left[0]: top_left[0] + facemask_width] = final_facemask3
            facemaskList.append(framekn95)
            faceIDList.append(faceID+'1')
            facemaskList.append(frameBlue)
            faceIDList.append(faceID+'2')
            facemaskList.append(frameBlack)
            faceIDList.append(faceID+'3')
            #Flip image from Original                   #DBL_266
            frameFlip = cv2.flip(frame,1)
            facemaskList.append(frameFlip)
            faceIDList.append(faceID+'4')

        return faceIDList,facemaskList


'''
**********************************
********* Unit Test **************
*** https://docs.python.org/2/library/unittest.html#assert-methods *****
**********************************
'''
class TC001_Test_SingleTone(unittest.TestCase):
   @unittest.skipIf(_debugTest==True,"DebugMode")
   def test001_1_TestSingletoneException(self):
      print('.******************** test001_1_TestSingletoneException *********************')
      faceIdentification = ST_FaceID(useTensorFlow=_TestWithTensorFlow)  #DBL_40
      exceptionFlag = False 
      try:
         faceIdentificatio2 = ST_FaceID(useTensorFlow=_TestWithTensorFlow)   #DBL_40
      except Exception as e:
         exceptionFlag = True
      else:
         pass
      self.assertTrue(exceptionFlag,True)
   @unittest.skipIf(_debugTest==True,"DebugMode")
   def test001_2_TestMultipleGetInstances(self):
      print('******************** test001_2_TestMultipleGetInstances ********************')
      faceIdentification = ST_FaceID.getInstance()
      faceIdentification2 = ST_FaceID.getInstance()
      self.assertEqual(faceIdentification, faceIdentification2)

class TC002_Test_InitializeDB(unittest.TestCase):
    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_01_AddFaceIDs_MeganFox(self):
        print('******************** test002_1_AddFaceIDs_MeganFox *************************')
        faceIdentification = ST_FaceID.getInstance()
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'MeganFox','path':'./TestCaseImages/MeganFox.jpg'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        expected = [{'sap_number': 'MeganFox', 'status': True, 'comment': 'MeganFox was added to ST_FaceID.Model'}]
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_03_Load_Model(self):
        print('******************** test002_3_Load_Model **********************************')
        faceIdentification = ST_FaceID.getInstance()
        result = faceIdentification.Load('unitestModel.pkl')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Model was loaded on ST_FaceID.Model'}
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_04_Load_Model_File_Not_Found(self):
        print('******************** test002_4_Load_Model_File_Not_Found *******************')
        faceIdentification = ST_FaceID.getInstance()
        result = faceIdentification.Load('No_File_Path.pkl')
        self.assertEqual(result['status'],False)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_05_Train_Model(self):
        print('******************** test002_5_Train_Model *********************************')
        faceIdentification = ST_FaceID.getInstance()
        result = faceIdentification.Train('./TestCaseImages','unitestModel.pkl',['jpg'])
        self.assertGreater(len(result),3)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_06_Identify_Face(self):
        print('******************** test002_6_Identify_Face *******************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was found on ST_FaceID.Model','faceID':'MeganFox'}
        frame = face_recognition.load_image_file('./UnitTestImages/TestMeganFox.jpg')
        face_encoding = face_recognition.face_encodings(frame)[0]
        result = faceIdentification.IdentifyFace(face_encoding, tolerance=0.6)
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_07_RemoveFaceID(self):
        print('******************** test002_7_RemoveFaceID ********************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','MeganFox')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT: 'MeganFox' + ' was removed from the ST_FaceID.Model'}
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_08_CheckFaceRemoved(self):
        print('******************** test002_08_CheckFaceRemoved ***************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT:'face image was NOT found on ST_FaceID.Model','faceID':'0000_0000'}
        frame = face_recognition.load_image_file('./UnitTestImages/TestMeganFox.jpg')
        face_encoding = face_recognition.face_encodings(frame)[0]
        result = faceIdentification.IdentifyFace(face_encoding)
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_09_UpdateFaceIDs_MeganFox(self):
        print('******************** test002_9_UpdateFaceIDs_MeganFox Updated **************')
        faceIdentification = ST_FaceID.getInstance()
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'MeganFox','path':'./TestCaseImages/MeganFox.jpg'})
        result = faceIdentification.UpdateFaceIDs('unitestModel.pkl',objectsToTrainList)
        expected = [{fid_cfg.GENERAL_RESULT_USER_ID:'MeganFox',fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'MeganFox was added to ST_FaceID.Model'}]
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_10_Savemodel(self):
        print('******************** test002_10_Savemodel **********************************')
        faceIdentification = ST_FaceID.getInstance()
        result = faceIdentification.SaveModel('unitestModel.pkl')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:True,fid_cfg.GENERAL_RESULT_COMMNENT:'Model was saved on ' + 'unitestModel.pkl'}
        del faceIdentification
        self.assertEqual(result,expected)

    @unittest.skipIf(_TestWithTensorFlow==False,"useTensorFlow")  #DBL_40
    def test002_11_GetMaskStatus(self):
        print('******************** test002_11_GetMaskStatus ******************************')
        faceIdentification = ST_FaceID.getInstance()
        frame = face_recognition.load_image_file('./UnitTestImages/Mask.png')
        result = faceIdentification.GetMaskStatus(frame)
        self.assertEqual(result['maskStatus'],True)

    @unittest.skipIf(_TestWithTensorFlow==False,"useTensorFlow")   #DBL_40
    def test002_12_GetMaskStatus(self):
        print('******************** test002_12_GetMaskStatus ******************************')
        faceIdentification = ST_FaceID.getInstance()
        frame = face_recognition.load_image_file('./UnitTestImages/No_Mask.jpg')
        result = faceIdentification.GetMaskStatus(frame)
        self.assertEqual(result['maskStatus'],False)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_13_RemoveFaceID(self):
        print('******************** test002_13_RemoveFaceID *******************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','UserID_DoesNot_Exist')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT: 'UserID_DoesNot_Exist was not found on the ST_FaceID.Model'}
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_14_FaceIDWithMask(self):
        print('******************** test002_14_IdentifyWithMask ***************************')
        faceIdentification = ST_FaceID.getInstance()
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'ArturoGaona','path':'./MaskIDTest/2161_Reference.jpg'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        frame = face_recognition.load_image_file('./MaskIDTest/2161_Mask.jpg')
        frame = frame[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        face_encoding = face_recognition.face_encodings(frame)[0]
        result = faceIdentification.IdentifyFace(face_encoding, tolerance=0.7)
        expected = {'status': True, 'comment': 'face image was found on ST_FaceID.Model', 'faceID': 'ArturoGaona'}
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_15_AddFaceIDsFromUrl(self):         # DBL_41
        print('******************** test002_15_AddFaceIDsFromUrl **************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'personFromUrl','path':'https://thispersondoesnotexist.com/image'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        expected = [{fid_cfg.GENERAL_RESULT_USER_ID:'personFromUrl','status': True, 'comment': 'personFromUrl was added to ST_FaceID.Model'}]
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_16_AddFacesFromUrlAndLocal(self):   # DBL_41
        print('******************** test002_16_AddFacesFromUrlAndLocal ********************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        faceIdentification.RemoveFaceID('unitestModel.pkl','ArturoGaona')
        objectsToTrainList = []
        try:
            # To execute This Unittest
            # Ensure that you have the infraestructure to be able to read the http://192.168.1.93/urlshare/2161_No_Mask.jpg
            objectsToTrainList.append({'faceID':'UrlArturoGaona','path':'http://192.168.1.93/urlshare/2161_No_Mask.jpg'})
            objectsToTrainList.append({'faceID':'thispersondoesnotexist','path':'https://thispersondoesnotexist.com/image'})
            result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
            frame = face_recognition.load_image_file('./MaskIDTest/2161_Mask.jpg')
            face_encoding = face_recognition.face_encodings(frame)[0]
            result = faceIdentification.IdentifyFace(face_encoding, tolerance=0.7)
            expected = {'status': True, 'comment': 'face image was found on ST_FaceID.Model', 'faceID': 'UrlArturoGaona'}
            self.assertEqual(result,expected)
        except Exception as e:
            pass
    
    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_18_AddSimilarIDs(self):         
        print('******************** test002_18_AddSimilarIDs ******************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'185','path':'https://thispersondoesnotexist.com/image'})
        objectsToTrainList.append({'faceID':'41854','path':'https://thispersondoesnotexist.com/image'})
        objectsToTrainList.append({'faceID':'41851','path':'https://thispersondoesnotexist.com/image'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        expected = [{fid_cfg.GENERAL_RESULT_USER_ID:'185','status': True, 'comment': '185 was added to ST_FaceID.Model'},
                    {fid_cfg.GENERAL_RESULT_USER_ID:'41854','status': True, 'comment': '41854 was added to ST_FaceID.Model'},
                    {fid_cfg.GENERAL_RESULT_USER_ID:'41851','status': True, 'comment': '41851 was added to ST_FaceID.Model'}]
        faceIdentification.RemoveFaceID('unitestModel.pkl','185')           #DBL_266 Issue with thispersondoesnotexist
        faceIdentification.RemoveFaceID('unitestModel.pkl','41854')         #DBL_266 Issue with thispersondoesnotexist
        faceIdentification.RemoveFaceID('unitestModel.pkl','41851')         #DBL_266 Issue with thispersondoesnotexist
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_19_AddSimilarIDs(self):         
        print('******************** test002_19_AddSimilarIDs ******************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'234','path':'https://thispersondoesnotexist.com/image'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        expected = [{fid_cfg.GENERAL_RESULT_USER_ID:'234','status': True, 'comment': '234 was added to ST_FaceID.Model'}]
        faceIdentification.RemoveFaceID('unitestModel.pkl','234')           #DBL_266 Issue with thispersondoesnotexist
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")   #DBL_241
    def test002_20_getHumanity(self):
        print('******************** test002_20_getHumanity From image in cel **************')
        faceIdentification = ST_FaceID.getInstance()
        #Load Cascade models
        facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        eyeLcascade = cv2.CascadeClassifier(fid_cfg.CASCADE_LEYE_MODEL)
        eyeRcascade = cv2.CascadeClassifier(fid_cfg.CASCADE_REYE_MODEL)
        #Load Images or get from stereo Camera
        frame_L = face_recognition.load_image_file('./UnitTestImages/Photo_44cm_L.jpg')
        frame_R = face_recognition.load_image_file('./UnitTestImages/Photo_44cm_R.jpg')
        frame_L = frame_L[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame_R = frame_R[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #Convert to gray scale
        gray_frame_L = cv2.cvtColor(frame_L, cv2.COLOR_BGR2GRAY)
        gray_frame_R = cv2.cvtColor(frame_R, cv2.COLOR_BGR2GRAY)

        faces_L = facecascade.detectMultiScale(gray_frame_L, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        faces_R = facecascade.detectMultiScale(gray_frame_R, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)

        #Get ROI from faces L and R
        (x_L, y_L, w_L, h_L) = faces_L[0]
        (x_R, y_R, w_R, h_R) = faces_R[0]
        face_ROI_L = gray_frame_L[y_L:y_L+h_L,x_L:x_L+w_L]
        face_ROI_R = gray_frame_R[y_R:y_R+h_R,x_R:x_R+w_R]
        #Get Letf Eye form both cameras
        eyesL_L = eyeLcascade.detectMultiScale(face_ROI_L, scaleFactor=1.1,minNeighbors=5,minSize=(5, 5),flags=cv2.CASCADE_SCALE_IMAGE)
        eyesL_R = eyeRcascade.detectMultiScale(face_ROI_R, scaleFactor=1.1,minNeighbors=5,minSize=(5, 5),flags=cv2.CASCADE_SCALE_IMAGE)    

        x_coord_L, x_coord_R = faceIdentification.getRefPoints(eyesL_L, eyesL_R,x_L,x_R)
        isHuman = faceIdentification.getHumanity(x_coord_L, x_coord_R, w_L)
        self.assertEqual(isHuman,False)

    @unittest.skipIf(_debugTest==True,"DebugMode")   #DBL_241
    def test002_21_getHumanity(self):
        print('******************** test002_21_getHumanity From Real person ***************')
        faceIdentification = ST_FaceID.getInstance()
        #Load Cascade models
        facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        eyeLcascade = cv2.CascadeClassifier(fid_cfg.CASCADE_LEYE_MODEL)
        eyeRcascade = cv2.CascadeClassifier(fid_cfg.CASCADE_REYE_MODEL)
        #Load Images or get from stereo Camera
        frame_L = face_recognition.load_image_file('./UnitTestImages/Real_44cm_L.jpg')
        frame_R = face_recognition.load_image_file('./UnitTestImages/Real_44cm_R.jpg')
        frame_L = frame_L[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame_R = frame_R[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #Convert to gray scale
        gray_frame_L = cv2.cvtColor(frame_L, cv2.COLOR_BGR2GRAY)
        gray_frame_R = cv2.cvtColor(frame_R, cv2.COLOR_BGR2GRAY)

        faces_L = facecascade.detectMultiScale(gray_frame_L, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        faces_R = facecascade.detectMultiScale(gray_frame_R, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)

        #Get ROI from faces L and R
        (x_L, y_L, w_L, h_L) = faces_L[0]
        (x_R, y_R, w_R, h_R) = faces_R[0]
        face_ROI_L = gray_frame_L[y_L:y_L+h_L,x_L:x_L+w_L]
        face_ROI_R = gray_frame_R[y_R:y_R+h_R,x_R:x_R+w_R]
        eyesL_L = eyeLcascade.detectMultiScale(face_ROI_L, scaleFactor=1.1,minNeighbors=5,minSize=(5, 5),flags=cv2.CASCADE_SCALE_IMAGE)
        eyesL_R = eyeRcascade.detectMultiScale(face_ROI_R, scaleFactor=1.1,minNeighbors=5,minSize=(5, 5),flags=cv2.CASCADE_SCALE_IMAGE)    

        x_coord_L, x_coord_R = faceIdentification.getRefPoints(eyesL_L, eyesL_R,x_L,x_R)
        depth = faceIdentification.getDepth(x_coord_L, x_coord_R)
        isHuman = faceIdentification.getHumanity(x_coord_L, x_coord_R, w_L)
        self.assertEqual(isHuman,True)

    @unittest.skipIf(_debugTest==True,"DebugMode")   #DBL_241
    def test002_22_getHumanityFI(self):
        print('******************** test002_22_getHumanityFI ******************************')
        faceIdentification = ST_FaceID.getInstance()
        #Load Cascade models
        facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)

        #Load Images or get from stereo Camera
        frame_L = face_recognition.load_image_file('./UnitTestImages/Real_44cm_L.jpg')
        frame_R = face_recognition.load_image_file('./UnitTestImages/Real_44cm_R.jpg')
        
        frame_L = frame_L[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame_R = frame_R[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #Convert to gray scale
        gray_frame_L = cv2.cvtColor(frame_L, cv2.COLOR_BGR2GRAY)
        gray_frame_R = cv2.cvtColor(frame_R, cv2.COLOR_BGR2GRAY)

        faces_L = facecascade.detectMultiScale(gray_frame_L, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        faces_R = facecascade.detectMultiScale(gray_frame_R, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)

        #Get ROI from faces L and R
        (x_L, y_L, w_L, h_L) = faces_L[0]
        (x_R, y_R, w_R, h_R) = faces_R[0]

        face_ROI_L = gray_frame_L[y_L:y_L+h_L,x_L:x_L+w_L]
        face_ROI_R = gray_frame_R[y_R:y_R+h_R,x_R:x_R+w_R]


        face_landmarks_L = face_recognition.face_landmarks(face_ROI_L, face_locations=None, model = 'small')
        face_landmarks_R = face_recognition.face_landmarks(face_ROI_R, face_locations=None, model = 'small')

        x_coord_L, x_coord_R = faceIdentification.getRefPointsFI(face_landmarks_L,face_landmarks_R,x_L,x_R)

        depth = faceIdentification.getDepth(x_coord_L, x_coord_R)
        isHuman = faceIdentification.getHumanity(x_coord_L, x_coord_R, w_L)
        self.assertEqual(isHuman,True)

    @unittest.skipIf(_debugTest==True,"DebugMode")   #DBL_241
    def test002_23_getHumanityFI(self):
        print('******************** test002_23_getHumanityFI ******************************')
        faceIdentification = ST_FaceID.getInstance()
        #Load Cascade models
        facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        #Load Images or get from stereo Camera
        frame_L = face_recognition.load_image_file('./UnitTestImages/Photo_44cm_L.jpg')
        frame_R = face_recognition.load_image_file('./UnitTestImages/Photo_44cm_R.jpg')    
        
        frame_L = frame_L[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame_R = frame_R[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #Convert to gray scale
        gray_frame_L = cv2.cvtColor(frame_L, cv2.COLOR_BGR2GRAY)
        gray_frame_R = cv2.cvtColor(frame_R, cv2.COLOR_BGR2GRAY)

        faces_L = facecascade.detectMultiScale(gray_frame_L, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        faces_R = facecascade.detectMultiScale(gray_frame_R, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)

        #Get ROI from faces L and R
        (x_L, y_L, w_L, h_L) = faces_L[0]
        (x_R, y_R, w_R, h_R) = faces_R[0]

        face_ROI_L = gray_frame_L[y_L:y_L+h_L,x_L:x_L+w_L]
        face_ROI_R = gray_frame_R[y_R:y_R+h_R,x_R:x_R+w_R]


        face_landmarks_L = face_recognition.face_landmarks(face_ROI_L, face_locations=None, model = 'small')
        face_landmarks_R = face_recognition.face_landmarks(face_ROI_R, face_locations=None, model = 'small')

        x_coord_L, x_coord_R = faceIdentification.getRefPointsFI(face_landmarks_L,face_landmarks_R,x_L,x_R)

        depth = faceIdentification.getDepth(x_coord_L, x_coord_R)
        isHuman = faceIdentification.getHumanity(x_coord_L, x_coord_R, w_L)
        self.assertEqual(isHuman,False)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_24_ContrastFaceIDTest(self):
        print('******************** test002_24_ContrastFaceIDTest *************************')
        faceIdentification = ST_FaceID.getInstance()
        faceCascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)

        frame = face_recognition.load_image_file('./UnitTestImages/ArturoGaonaContrasted.jpg')
        frame = frame[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        contrasted_image = faceIdentification.Contrast(frame)
        contrasted_gray = cv2.cvtColor(contrasted_image, cv2.COLOR_BGR2GRAY)
        contrasted_faces = faceCascade.detectMultiScale(contrasted_gray,scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        self.assertEqual(len(contrasted_faces),1)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_25_NoContrastFaceIDTest(self):
        print('******************** test002_25_NoContrastFaceIDTest ***********************')
        faceIdentification = ST_FaceID.getInstance()
        faceCascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        frame = face_recognition.load_image_file('./UnitTestImages/ArturoGaonaContrasted.jpg')
        frame = frame[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        self.assertEqual(len(faces),0)

    @unittest.skipIf(_debugTest==True,"DebugMode")  #DBL_262
    def test002_26_GetFaceMasksImages(self):
        print('******************** test002_26_GetFaceMasksImages ****************************')
        faceIdentification = ST_FaceID.getInstance()
        #Load Cascade models
        facecascade = cv2.CascadeClassifier(fid_cfg.CASCADE_MODEL)
        frame = face_recognition.load_image_file('./UnitTestImages/TestMeganFox.jpg')
        frame = frame[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #Convert to gray scale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(gray_frame, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
        #Get ROI from faces L and R
        (x, y, w, h) = faces[0]
        face_ROI = frame[y:y+h+int(h*0.10),x:x+w]
        scale_percent = 25
        width = int(face_ROI.shape[1] * scale_percent / 100)
        height = int(face_ROI.shape[0] * scale_percent / 100)
        dsize = (width, height)
        face_ROI = cv2.resize(face_ROI,dsize)

        faceID_List,imageWithFaceMaskList = faceIdentification.GetFaceMasksImages(frame = face_ROI,faceID='0000_1',face_mask_size = 0.90)
        #for faceID, frame in zip(faceID_List, imageWithFaceMaskList):              #Debug DBL_266
        #    cv2.imwrite(faceID+'.jpg', frame)

        expected_list = ['0000_1', '0000_11', '0000_12', '0000_13','0000_14']
        self.assertEqual(faceID_List,expected_list)
        self.assertEqual(len(faceID_List),5)
        self.assertEqual(len(imageWithFaceMaskList),5)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_27_IdentifyWithMask(self):
        print('******************** test002_27_IdentifyWithMask ***************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')   
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','234')                  #Unittest issues on DBL_265     
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','personFromUrl')
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','ArturoGaona')
        init_id_on_list = len(faceIdentification.Model[fid_cfg.MODEL_FACE_LIST])
        objectsToTrainList = []
        objectsToTrainList.append({'faceID':'ArturoGaona_1','path':'./MaskIDTest/2161_Reference.jpg'})
        result = faceIdentification.AddFaceIDs('unitestModel.pkl',objectsToTrainList)
        end_id_on_list = len(faceIdentification.Model[fid_cfg.MODEL_FACE_LIST])
        frame = face_recognition.load_image_file('./MaskIDTest/2161_Mask.jpg')
        frame = frame[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        face_encoding = face_recognition.face_encodings(frame)[0]
        result = faceIdentification.IdentifyFace(face_encoding, tolerance=0.7)
        self.assertEqual(end_id_on_list,init_id_on_list+5)                              #DBL266
        expected = {'status': True, 'comment': 'face image was found on ST_FaceID.Model', 'faceID': 'ArturoGaona'}
        self.assertEqual(result,expected)

    @unittest.skipIf(_debugTest==True,"DebugMode")
    def test002_28_RemoveFaceID(self):
        print('******************** test002_28_RemoveFaceID ********************************')
        faceIdentification = ST_FaceID.getInstance()
        faceIdentification.Load('unitestModel.pkl')        
        result = faceIdentification.RemoveFaceID('unitestModel.pkl','ArturoGaona')
        expected = {fid_cfg.GENERAL_RESULT_STATUS:False,fid_cfg.GENERAL_RESULT_COMMNENT: 'ArturoGaona' + ' was not found on the ST_FaceID.Model'}
        self.assertEqual(result[fid_cfg.GENERAL_RESULT_STATUS],expected[fid_cfg.GENERAL_RESULT_STATUS])


if __name__ == '__main__':
    unittest.main()

######################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
#
# Date          userid          Description                                   
# 26-Aug-2020   Arturo Gaona    first release of the design implementation    
#
# 20-Sep-2020   Arturo Gaona    -Include capability to train images from url  
#                               -Implement solution for issues: 
#                                   * DBL_40
#                                   * DBL_24
#                                   * DBL_21
#                                   * DBL_41
#
# 09-Nov-2020   Arturo Gaona    Implement train with different facemasks models 
#                                   * DBL_134
#
# 18-Nov-2020   Arturo Gaona    Remove already exist verification
#                                   * DBL_134
#    
# 24-Mar-2021 Arturo Gaona      Implement methods for distance and depth 
#                                   * DBL_241:
#
# 30-Apr-2021 Arturo Gaona      Implement methods for distance and depth on Initial Test
#                                   * DBL_257: Implemented on Initial Test
#
# 25-May-2021   Arturo Gaona    Implement train with different virtual facemasks models 
#                                   * DBL_262
#
# 03-Jun-2021   Arturo Gaona  Solve the Issue DBL_265, when there is a error on Face ID if the Virtual mask was added
#                                   * DBL_265
#
# 03-Jun-2021   Arturo Gaona    Implement Issue DBL_266 add flip image to face id
#                                   * DBL_266_Up
#
# 04-Dic-2021   Arturo Gaona    Implement euclidean distance to determine similirity instead of simple comparation
#                                   * #DBL_321_Use_euclidean_distance for face identification
########################################################################################
########################################################################################