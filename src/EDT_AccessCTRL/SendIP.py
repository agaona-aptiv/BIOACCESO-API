'''
Created on 01-Nov-2020
@author: José Arturo Gaona
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex.
#  \endverbatim
#  LICENSE
#          Module: **SendIP
#          Description: **This module reports IP and MAC over the network using Broadcastprotocol
#          Enterprise: Condumex
#          SW Developer: **José Arturo Gaona Cuadra
#          
#          File: **SendIP.py
#          Feature: **Manufacture
#          Design:  **NA
#          Deviations: **NA
#   
#  **Information that must change according to the script
#########################################################################################
#pip install get-mac
import socket
import time
import uuid, re 
import os.path

mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
min_broadcast_report = 5
PORT = 37020
REPORT_TIME = 5
MAN_CFG_FILE_PATH = '/home/edt/Documents/Share/EDT_AccessCTRL/Config_Test/Manufacturing/MAN_CFG.txt'


def CheckManufacturing(filepath, variable, value):
    '''
        This method returns True if the filepath exist and the variable with the value defined does have the value defined
        in other case will return False
    '''
    flag = False
    if os.path.exists(filepath):
        f = open(filepath, "r")
        for line in f.readlines():
            if (variable in line ):
                if (value not in line):
                    flag = True
                    break
        f.close()
    return flag

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip = get_ip()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
jetsonInfo = {'IP':ip,'MAC':mac}
print('jetsonInfo: ',jetsonInfo)
message = str(jetsonInfo)
msgBytes = bytes(message, 'utf-8')
counter = 0
while True:
    server.sendto(msgBytes, ('<broadcast>', PORT))
    print("jetsonInfo sent:" + message)
    time.sleep(REPORT_TIME)
    manufacture_conf_file = CheckManufacturing(MAN_CFG_FILE_PATH,variable = 'serial_number',value='BP0000')
    if (manufacture_conf_file == True and counter >= min_broadcast_report):
        break
    counter = counter+1


######################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
#
# Date          userid          Description                                   
# 10-May-2021   Arturo Gaona    DBL_641: first release of the design implementation 
######################################################################################