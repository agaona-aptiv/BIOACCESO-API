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
from random import randint
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

# Strings used to generate the information on the json object sent to the HUB (POST request)
INT_USER_TYPE = 1
INT_MASK = 1
STR_AUTH_ACCESS = "authorized_access"
STR_DEVICE_ID = "device_id"
URL = 'https://sake.condumex.com.mx/sba_hub/API/public/index.php/api/v1/hubapi'
MAC_ADDRESS = '48:B0:2D:15:E8:1C'
TOKEN = 'd8f6e75db63f0871a9b9ff0f10a749b0e0cf60649ca57dea3aea0d53e2e2bf95'

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
        print('Init Start.')
        self.MAC_address = MAC_ADDRESS
        self.Access_Code = TOKEN
        self.Device = MAC_ADDRESS
        self.PostDataQueue = None
        self.URL_RAW = None
        self.HUB_Service = HUB_Service
        self.HUB_Service_Pending_User = HUB_Service_Pending_User
        self.HUB_Service_Token = HUB_Service_Token
        self.failedPostUsers = []
        self.tokenInfo = {}
        self.Token = "TokenR"
        print('Init Finished.')
    
    def postLogUsers(self, URL_BASE):
        user_df = pd.read_csv('team_users.csv')
        #print(user_df)
        userList = []
        for (sap_id, monitor_id) in zip(user_df['str_sap_id'],user_df['str_monitor_id']):
            str_sap_id = ''+str(sap_id)
            str_monitor_id = str(monitor_id)
            int_temperature = randint(357, 368)     #Random value between [35.7-36.8]
            minutes = randint(0,59)
            time_now = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
            int_date_time = int(time_now.timestamp())
            userList.append({"sap_number": sap_id,
                             "monitor_id": str_monitor_id,
                             "user_type": INT_USER_TYPE,
                             "temperature": int_temperature,
                             "mask": INT_MASK,
                             "date_time": int_date_time,
                             "authorized_access": True,
                             "device_id": self.Device})

        try:
            POST_URL = URL_BASE + self.HUB_Service_Pending_User
            if ProxyEnabled:
                r = requests.post(url=POST_URL, proxies=ProxyRequest, json=userList,
                                  timeout=REQUEST_TIMEOUT_POST_PENDING,
                                  auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
            else:
                r = requests.post(url=POST_URL, json=userList, timeout=REQUEST_TIMEOUT_POST_PENDING,
                                  auth=BearerAuth(self.Token), verify=False)  # add verify False SSL
            print('POST_URL: ',POST_URL)
            print('Log POST Code: ' + str(r.status_code))
        except Exception as exp:
            print('Exception: ' + str(exp))
        return r.status_code

    def requestToken(self, URL_BASE):
        r = requests.Response
        try:
            tokenURL = URL_BASE + self.HUB_Service_Token
            self.tokenInfo = {"mac_address": self.MAC_address,
                              "access_code": self.Access_Code}
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
            self.Token = token_Response["token"]

        print("Token response: " + str(r.status_code))
        return r.status_code

if __name__ == "__main__":
    # Create instance of PostService
    postServiceInst = PostService()

    # Request token
    print('Requesting token from HUB @ ' + URL)
    r1 = postServiceInst.requestToken(URL)
    time.sleep(1)

    # If success, continue with Log process
    # Else, finish script
    if ResponseCode.OK.value == int(r1):
        print('Token: ' + str(postServiceInst.Token))

        # Process Log file
        r2 = postServiceInst.postLogUsers(URL)
        time.sleep(1)
        if ResponseCode.OK.value == int(r2):
            print('Success.')
        else:
            print('Could not process Log file.')
    else:
        print('Failed at acquiring token. Log file processing aborted.')