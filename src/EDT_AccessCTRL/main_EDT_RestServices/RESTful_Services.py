# Created on July 2020
# Author Pablo Mejia

#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: REST_Services
#          Program: REST Services to manage users
#          Enterprise: Condumex
#          SW Developer: Pablo Mejia
#          FILE DESCRIPTION
#          File: REST_Services.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################

from enum import Enum
from flask import Flask, json, request
from flask_restful import Api, Resource
from sys import platform, path
from os import path
from PIL import Image
import urllib.request
import requests
import shelve
import os
import sys
import configparser
import socket
from multiprocessing.connection import Listener, Client
import multiprocessing
import time

# Add to path modules located in different folders
sys.path.append(os.getcwd())

from mod_FaceID.ST_FaceID import *
import mod_FaceID.ST_FaceID_cfg as fid_cfg
import mod_EDT_AccessCTRL.EDT_AccessCTRL_cfg as ac_cfg

# Constants to run the REST api
PORT = 81
DEBUG = True

# Strings used to build the report to the HUB
STR_REPORT = 'Report'
STR_STATUS = 'Status'
STR_OK = 'OK'
STR_NOK = 'NOK'
STR_USER = 'User '
STR_NEW_USER = ' was added to the database.'
STR_PRESENT_USER = 'Users already present on the database: ['
STR_NO_USER = ' is not present on the database.'
STR_DELETED_USER = ' has been deleted.'
STR_UPDATED_USER = ' has been updated.'
STR_USERS_ADDED = 'UsersAdded'
STR_USERS_UPDATED = 'UsersUpdated'
STR_USERS_DELETED = 'UsersDeleted'
STR_EXISTING_USERS = 'ExistingUsers'
STR_FAILED_USERS = 'FailedUsers'
STR_FAILED_REPORTS = 'FailReports'
STR_FAILED_IMAGES = 'FailedImages'
STR_EXCEPTION = 'Exception'
STR_DECODING_EXCEPTION = 'Error while decoding. Error message: '
STR_ID = 'user_id'
STR_REPORT = 'report'

# Strings used for the Face ID algorithm
STR_FACE_ID = 'faceID'
STR_PATH = 'path'
STR_GENERAL_RESULT_STATUS = 'status'
STR_MODEL_FILE_PATH = 'UserFaceIDs.pkl'

# Strings used to access the information on the json object sent by the HUB
STR_USER_ID = 'sap_number' #new
STR_SAP_NUMBER = 'sap_number' #old
STR_NAME = 'name'
STR_LAST_NAME = 'last_name'
STR_MONITOR_ID = 'monitor_id'
STR_USER_TYPE = 'user_type'
STR_PHOTO_PATH = 'photo_path'

# Stings used to load the configuration
STR_SERVER_CFG_SECTION = 'SS_Configuration'
STR_LOCAL_IP = 'dba_ip'

# Variables used for ProTeUS Configurations
PRO_ACCESS_CODE = 'access_code'
PRO_HUB_URL = 'hub_url'
PRO_MAN_SERIAL_NUMBER = 'man_serial_number'
PRO_MAC_ADDRESS = 'mac_address'
PRO_ADDRESS = 'localhost'
PRO_HEADER = 'header'
PRO_IS_BOOL = 'isBool'
PRO_MSG_DATA = 'msgData'
PRO_SUCCESS = 'Success'
PRO_FAIL = 'Fail'
PRO_NOT_SUPPORTED = 'Not_Supported'
PRO_PORT = 6000
PRO_MANUFACTURING_SERVICE = 16
PRO_PRODUCT_SERVICE = 84
PRO_SESSION_OPEN = 2
PRO_SESSION_CLOSE = 4
PRO_SUBSERVICE_SECURITY_LVL_1 = 6
PRO_SUBSERVICE_SECURITY_LVL_2 = 10
PRO_SUBSERVICE_READ_MAN_SERIAL = 14
PRO_SUBSERVICE_READ_MAC = 18
PRO_SUBSERVICE_READ_HUB_URL = 52
PRO_SUBSERVICE_WRITE_HUB_URL = 54
PRO_SUBSERVICE_READ_AC = 60
PRO_SUBSERVICE_WRITE_AC = 62
PRO_UNUSED_BYTE = 255

