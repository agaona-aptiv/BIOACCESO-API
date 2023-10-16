# Created on July 2020
# Author Pablo Mejia

#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: POST_Service
#          Program: POST service
#          Enterprise: Condumex
#          SW Developer: Pablo Mejia
#          FILE DESCRIPTION
#          File: POST_Service.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################
# from flask import json
import requests
import datetime
import time
import os
import queue
import multiprocessing as mp
from enum import Enum
import signal
import shelve
import sys
from sys import platform
import configparser
from uuid import getnode
from inspect import currentframe
from threading import Timer  # DBL_198

from Config_Test.EDT_Debug import EDT_Logger

# Add to path modules located in different folders
sys.path.append(os.getcwd())

# Request parameters
PORT = "81"

#***********************
from bmp280 import BMP280
from smbus2 import SMBus
from time import sleep
from mod_Temperature.ST_Temperature import *
#******************

# Logger 
def Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('post', debug_line, text)
    

#************************************************************************************************************************
def Room_Temp_Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('room_temp', debug_line, text)
#************************************************************************************************************************
   

REQUEST_TIMEOUT = (3, 3)  # 3 second to connect, 3 second to receive response
REQUEST_TIMEOUT_POST_PENDING = (3, 6)
HUB_Service = '/records/register'
HUB_Service_Pending_User = '/records/pending'
HUB_Service_Token = '/auth/device'
HUB_Service_Date = '/device/date'
HUB_Service_Room_Temperature = '/weather'  # DBL_198 GET endpoint for room temperature
REQUEST_ROOM_TEMPERATURE_TIME = 900  # DBL_198 Room temperature should be requested every 15 minutes (900 seconds)
MAX_PENDING_USERS = 1000

# Strings used to generate the information on the json object sent to the HUB (POST request)
STR_SAP_NUMBER = "sap_number"
STR_MONITOR_ID = "monitor_id"
STR_USER_TYPE = "user_type"
STR_TEMPERATURE = "temperature"
STR_MASK = "mask"
STR_DATE_TIME = "date_time"
STR_AUTH_ACCESS = "authorized_access"
STR_DEVICE_ID = "device_id"

# Strings used to access the information on the json object sent by MAIN Process
STR_SAP_NUMBER_M = 'userID'
STR_MONITOR_ID_M = 'monitorID'
STR_USER_TYPE_M = 'userType'
STR_TEMPERATURE_M = 'temp'
STR_MASK_M = 'mask'
STR_AUTH_ACCESS_M = 'authorizedAccess'
STR_DEVICE_ID_M = 'DeviceID'

# Strings used to load configuration
STR_POST_CFG_SECTION_SS = 'SS_Configuration'
STR_POST_CFG_SECTION_MAN = 'MAN_Configuration'
STR_MAC_ADDRESS = 'mac_address'
STR_ACCESS_CODE = 'access_code'
STR_HUB_URL = 'hub_url'

# Strings used to access the information on the json object sent by the HUB (Token Response)
STR_TOKEN = 'token'
STR_DEVICE = 'device'

# String used to access the HUB timestamp
STR_TIMESTAMP = 'timestamp'

# Assign the path to the document based on the platform running the script
if 'linux' == platform or 'linux2' == platform:

    USERS_DB_PATH = os.getcwd() + '/Users_Not_Reported/'
    USERS_DB_NAME = 'Users_Not_Reported'
    CONFIGURATION_FILE = 'POST_Test/POST_CFG.txt'
    CONFIGURATION_FILE_SS = 'Config_Test/SpecificServices/SS_CFG.txt'
    CONFIGURATION_FILE_MAN = 'Config_Test/Manufacturing/MAN_CFG.txt'

    # DBL_198 File to save room temperature
    ROOM_TEMP_DB_PATH = os.getcwd() + '/mod_Temperature/'
    ROOM_TEMP_DB_NAME = 'Room_Temperature.txt'

