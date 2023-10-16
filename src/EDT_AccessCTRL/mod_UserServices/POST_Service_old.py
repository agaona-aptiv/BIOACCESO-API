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
#          Module: Stubs
#          Description: This script provides stubs for host.
#          Enterprise: Condumex
#          SW Developer: Ernesto Ulises Beltran
#
#          File: POST_Service.py
#          Feature: Stubs
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################

from flask import Flask, json
from flask_restful import Api, Resource
from os import path
import uuid
import requests
import datetime
import pickle
import os

# Ensure that PORT has remote access by able to be used
# -->  https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html
PORT = 81
DEBUG = True

MAC = str(hex(uuid.getnode()))
DeviceID = MAC.upper().replace('0X', '')
#URL_BASE = 'http://10.222.101.42/api/index.php/api/v1/hubapi/registerEvent/'
#URL_BASE = 'http://localhost:81/HUB_Service/'
URL_BASE = 'http://misaplicaciones.cidec.com.mx/sba_hub/API/public/index.php/api/v1/hubapi/registerEvent/'

BACKUP_DB_PATH = os.getcwd() + '/'
BACKUP_DB_NAME = 'Users_Not_Reported.bin'

app = Flask(__name__)
api = Api(app)


# This function will post a user's information to the HUB
# def postUser(compoundID, userType, temp, mask, authorizedAccess):
def postUser(incomingUser):
    # Read current date and time for the timestamp
    currentTime = datetime.datetime.now().timestamp()
    userInfo = {'sap_number': int(incomingUser['userID']),
                'monitor_id': incomingUser['monitorID'],
                'user_type': int(incomingUser['userType']),
                'temperature': incomingUser['temp'],
                'mask': incomingUser['mask'],
                'date_time': int(currentTime),
                'authorized_access': incomingUser['authorizedAccess'],
                'device_id': incomingUser['DeviceID']}
    print('sap_number: ' + str(userInfo['sap_number']) + ', type: ' + str(type(userInfo['sap_number'])))
    print('monitor_id: ' + str(userInfo['monitor_id']) + ', type: ' + str(type(userInfo['monitor_id'])))
    print('user_type: ' + str(userInfo['user_type']) + ', type: ' + str(type(userInfo['user_type'])))
    print('temperature: ' + str(userInfo['temperature']) + ', type: ' + str(type(userInfo['temperature'])))
    print('mask: ' + str(userInfo['mask']) + ', type: ' + str(type(userInfo['mask'])))
    print('date_time: ' + str(userInfo['date_time']) + ', type: ' + str(type(userInfo['date_time'])))
    print('authorized_access: ' + str(userInfo['authorized_access']) + ', type: ' + str(type(userInfo['authorized_access'])))
    print('device_id: ' + str(userInfo['device_id']) + ', type: ' + str(type(userInfo['device_id'])))

    return 0


# Placeholder to trigger the post function
# Postman example:
# http://localhost:81/POST_Service/{"ID": "1111_00001", "UserType": "1",
# "Temperature": "365", "Mask": "1", "Access": "true"}
class POST_Service(Resource):

    def post(self, strJsonUser):
        incomingUser = json.loads(strJsonUser)

        dataToSend = {'userID': (incomingUser['ID'].split('_'))[0],
                      'monitorID': (incomingUser['ID'].split('_'))[1],
                      'userType': incomingUser['UserType'],
                      'temp': incomingUser['Temperature'],
                      'mask': incomingUser['Mask'],
                      'authorizedAccess': incomingUser['Access'],
                      'DeviceID': DeviceID}

        # postUser(incomingUser["ID"], incomingUser["UserType"], incomingUser["Temperature"],
        #         incomingUser["Mask"], incomingUser["Access"])
        postUser(dataToSend)

        return 'Post process finished.', 200


# api.add_resource(POST_Service, "/POST_Service/<string:strJsonUser>")
# app.run(debug=DEBUG, port=PORT)

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
#########################################################################################