# Enum used for different response codes
class ResponseCode(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    PROCESSING_ERROR = 422


# Enum used for ProTeUS response codes
class ProTeUSResponse(Enum):
    SER_NOT_SUPPORTED = 0
    SUB_NOT_SUPPORTED = 1
    OK = 2
    GENERAL_FAIL = 3
    WRONG_LENGTH = 4
    OUT_OF_RANGE = 5
    CANT_MODIFY = 6
    COM_NOT_SUPPORTED = 7
    PROTEUS_ERROR = 254
    CLIENT_ERROR = 255


# Load Face ID instance
faceIdentification = ST_FaceID(useTensorFlow=False)
result = faceIdentification.Load(ac_cfg.MODEL_FILE_PATH)
print(result)

# Assign the path to the document based on the platform running the script
if 'linux' == platform or 'linux2' == platform:

    USERS_DB_PATH = os.getcwd() + '/Users_Database/'
    USERS_DB_NAME = 'Users_Database'
    CONFIGURATION_FILE = 'Config_Test/SpecificServices/SS_CFG.txt'

elif 'win32' == platform:

    USERS_DB_PATH = 'C:\\Users_Database\\'
    USERS_DB_NAME = 'Users_Database'
    CONFIGURATION_FILE = 'Config_Test\\SpecificServices\\SS_CFG.txt'

# Load configuration
LOCAL_IP = ''
try:
    cfgParser = configparser.RawConfigParser()
    cfgParser.read(CONFIGURATION_FILE)
    LOCAL_IP = cfgParser.get(STR_SERVER_CFG_SECTION, STR_LOCAL_IP)
    print('-----------LOCAL_IP:' + str(LOCAL_IP))
except Exception as e:
    pass

if 1 >= len(LOCAL_IP):
    LOCAL_IP = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
    if LOCAL_IP == '':
        LOCAL_IP = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
    print('LOCAL_IP:' + str(LOCAL_IP))

app = Flask(__name__)
api = Api(app)


################################################################################
# Code for DBL_152
# Remove downloaded images.
################################################################################
# Method to remove downloaded images
def DeleteImages():
    try:
        with os.scandir(USERS_DB_PATH) as dirElements:
            i = 0
            for element in dirElements:
                if element.name.lower().endswith('.jpg'):
                    os.remove(USERS_DB_PATH + element.name)
    except Exception as exp:
        print('Error: ' + str(exp))


# Method to connect and interact with ProTeUS
def process_client(intData):
    try:
        data = bytes(intData)
        address = ('localhost', localPORT)

        with Client(address, authkey=b'password') as conn:
            conn.send(data)
            response = conn.recv()

    except Exception as exp:
        response = [PRO_UNUSED_BYTE, str(exp)]

    return response


# Class to hold the New User Endpoint's functions
class New_User(Resource):

    # Postman example:
    # http://localhost:81/New_User/
    # {
    #     "sap_number": 5398,
    #     "nombre": "Pablo Daniel",
    #     "apellido_paterno": "Mejia",
    #     "apellido_materno": "Flores",
    #     "monitor_id": 67399,
    #     "user_type": 1,
    #     "photo_path": "TBD"
    # }
    def post(self):

        # Variables used to build the response
        report = {STR_EXCEPTION: []}

        # List of objects to train the Face ID algorithm
        objectsToTrain = []

        # Collections used to handle incoming users
        # exceptionUsers = []
        trueNewUsers = []
        # existingUsers = []
        failedUsers = []
        # failedReports = []
        failedImages = {STR_EXCEPTION: [], STR_FAILED_REPORTS: []}
        newUsersDictionary = {}

        try:
            # If the database's folder does not exist, create it
            if not path.isdir(USERS_DB_PATH):
                os.mkdir(USERS_DB_PATH)

            # Extract the data from the json object
            jsonData = request.get_json(force=True)
            usersList = jsonData['users']

            # Check if new user exists on the database
            # If the user already exists, add to existingUsers list
            # Else, add the user to objectsToTrain list
            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:

                for newUser in usersList:
                    imageCounter = 0
                    ################################################################################
                    # Code for DBL_243
                    # Receive several photo paths.
                    ################################################################################
                    
                    for imagePath in newUser[STR_PHOTO_PATH]:
                        
                        try:
                            print(str(imagePath)) #DBL_292;DBL_293
                            if '_1' in imagePath:
                                imageCounter = 1
                            elif '_2' in imagePath:
                                imageCounter = 2
                            elif '_3' in imagePath:
                                imageCounter = 3
                            else:
                                print('ERROR EN LA imageCounter')

                            # Extract the image from the URL
                            ################################################################################
                            # Code for DBL_152
                            # Undo DBL_44's patch removal.
                            ################################################################################
                            respImage = requests.get(imagePath, stream=True, verify=False).content
                            imageFileName = USERS_DB_PATH + str(newUser[STR_USER_ID]) + '_' + str(imageCounter) + '.jpg'
                            newUserID = str(newUser[STR_USER_ID]) + '_' + str(imageCounter)
                            #imageCounter = imageCounter + 1
                            with open(imageFileName, 'wb') as imageFile:
                                imageFile.write(respImage)
                                
                            # Create the list of the users to add to the face ID algorithm
                            objectsToTrain.append({STR_FACE_ID: str(newUserID), #DBL_292;DBL_293
                                                   STR_PATH: imageFileName,
                                                   fid_cfg.KEY_HUB_PHOTO_PATH: imagePath})
                            
                            newUsersDictionary[str(newUser[STR_USER_ID])] = newUser

                        except Exception as exp:
                            # exceptionUsers.append(STR_USER + str(newUser[STR_USER_ID]) + ': ' + str(exp))
                            failedImages[STR_EXCEPTION].append({STR_PATH:   imagePath,
                                                                STR_REPORT: str(exp),
                                                                STR_ID:     int(newUser[STR_USER_ID])})

                # Train the Face ID algorithm with the objectsToTrain list
                if 0 < len(objectsToTrain):
                    try:
                        trainResult = faceIdentification.AddFaceIDs(ac_cfg.MODEL_FILE_PATH, objectsToTrain)

                        for result in trainResult:
                            if not result[fid_cfg.GENERAL_RESULT_STATUS]:
                                result[fid_cfg.GENERAL_RESULT_USER_ID] = result[fid_cfg.GENERAL_RESULT_USER_ID].split('_')[0]
                                failedUsers.append(int(result[fid_cfg.GENERAL_RESULT_USER_ID]))
                                # failedReports.append(result[fid_cfg.GENERAL_RESULT_COMMNENT])
                                # failedImages.append(result[fid_cfg.GENERAL_RESULT_HUB_PATH])
                                failedImages[STR_FAILED_REPORTS].append(
                                    {STR_PATH:   result[fid_cfg.GENERAL_RESULT_HUB_PATH],
                                     STR_REPORT: result[fid_cfg.GENERAL_RESULT_COMMNENT],
                                     STR_ID:     int(result[fid_cfg.GENERAL_RESULT_USER_ID])})
                            else:
                                result[fid_cfg.GENERAL_RESULT_USER_ID] = result[fid_cfg.GENERAL_RESULT_USER_ID].split('_')[0]
                                userDatabase[str(result[fid_cfg.GENERAL_RESULT_USER_ID])] = \
                                    newUsersDictionary[str(result[fid_cfg.GENERAL_RESULT_USER_ID])]
                                trueNewUsers.append(int(result[fid_cfg.GENERAL_RESULT_USER_ID]))

                    except Exception as exp:
                        # exceptionUsers.append(str(exp))
                        report[STR_EXCEPTION].append(str(exp))

            ################################################################################
            # Code for DBL_152
            # Remove downloaded images.
            ################################################################################
            DeleteImages()

            # report[STR_EXCEPTION] = exceptionUsers
            r = ResponseCode.OK.value

        except Exception as e:
            report[STR_EXCEPTION].append(str(e))
            r = ResponseCode.PROCESSING_ERROR.value

        report[STR_USERS_ADDED] = list(set(trueNewUsers))
        # report[STR_EXISTING_USERS] = existingUsers
        report[STR_FAILED_USERS] = list(set(failedUsers))
        # report[STR_FAILED_REPORTS] = failedReports
        report[STR_FAILED_IMAGES] = failedImages

        # Build the json response
        jsonResponse = report
        serviceResponse = json.dumps(jsonResponse)

        return serviceResponse, r


# Class to hold the Mod User Endpoint's functions
class Modify_User(Resource):

    # Postman example:
    # http://localhost:81/Mod_User/
    # {
    #     "sap_number": 5398,
    #     "nombre": "Pablo Daniel",
    #     "apellido_paterno": "Mejia",
    #     "apellido_materno": "Flores",
    #     "monitor_id": 67399,
    #     "user_type": 1,
    #     "photo_path": "TBD_1"
    # }
    def patch(self):

        # If the database's folder does not exist, create it
        if not path.isdir(USERS_DB_PATH):
            os.mkdir(USERS_DB_PATH)

        # Default response code
        r = ResponseCode.OK.value

        # Variables used to build the response
        report = {STR_EXCEPTION: []}

        # List of objects to train the Face ID algorithm
        objectsToTrain = []

        # Collections used to handle incoming users
        # exceptionUsers = []
        updatedUsers = []
        failedUsers = []
        # failedReports = []
        failedImages = {STR_EXCEPTION: [], STR_FAILED_REPORTS: []}
        updatedUsersDictionary = {}

        # Extract the data from the json object
        extractSuccess = False
        try:
            jsonData = request.get_json(force=True)
            usersList = jsonData['users']
            extractSuccess = True

            if extractSuccess:
                # Extract the image from the URL
                for modUser in usersList:
                    imageCounter = 1
                    ################################################################################
                    # Code for DBL_243
                    # Receive several photo paths.
                    ################################################################################
                    for imagePath in modUser[STR_PHOTO_PATH]:

                        ################################################################################
                        # Code for DBL_152
                        # Undo DBL_44's patch removal.
                        ################################################################################
                        try:
                            print(str(imagePath))  #DBL_292;DBL_293
                            if '_1' in imagePath:  
                                imageCounter = 1
                            elif '_2' in imagePath:
                                imageCounter = 2
                            elif '_3' in imagePath:
                                imageCounter = 3
                            else:
                                print('ERROR EN LA imageCounter')
                            respImage = requests.get(imagePath, stream=True, verify=False).content
                            imageFileName = USERS_DB_PATH + str(modUser[STR_USER_ID]) + '_' + str(imageCounter) + '.jpg'
                            modUserID = str(modUser[STR_USER_ID]) + '_' + str(imageCounter)
                            #imageCounter = imageCounter + 1
                            with open(imageFileName, 'wb') as imageFile:
                                imageFile.write(respImage)

                            # Create the list of the users to add to the face ID algorithm
                            objectsToTrain.append({STR_FACE_ID: str(modUserID),  #DBL_292;DBL_293
                                                   STR_PATH: imageFileName,
                                                   fid_cfg.KEY_HUB_PHOTO_PATH: imagePath})
                            updatedUsersDictionary[str(modUser[STR_USER_ID])] = modUser

                        except Exception as exp:
                            failedUsers.append(int(modUser[STR_USER_ID]))
                            # failedReports.append(STR_USER + str(modUser[STR_USER_ID]) + ': ' + str(exp))
                            # exceptionUsers.append(STR_USER + str(modUser[STR_USER_ID]) + ': ' + str(exp))
                            # failedImages.append(imagePath)
                            failedImages[STR_EXCEPTION].append({STR_PATH:   imagePath,
                                                                STR_REPORT: str(exp),
                                                                STR_ID:     int(modUser[STR_USER_ID])})

                if 0 < len(objectsToTrain):
                    # Retrain the face ID algorithm
                    trainResult = faceIdentification.UpdateFaceIDs(ac_cfg.MODEL_FILE_PATH, objectsToTrain)
                    with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                        # Inspect each of the update results
                        for result in trainResult:
                            # If the training fails, send report to the HUB
                            # Else, add user to the database and report success
                            if not result[fid_cfg.GENERAL_RESULT_STATUS]:
                                result[fid_cfg.GENERAL_RESULT_USER_ID] = result[fid_cfg.GENERAL_RESULT_USER_ID].split('_')[0]
                                failedUsers.append(int(result[fid_cfg.GENERAL_RESULT_USER_ID]))
                                # failedReports.append(result[fid_cfg.GENERAL_RESULT_COMMNENT])
                                # failedImages.append(result[fid_cfg.GENERAL_RESULT_HUB_PATH])
                                failedImages[STR_FAILED_REPORTS].append(
                                    {STR_PATH: result[fid_cfg.GENERAL_RESULT_HUB_PATH],
                                     STR_REPORT: result[fid_cfg.GENERAL_RESULT_COMMNENT],
                                     STR_ID: int(result[fid_cfg.GENERAL_RESULT_USER_ID])})
                            else:
                                result[fid_cfg.GENERAL_RESULT_USER_ID] = result[fid_cfg.GENERAL_RESULT_USER_ID].split('_')[0]
                                userDatabase[str(result[fid_cfg.GENERAL_RESULT_USER_ID])] = \
                                    updatedUsersDictionary[str(result[fid_cfg.GENERAL_RESULT_USER_ID])]
                                updatedUsers.append(int(result[fid_cfg.GENERAL_RESULT_USER_ID]))

        except Exception as exp:
            report[STR_EXCEPTION].append(STR_DECODING_EXCEPTION + str(exp))
            r = ResponseCode.PROCESSING_ERROR.value

        ################################################################################
        # Code for DBL_152
        # Remove downloaded images.
        ################################################################################
        DeleteImages()

        report[STR_USERS_ADDED] = list(set(updatedUsers))
        report[STR_FAILED_USERS] = list(set(failedUsers))
        # report[STR_FAILED_REPORTS] = failedReports
        # report[STR_EXCEPTION] = exceptionUsers
        report[STR_FAILED_IMAGES] = failedImages

        # Build the json response
        jsonResponse = report
        serviceResponse = json.dumps(jsonResponse)

        return serviceResponse, r

    # Postman example:
    # http://localhost:81/Mod_User/
    # {
    #     "sap_number": 5398
    # }
    def delete(self):

        # If the database's folder does not exist, create it
        if not path.isdir(USERS_DB_PATH):
            os.mkdir(USERS_DB_PATH)

        # Variables used to build the response
        report = {}

        # Collections used to handle incoming users
        deletedUsers = []
        failedUsers = []

        # Default response code
        r = ResponseCode.OK.value

        try:
            # Extract the data from the json object
            jsonData = request.get_json(force=True)
            usersList = jsonData['users']

            successDecoding = True

            # Retrain the face ID algorithm
            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                # Try to remove each user from both the db and pkl
                for delUser in usersList:
                    
                    try:

                        ################################################################################
                        # Code for DBL_67
                        # Always try to delete from FaceID first
                        ################################################################################
                        # Create a list to look for the ID in the Face ID model
                        idList = [str(delUser[STR_USER_ID]) + '_1', str(delUser[STR_USER_ID]) + '_11',
                                  str(delUser[STR_USER_ID]) + '_12', str(delUser[STR_USER_ID]) + '_13',
                                  str(delUser[STR_USER_ID]) + '_14', str(delUser[STR_USER_ID]) + '_0',
                                  str(delUser[STR_USER_ID]) + '_2', str(delUser[STR_USER_ID]) + '_3',
                                  str(delUser[STR_USER_ID])]
                        for id_to_remove in idList:
                            trainResult = faceIdentification.RemoveFaceID(ac_cfg.MODEL_FILE_PATH, str(id_to_remove))
                        
                        print(str(delUser[STR_USER_ID]))
                        if str(delUser[STR_USER_ID]) in userDatabase:
                            del userDatabase[str(delUser[STR_USER_ID])]

                        # Look for the ID in the db
                        if str(delUser[STR_USER_ID]) in userDatabase:
                            successDecoding = False



                        # Look for the ID in the Face ID model
                        for id in idList:
                            if id in faceIdentification.Model[fid_cfg.MODEL_FACE_LIST]:
                                successDecoding = False

                        if successDecoding:
                            deletedUsers.append(int(delUser[STR_USER_ID]))
                        else:
                            failedUsers.append(int(delUser[STR_USER_ID]))

                    except Exception as exp:
                        failedUsers.append(int(delUser[STR_USER_ID]))

        except Exception as exp:
            report[STR_EXCEPTION] = STR_DECODING_EXCEPTION + str(exp)
            r = ResponseCode.PROCESSING_ERROR.value

        report[STR_USERS_DELETED] = deletedUsers
        report[STR_FAILED_USERS] = failedUsers

        # Build the json response
        jsonResponse = report
        serviceResponse = json.dumps(jsonResponse)

        return serviceResponse, r


# Class to hold the Get Info Endpoint's functions
class Get_Info(Resource):

    # Postman example:
    # http://localhost:81/Get_Info/
    # {
    #     "sap_number": 5398
    # }
    def get(self):

        # Variables used to build the response
        report = ''

        try:
            # Extract the data from the json object
            jsonData = request.get_json(force=True)
            getUser = {STR_USER_ID: jsonData[STR_USER_ID]}

            # If the database's folder does not exist, create it
            if not path.isdir(USERS_DB_PATH):
                os.mkdir(USERS_DB_PATH)

            # Check if the user exists on the database
            # If the user exists, add the information of the user to the report
            # Else, report that the user is not present on the database
            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'r') as userDatabase:
                if str(getUser[STR_USER_ID]) in userDatabase:
                    report = userDatabase[str(getUser[STR_USER_ID])]
                    status = STR_OK
                    r = ResponseCode.OK.value
                else:
                    report = STR_USER + str(getUser[STR_USER_ID]) + STR_NO_USER
                    status = STR_NOK
                    r = ResponseCode.NO_CONTENT.value

        except Exception as e:
            report = str(e)
            status = STR_NOK
            r = ResponseCode.PROCESSING_ERROR.value

        # Build the json response
        jsonResponse = {STR_STATUS: status, STR_REPORT: report}
        serviceResponse = json.dumps(jsonResponse)
        return serviceResponse, r


