#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: BioAccess User lost post 
#          Program: POST service
#          Enterprise: Condumex
#          SW Developer: Arturo Gaona
#          FILE DESCRIPTION
#          File: POST_Users.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#########################################################################################
# from flask import json
import requests
import datetime
import time
import os
from enum import Enum
import shelve
import sys
import configparser
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Add to path modules located in different folders
sys.path.append(os.getcwd())

REQUEST_TIMEOUT = (3, 3)  # 3 second to connect, 3 second to receive response
REQUEST_TIMEOUT_POST_PENDING = (3, 6)
HUB_Service = '/records/register'
HUB_Service_Pending_User = '/records/pending'
HUB_Service_Token = '/auth/device'
HUB_Service_Date = '/device/date'
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

# Strings used to generate the information on the json object sent to the HUB (Token request)
STR_MAC_ADDRESS = "mac_address"
STR_ACCESS_CODE = "access_code"

# Strings used to access the information on the json object sent by the HUB (Token Response)
STR_TOKEN = "token"
STR_DEVICE = "device"

# Strings used to access the POST configuration
STR_POST_CFG_SECTION = 'POST_Configuration'
STR_SERVER_CFG_SECTION = 'SERVER_CONFIGURATION'
STR_HUB_URL = 'hub_url'

# HUB type and Proxy
# Remove when not using VPN/proxy
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
        print(token)

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class PostService:
    def __init__(self,MAC_address = '48:B0:2D:15:E4:26',Access_Code = '25d972a06e15afff70caffad2c258a92a1a9d154513ed251e46a3b5d708d3403', hub_name_or_IP = '157.55.183.132'):
        url_base='https://'+ hub_name_or_IP +'/sba_hub/API/public/index.php/api/v1/hubapi'
        print('Init Start with Default values.')
        self.URL_Base = url_base
        self.HUB_IP = hub_name_or_IP
        self.MAC_address = MAC_address
        self.Access_Code = Access_Code
        self.Device = MAC_address
        self.PostDataQueue = None
        self.URL_RAW = None
        self.HUB_Service = HUB_Service
        self.HUB_Service_Pending_User = HUB_Service_Pending_User
        self.HUB_Service_Token = HUB_Service_Token
        self.failedPostUsers = []
        self.tokenInfo = {}
        self.Token = "TokenR"
        print('URL_Base:',self.URL_Base)
        print('HUB_IP:',self.HUB_IP)
        print('MAC_address:',self.MAC_address)
        print('Access_Code:',self.Access_Code)
        print('Device:',self.Device)
        print('HUB_Service:',self.HUB_Service)
        print('HUB_Service:',self.HUB_Service)
        print('HUB_Service_Pending_User:',self.HUB_Service_Pending_User)
        print('Initial values Finished.')

    def postLogUsers(self, device_user_list):
        # Post Registers_Lost.xlsx users
        # Read failed user request file
        try:
            userList = device_user_list
            print('Users to process: ',len(userList))
            if len(userList) > 0:
                r = self.requestToken()
                time.sleep(3)                
                print('Posting users.')
                POST_URL = self.URL_Base + self.HUB_Service_Pending_User
                r = requests.post(url=POST_URL, json=userList, timeout=REQUEST_TIMEOUT_POST_PENDING,
                                  auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
                print('Log POST Code: ' + str(r.status_code))
            else:
                print('No users found.')
                r = requests.Response
                r.status_code = 0

        except Exception as exp:
            print('Exception: ' + str(exp))

        return r.status_code

    def requestToken(self):
        url_base='https://'+ self.HUB_IP +'/sba_hub/API/public/index.php/api/v1/hubapi'
        r = requests.Response
        try:
            tokenURL = url_base + self.HUB_Service_Token
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

        print("Token response: " + str(r.status_code))
        return r.status_code


if __name__ == "__main__":
    #Explore current directory for EDT logs
    pd_users = pd.read_excel('Registros_Perdidos.xlsx')
    pd_devices_info = pd.read_excel('dispositivos.xlsx')
    pd_usuarios_info = pd.read_excel('usuarios.xlsx')
    devices = pd_users.device.unique()
    for device in devices:
        # Create instance of PostService
        #pass pd_devices_info as parameter 
        mac_address = pd_devices_info[pd_devices_info['IP_Address'] == device]['MAC_Address'].values[0]
        access_code= pd_devices_info[pd_devices_info['IP_Address'] == device]['Access_Code'].values[0]
        hub_IP= pd_devices_info[pd_devices_info['IP_Address'] == device]['hub_name_or_IP'].values[0]
        postServiceInst = PostService(MAC_address = mac_address,Access_Code = access_code, hub_name_or_IP = hub_IP)
        print('processing pending users from :', device)
        pd_users_in_device = pd_users[pd_users['device'] == device]
        collectedUsers = []
        for i in range(0,len(pd_users_in_device)):
            #print('Reading users from Registers_Lost.xlsx.')
            device = str(pd_users_in_device['device'].iloc[i]).strip()
            userID = str(pd_users_in_device['user_id'].iloc[i]).strip()
            temperature = int(pd_users_in_device['body_temperature'].iloc[i] * 10)
            registerTime = str(pd_users_in_device['date_time'].iloc[i]).strip()
            registerTime = int(datetime.datetime.timestamp(datetime.datetime.strptime(registerTime, '%Y-%m-%d %H:%M:%S.%f')))
            collectedUsers.append({'device':device,'userID': userID, 'temperature': temperature, 'timestamp': registerTime})
        userList=[]
        for user in collectedUsers:
            #if user['userID'] in userDatabase:
            pd_users[pd_users['device'] == device]
            monitor_id = pd_usuarios_info[pd_usuarios_info['#Empleado']==int(user['userID'])]
            if (len(monitor_id)>0):
                monitor_id = str(monitor_id['ID_Seguimiento'].values[0])
                userList.append({STR_SAP_NUMBER: str(int(user['userID'])),
                                 STR_MONITOR_ID: monitor_id,
                                 STR_USER_TYPE: 1,
                                 STR_TEMPERATURE: user['temperature'],
                                 STR_MASK: 1,
                                 STR_DATE_TIME: user['timestamp'],
                                 STR_AUTH_ACCESS: True,
                                 STR_DEVICE_ID: mac_address})
        if (len(userList)>0):
            print('processing: ', len(userList), ' on device:', device)
            postServiceInst.postLogUsers(userList)
    

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Jun-23-2022 Arturo Gaona
#   + Created initial file based on User POST module.
#
#########################################################################################