elif 'win32' == platform:

    USERS_DB_PATH = 'C:\\Users_Not_Reported\\'
    USERS_DB_NAME = 'Users_Not_Reported'
    CONFIGURATION_FILE = 'POST_Test\\POST_CFG.txt'
    CONFIGURATION_FILE_SS = 'Config_Test\\SpecificServices\\SS_CFG.txt'
    CONFIGURATION_FILE_MAN = 'Config_Test\\Manufacturing\\MAN_CFG.txt'

    # DBL_198 File to save room temperature
    ROOM_TEMP_DB_PATH = 'C:\\mod_Temperature\\'
    ROOM_TEMP_DB_NAME = 'Room_Temperature.txt'

try:
    cfgParser = configparser.RawConfigParser()
    cfgParser.read(CONFIGURATION_FILE_SS)
    URL = cfgParser.get(STR_POST_CFG_SECTION_SS, STR_HUB_URL)
except Exception as exp:
    Logger('Could not load configuration from file. Exception: ' + str(exp))

# HUB type and Proxy
# Remove when not using VPN/proxy
IsTest = False
ProxyEnabled = False
ProxyRequest = {'http': 'http://user:password@proxy-amer.delphiauto.net:8080'}


# Enum used for different response codes
class ResponseCode(Enum):
    OK = 200
    UNAUTHORIZED = 401
    SERVICE_UNAVAILABLE = 503


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class PostService:
    def __init__(self):

        try:
            cfgParser = configparser.RawConfigParser()
            cfgParser.read(CONFIGURATION_FILE_SS)
            self.Access_Code = cfgParser.get(STR_POST_CFG_SECTION_SS, STR_ACCESS_CODE)

            cfgParser.read(CONFIGURATION_FILE_MAN)
            self.MAC_address = cfgParser.get(STR_POST_CFG_SECTION_MAN, STR_MAC_ADDRESS)
            self.Device = cfgParser.get(STR_POST_CFG_SECTION_MAN, STR_MAC_ADDRESS)
            self.PostDataQueue = None
            self.URL_RAW = None
            self.PORT = PORT
            self.HUB_Service = HUB_Service
            self.HUB_Service_Pending_User = HUB_Service_Pending_User
            self.HUB_Service_Token = HUB_Service_Token
            self.failedPostUsers = []
            self.tokenInfo = {}
            self.Token = "TokenR"
            self.reqRoomTempAllow = True  # DBL_198 Flag to allow the room temperature request
            self.reqRoomTempTimer = Timer(REQUEST_ROOM_TEMPERATURE_TIME, self.ReqRoomTempTimeout)
            self.tb = ST_Temperature.getInstance()
            Logger('Init Finished.')

        except Exception as e:
            self.MAC_address = str(hex(getnode())).upper().replace('0X', '')
            self.Access_Code = ' '
            self.Device = str(hex(getnode())).upper().replace('0X', '')
            self.PostDataQueue = None
            self.URL_RAW = None
            self.PORT = PORT
            self.HUB_Service = HUB_Service
            self.HUB_Service_Pending_User = HUB_Service_Pending_User
            self.HUB_Service_Token = HUB_Service_Token
            self.failedPostUsers = []
            self.tokenInfo = {}
            self.Token = "TokenR"
            self.reqRoomTempAllow = True  # DBL_198 Flag to allow the room temperature request
            self.reqRoomTempTimer = Timer(REQUEST_ROOM_TEMPERATURE_TIME, self.ReqRoomTempTimeout)
            Logger('Init Failed. Using default values. Exception: ' + str(e))

    def postMain(self, conn):
        # Request Token and send feedback to main process about conexion state
        # Create the full URL and attempt to send token request to HUB

        try:
            # IsTest is used  when using IP address for testing
            if IsTest:
                URL_BASE = "https://[" + self.URL_RAW + ']:81/'  # add s https
            else:
                URL_BASE = self.URL_RAW
            Logger('Requesting token from HUB @ ' + URL_BASE)
            HUB_Response = self.requestToken(URL_BASE)
            # Send to main process status code of token request
            conn.send(HUB_Response)
            conn.close()
            Logger('Token Response: ' + str(HUB_Response))
        except Exception as e:
            URL_BASE = self.URL_RAW
            Logger('Error while requesting Token from postMain. Exception: ' + str(e))

        ################################################################################
        # Code for DBL_30
        # Request date and time from HUB
        ################################################################################
        # Request HUB's date
        try:
            Logger('Requesting date from HUB @ ' + URL_BASE)
            GET_URL = URL_BASE + HUB_Service_Date
            rDate = requests.get(url=GET_URL, timeout=REQUEST_TIMEOUT, auth=BearerAuth(self.Token),
                                 verify=False)  # add verify False SSL
            # Logger('ssl ' + str(rDate))
            hubDate = rDate.json()
            hubTS = hubDate[STR_TIMESTAMP]

            # Set system's timestamp
            time.clock_settime(0, hubTS)
            Logger('Datetime set with timestamp: ' + str(hubTS))
            
            ################################################################################
            # Code for DBL_254
            # Send pending users after initial setup.
            ################################################################################
            if ResponseCode.OK.value == rDate.status_code:
                Logger('Looking for failed users to post.')
                self.postPendingUsers(URL_BASE)
                    
        except Exception as e:
            Logger('Set of datetime failed. Exception: ' + str(e))

        while True:

            # Get  one queue element
            userInfo = {}

            try:
                post_request = self.PostDataQueue.get(block=False)
            except queue.Empty:
                pass
            except Exception as e:
                Logger('Error while getting user from queue. Exception: ' + str(e))
            else:
                try:
                    if post_request is not None:
                        # Read current date and time for the timestamp
                        currentTime = datetime.datetime.now().timestamp()
                        # Generate userInfo according to HUB keys
                        userInfo = {STR_SAP_NUMBER: int(post_request['userID']),
                                    STR_MONITOR_ID: str(post_request['monitorID']),
                                    STR_USER_TYPE: int(post_request['userType']),
                                    STR_TEMPERATURE: int(post_request['temp']),
                                    STR_MASK: int(post_request['mask']),
                                    STR_DATE_TIME: int(currentTime),
                                    STR_AUTH_ACCESS: bool(post_request['authorizedAccess']),
                                    STR_DEVICE_ID: str(self.Device)}
                        self.PostDataQueue.task_done()
                        Logger('User taken from queue: ' + str(userInfo))
                except Exception as e:
                    Logger('Error while building userInfo. Exception: ' + str(e))

            # Open/create pending users file
            # Post single user
            try:
                if len(userInfo) > 0:
                    HUB_Response = self.postSingleUser(URL_BASE, userInfo)
                    # If token has expired, request new token/ device ID and attempt to post user again
                    if ResponseCode.UNAUTHORIZED.value == int(HUB_Response):
                        HUB_Token_Response = self.requestToken(URL_BASE)
                        if ResponseCode.OK.value == int(HUB_Token_Response):
                            HUB_Response = self.postSingleUser(URL_BASE, userInfo)
                            Logger('POST response from HUB: ' + str(HUB_Response))
                    # If the request was successful, send pending users
                    if ResponseCode.OK.value == int(HUB_Response):
                        Logger('Looking for failed users to post.')
                        self.postPendingUsers(URL_BASE)
                    else:
                        # Add userInfo to Users_Not_Reported
                        try:
                            Logger('Saving to Users_Not_Reported.')
                            if not os.path.isdir(USERS_DB_PATH):
                                os.mkdir(USERS_DB_PATH)
                            # Else, add the user to objectsToTrain list
                            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                                userDatabase[str(userInfo['sap_number']) + '_' + str(userInfo['date_time'])] = userInfo
                            Logger('Saved to Users_Not_Reported.')
                        except Exception as e:
                            Logger('Error while saving to Users_Not_Reported. Exception: ' + str(e))

                time.sleep(2)
            except Exception as e:
                Logger('General error while posting userInfo. Exception: ' + str(e))

            ########################################################################################################
            # DBL_198 - Implementing request for getting the room temperature from HUB service
            try:
                if self.reqRoomTempAllow:
                    # Request HUB's room temperature
                    try:
                        self.StartReqRoomTempTimer(REQUEST_ROOM_TEMPERATURE_TIME)
                        Logger('Requesting room temperature from HUB @ ' + URL_BASE)