# Class to hold the Configurations Endpoint's functions
class Configurations(Resource):

    def put(self):
        # Variables used to build the response
        report = {}
        successfulServices = []
        failedServices = []
        nonSupportedServices = []

        # Dictionaries used to manage specific services and manufacture services
        specificServices = {}
        manufactureServices = {}

        try:
            # Extract the data from the json object
            jsonData = request.get_json(force=True)

            # Go through all the elements on the service dictionary
            for service in jsonData:

                # Access Code Configuration
                if PRO_ACCESS_CODE == service:
                    # Create the information for the specific ProTeUS service
                    specificServices[service] = {PRO_HEADER: [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_WRITE_AC],
                                                 PRO_MSG_DATA: jsonData[service],
                                                 PRO_IS_BOOL: False}

                # HUB URL Configuration
                elif PRO_HUB_URL == service:
                    # Create the information for the specific ProTeUS service
                    specificServices[service] = {PRO_HEADER: [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_WRITE_HUB_URL],
                                                 PRO_MSG_DATA: jsonData[service],
                                                 PRO_IS_BOOL: False}

                else:
                    nonSupportedServices.append(service)

            # Process specific services first
            # Initiate session
            messageList = [PRO_PRODUCT_SERVICE, PRO_SESSION_OPEN]
            process_client(messageList)
            # Unlock security level 2
            messageList = [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_SECURITY_LVL_2]
            process_client(messageList)

            # Go through all the specific services
            for service in specificServices:
                # Check if the message is a string or a bool
                if specificServices[service][PRO_IS_BOOL] is False:

                    # Create the list to hold the data for ProTeUS
                    dataList = []

                    # Add the length of the message to the data list
                    dataList.append(len(jsonData[service]))

                    # Convert each character to int
                    for element in specificServices[service][PRO_MSG_DATA]:
                        dataList.append(ord(element))

                    # Merge the header with the data
                    serviceList = specificServices[service][PRO_HEADER] + dataList

                    # Send information to ProTeUS
                    resultList = process_client(serviceList)

                    # Check if the response was correct
                    # If it is not correct, check for errors or exceptions
                    if resultList[0] == specificServices[service][PRO_HEADER][0]:
                        if resultList[3] == 2:
                            successfulServices.append(service)
                        else:
                            failedServices.append(service)
                    elif resultList[0] == PRO_UNUSED_BYTE:
                        failedServices.append(service)

            # Close specific services session
            messageList = [PRO_PRODUCT_SERVICE, PRO_SESSION_CLOSE]
            process_client(messageList)

        except Exception as e:
            pass

        report[PRO_SUCCESS] = successfulServices
        report[PRO_FAIL] = failedServices
        report[PRO_NOT_SUPPORTED] = nonSupportedServices
        r = 200
        # Build the json response
        jsonResponse = report
        serviceResponse = json.dumps(jsonResponse)

        return serviceResponse, r

    def get(self):
        # Variables used to build the response
        report = {}
        nonSupportedServices = []

        # Dictionaries used to manage specific services and manufacture services
        specificServices = {}
        manufactureServices = {}
        try:
            # Extract the data from the json object
            jsonData = request.get_json(force=True)
            queryList = jsonData['query']

            # Go through all the elements on the service list
            for service in queryList:
                # Variable to proceed in case the service is supported
                isSupported = False

                # Access Code Reading
                if PRO_ACCESS_CODE == service:
                    # Create the information for the specific ProTeUS request
                    specificServices[service] = {PRO_HEADER: [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_READ_AC, 0],
                                                 PRO_IS_BOOL: False}

                # HUB URL Reading
                elif PRO_HUB_URL == service:
                    # Create the information for the specific ProTeUS request
                    specificServices[service] = {PRO_HEADER: [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_READ_HUB_URL, 0],
                                                 PRO_IS_BOOL: False}

                # Serial Number Reading
                elif PRO_MAN_SERIAL_NUMBER == service:
                    # Create the information for the specific ProTeUS request
                    manufactureServices[service] = {PRO_HEADER: [PRO_MANUFACTURING_SERVICE,
                                                    PRO_SUBSERVICE_READ_MAN_SERIAL, 0],
                                                    PRO_IS_BOOL: False}

                # MAC Address Reading
                elif PRO_MAC_ADDRESS == service:
                    # Create the information for the specific ProTeUS request
                    manufactureServices[service] = {PRO_HEADER: [PRO_MANUFACTURING_SERVICE,
                                                    PRO_SUBSERVICE_READ_MAC, 0],
                                                    PRO_IS_BOOL: False}

                else:
                    nonSupportedServices.append(service)

            # Process specific services first
            # Initiate session
            messageList = [PRO_PRODUCT_SERVICE, PRO_SESSION_OPEN]
            process_client(messageList)
            # Unlock security level 2
            messageList = [PRO_PRODUCT_SERVICE, PRO_SUBSERVICE_SECURITY_LVL_2]
            process_client(messageList)

            # Go through all the specific services
            for service in specificServices:
                # Check if the message is a string or a bool
                if specificServices[service][PRO_IS_BOOL] is False:
                    resultList = process_client(specificServices[service][PRO_HEADER])

                    # Check if the response was correct
                    # If it is not correct, check for errors or exceptions
                    if resultList[0] == specificServices[service][PRO_HEADER][0]:
                        if resultList[3] == 2:
                            # Convert the result to ascii
                            resultSTR = ''
                            for element in resultList:
                                resultSTR = resultSTR + chr(int(element))
                        else:
                            try:
                                resultSTR = ProTeUSResponse(resultList[3]).name
                            except Exception:
                                resultSTR = ProTeUSResponse.PROTEUS_ERROR.name

                    elif resultList[0] == PRO_UNUSED_BYTE:
                        resultSTR = ProTeUSResponse.CLIENT_ERROR.name

                    # Add the result to the report
                    report[service] = resultSTR

            # Close specific services session
            messageList = [PRO_PRODUCT_SERVICE, PRO_SESSION_CLOSE]
            process_client(messageList)

            # Process manufacture services last
            # Initiate session
            messageList = [PRO_MANUFACTURING_SERVICE, PRO_SESSION_OPEN]
            process_client(messageList)
            # Unlock security level 1
            messageList = [PRO_MANUFACTURING_SERVICE, PRO_SUBSERVICE_SECURITY_LVL_1]
            process_client(messageList)

            # Go through all the manufacture services
            for service in manufactureServices:
                # Check if the message is a string or a bool
                if manufactureServices[service][PRO_IS_BOOL] is False:
                    resultList = process_client(manufactureServices[service][PRO_HEADER])

                    # Check if the response was correct
                    # If it is not correct, check for errors or exceptions
                    if resultList[0] == manufactureServices[service][PRO_HEADER][0]:
                        if resultList[3] == 2:
                            # Convert the result to ascii
                            resultSTR = ''
                            for element in resultList:
                                resultSTR = resultSTR + chr(int(element))
                        else:
                            try:
                                resultSTR = ProTeUSResponse(resultList[3]).name
                            except Exception:
                                resultSTR = ProTeUSResponse.PROTEUS_ERROR.name

                    elif resultList[0] == PRO_UNUSED_BYTE:
                        resultSTR = ProTeUSResponse.CLIENT_ERROR.name

                    # Add the result to the report
                    report[service] = resultSTR

            # Close manufacture services session
            messageList = [PRO_MANUFACTURING_SERVICE, PRO_SESSION_CLOSE]
            process_client(messageList)

        except Exception:
            pass

        report[PRO_NOT_SUPPORTED] = nonSupportedServices
        r = 200
        # Build the json response
        jsonResponse = report
        serviceResponse = json.dumps(jsonResponse)

        return serviceResponse, r


# LOCAL_IP = 'localhost'
# LOCAL_IP = '[2806:103e:27:d63:4094:6f2a:bf0b:953c]'
# api.add_resource(EDT_Service, '/EDT_Service/<string:jsonUser>')
api.add_resource(Get_Info, "/Get_Info/")
api.add_resource(New_User, "/New_User/")
api.add_resource(Modify_User, "/Mod_User/")
api.add_resource(Configurations, "/Configurations/")
# app.run(debug=DEBUG, port=PORT)
app.run(host=LOCAL_IP, port=PORT)

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Sep-25-2020 Pablo Mejia
#   + DBL_43
#      - Created initial file.
#      - Adapt POST & PATCH to work with current ST_FACE_ID.
# Oct-23-2020 Pablo Mejia
#   + DBL_44
#      - Remove FaceID patch.
# Nov-12-2020 Pablo Mejia
#   + DBL_67
#      - Always try to delete user from FaceID.
#      - Added retry to delete user from model when it fails the first time.
# Nov-23-2020 Pablo Mejia
#   + DBL_152
#      - Undo DBL_44's patch removal.
#      - Remove downloaded images.
# Jan-25-2021 Pablo Mejia
#   + DBL_202
#      - Train existing users in POST.
#      - Accept multiple users for PATCH and DELETE.
#      - Pull LOCAL_IP from POST_CFG.txt.
# Feb-02-2021 Pablo Mejia
#   + DBL_208
#      - Read configuration from SS_CFG.txt.
# Feb-08-2021 Pablo Mejia
#   + DBL_212
#      - Re-install DBL_202 changes.
# Mar-31-2021 Pablo Mejia
#   + DBL_243
#      - Receive several photo paths for POST and PATCH.
# May-03-2021 Pablo Mejia
#   + DBL_259
#      - Add Configurations endpoint for ProTeUS functions.
#
# Junio 25 Lucia Chavez
#   + DBL_292; DBL_293
#      - Add multiple images to train to FaceID adding _
#########################################################################################