#************************************************************************************************************************
# Change for debugging. Save timestamp of the room temperature.
# REMOVE THIS CODE AFTER COMPLETING THE TEST
                        try:
                            #BMP280s
                            #****************************************************************************************
                            bus = SMBus(1)
                            bmp280 = BMP280(i2c_dev=bus)
                            tbmp = bmp280.get_temperature()
                            #****************************************************************************************
                            Logger('Requesting  bmp temperature ' + str(tbmp))
                        except Exception as e:
                            Logger("Exception bmp: " +str(e))
                        
                        temp_tb = self.tb.GetAmbientTemperature()
                        Logger('Requesting  MLX_junction ' + str(temp_tb))
                        
                        Room_Temp_Logger('BMP TEMPERATURE: ' + str(tbmp) + ' TB TEMPERATURE: ' + str(temp_tb))
#************************************************************************************************************************
                        GET_ROOM_TEMP_URL = URL_BASE + HUB_Service_Room_Temperature
                        rRoomTemp = requests.get(url=GET_ROOM_TEMP_URL, timeout=REQUEST_TIMEOUT,
                                                 auth=BearerAuth(self.Token), verify=False)
                        ################################################################################
                        # Code for DBL_229
                        # Request Token when expired.
                        ################################################################################
                        if ResponseCode.UNAUTHORIZED.value == int(rRoomTemp.status_code):
                            HUB_Token_Response = self.requestToken(URL_BASE)
                            if ResponseCode.OK.value == int(HUB_Token_Response):
                                rRoomTemp = requests.get(url=GET_ROOM_TEMP_URL, timeout=REQUEST_TIMEOUT,
                                                         auth=BearerAuth(self.Token), verify=False)
                                hubRoomTemp = rRoomTemp.json()
                        else:
                            hubRoomTemp = rRoomTemp.json()

                        # Store info to file
                        Logger('Downloading room temperature to file!')
                        cfgParser = configparser.RawConfigParser()
                        if not os.path.exists(ROOM_TEMP_DB_PATH + ROOM_TEMP_DB_NAME):
                            if not os.path.isdir(ROOM_TEMP_DB_PATH):
                                os.mkdir(ROOM_TEMP_DB_PATH)

                            cfgParser.add_section('Room Temperature')
                        else:
                            cfgParser.read(ROOM_TEMP_DB_PATH + ROOM_TEMP_DB_NAME)

                        for key in hubRoomTemp:
                            cfgParser.set('Room Temperature', key, hubRoomTemp[key])

                        with open(ROOM_TEMP_DB_PATH + ROOM_TEMP_DB_NAME, 'w') as roomTempFile:
                            cfgParser.write(roomTempFile)
                            
                        Room_Temp_Logger('Service TEMPERATURE: ' + str(hubRoomTemp['temperature']))
                        Logger('Room temperature was updated successful!' + str(hubRoomTemp['temperature']))

                    except Exception as exp1:
                        Logger('Exception while processing the room temperature: ' + str(exp1))

            except Exception as e:
                Logger('General error while setting room temperature. Exception: ' + str(e))

            ########################################################################################################

    def postSingleUser(self, URL_BASE, userInfo):
        # Create the full URL and attempt to send ONE post request to HUB
        r = requests.Response
        try:
            POST_URL = URL_BASE + self.HUB_Service
            if ProxyEnabled:
                r = requests.post(url=POST_URL, proxies=ProxyRequest, json=userInfo, timeout=REQUEST_TIMEOUT,
                                  auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
            else:
                r = requests.post(url=POST_URL, json=userInfo, timeout=REQUEST_TIMEOUT, auth=BearerAuth(self.Token),
                                  verify=False)  # add verify False SSL
        except Exception as e:
            # print('Can\'t connect to HUB.\nException: ' + str(e))
            Logger('Single user post error. Exception: ' + str(e))
            r.status_code = ResponseCode.SERVICE_UNAVAILABLE.value
        # print("Single user response: " + str(r.status_code))

        return r.status_code

    def postPendingUsers(self, URL_BASE):
        # Post 1000 pending users
        # Read failed user request file
        userList = []

        try:
            if not os.path.isdir(USERS_DB_PATH):
                os.mkdir(USERS_DB_PATH)
            # Else, add the user to objectsToTrain list
            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                # Obtain UserInfo for 1000 pending requests
                for index, user in enumerate(userDatabase):
                    pendingUserInfo = userDatabase[user]
                    userList.append(pendingUserInfo)
                    Logger('Loading pending user: ' + str(pendingUserInfo))
                    if index == MAX_PENDING_USERS:
                        break
        except Exception as e:
            Logger('Error while loading pending users. Exception: ' + str(e))

        r = requests.Response
        try:
            if len(userList) > 0:
                try:
                    POST_URL = URL_BASE + self.HUB_Service_Pending_User
                    if ProxyEnabled:
                        r = requests.post(url=POST_URL, proxies=ProxyRequest, json=userList,
                                          timeout=REQUEST_TIMEOUT_POST_PENDING,
                                          auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
                    else:
                        r = requests.post(url=POST_URL, json=userList, timeout=REQUEST_TIMEOUT_POST_PENDING,
                                          auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
                        Logger('Pending users POST HUB response: ' + str(r.status_code))
                except Exception as e:
                    # print('Can\'t connect to HUB.\nException: ' + str(e))
                    Logger('Exception: ' + str(e))
                    r.status_code = ResponseCode.SERVICE_UNAVAILABLE.value

                # Remove users from pending list if request was successful
                if ResponseCode.OK.value == int(r.status_code):
                    with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                        for user in userList:
                            userDatabase.pop(str(user['sap_number']) + '_' + str(user['date_time']))
                            Logger('Removing from Users_Not_Reported: ' + str(user))

                status = r.status_code
            else:
                Logger('No pending users.')
                status = "No pending users"
        except Exception as e:
            Logger('General error while posting pending users. Exception: ' + str(e))

        # print("Pending user response: " + str(status))
        return status

    def requestToken(self, URL_BASE):
        try:
            r = requests.Response
            try:
                tokenURL = URL_BASE + self.HUB_Service_Token
                self.tokenInfo = {STR_MAC_ADDRESS: self.MAC_address,
                                  STR_ACCESS_CODE: self.Access_Code}
                if ProxyEnabled:
                    r = requests.get(url=tokenURL, proxies=ProxyRequest, json=self.tokenInfo, timeout=REQUEST_TIMEOUT,
                                     verify=False)  # add verify False SSL
                else:
                    r = requests.post(url=tokenURL, json=self.tokenInfo, timeout=REQUEST_TIMEOUT,
                                      verify=False)  # add verify False SSL
            except Exception as e:
                print('Can\'t connect to HUB.\nException: ' + str(e))
                r.status_code = ResponseCode.SERVICE_UNAVAILABLE.value
            # If the request was successful, save token
            if ResponseCode.OK.value == int(r.status_code):
                token_Response = r.json()
                self.Token = token_Response[STR_TOKEN]
        except Exception as e:
            Logger('General error while requesting token. Exception: ' + str(e))

        return r.status_code

    ########################################################################################################
    # DBL_198 - Implementing request for getting the room temperature from HUB service
    def StartReqRoomTempTimer(self, timeLimit=900):
        try:
            self.StopReqRoomTempTimer()
            if timeLimit > 0:
                self.reqRoomTempTimer = Timer(timeLimit, self.ReqRoomTempTimeout)
                self.reqRoomTempTimer.start()
                Logger('Starting new request room temperature timer with limit {0}'.format(timeLimit))
        except Exception as e:
            Logger('StartReqRoomTempTimer error: ' + str(e))

    def StopReqRoomTempTimer(self):
        try:
            self.reqRoomTempAllow = False
            if self.reqRoomTempTimer.is_alive():
                Logger('Request room temperature timer is alive, stoping it')
                self.reqRoomTempTimer.cancel()
                self.reqRoomTempTimer.join()
        except Exception as e:
            Logger('StopReqRoomTempTimer error: ' + str(e))

    def ReqRoomTempTimeout(self):
        try:
            Logger('Request room temperature timeout')
            self.reqRoomTempAllow = True
        except Exception as e:
            Logger('ReqRoomTempTimeout error: ' + str(e))
    ########################################################################################################


class PostProcessHandler:
    dataQueue = None
    PostServiceInst = None
    PostServiceProcess = None

    @classmethod
    def Init(cls):
        # Initialize: Queue,  PostService instance , Post Service process, Pipe
        # Return: HUB response, POST process ID, POST process status
        cls.dataQueue = mp.JoinableQueue()
        cls.PostServiceInst = PostService()
        # This is a config parameter, pending to define how to read/import, is PORT going to be a confing parameter TODO: Define method to read this parameter
        cls.PostServiceInst.URL_RAW = URL
        cls.PostServiceInst.PostDataQueue = cls.dataQueue
        parent_conn, child_conn = mp.Pipe()
        # Start Process
        cls.PostServiceProcess = mp.Process(target=cls.PostServiceInst.postMain, args=(child_conn,))
        cls.PostServiceProcess.daemon = True
        cls.PostServiceProcess.start()
        # Obtain first HUB response
        HUB_Response = parent_conn.recv()
        # If the database's folder does not exist, create it
        try:
            if not os.path.isdir(USERS_DB_PATH):
                os.mkdir(USERS_DB_PATH)
            # Else, add the user to objectsToTrain list
            with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                pass
        except Exception as e:
            Logger('Error while creating users DB. Exception: ' + str(e))

        return HUB_Response, cls.PostServiceProcess, cls.PostServiceProcess.is_alive()

    @classmethod
    def is_alive(cls):
        return cls.PostServiceProcess.is_alive()

    @classmethod
    def Shutdown(cls):
        # Stop and delete: POST process, Queue,  POST Service instance
        # Return: POST process status
        # Terminate Process
        Logger('++++++++++ SHUT DOWN ++++++++++')
        cfgParser = configparser.RawConfigParser()
        cfgParser.read(CONFIGURATION_FILE_MAN)
        MAC = cfgParser.get(STR_POST_CFG_SECTION_MAN, STR_MAC_ADDRESS)
        if 'linux' == platform or 'linux2' == platform:
            pid = cls.PostServiceProcess.pid
            os.kill(int(pid), signal.SIGTERM)
        elif 'win32' == platform:
            cls.PostServiceProcess.terminate()
        # Wait process to finish
        while cls.PostServiceProcess.is_alive():
            pass
        queueElemCount = 0
        # TODO:Change to while queue not empty once strategy for calling shutdown is defined
        while queueElemCount < 100:
            try:

                post_request = cls.dataQueue.get(block=False)

            except queue.Empty:
                break
            else:
                if post_request is not None:
                    # Read current date and time for the timestamp
                    currentTime = datetime.datetime.now().timestamp()
                    # Generate userInfo according to HUB keys
                    userInfo = {STR_SAP_NUMBER: int(post_request['userID']),
                                STR_MONITOR_ID: str(post_request['monitorID']),
                                STR_USER_TYPE: int(post_request['userType']),
                                STR_TEMPERATURE: int(post_request['temp']),
                                STR_MASK: int(post_request['mask']),
                                STR_DATE_TIME: int(currentTime),
                                STR_AUTH_ACCESS: bool(post_request['authorizedAccess']),
                                STR_DEVICE_ID: str(MAC)}
                    # Add userInfo to Users_Not_Reported
                    try:
                        if not os.path.isdir(USERS_DB_PATH):
                            os.mkdir(USERS_DB_PATH)
                        # Else, add the user to objectsToTrain list
                        with shelve.open(USERS_DB_PATH + USERS_DB_NAME, 'c') as userDatabase:
                            userDatabase[str(userInfo['sap_number']) + '_' + str(userInfo['date_time'])] = userInfo
                    except Exception as e:
                        print(e)
                    cls.dataQueue.task_done()
                queueElemCount = queueElemCount + 1

        # Delete POSTService:
        del cls.PostServiceInst
        return cls.PostServiceProcess.is_alive()


if __name__ == "__main__":
    # Inicializar POST
    result = PostProcessHandler.Init()
    print(result)
    n = 5000
    while (n < 5050):
        time.sleep(1)
        # Add elements to shared queue

        userInfo = {STR_SAP_NUMBER_M: n,
                    STR_MONITOR_ID_M: "89333",
                    STR_USER_TYPE_M: 1,
                    STR_TEMPERATURE_M: 379,
                    STR_MASK_M: 1,
                    STR_AUTH_ACCESS_M: False,
                    STR_DEVICE_ID_M: "12:B3:07:76:D6:22"}

        PostProcessHandler.dataQueue.put(userInfo)
        print(str(n) + " queued")
        n = n + 1
    # Stop and finish POST process
    shutdown = PostProcessHandler.Shutdown()
    # Print post process status (must be False)
    print(shutdown)
    time.sleep(2)
    # Request POST process status (must be False)
    print(PostProcessHandler.PostServiceProcess, PostProcessHandler.PostServiceProcess.is_alive())

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Sep-30-2020 Pablo Mejia/Lucero Buenrostro
#   + Created initial file.
#
# Oct-12-2020 Pablo Mejia
#   + DBL_68:
#      - Pull POST critical from POST_CFG.txt.
#
# Oct-23-2020 Pablo Mejia
#   + DBL_30:
#      - Request time and date from HUB and save it to system.
#
# Oct-29-2020 Pablo Mejia
#   + DBL_111:
#      - Rest service improvements, added try/except when setting date, and logger added.
# 16 Noviembre 2020 Lucia Chavez
#         Add  verify False in responses.
#
# Jan-20-2021 Leobardo N Hernandez
#   + DBL_198:
#      - Added the code for requesting the room temperature to the HUB every 15 minutes.
#
# Jan-26-2021 Leobardo N Hernandez
#   + DBL_198:
#      - Added initialization of the timer variable used for requesting room temperature.
#
# Feb-02-2021 Pablo Mejia
#   + DBL_208:
#      - Read configuration from SS_CFG.txt and MAN_CFG.txt.
#
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225:
#      - Updated function Logger().
#
# Mar-04-2021 Leobardo N Hernandez
#   + DBL_229:
#      - Request Token when expired for temperature.
#
# Mar-10-2021 Pablo Mejia
#   + DBL_235:
#      - Protect unprotected code.
#      - Improve Logger descriptions.
#
# Mar-18-2021 Leobardo N Hernandez
#   + DBL_235:
#      - Updated Logger function to use the common EDT_Logger.
#
# Mar-18-2021 Leobardo N Hernandez
#   + DBL_235:
#      - Changed SERVICEUNAVAILABLE by SERVICE_UNAVAILABLE.
#
# Apr-22-2021 Pablo Mejia
#   + DBL_254:
#      - Send pending users after initial setup
#Junio BMP
#   + DBL_286:
#      -BMP.
#    DBL_319
#       TryCatch in TA using BMP or service information 
#
# Febrero-2022 Arturo Gaona
#   + DBL_323_PostServiceProcess Is_alive issue
#       - Check that PostServiceProcess is alive to send the post
#       - Improve resize method considering isometric projection
#########################################################################################
