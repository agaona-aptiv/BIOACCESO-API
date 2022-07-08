#http://localhost:5000/
from warnings import catch_warnings
from flask import request, current_app as app               # python3 -m pip install flask-restx
from flask_restx import Namespace, Resource, fields
import paramiko                                             #python3 -m pip install paramiko
import numpy as np                                          #python3 -m pip install numpy
import re
from datetime import date
from os import path
import datetime
import time
import os
import cv2                                                  #python3 -m pip install opencv-python
from Levenshtein import distance as lev                     #python310 -m pip install Levenshtein
import pandas as pd
import shutil
import requests
from urllib.request import Request, urlopen 
import urllib.request
from PIL import Image
import ssl
import pickle
import shelve
try:
    import face_recognition                                     #python38 -m pip install face-recognition
except:
    pass
try:
    import openpyxl
except Exception as e:
    os.system('python38 -m pip install openpyxl')
    raise e
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#Update Host
import api.Update_Alias

Black= ""
Dark_Gray=""
Red=""
Light_Red=""
Green=""
Light_Green=""
Brown_Orange=""
Yellow=""
Blue=""
Light_Blue=""
Purple=""
Light_Purple=""
Cyan=""
Light_Cyan=""
Light_Gray=""
White=""
'''
Black= "\033[0;30m"
Dark_Gray="\033[1;30"
Red="\033[0;31m"
Light_Red="\033[1;31m"
Green="\033[0;32m"
Light_Green="\033[1;32m"
Brown_Orange="\033[0;33m"
Yellow="\033[1;33m"
Blue="\033[0;34m"
Light_Blue="\033[1;34m"
Purple="\033[0;35m"
Light_Purple="\033[1;35m"
Cyan="\033[0;36m"
Light_Cyan="\033[1;36m"
Light_Gray="\033[0;37m"
White="\033[1;37m"
'''

namespace = Namespace("Bioaccess", description="Bioaccess Reports")

check_DBL_model_data = namespace.inherit("DBLStatusData",
    {
        "hosts": fields.String(description="Check that DBL list ID are implemented on the device list", 
            example=
            "['BIOACCESO'" + 
            ",'CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA6','CELAYA5','CELAYA4','CELAYA3','CELAYA2','CELAYA1']",
            required=True),
    },
)

status_model_data = namespace.inherit("DeviceStatusData",
    {
        "hosts": fields.String(description="place the IP address list to get status log", 
            example=
            "['CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA1','CELAYA2','CELAYA3','CELAYA4','CELAYA5','CELAYA6']",
            required=True),
    },
)

get_config_Config_Pkl_DBs_model = namespace.inherit("GetConfigPklDBs",
    {
        "hosts": fields.String(description="place the IP address list to get UserFaceIDs.pkl and Users_Database.db", 
            example=
            "['BIOACCESO'" + 
            ",'CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA6','CELAYA5','CELAYA4','CELAYA3','CELAYA2','CELAYA1']",
            required=True),
    },
)

get_logs_model_data = namespace.inherit("DeviceGetLogs",
    {
        "hosts": fields.String(description="place the IP address list to get Bioaccess logs", 
            example="['CARSO','CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35']", 
            required=True),
        "initial_date": fields.String(description="place the initial date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),
        "end_date": fields.String(description="place the end date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),            
        "_ImagesLog": fields.String(description="set as True or False is this log is requiered", 
            example= "False", 
            required=True),            
        "_Logs": fields.String(description="set as True or False is this log is requiered", 
            example= "True", 
            required=True),            
        "_Termografias": fields.String(description="set as True or False is this log is requiered", 
            example= "False", 
            required=True),            
    },
)

get_ethernet_model_info = namespace.inherit("GetEthernetInfo",
    {
        "hosts": fields.String(description="place the IP address list to get Bioaccess logs", 
            example=
            "['CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA4','CELAYA3','CELAYA2','CELAYA1']", 
            required=True),
    },
)

get_screenshot_model = namespace.inherit("GetScreenshot",
    {
        "hosts": fields.String(description="place the IP address list to get screenshot", 
            example=
            "['BIOACCESO'" + 
            ",'CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA4','CELAYA3','CELAYA2','CELAYA1']", 
            required=True),
    },
)

check_freeze_model = namespace.inherit("checkFreezeData",
    {
        "hosts": fields.String(description="Check if there is a freeze by screenshot this method spends at least 15 seconds by host", 
            example=
            "[" + 
            "'CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA6','CELAYA5','CELAYA4','CELAYA3','CELAYA2','CELAYA1']",
            required=True),
    },
)

replace_string_model = namespace.inherit("replaceString",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you plan to update files", 
            example="['BIOACCESO']", 
            required=True
            ),
        "target_file_path": fields.String(
            description="Full file path where the replace will be performed", 
            example="/home/edt/Documents/Share/EDT_AccessCTRL/mod_Temperature/ST_Temperature_cfg.py", 
            required=True
            ),
        "str_to_find": fields.String(
            description="String to be find and replace and replace", 
            example="FACTOR_PLANTA = 0.880", 
            required=True
            ),
        "str_to_replace": fields.String(
            description="String to be replaced, NOTICE this procedure does NOT REBOOT the host, considere it in case is requiered... ", 
            example="FACTOR_PLANTA = 0.910", 
            required=True
            ),
    },
)

analize_images_model = namespace.inherit("analizeImagesLog",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you plan to analize Image logs", 
            example=
            "['CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA6','CELAYA5','CELAYA4','CELAYA3','CELAYA2','CELAYA1']",
            required=True
            ),
        "initial_date": fields.String(description="place the initial date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),
        "end_date": fields.String(description="place the end date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),        
    },
)

set_date_model = namespace.inherit("setDate",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you plan set current datetime", 
            example="['BIOACCESO']", 
            required=True
            ),      
    },
)

update_file_model = namespace.inherit("updateFile",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you plan to update file", 
            example="['BIOACCESO']", 
            required=True
            ),
        "source_file_path": fields.String(
            description="Local source full file path from the replace will be performed", 
            example="C:\\Share\\AcessCRTL_EDT\\Code\\GitHub\\QSC01376_DBL\\QSC01376_DBL\\EDT_AccessCTRL\\mod_EDT_AccessCTRL\\EDT_AccessCTRL.py", 
            required=True
            ),        
        "target_file_path": fields.String(
            description="Full file path where the replace will be performed", 
            example="/home/edt/Documents/Share/EDT_AccessCTRL/mod_EDT_AccessCTRL/EDT_AccessCTRL.py", 
            required=True
            ),
    },
)

clear_logs_model_data = namespace.inherit("DeviceClearLogs",
    {
        "hosts": fields.String(description="place the IP address list to get Bioaccess logs", 
            example=
            "['BIOACCESO'" + 
            ",'CARSO'"+
            ",'CUPRO25','CUPRO31','CUPRO32','CUPRO33','CUPRO34','CUPRO35'"+
            ",'CELAYA4','CELAYA3','CELAYA2','CELAYA1']", 
            required=True),
        "initial_date": fields.String(description="place the initial date to start cleaning logs", 
            example= str(date.today() - datetime.timedelta(days=14)), 
            required=True),
        "end_date": fields.String(description="place the end date to clean logs", 
            example= str(date.today() - datetime.timedelta(days=5)), 
            required=True),            
    },
)

update_software_model = namespace.inherit("updateSWVersion",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you plan to update All files", 
            example="['BIOACCESO']", 
            required=True
            ),
        "source_file_path": fields.String(
            description="Local source full file path from the replace will be performed", 
            example="C:\\Share\\AcessCRTL_EDT\\Code\\GitHub\\SW_26.3_BMP", 
            required=True
            ),        
    },
)

estimate_temp_factor_model = namespace.inherit("estimateTempFactor",
    {
        "hosts": fields.String(
            description="IP list address of the hosts you want to update", 
            example="['BIOACCESO']", 
            required=True
            ),
        "initial_date": fields.String(description="place the initial date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),
        "end_date": fields.String(description="place the end date to start getting logs", 
            example= str(date.today() - datetime.timedelta(days=1)), 
            required=True),
        "min_factor": fields.String(
            description="min temperature value to start estimation", 
            example="0.900", 
            required=True),
        "max_factor": fields.String(
            description="max temperature value to end estimation", 
            example="1.100", 
            required=True),
        "step": fields.String(
            description="step value to increase min_factor up to max_value", 
            example="0.001", 
            required=True),
    },
)

verify_PKL_vs_HUB_model = namespace.inherit("validate_pkl_vs_hub",
    {
        "hosts": fields.String(
            description="IP list address of the devices that you want to check vs", 
            example="['CARSO']", 
            required=True
            ),
        "hub_address": fields.String(description="write the IP list address or host list names to verify", 
            example="['157.55.183.132']",
            required=True),
    },
)

soft_reboot_model = namespace.inherit("soft_reboot",
    {
        "hosts": fields.String(
            description="IP list address of the devices that you make soft reboot", 
            example="['BIOACCESO']", 
            required=True
            ),
    },
)

sudo_reboot_model = namespace.inherit("sudo_reboot",
    {
        "hosts": fields.String(
            description="IP list address of the devices that you make soft reboot", 
            example="['BIOACCESO']", 
            required=True
            ),
    },
)

check_pkl_db_model = namespace.inherit("check_pkl_db",
    {
        "hosts": fields.String(
            description="IP list address of the devices that you make soft reboot", 
            example="['BIOACCESO']", 
            required=True
            ),
    },
)

set_mant_mode_model = namespace.inherit("set_mant_mode",
    {
        "hosts": fields.String(
            description="IP list address of the devices that you set Manteinance mode", 
            example="['BIOACCESO']", 
            required=True
            ),
        "maintenance": fields.String(description="set as True or False is this maintenance mode is requiered", 
            example= "True", 
            required=True),
    },
)

@namespace.route("/19_mant_mode")
class ClassSetMaintenance(Resource):
    def sudo_systemctl(self,host,port,mode,service,username,password):
        result={}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        try:
            result['host']=host
            result['Exception'] = 'NA'
            command = 'sudo systemctl ' + mode + ' ' +service + '.service'
            command_comment = service + '.service '+mode + 'ed'

            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            lines = stdout.readlines()
            print(lines)
            result['status'] = command_comment
        except Exception as e:
            result['status'] = command_comment
            result['Exception'] = str(e)
        ssh.close()        
        return result
    def update_file(self,host,port,username,password,source_file_path,target_file_path):
        result={}
        result['host']=host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        command = 'sudo rm -f ' + target_file_path
        session = ssh.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()        
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        stdin.flush()
        lines = stdout.readlines()
        print(lines)
        sftp.put(source_file_path,target_file_path)
        result['state']='FILE_UPDATED'
        sftp.close()
        ssh.close()        
        return result

    def set_wall_paper(self,host,port,username,password,source_file):
        result={}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        try:
            result['host']=host
            result['Exception'] = 'NA'
            command = ' gsettings set org.gnome.desktop.background picture-uri ' + source_file
            command_comment = 'Wallpaper was set as :' + source_file
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            result['status'] = command_comment
        except Exception as e:
            result['status'] = command_comment
            result['Exception'] = str(e)
        ssh.close()        
        return result
            
    @namespace.expect(set_mant_mode_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        maintenance = eval(request.json['maintenance'])
        port = 22
        username = 'edt'        #os.environ['EDT_USER']
        password = 'admin'      #os.environ['EDT_PASSWORD']
        respuesta={}
        source_file_path = 'screen_mantenimiento.jpg'
        target_file_path='/home/edt/Documents/Share/screen_mantenimiento.jpg'
        results=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                mode='start'
                if (maintenance==True):
                    mode='stop'
                results.append(self.sudo_systemctl(host=host,port=port,mode=mode,service='sba',username=username,password=password))
                results.append(self.sudo_systemctl(host=host,port=port,mode=mode,service='rest',username=username,password=password))
                results.append(self.sudo_systemctl(host=host,port=port,mode=mode,service='handler',username=username,password=password))
                results.append(self.update_file(host=host,port=port,username=username,password=password,source_file_path = source_file_path,target_file_path=target_file_path))
                if (maintenance==False):
                    target_file_path='/home/edt/Documents/Share/NVIDIA_Wallpaper.jpg'
                results.append(self.set_wall_paper(host=host,port=port,username=username,password=password,source_file=target_file_path))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta = {'host':host,'exception':exception}
                results.append(respuesta)

        data_set = pd.DataFrame.from_records(results)
        print(data_set)

        return results

@namespace.route("/18_check_pkl_db")
class ClassCheckPklDB(Resource):
    def download_files(self, host,port,username,password):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        #Create target folder structure
        #if (path.exists(host)==True):
        #    shutil.rmtree(host)
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host+'\\_Config_Pkl_DBs\\')==False):
            os.mkdir(host+'\\_Config_Pkl_DBs\\')

        target_path = str(os. getcwd()) + '\\'+ host + '\\_Config_Pkl_DBs\\'
        target_path_file = target_path + 'UserFaceIDs.pkl'
        source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/UserFaceIDs.pkl'
        sftp.get(source_path_file,target_path_file)

        target_path_file = target_path + 'Users_Database.db'
        source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/Users_Database/Users_Database.db'
        sftp.get(source_path_file,target_path_file)        
        sftp.close()
        ssh.close()
        return target_path

    def read_Users_Database(self,file):
        users_in_db=[]
        if path.isfile(file):
            #C:\Share\AcessCRTL_EDT\SaveLogs\APIs\API-Bioacceso\BIOACCESO\_Config_Pkl_DBs\Users_Database.db
            print('Extracting: ' + file)

            with shelve.open(file,'r') as usersDB:
                print('usersDB')
                items = list(usersDB.items())
                keys = list(usersDB.keys())
                values = list(usersDB.values())
                print(items)
                print(keys)
                print(values)
                #for user in usersDB:
                #    print('usersDB[user]["sap_number"]:',usersDB[user]['sap_number'])

        return users_in_db
                    
    def check_pkl_db(self,host,port,username,password):
        result={}
        try:
            command_comment='NA'
            target_path = self.download_files(host,port,username,password)
            users_in_db = self.read_Users_Database(target_path+ 'Users_Database.db')
            result['host']=host
            result['Exception'] = 'NA'
            command_comment = 'Files saved on:' + target_path
            result['status'] = command_comment
        except Exception as e:
            result['status'] = command_comment
            result['Exception'] = str(e)

        return result
            
    @namespace.expect(check_pkl_db_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        results=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                results.append(self.check_pkl_db(host=host,port=port,username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta = {'host':host,'exception':exception}
                results.append(respuesta)

        data_set = pd.DataFrame.from_records(results)
        print(data_set)

        return results

@namespace.route("/17_sudo_reboot")
class ClassSudoReboot(Resource):
    def sudo_reboot(self,host,port,service,username,password):
        result={}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        try:
            result['host']=host
            result['Exception'] = 'NA'
            command = 'sudo systemctl stop '+service + '.service'
            command_comment = service + '.service stopped'
            if service =='reboot':
                command = 'sudo reboot'
                command_comment = 'system reboot'

            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            lines = stdout.readlines()
            result['status'] = command_comment
        except Exception as e:
            result['status'] = command_comment
            result['Exception'] = str(e)
        
        ssh.close()        
        return result
            
    @namespace.expect(sudo_reboot_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        results=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                results.append(self.sudo_reboot(host=host,port=port,service='sba',username=username,password=password))
                results.append(self.sudo_reboot(host=host,port=port,service='rest',username=username,password=password))
                results.append(self.sudo_reboot(host=host,port=port,service='handler',username=username,password=password))
                time.sleep(5)
                results.append(self.sudo_reboot(host=host,port=port,service='reboot',username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta = {'host':host,'exception':exception}
                results.append(respuesta)

        data_set = pd.DataFrame.from_records(results)
        print(data_set)

        return results

@namespace.route("/16_soft_reboot")
class ClassSoftReboot(Resource):
    def soft_reboot(self,host,port,service,username,password):
        result={}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        try:
            result['host']=host
            result['Exception'] = 'NA'

            command = 'sudo systemctl restart '+service + '.service'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            lines = stdout.readlines()
            result['status'] = service + '.service restarted'


        except Exception as e:
            result['Exception'] = str(e)
        
        ssh.close()        
        return result
            
    @namespace.expect(soft_reboot_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        results=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                results.append(self.soft_reboot(host=host,port=port,service='sba',username=username,password=password))
                results.append(self.soft_reboot(host=host,port=port,service='rest',username=username,password=password))
                results.append(self.soft_reboot(host=host,port=port,service='handler',username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta = {'host':host,'exception':exception}
                results.append(respuesta)

        data_set = pd.DataFrame.from_records(results)
        print(data_set)

        return results

@namespace.route("/15_verify_pkl_vs_hub")
class ClassVerifyPKLvsHUB(Resource):

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
    
    def download_pkl_file(self, host,port,username,password):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        #Create target folder structure
        #if (path.exists(host)==True):
        #    shutil.rmtree(host)
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host+'\\_Config_Pkl_DBs\\')==False):
            os.mkdir(host+'\\_Config_Pkl_DBs\\')

        target_path = str(os. getcwd()) + '\\'+ host + '\\_Config_Pkl_DBs\\'
        target_path_file = target_path + 'UserFaceIDs.pkl'
        source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/UserFaceIDs.pkl'
        sftp.get(source_path_file,target_path_file)
        sftp.close()
        ssh.close()
        return target_path_file
    
    def verify_pkl_vs_hub(self,host,hub,download_pkl_file):
        result={}
        result['host']=host
        result['hub']=hub
        pkl_file = download_pkl_file
        user = 'userDommy'
        password = 'PassDommy'
        url = 'https://'+hub+'/sba_hub/API/public/index.php/api/v1/hubapi/auth/login'
        payload = {"userid": user, "passwd": password}
        response = requests.post(url, data=payload,verify=False)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        print('Loading: ' + download_pkl_file + ' ...')
        with open(download_pkl_file, 'rb') as f:
            pkl_model = pickle.load(f)
        print('Users IDs loaded: ' + str(len(pkl_model['faceEncodeList'])))
        result['pkl_users']= len(pkl_model['faceEncodeList'])
        user_id_similarity_issue=[]
        user_label_not_in_hub=[]

        #Avoid labels autogentated by the BIOACCESS for mask detection
        pkl_list=[]
        for labelID in pkl_model['faceIDList']:
            face_mask_label = labelID.endswith('_11') or labelID.endswith('_12') or labelID.endswith('_13') or labelID.endswith('_14')
            if (not face_mask_label):
                pkl_list.append(labelID)

        for labelID in pkl_list:
            print('labelID:',labelID)
            line = labelID
            try:
                employ_id = labelID.split('_')[0]
                line = line + ',' + employ_id
                url = 'https://'+hub+'/sba_hub/API/public/index.php/api/v1/hubapi/storage/'+employ_id+'/'+ labelID+ '.jpg'
                image = Image.open(urllib.request.urlopen(url, timeout=10,context=ctx))
                image = np.asarray(image)
                image = image[:, :, ::-1]
                line = line +  ',Loaded'
                if labelID.endswith('_1'):
                    face_encoding = face_recognition.face_encodings(image)[0]
                    reference_label = labelID
                    reference_image = image
                    line = line +  ',locations: ' + str(len(face_encoding))
                elif (employ_id in labelID) and (employ_id in reference_label) :
                    if (len(face_encoding) is not None) and not (labelID.endswith('_0')):
                        check_face_locations = face_recognition.face_encodings(image)[0]
                        line = line +  ',locations: ' + str(len(check_face_locations))
                        distance = face_recognition.face_distance([face_encoding],check_face_locations)[0]
                        line = line +  ',Distance:' + str(distance)
                        if (distance > 0.47):
                            line = line +  ', PICTURE ISSUE ***'
                            user_id_similarity_issue.append(labelID)
                            reference_image = self.image_resize(reference_image,height=300)
                            image = self.image_resize(image,height=300)
                            
                            image_file = host+'\\_Config_Pkl_DBs\\'+labelID+'.jpg'
                            image_ref_file = host+'\\_Config_Pkl_DBs\\'+reference_label+'.jpg'
                            print('image_ref_file:',image_ref_file)
                            print('image_file:',image_file)
                        
                            issue_img = cv2.hconcat([reference_image, image])
                            issue_img = cv2.putText(issue_img,'Employ_id:' + str(employ_id)               ,(10,20),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0), 1)
                            issue_img = cv2.putText(issue_img,'Similarity ISSUE: ' + str(distance) ,(10,40),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0), 1)
                            cv2.imwrite(image_file,issue_img)
                            print(line)
            except Exception as e:
                #print('Exception:',str(e))
                user_label_not_in_hub.append(labelID)
                pass

        if (len(user_id_similarity_issue)==0):
            user_id_similarity_issue = ['NO_ISSUES_FOUND']

        if (len(user_label_not_in_hub)==0):
            user_label_not_in_hub = ['ALL_LABELS_IN_HUB']

        result['user_id_similarity_issue']=user_id_similarity_issue
        result['user_label_not_in_hub']=user_label_not_in_hub
        return result

    @namespace.expect(verify_PKL_vs_HUB_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        hubs = eval(request.json['hub_address'])

        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        results=[]
        if (len(hosts) == len(hubs)):
            for (host,hub) in zip(hosts,hubs):
                print('Processing: ',host + ' vs ' + hub)
                try:
                    download_pkl_file = self.download_pkl_file(host=host,port=port,username=username,password=password)
                    results.append(self.verify_pkl_vs_hub(host=host,hub=hub,download_pkl_file = download_pkl_file))

                except Exception as e:
                    print('Exception was found processing ' + host + ' : ' + str(e))
                    exception = 'Exception was found processing ' + host + ' : ' + str(e)
                    respuesta[host] = {'host':host,'exception':exception}
                    results.append(respuesta)
            
            data_set = pd.DataFrame.from_records(results)
            print(data_set)
        else:
            results.append({'exception':' The number of hosts does not match with the number of hubs list'})
        return results

@namespace.route("/14_estimate_factor")
class ClassEstimateFactor(Resource):
    
    def download_DATA_information(self, host,port,username,password,initial_date = date.today() - datetime.timedelta(days=1),end_date = date.today() - datetime.timedelta(days=1)):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        #Create target folder structure
        if (path.exists(host)==True):
            shutil.rmtree(host)
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_Logs')==False):
            os.mkdir(host + '/_Logs')

        #Job for all dates requiered
        current_date = initial_date
        result['target_path'] = os.path.join(os.getcwd(),host)
        while (current_date <= end_date):
            #Create Day folder
            if (path.exists(host + '/_Logs/'+ str(current_date))==False):
                os.mkdir(host +'/_Logs/'+ str(current_date))

            #Get _Logs
            logs_file_counter=0
            target_path = host + '\\_Logs\\' + str(current_date) + '\\'
            source_path = '/home/edt/Documents/Share/_Logs/'
            command = 'ls -l /home/edt/Documents/Share/_Logs/temperature_log_'+str(current_date) + '.log'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for file in lines:
                sourceFile = file.split('/home/edt/Documents/Share/_Logs/')[1]
                sourceFile = re.sub(r"[^a-zA-Z0-9. _-]","",sourceFile)
                #print('target_path:       ' + target_path + sourceFile)
                #print('source_path_file: ' + source_path + sourceFile)
                remote_path = source_path + sourceFile
                local_path = target_path + sourceFile
                sftp.get(remote_path, local_path)
                logs_file_counter=logs_file_counter+1
            result['logs_file_counter']=logs_file_counter
            current_date = current_date+ datetime.timedelta(days=1)
        
        sftp.close()
        ssh.close()
        return result
    
    def ConvertSurfaceToBody(self,temperature, ta, surface_temperature,FACTOR_PLANTA):
        '''
            ConvertSurfaceToBody(distance_temperature, ta, surface_temperature,FACTOR_PLANTA)
            Biophysical Conversion Formula
            ta = Ambient temperature read from FIR sensor
            tf = Forehead temperature read from FIR sensor, known as TO; Object Temperature
        '''
        low = 35.0
        high = 37.5
        tcore_body = 36.0
        tf = temperature * FACTOR_PLANTA

        # compute thresholds
        if ta <= 25:
            low = 32.66 + 0.186 * (ta - 25)
            high = 34.84 + 0.148 * (ta - 25)
        elif ta > 25:
            low = 32.66 + 0.086 * (ta - 25)
            high = 34.84 + 0.100 * (ta - 25)
        #compute core body temperature
        if tf < low:
            tcore_body = 36.3 + (0.551658273 + 0.021525068 * ta) * (tf - low)
        elif low < tf < high:
            tcore_body = 36.3 + (0.5 / (high - low)) * (tf - low)
        elif tf > high:
            tcore_body = 36.8 + (0.829320618 + 0.002364434 * ta) * (tf - high)

        return tcore_body

    def get_file_to_process(self,hosts):
        print('Exploring folder/subfolders for hosts:',str(hosts))
        files_to_process = []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                path=os.path.join(root,file)
                include_host = any(host in path for host in hosts)
                if (file.startswith('temperature_log') and file.endswith("log")) and (include_host==True):
                    files_to_process.append(path)
        return files_to_process        
    
    def get_DATA_information(self,temperature_log_files):
        '''
            if 
                distance_temperature = vdd_temperature + 0.0243 * (distance - 15)
                vdd_temperature = surface_temperature   
            then: 
                distance = (distance_temperature - vdd_temperature)/0.0243 + 15
                distance = (distance_temperature - surface_temperature)/0.0243 + 15
            2022-02-25 06:39:30.552: DATA,    31.436543      ,  31.436543    , 32.175551194986326 ,   36.5         ,11.91,17.785303115844727,17.277763,11.91 ,919034
                    Date_time      : DATA,surface_temperature,vdd_temperature,distance_temperature,body_temperature, tw  ,   tmin           ,   ta    , tbmp ,SAP_ID
        '''
        data_set = []
        for temperature_log_file_path in temperature_log_files:
            temperature_log_file =  open(temperature_log_file_path)
            temperature_log_file_lines = temperature_log_file.readlines()
            device = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(temperature_log_file_path))))
            print('device:',device)
            cnt_line = 0
            for line in temperature_log_file_lines:
                temperature_info={}
                if ('DATA' in line):
                    try:
                        temperature_info['device']=device
                        line_split = line.split('DATA,')[1].split(',')
                        temperature_info['date_time']=line[9:32]
                        temperature_info['surface_temperature']=eval(line_split[0])
                        temperature_info['vdd_temperature']=eval(line_split[1])
                        temperature_info['distance_temperature']=eval(line_split[2])
                        temperature_info['body_temperature']=eval(line_split[3])
                        temperature_info['tw']=eval(line_split[4])
                        temperature_info['tb']=eval(line_split[5])
                        temperature_info['tmin']=eval(line_split[6])
                        temperature_info['ta']=eval(line_split[7])
                        temperature_info['user_id']=re.sub(r"[^a-zA-Z0-9]","",str(line_split[-1])) 
                        if ('Temperature to HUB' in temperature_log_file_lines[cnt_line+1]):
                            #print('line+1:',temperature_log_file_lines[cnt_line-1])
                            #print('line:',temperature_log_file_lines[cnt_line])
                            #print('line+1:',temperature_log_file_lines[cnt_line+1])
                            line_split = temperature_log_file_lines[cnt_line+1].split(' ')
                            temperature_info['user_id']=re.sub(r"[^a-zA-Z0-9]","",str(line_split[-1])) 
                            data_set.append(temperature_info)
                    except Exception as e:
                        pass                        
                cnt_line= cnt_line+1
        pd.DataFrame.from_records(data_set).to_excel('./'+device+'/'+device+'_data_set.xlsx')
        return data_set

    def get_factor(self,data_set,min_factor,max_factor,step):
        '''
            Estimate new FACTOR by calculating new temperature values with different FACTORs [min value to max, ]
        '''
        result_list = []
        device_list = data_set['device'].unique()
        for device in device_list:
            result = {}
            device_data_set = data_set.loc[(data_set['device'] == device)]
            low_temperatures = data_set.loc[(data_set['device'] == device) & (data_set['body_temperature'] < 35.0)]
            high_temperatures = data_set.loc[(data_set['device'] == device) & (data_set['body_temperature'] > 37.5)]
            not_reported_high_temperatures = data_set.loc[(data_set['device'] == device) & (data_set['body_temperature'] > 40)]
            not_reported_low_temperatures = data_set.loc[(data_set['device'] == device) & (data_set['body_temperature'] < 35)]
            result['device'] = device
            result['total'] = len(device_data_set.index)
            result['low'] = len(low_temperatures.index)
            result['high'] = len(high_temperatures.index)
            result['max'] = data_set['body_temperature'].max()
            result['min'] = data_set['body_temperature'].min()
            result['lecture_error'] = len(not_reported_low_temperatures.index) + len(not_reported_high_temperatures.index)
            result['performance'] = 100 * (1 - (result['low'] + result['high'])/result['total'])
            total_temperatures = result['total']
            
            best_factor = 'ACTUAL IS THE BEST'
            best_performance = result['performance']
            for current_factor in np.arange(min_factor,max_factor,step):
                #                       body_temperature = ST_Temperature.ConvertSurfaceToBody(distance_temperature       ,     ta,        surface_temperature)
                new_body_temperature = device_data_set.apply(lambda row : self.ConvertSurfaceToBody(row['distance_temperature'],row['ta'], row['surface_temperature'],current_factor), axis = 1)
                low_temperatures = len(new_body_temperature.loc[new_body_temperature < 35.0])
                high_temperatures = len(new_body_temperature.loc[new_body_temperature > 37.5])
                current_performance = 100 * (1 - (low_temperatures + high_temperatures)/total_temperatures)
                #print('device:',device)
                #print('low_temperatures: ' + str(low_temperatures) + ' high_temperatures: ' + str(high_temperatures)  + ' current_performance: ' + str(current_performance))
                if current_performance > best_performance:
                    result['new_low'] = low_temperatures
                    result['new_high'] = high_temperatures                    
                    result['new_max'] = new_body_temperature.max()
                    result['new_min'] = new_body_temperature.min()
                    result['new_performance'] = best_performance
                    best_performance = current_performance
                    best_factor = current_factor

            result['new_factor'] = best_factor
            result_list.append(result)
        return result_list

    @namespace.expect(estimate_temp_factor_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        initial_date = request.json['initial_date']
        initial_date = datetime.date(year=int(initial_date[0:4]), month=int(initial_date[5:7]), day=int(initial_date[8:10]))
        end_date = request.json['end_date']
        end_date = datetime.date(year=int(end_date[0:4]), month=int(end_date[5:7]), day=int(end_date[8:10]))
        min_factor = eval(request.json['min_factor'])
        max_factor = eval(request.json['max_factor'])
        step = eval(request.json['step'])

        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        results=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                result = self.download_DATA_information(host=host,port=port,username=username,password=password,initial_date=initial_date,end_date=end_date)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        try:
            temperature_log_files = self.get_file_to_process(hosts)
            data_set_list = self.get_DATA_information(temperature_log_files)
            data_set = pd.DataFrame.from_records(data_set_list)
            respuesta = self.get_factor(data_set,min_factor=min_factor,max_factor=max_factor,step = step)

        except Exception as e:
                print('Exception was found processing data set: '+ str(e))
                respuesta[host] = {'host':host,'exception':str(e)}
        try:
            data_set = pd.DataFrame.from_records(respuesta).sort_values('performance')
            print(data_set)
        except Exception as e:
            pass
        return respuesta

@namespace.route("/13_update_software")
class ClassUpdateSW(Resource):
    def update_software(self,host,port,username,password,source_file_path):
        result={}
        try:
            result['host']=host
            result['exception'] = 'NA'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            sftp = ssh.open_sftp()

            update_file_list = []
            for root, dirs, files in os.walk(source_file_path):
                for file in files:
                    if file.endswith(".sh") or (file.endswith(".py") and not file.endswith("_cfg.py") and not file.endswith("__.py")):
                        path=os.path.join(root,file)
                        path = os.path.abspath(path)
                        update_file_list.append(path)

            result['list_file_result'] = []
            for source_file in update_file_list:
                target_file_path = '/home/edt/Documents' + source_file.replace(source_file_path,'').replace('\\','/')
                result['list_file_result'].append(self.update_file(ssh,sftp,password,source_file,target_file_path))

            sftp.close()
            ssh.close()
        except Exception as e:
            result['host']=host
            result['exception'] = str(e)

        for result_file in result['list_file_result']:
            print('-'*50)
            for key in result_file.keys():
                print(str(key) + ':' + str(result_file[key]))
        print('-'*50)
        return result 

    def update_file(self,ssh,sftp,password,source_file_path,target_file_path):
        result={}
        result['state']='SOURCE_FILE_NOT_FOUND'
        result['execption']='NA'

        try:
            #Check Target file
            command = 'ls -l ' + target_file_path
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if len(lines) > 0:
                result['state']='TARGET_FILE_NEEDS_BACKUP'
            else:
                result['state']='TARGET_FILE_DOES_NOT_EXIST'

            str_source_time = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(source_file_path)))
            if ('TARGET_FILE_NEEDS_BACKUP' in result['state']):
                #Check if source file and target file are different by date test
                command = 'stat ' + target_file_path
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                target_time = lines[6].split(' ')[1]            #lines[6] = Change: 2021-09-17 09:39:12.881742988 -0500 => split by ' ' and get second element
                if (str_source_time in target_time):
                    result['state']='TARGET_FILE_ALREADY_UPDATED'

            if ('TARGET_FILE_NEEDS_BACKUP' in result['state']):
                command = 'sudo cp ' + target_file_path + ' ' + target_file_path + '.bkp'
                session = ssh.get_transport().open_session()
                session.set_combine_stderr(True)
                session.get_pty()                
                session.exec_command(command)
                stdin = session.makefile('wb', -1)
                stdout = session.makefile('rb', -1)
                stdin.write(password + '\n')
                stdin.flush()
                if len(lines) > 0:
                    result['state']='FILE_BACKUP_DONE'
                    result['comments'] = 'File was backup on :' + target_file_path + '.bkp'

            if ('FILE_BACKUP_DONE' in result['state']) or ('TARGET_FILE_DOES_NOT_EXIST'in result['state']):
                command = 'sudo chmnod 777 ' +target_file_path
                session = ssh.get_transport().open_session()
                session.set_combine_stderr(True)
                session.get_pty()                
                session.exec_command(command)
                stdin = session.makefile('wb', -1)
                stdout = session.makefile('rb', -1)
                stdin.write(password + '\n')
                stdin.flush()
                
                sftp.put(source_file_path,target_file_path)
                result['state']='FILE_UPDATED'
                command = 'touch -d '+str_source_time + ' ' + target_file_path
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                result['updated_date'] = str_source_time
                result['state']='FILE_UPDATED_TOUCHED'

        except Exception as e:
            result['execption']=str(e)
            
        return result
            
    @namespace.expect(update_software_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        source_file_path  = str(request.json['source_file_path'])
        
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.update_software(host=host,port=port,username=username,password=password,source_file_path=source_file_path)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        return respuesta

@namespace.route("/12_clear_logs")
class ClassClearlogs(Resource):
    def clear_logs(self, host,port,username,password,initial_date = date.today() - datetime.timedelta(days=14),end_date = date.today() - datetime.timedelta(days=7)):
        result = {}
        result['host']=host
        result['state']='True'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        #Job for all dates requiered
        current_date = initial_date
        total_files = 0
        while (current_date <= end_date):
            #Clear _ImagesLog
            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/*'+str(current_date) + '*.jpg | wc -l' 
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                total_files = total_files + eval(r''+ str(line).replace('\n',''))

            command = 'sudo rm -f /home/edt/Documents/Share/_ImagesLog/*'+str(current_date) + '*.jpg'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            
            #Clear _Termografias
            command = 'ls -l /home/edt/Documents/Share/_Termografias/*'+str(current_date) + '*.csv | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                total_files = total_files + eval(r''+ str(line).replace('\n',''))
            command = 'sudo rm -f /home/edt/Documents/Share/_Termografias/*'+str(current_date) + '*.csv'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()

            #Clear _Logs
            command = 'ls -l /home/edt/Documents/Share/_Logs/*'+str(current_date) + '*.log | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                total_files = total_files + eval(r''+ str(line).replace('\n',''))
            command = 'sudo rm -f /home/edt/Documents/Share/_Logs/*'+str(current_date) + '*.log'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()

            current_date = current_date+ datetime.timedelta(days=1)
        
        ssh.close()
        result['files_removed']=total_files
        return result
            
    @namespace.expect(clear_logs_model_data, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        initial_date = request.json['initial_date']
        initial_date = datetime.date(year=int(initial_date[0:4]), month=int(initial_date[5:7]), day=int(initial_date[8:10]))
        end_date = request.json['end_date']
        end_date = datetime.date(year=int(end_date[0:4]), month=int(end_date[5:7]), day=int(end_date[8:10]))
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.clear_logs(host=host,port=port,username=username,password=password,initial_date=initial_date,end_date=end_date)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}

            print('*'*50)
            for host in respuesta.keys():
                print(str(respuesta[host]))
            print('*'*50)
        
        return respuesta

@namespace.route("/11_update_file")
class ClassUpdateFile(Resource):
    def update_file(self,host,port,username,password,source_file_path,target_file_path):
        result={}
        result['host']=host
        result['state']='SOURCE_FILE_NOT_FOUND'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        if (os.path.exists(source_file_path)):
            result['state']='TARGET_FILE_NOT_FOUND'

        command = 'ls -l ' + target_file_path
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        if len(lines) > 0:
            result['state']='TARGET_FILE_FOUND'

        if ('TARGET_FILE_FOUND' in result['state']):
            command = 'cp ' + target_file_path + ' ' + target_file_path + '.bkp'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if len(lines) == 0:
                result['state']='FILE_BACKUP'
                result['comments'] = 'File was backup on :' + target_file_path + '.bkp'
        if ('FILE_BACKUP' in result['state']):
            time.sleep(2)
            sftp.put(source_file_path,target_file_path)
            result['state']='FILE_UPDATED'

        sftp.close()
        ssh.close()        
        return result
            
    @namespace.expect(update_file_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        source_file_path  = str(request.json['source_file_path'])
        target_file_path  = str(request.json['target_file_path'])
        
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.update_file(host=host,port=port,username=username,password=password,source_file_path=source_file_path,target_file_path=target_file_path)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        print('DEV,  IP   , STATE')
        for host in respuesta.keys():
            print('host,' +  str(host) + ',' + respuesta[host]['state'] )
        
        return respuesta

@namespace.route("/10_set_date_time")
class ClassSetDateTime(Resource):
    def set_date(self,host,port,username,password):
        result={}
        result['host']=host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        str_date_time = str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))

        try:
            result['Exception'] = 'NA'
            command = 'sudo date --set="' +str_date_time +'"'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            result['status'] = 'sw clock systohc'

            command = 'sudo hwclock --systohc'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            result['status'] = 'hwclock systohc'

            command = 'sudo systemctl restart rest.service'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()
            result['status'] = 'rest.service restarted'

            command = 'sudo systemctl restart handler.service'
            session = ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()        
            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(password + '\n')
            stdin.flush()

            result['date_updated'] = str_date_time
            result['status'] = 'handler.service restarted'
        except Exception as e:
            result['Exception'] = str(e)
        
        ssh.close()        
        return result
            
    @namespace.expect(set_date_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.set_date(host=host,port=port,username=username,password=password)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        print('DEV,  IP   , STATE')
        for host in respuesta.keys():
            print('host,' +  str(host) + ',' + str(respuesta[host]))
        return respuesta

@namespace.route("/09_string_replace")
class ClassReplaceStringtatus(Resource):
    def replace_string_file(self,file_path,str_to_find,str_to_replace):
        #input file
        fin = open(file_path, "rt")
        #output file to write the result to
        file_out = file_path+'.udt'
        fout = open(file_out, "wt")
        #for each line in the input file
        for line in fin:
            #read replace the string and write to output file
            fout.write(line.replace(str_to_find, str_to_replace))
        #close input and output files
        fin.close()
        fout.close()
        return file_out

    def replace_string(self,host,port,username,password,target_file_path,str_to_find,str_to_replace):
        result={}
        result['host']=host
        result['state']='FILE_NOT_FOUND'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        command = 'ls -l ' + target_file_path
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        if len(lines) > 0:
            result['state']='STRING_NOT_FOUND'
        if ('STRING_NOT_FOUND' in result['state']):
            command = 'cat ' + target_file_path + ' | grep "' + str_to_find + '"'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if len(lines) > 0:
                result['state']='STRING_FOUND'
            else:
                min_str_to_find = str_to_find.split(' ')[0]
                command = 'cat ' + target_file_path + ' | grep "' + min_str_to_find + '"'
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                min_lev_distance = len(str_to_find)
                print('min_lev_distance:',min_lev_distance)
                best_match = None
                for line in lines:
                    print(line)
                    lev_distance = lev(min_str_to_find,line)
                    print('lev_distance:',lev_distance)
                    if  lev_distance > min_lev_distance:
                        min_lev_distance = lev_distance
                        best_match = line
                if best_match is not None:
                    result['state']='STRING_VALUE_NOT_FOUND:' + str(best_match)

        if ('STRING_FOUND' in result['state']):
            local_file_path =  os.path.basename(target_file_path)
            print(local_file_path)
            sftp.get(target_file_path,local_file_path)
            file_out = self.replace_string_file(local_file_path,str_to_find,str_to_replace)
            result['state']='STRING_REPLACED'
        if ('STRING_REPLACED' in result['state']):
            command = 'cp ' + target_file_path + ' ' + target_file_path + '.bkp'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if len(lines) == 0:
                result['state']='FILE_BACKUP'
                result['comments'] = 'File was backup on :' + target_file_path + '.bkp'
        if ('FILE_BACKUP' in result['state']):
            sftp.put(file_out,target_file_path)
            result['state']='FILE_UPDATED'

        sftp.close()
        ssh.close()        
        return result
            
    @namespace.expect(replace_string_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        target_file_path  = str(request.json['target_file_path'])
        
        str_to_find = str(request.json['str_to_find'])
        str_to_replace = str(request.json['str_to_replace'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.replace_string(host=host,port=port,username=username,password=password,target_file_path=target_file_path,str_to_find=str_to_find,str_to_replace=str_to_replace)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        print('DEV,  IP   , STATE')
        for host in respuesta.keys():
            print('host,' +  str(host) + ',' + respuesta[host]['state'] )
        
        return respuesta

@namespace.route("/08_get_logs")
class ClassGetlogs(Resource):
    def get_logs(self, host,port,username,password,initial_date = date.today() - datetime.timedelta(days=1),end_date = date.today() - datetime.timedelta(days=1),_ImagesLog=True,_Logs=True,_Termografias=True):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        #Create target folder structure
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_ImagesLog')==False) and _ImagesLog==True:
            os.mkdir(host + '/_ImagesLog')
        if (path.exists(host + '/_Logs')==False) and _Logs==True:
            os.mkdir(host +'/_Logs')
        if (path.exists(host + '/_Termografias')==False) and _Termografias==True:
            os.mkdir(host + '/_Termografias')

        #Job for all dates requiered
        current_date = initial_date
        result['target_path'] = os.path.join(os.getcwd(),host)
        while (current_date <= end_date):
            #Create Day folder
            if _ImagesLog==True:
                if (path.exists(host + '/_ImagesLog/' + str(current_date))==False):
                    os.mkdir(host + '/_ImagesLog/' + str(current_date))

                #Get _ImagesLog
                img_file_counter=0
                target_path = host + '\\_ImagesLog\\' + str(current_date) + '\\'
                source_path = '/home/edt/Documents/Share/_ImagesLog/'
                command = 'ls -l /home/edt/Documents/Share/_ImagesLog/*'+str(current_date) + '*.jpg'
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                for file in lines:
                    sourceFile = file.split('/home/edt/Documents/Share/_ImagesLog/')[1]
                    sourceFile = re.sub(r"[^a-zA-Z0-9. _-]","",sourceFile)
                    #print('target_path:       ' + target_path + sourceFile)
                    #print('source_path_file: ' + source_path + sourceFile)
                    remote_path = source_path + sourceFile
                    local_path = target_path + sourceFile
                    sftp.get(remote_path, local_path)
                    img_file_counter=img_file_counter+1
                result['img_file_counter']=img_file_counter                

            if _Logs==True:
                if (path.exists(host + '/_Logs/'+ str(current_date))==False):
                    os.mkdir(host +'/_Logs/'+ str(current_date))

                #Get _Logs
                logs_file_counter=0
                target_path = host + '\\_Logs\\' + str(current_date) + '\\'
                source_path = '/home/edt/Documents/Share/_Logs/'
                command = 'ls -l /home/edt/Documents/Share/_Logs/*'+str(current_date) + '*.log'
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                for file in lines:
                    sourceFile = file.split('/home/edt/Documents/Share/_Logs/')[1]
                    sourceFile = re.sub(r"[^a-zA-Z0-9. _-]","",sourceFile)
                    #print('target_path:       ' + target_path + sourceFile)
                    #print('source_path_file: ' + source_path + sourceFile)
                    remote_path = source_path + sourceFile
                    local_path = target_path + sourceFile
                    sftp.get(remote_path, local_path)
                    logs_file_counter=logs_file_counter+1
                result['logs_file_counter']=logs_file_counter

            if  _Termografias==True:
                if (path.exists(host + '/_Termografias/'+ str(current_date))==False):
                    os.mkdir(host + '/_Termografias/'+str(current_date))
                #Get _Termografias
                thermologs_file_counter=0
                target_path = host + '\\_Termografias\\' + str(current_date) + '\\'
                source_path = '/home/edt/Documents/Share/_Termografias/'
                command = 'ls -l /home/edt/Documents/Share/_Termografias/*'+str(current_date) + '*.csv'
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                for file in lines:
                    sourceFile = file.split('/home/edt/Documents/Share/_Termografias/')[1]
                    sourceFile = re.sub(r"[^a-zA-Z0-9. _-]","",sourceFile)
                    #print('target_path:       ' + target_path + sourceFile)
                    #print('source_path_file: ' + source_path + sourceFile)
                    remote_path = source_path + sourceFile
                    local_path = target_path + sourceFile
                    sftp.get(remote_path, local_path)		
                    thermologs_file_counter=thermologs_file_counter+1
                result['thermologs_file_counter']=thermologs_file_counter

            current_date = current_date+ datetime.timedelta(days=1)
        
        sftp.close()
        ssh.close()
        
        return result
            
    @namespace.expect(get_logs_model_data, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        initial_date = request.json['initial_date']
        initial_date = datetime.date(year=int(initial_date[0:4]), month=int(initial_date[5:7]), day=int(initial_date[8:10]))
        end_date = request.json['end_date']
        end_date = datetime.date(year=int(end_date[0:4]), month=int(end_date[5:7]), day=int(end_date[8:10]))
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.get_logs(host=host,port=port,username=username,password=password,initial_date=initial_date,end_date=end_date)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        
        return respuesta

@namespace.route("/07_get_config_Config_Pkl_DBs")
class ClassGetConfigPklDBs(Resource):
    def get_config_Config_Pkl_DBs(self, host,port,username,password):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        #Create target folder structure
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_Config_Pkl_DBs')==False):
            os.mkdir(host + '/_Config_Pkl_DBs')

        #Get UserFaceIDs.pkl
        result['host'] = host
        try:
            result['target_path'] = str(os. getcwd()) + '\\'+ host + '\\_Config_Pkl_DBs\\'
            target_path_file = result['target_path'] + 'UserFaceIDs.pkl'
            source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/UserFaceIDs.pkl'
            sftp.get(source_path_file,target_path_file)
            result['pkl_state'] = str('UserFaceIDs.pkl download successfully')
        except Exception as e:
            result['pkl_state'] = str(e)



        #Get Users_Database.csv
        try:
            target_path_file = result['target_path'] + 'Users_Database.csv'
            source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/Users_Database/Users_Database.csv'
            sftp.get(source_path_file,target_path_file)
            result['db_csv_state'] = str('Users_Database.csv download successfully')
        except Exception as e:
            result['db_csv_state'] = str(e)

        #Get Users_Database.db
        try:
            target_path_file = result['target_path'] + 'Users_Database.db'
            source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/Users_Database/Users_Database.db'
            sftp.get(source_path_file,target_path_file)
            result['db_db_state'] = str('Users_Database.db download successfully')
        except Exception as e:
            result['db_db_state'] = str(e)

        #Get MAN_CFG.txt
        try:
            target_path_file = result['target_path'] + 'MAN_CFG.txt'
            source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/Config_Test/Manufacturing/MAN_CFG.txt'
            sftp.get(source_path_file,target_path_file)
            result['MAN_CFG'] = str('MAN_CFG.txt download successfully')
        except Exception as e:
            result['MAN_CFG'] = str(e)            

        #Get SS_CFG.txt
        try:
            target_path_file = result['target_path'] + 'SS_CFG.txt'
            source_path_file = '/home/edt/Documents/Share/EDT_AccessCTRL/Config_Test/SpecificServices/SS_CFG.txt'
            sftp.get(source_path_file,target_path_file)
            result['SS_CFG'] = str('SS_CFG.txt download successfully')
        except Exception as e:
            result['SS_CFG'] = str(e)            
        
        sftp.close()
        ssh.close()
        
        return result
            
    @namespace.expect(get_config_Config_Pkl_DBs_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta.append(self.get_config_Config_Pkl_DBs(host=host,port=port,username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                #respuesta[host] = {'host':host,'exception':exception}

        data_set = pd.DataFrame.from_records(respuesta)
        print(data_set)         
        return respuesta

@namespace.route("/06_get_ethernet_info")
class ClassGetEthernerInfo(Resource):

    def get_BMP(self,ssh):
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_Temperature/ST_Temperature.py | grep "bmp280 ="'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        if len(lines)>0:
            bmp = lines[0]
            bmp = bmp.split('=')[0]
            bmp = not ('#' in bmp)
            if bmp:
                bmp = 'BMP'
            else:
                bmp = 'NO_BMP'
        else:
            bmp = 'NOT DETERMINED'
        return bmp

    def get_dns(self,ssh):
        command = 'nmcli device show | grep IP4.DNS'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        if len(lines)>0:
            dns = lines[0]
            dns = dns.split(':')[1]
            dns = re.sub(r"[^0-9.]","",dns)       #Accept only valid MAC chars and lent(48:b0:2d:15:e4:7c)
        else:
            dns = str(lines)
        return dns

    def get_mac(self,ssh):
        command = 'nmcli device show | grep GENERAL.HWADDR:'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        hwaddr = lines[0]
        hwaddr = hwaddr.split('.HWADDR:')[1]
        hwaddr = re.sub(r"[^0-9:^A-Z]","",hwaddr)       #Accept only valid MAC chars and lent(48:b0:2d:15:e4:7c)
        return hwaddr

    def get_gateway(self,ssh):
        command = 'nmcli device show | grep IP4.GATEWAY:'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        gateway = lines[0]
        gateway = gateway.split(':')[1]
        gateway = re.sub(r"[^0-9.]","",gateway)       #Accept only valid MAC chars and lent(48:b0:2d:15:e4:7c)
        return gateway

    def get_ethernet_info(self,host,port,username,password):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        #get_ehternet info
        result['host'] = host
        result['mac'] = self.get_mac(ssh)
        result['gateway'] = self.get_gateway(ssh)
        result['dns'] = self.get_dns(ssh)
        result['bmp'] = self.get_BMP(ssh)
        ssh.close()
        return result

    @namespace.expect(get_ethernet_model_info, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")

    def post(self):
        """Get ethernet configuration from a device given the IP address"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta.append(self.get_ethernet_info(host=host,port=port,username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)

        data_set = pd.DataFrame.from_records(respuesta)
        print(data_set)      
        return respuesta

@namespace.route("/05_check_dbl_implementation")
class ClassDBLStatus(Resource):
    def Check_DBL_327(self,host,ssh,password):
        dbl_id = 'DBL_327'
        missing_updated_files = False
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/POST_Test/POST_Service.py |grep "DBL_327"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        if (len(ssh_response) < 1):
            missing_updated_files = True

        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_Temperature/ST_Temperature.py |grep "DBL_327"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'implemented'
        if (len(ssh_response) < 1):
            missing_updated_files = True

        dbl_status = 'implemented'
        if (missing_updated_files==True):
            dbl_status = 'NOT_implemented'

        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info    

    def Check_DBL_326(self,host,ssh,password):
        dbl_id = 'DBL_326'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/POST_Test/POST_Service.py |grep "DBL_326"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_325(self,host,ssh,password):
        dbl_id = 'DBL_325'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_Temperature/ST_Temperature.py |grep "DBL_325"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info    

    def Check_DBL_324_EDT_Debug(self,host,ssh,password):
        dbl_id = 'DBL_324 on EDT_Debug.py'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/Config_Test/EDT_Debug.py | grep "DBL_324"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_323_POST_Service(self,host,ssh,password):
        dbl_id = 'DBL_323 on POST_Service.py'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/POST_Test/POST_Service.py | grep "DBL_323"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_323_AccessCTRL_Main(self,host,ssh,password):
        dbl_id = 'DBL_323 on AccessCTRL_Main.py'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_EDT_AccessCTRL/AccessCTRL_Main.py | grep "DBL_323"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_323_EDT_AccessCTRL(self,host,ssh,password):
        dbl_id = 'DBL_323 on EDT_AccessCTRL.py'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_EDT_AccessCTRL/EDT_AccessCTRL.py | grep "DBL_323"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info        

    def Check_ufw_9518(self,host,ssh,password):
        dbl_id = 'DBL_316,Firewall UFW 8518'
        command = 'cat /home/edt/Documents/Share/Security/ClosePorts.sh |grep "ufw allow 9518"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_443(self,host,ssh,password):
        dbl_id = 'DBL_316, Firewall UFW 443'
        command = 'cat /home/edt/Documents/Share/Security/ClosePorts.sh |grep "ufw allow 443"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info    

    def Check_DBL_322(self,host,ssh,password):
        dbl_id = 'DBL_322'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_Temperature/ST_Temperature.py |grep "DBL_322"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_321(self,host,ssh,password):
        dbl_id = 'DBL_321'
        command = 'cat /home/edt/Documents/Share/EDT_AccessCTRL/mod_FaceID/ST_FaceID.py |grep "DBL_321_Use_euclidean_distance"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_318(self,host,ssh,password):
        dbl_id = 'DBL_318'
        command = 'crontab -l |grep "SearchFreeze"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info

    def Check_DBL_316(self,host,ssh,password):
        dbl_id = 'DBL_316'
        command = 'cat /home/edt/Documents/Share/InitialTest.sh |grep "jetson_clocks"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info        

    def Check_Limit_syslog(self,host,ssh,password):
        dbl_id = 'Limit_Syslog'
        command = 'cat /etc/rsyslog.d/50-default.conf |grep "outchannel"'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        dbl_status = 'NOT_implemented'
        if (len(ssh_response) > 0):
            dbl_status = 'implemented'
        dbl_info = {'host':host,'DBL_ID':dbl_id,'DBL_STATUS':dbl_status,'COMMENT':str(ssh_response)}
        return dbl_info                

    def Check_DBL_Status(self,host,port,username,password):
        result = []
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        #Check_dbl_status       
        result.append(self.Check_Limit_syslog(host,ssh,password))
        result.append(self.Check_ufw_9518(host,ssh,password))
        result.append(self.Check_DBL_443(host,ssh,password))
        result.append(self.Check_DBL_322(host,ssh,password))
        result.append(self.Check_DBL_321(host,ssh,password))
        result.append(self.Check_DBL_318(host,ssh,password))
        result.append(self.Check_DBL_316(host,ssh,password))
        result.append(self.Check_DBL_323_EDT_AccessCTRL(host,ssh,password))
        result.append(self.Check_DBL_323_AccessCTRL_Main(host,ssh,password))
        result.append(self.Check_DBL_323_POST_Service(host,ssh,password))
        result.append(self.Check_DBL_324_EDT_Debug(host,ssh,password))
        result.append(self.Check_DBL_325(host,ssh,password))
        result.append(self.Check_DBL_326(host,ssh,password))
        result.append(self.Check_DBL_327(host,ssh,password))
        ssh.close()
        return result
        
    @namespace.expect(check_DBL_model_data, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta=[]
        result=pd.DataFrame()
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta = self.Check_DBL_Status(host=host,port=port,username=username,password=password)
                data_set = pd.DataFrame.from_records(respuesta)
                result = pd.concat([result, data_set],ignore_index=True)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                #respuesta[host] = {'host':host,'exception':exception}

        respuesta = result.to_dict(orient="split")
        print(result)
        return respuesta

@namespace.route("/04_analize_images_log")
class ClassAnalizeImagesLog(Resource):

    def count_image_with_face(self, host,port,username,password,initial_date = date.today() - datetime.timedelta(days=1),end_date = date.today() - datetime.timedelta(days=1)):
        image_with_face = 0
        facecascade = cv2.CascadeClassifier('api/haarcascade_frontalface_alt6.xml')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        #Create target folder structure
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_ImagesLog')==False):
            os.mkdir(host + '/_ImagesLog')

        #Job for all dates requiered
        current_date = initial_date
        while (current_date <= end_date):
            if (path.exists(host + '/_ImagesLog/' + str(current_date))==False):
                os.mkdir(host + '/_ImagesLog/' + str(current_date))
            #Get _ImagesLog
            img_file_counter=0
            target_path = host + '\\_ImagesLog\\' + str(current_date) + '\\'
            source_path = '/home/edt/Documents/Share/_ImagesLog/'
            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/user_not_identified*'+str(current_date) + '*.jpg'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for file in lines:
                sourceFile = file.split('/home/edt/Documents/Share/_ImagesLog/')[1]
                sourceFile = re.sub(r"[^a-zA-Z0-9. _-]","",sourceFile)
                #print('target_path:       ' + target_path + sourceFile)
                #print('source_path_file: ' + source_path + sourceFile)
                remote_path = source_path + sourceFile
                local_path = target_path + sourceFile
                if (path.isfile(local_path)==False):
                    sftp.get(remote_path, local_path)
                img = cv2.imread(local_path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = facecascade.detectMultiScale(img_gray, scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
                if len(faces)>0:
                    image_with_face=image_with_face+1
            current_date = current_date+ datetime.timedelta(days=1)
        
        sftp.close()
        ssh.close()
        return image_with_face

    def analize_images_log(self,host,port,username,password,initial_date,end_date):
        result={}
        result['host']=host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        current_date = initial_date
        user_identified = 0
        user_not_identified = 0
        not_identified_with_face =0
        user_not_face=0
        fever_temp = 0
        suspicious_temp = 0
        users_normal_temp = 0
        users_hub_posted = 0
        users_not_temp = 0
        temp_users = 0
        times_array = []
        while (current_date <= end_date):
            source_path = '/home/edt/Documents/Share/_ImagesLog/'

            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/user_identified*'+str(current_date) + '*.jpg | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if (len(lines) > 0 ):
                str_last_line = str(lines[-1]).replace('total','')
                user_identified = eval(str_last_line) + user_identified

            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/user_not_identified*'+str(current_date) + '*.jpg | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if (len(lines) > 0 ):
                str_last_line = str(lines[-1]).replace('total','')
                user_not_identified = eval(str_last_line) + user_not_identified

            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/fever_temp*'+str(current_date) + '*.jpg | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if (len(lines) > 0 ):
                str_last_line = str(lines[-1]).replace('total','')
                fever_temp = eval(str_last_line) + fever_temp

            command = 'cat /home/edt/Documents/Share/_Logs/post_log_'+str(current_date) + '.log | grep "User taken from queue" | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            post_file_count=0
            if (len(lines) > 0 ):
                str_last_line = str(lines[-1])
                post_file_count = eval(str_last_line)
            users_hub_posted = users_hub_posted + post_file_count

            command = 'cat /home/edt/Documents/Share/_Logs/bioaccesso_perf_'+str(current_date) + '.log |grep "TIEMPO TOTAL DE IDENTIFICACI0N:\|TEMPERATURA:"'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            post_file_count=0
            line_cnt=0
            for line in lines:
                if 'TIEMPO TOTAL DE IDENTIFICACI0N:' in line:
                    if 'TEMPERATURA:' in lines[line_cnt+1]:
                        line = line.replace('TIEMPO TOTAL DE IDENTIFICACI0N:','')
                        if ' TEMPERATURA: 0s' not in lines[line_cnt+1]:
                            times_array.append(eval(line.split('s')[0]))
                line_cnt=line_cnt+1

            command = 'cat /home/edt/Documents/Share/_Logs/post_log_'+str(current_date) + '.log |grep "User taken from queue:"'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            post_file_count=0
            line_cnt=0
            normal_temp_counter=0
            for line in lines:
                try:
                    line = line.replace(',',':')
                    temperature = eval(str(line.split(':')[11]))
                    if (temperature>=350 and temperature < 375):
                        normal_temp_counter = normal_temp_counter+1
                except:
                    pass
            users_normal_temp=users_normal_temp+normal_temp_counter

            #command = 'cat /home/edt/Documents/Share/_Logs/bioaccesso_perf_'+str(current_date) + '.log |grep "TIEMPO TOMA DE TEMPERATURA: 0s" | wc -l'
            #stdin, stdout, stderr = ssh.exec_command(command)
            #lines = stdout.readlines()
            #no_temp_count=0
            #if (len(lines) > 0 ):
            #    str_last_line = str(lines[-1])
            #    no_temp_count = eval(str_last_line)
            #users_not_temp = users_not_temp + no_temp_count

            command = 'ls -l /home/edt/Documents/Share/_ImagesLog/suspicious_temp*'+str(current_date) + '*.jpg | wc -l'
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            if (len(lines) > 0 ):
                str_last_line = str(lines[-1]).replace('total','')
                suspicious_temp = eval(str_last_line) + suspicious_temp            

            current_date = current_date+ datetime.timedelta(days=1)

        not_identified_with_face = self.count_image_with_face(host,port,username,password,initial_date,end_date)
        try:
            result['users_hub_posted'] = users_hub_posted
            result['temp_users'] = users_normal_temp+fever_temp+suspicious_temp
            result['user_identified'] = user_identified
            result['user_not_identified'] = user_not_identified
            result['not_identified_with_face'] = not_identified_with_face
            total_face_records = user_identified+not_identified_with_face
            if (total_face_records!=0):
                result['face_performance'] = int(100*(user_identified/total_face_records))
            else:
                result['face_performance'] = np.nan

            result['users_normal_temp'] = users_normal_temp
            result['fever_temp'] = fever_temp
            result['suspicious_temp'] = suspicious_temp                            
            #result['users_not_temp'] = users_not_temp
            if (user_identified!=0):
                result['temp_performance'] = 100 - int(100*((fever_temp+suspicious_temp)/user_identified))
            else:
                result['temp_performance'] = np.nan

            if (len(times_array) > 0):
                times_array = np.array(times_array)
                time_max = times_array.max()
                time_min = times_array.min()
                time_mean = times_array.mean()
                result['time_max'] = time_max
                result['time_min'] = time_min
                result['time_mean'] = time_mean                
            else:
                result['time_max'] = np.nan
                result['time_min'] = np.nan
                result['time_mean'] = np.nan

        except Exception as e:
            print('Exception:',str(e))
            result['users_hub_posted'] = users_hub_posted
            result['temp_users'] = users_normal_temp+fever_temp+suspicious_temp
            result['user_identified'] = user_identified
            result['user_not_identified'] = user_not_identified
            result['not_identified_with_face'] = not_identified_with_face
            result['face_performance'] = np.nan            
            result['users_normal_temp'] = users_normal_temp
            result['fever_temp'] = fever_temp
            result['suspicious_temp'] = suspicious_temp                                        
            #result['users_not_temp'] = users_not_temp
            result['temp_performance'] = np.nan
            result['time_max'] = np.nan
            result['time_min'] = np.nan
            result['time_mean'] = np.nan            
 
        ssh.close()        
        return result
            
    @namespace.expect(analize_images_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        initial_date = request.json['initial_date']
        initial_date = datetime.date(year=int(initial_date[0:4]), month=int(initial_date[5:7]), day=int(initial_date[8:10]))
        end_date = request.json['end_date']
        end_date = datetime.date(year=int(end_date[0:4]), month=int(end_date[5:7]), day=int(end_date[8:10]))
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta.append(self.analize_images_log(host=host,port=port,username=username,password=password,initial_date=initial_date,end_date=end_date))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)

        data_set = pd.DataFrame.from_records(respuesta)
        data_set['Total'] = data_set['user_identified'] + data_set['user_not_identified']
        stats={}
        stats['host'] = 'Stadistics'
        stats['users_hub_posted'] = data_set['users_hub_posted'].sum()
        stats['user_identified'] = data_set['user_identified'].sum()
        stats['temp_users'] = data_set['temp_users'].sum()
        stats['user_not_identified'] = data_set['user_not_identified'].sum()
        stats['not_identified_with_face'] = data_set['not_identified_with_face'].sum()
        stats['face_performance'] = data_set['face_performance'].mean()        
        stats['users_normal_temp'] = data_set['users_normal_temp'].sum()
        stats['fever_temp'] = data_set['fever_temp'].sum()
        stats['suspicious_temp'] = data_set['suspicious_temp'].sum()        
        #stats['users_not_temp'] = data_set['users_not_temp'].sum()
        stats['temp_performance'] = data_set['temp_performance'].mean()        
        stats['time_max'] = data_set['time_max'].max()
        stats['time_min'] = data_set['time_min'].min()
        stats['time_mean'] = data_set['time_mean'].mean()
        stats['Total'] = data_set['Total'].sum()

        df_dictionary = pd.DataFrame([stats])
        data_set = pd.concat([data_set, df_dictionary], ignore_index=True)
        print(data_set)
        data_set.to_excel(str(date.today()) + '_'+hosts[0]+'-'+hosts[-1]+'_Images_log_report.xlsx')
        return respuesta

@namespace.route("/03_check_freeze")
class ClassCheckFreeze(Resource):
    def get_screenshot(self,ssh,sftp,host):
        #Create target folder structure
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_Screenshot')==False):
            os.mkdir(host + '/_Screenshot')

        #Get current target path
        target_path = str(os. getcwd()) + '\\'+ host + '\\_Screenshot\\'

        #Erase any previous screenshot
        command = 'pwd'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        source_path = lines[0]
        source_path = re.sub(r"[^a-z. /\^A-Z, ^0-9]","",source_path)

        #Take screenshot
        command = 'xwd -out screenshot.xwd -root -display :0.0'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        now = datetime.datetime.now()

        screenshot_file_name = str(date.today()) + '_' + str(now.strftime("%H_%M_%S"))+'.jpg'
        #print('*'*50)
        #print(screenshot_file_name)
        command = 'convert screenshot.xwd ' + screenshot_file_name
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()

        source_path_file = source_path+'/'+screenshot_file_name
        #print('source_path_file:',source_path_file)

        target_path_file =  target_path + screenshot_file_name
        print('target_path_file:',target_path_file)

        sftp.get(source_path_file,target_path_file)

        command = 'rm ' + source_path+'/'+screenshot_file_name
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()

        command = 'rm ' + source_path+'/screenshot.xwd'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()        

        return target_path_file

    def check_screenshot(self,host,port,username,password):
        result={}
        result['host']=host
        result['screenshot_state']='NOT_DEFINED'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            sftp = ssh.open_sftp()
            file_full_screenshot1 = self.get_screenshot(ssh,sftp,host)
            full_screenshot1 = cv2.imread(file_full_screenshot1)
            #Get ROI Screen1
            screenshot1 = full_screenshot1[124:524,0:599]
            screenshot1_hist = cv2.calcHist([screenshot1], [0], None, [256], [0, 256])
            zeros = np.count_nonzero(screenshot1_hist==0)
            if zeros > 200:
                result['screenshot_state']=Yellow + ' SLEEP ' + White             #Print Yellow
            else:
                time.sleep(5)
                file_full_screenshot2 = self.get_screenshot(ssh,sftp,host)
                full_screenshot2 = cv2.imread(file_full_screenshot2)
                #Get ROI Screen2
                screenshot2 = full_screenshot2[124:524,0:599]            
                screenshot2_hist = cv2.calcHist([screenshot2], [0], None, [256], [0, 256])
                img_hist_diff = cv2.compareHist(screenshot1_hist, screenshot2_hist, cv2.HISTCMP_BHATTACHARYYA)
                img_template_probability_match = cv2.matchTemplate(screenshot1, screenshot2, cv2.TM_CCOEFF_NORMED)[0][0]
                img_template_diff = 1 - img_template_probability_match
                # taking only 10% of histogram diff, since it's less accurate then template method
                commutative_image_diff = (img_hist_diff / 10) + img_template_diff
                result['image_diff'] = commutative_image_diff
                print('commutative_image_diff:',commutative_image_diff)
                if (commutative_image_diff < 0.001):
                    result['screenshot_state']=Light_Red + '--> FREEZE <--' + White
                else:
                    result['screenshot_state']=Green + ' AWAKE ' + White

            cv2.destroyAllWindows()
            sftp.close()
            ssh.close()
        except Exception as e:
            result['host']=host
            result['screenshot_state']='NOT_CONNECTED'

              
        return result
            
    @namespace.expect(check_freeze_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta=[]
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta.append(self.check_screenshot(host=host,port=port,username=username,password=password))
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)

        data_set = pd.DataFrame.from_records(respuesta)
        data_set.to_excel(str(date.today()) + '_'+hosts[0]+'-'+hosts[-1]+'_freeze_report.xlsx')
        print(data_set)
        return respuesta

@namespace.route("/02_get_screenshot")
class ClassGetScreenshot(Resource):
    def get_screenshot(self, host,port,username,password):
        result = {}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        #Create target folder structure
        if (path.exists(host)==False):
            os.mkdir(host)
        if (path.exists(host + '/_Screenshot')==False):
            os.mkdir(host + '/_Screenshot')

        #Job for all dates requiered
        result['target_path'] = str(os. getcwd()) + '\\'+ host + '\\_Screenshot\\'

        #Get _ImagesLog
        target_path = result['target_path']

        #Erase any previous screenshot
        command = 'pwd'
        #print('executing command:',command)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        source_path = lines[0]
        #print('command response:',lines)
        source_path = re.sub(r"[^a-z. /\^A-Z, ^0-9]","",source_path)

        #Take screenshot
        command = 'xwd -out screenshot.xwd -root -display :0.0'
        #print('executing command:',command)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        #print('command response:',lines)
        now = datetime.datetime.now()

        screenshot_file_name = str(date.today()) + '_' + str(now.strftime("%H_%M_%S"))+'.jpg'
        command = 'convert screenshot.xwd ' + screenshot_file_name
        #print('executing command:',command)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        #print('command response:',lines)

        source_path_file = source_path+'/'+screenshot_file_name
        #print('source_path_file:',source_path_file)

        target_path_file =  target_path + screenshot_file_name
        #print('target_path_file:',target_path_file)

        sftp.get(source_path_file,target_path_file)

        command = 'rm ' + source_path+'/'+screenshot_file_name
        #print('executing command:',command)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        #print('command response:',lines)

        command = 'rm ' + source_path+'/screenshot.xwd'
        #print('executing command:',command)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        #print('command response:',lines)

        sftp.close()
        ssh.close()
        
        return result
            
    @namespace.expect(get_screenshot_model, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        for host in hosts:
            print('Processing: ',host)
            try:
                respuesta[host] = self.get_screenshot(host=host,port=port,username=username,password=password)
            except Exception as e:
                print('Exception was found processing ' + host + ' : ' + str(e))
                exception = 'Exception was found processing ' + host + ' : ' + str(e)
                respuesta[host] = {'host':host,'exception':exception}
        return respuesta

@namespace.route("/01_status")
class ClassStatus(Resource):
    def Check_Log_Files(self,ssh,password):
        command = 'ls -l /home/edt/Documents/Share/_Termografias/ |wc -l'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        for line in lines:
            _Termografias_files = eval(r''+ str(line).replace('\n',''))

        command = 'ls -l /home/edt/Documents/Share/_ImagesLog/ |wc -l'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        for line in lines:
            _ImagesLog = eval(r''+ str(line).replace('\n',''))

        command = 'ls -l /home/edt/Documents/Share/_Logs/ |wc -l'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        for line in lines:
            _Logs = eval(r''+ str(line).replace('\n',''))
        
        total_log_files = _Termografias_files+_ImagesLog+_Logs
        if (total_log_files > 20000):
            total_log_files ={'log_status':False,'total_log_files':total_log_files}
        else:
            total_log_files ={'log_status':True,'total_log_files':total_log_files}
        return total_log_files

    def Check_disk(self,ssh,password):
        command = 'df -h |grep "/dev/m"'
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        disk_info = lines[0].split(' ')
        size = disk_info[3]
        used = disk_info[6]
        available= disk_info[9]
        percentage=eval(disk_info[11].replace('%',''))
        disk_status = False
        if percentage < 60:
            disk_status = True

        disk_info ={'disk_status':disk_status,'size':size,'used':used,'available':available,'percentage':percentage}
        return disk_info

    def Check_temperatures(self,ssh,password):
        command = 'cat /sys/devices/virtual/thermal/thermal_zone*/temp'
        stdin, stdout, stderr = ssh.exec_command(command)
        temperatures_info = stdout.readlines()
        temp=[]
        for current_temp in temperatures_info:
            temp.append(eval(r''+ str(current_temp).replace('\n',''))/1000.0)
        temp.pop(4)
        max_temp = np.max(np.array(temp))

        temp_status = False
        if max_temp < 70:
            temp_status = True

        temperatures_info = {'temp_status':temp_status,'AO':temp[0],'CPU':temp[1],'GPU':temp[2],'PLL':temp[3],'Tboard_tegra':temp[4]}
        return temperatures_info
    
    def Check_SBA_status(self,ssh,password):
        command = 'systemctl status sba |grep Active'
        stdin, stdout, stderr = ssh.exec_command(command)
        sba_service_status = stdout.readlines()
        sba_status = False
        if 'Active: active (running)' in str(sba_service_status):
            sba_status = True
            comment = 'Active'
        else:
            sba_status = False
            comment = str(sba_service_status).replace(':','_')
            comment = re.sub(r"[^a-zA-Z0-9 _-]","",comment).replace('_',':').replace('  ',' ')        

        command = 'sudo journalctl -u sba.service -f'
        session = ssh.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()        
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        time.sleep(1)
        stdin.write(chr(3))
        stdin.flush()
        lines = stdout.readlines()

        sba_status = True
        for line in lines:
            line = str(line).replace(':','_')
            line = re.sub(r"[^a-zA-Z0-9 _-]","",line).replace('_',':').replace('  ',' ')
            print(line)
            error_info = ''
            if 'ERROR' in str(line).upper():
                sba_status = False
                error_info = error_info + 'ERROR: ' + line
        if error_info != '':
            comment = comment + '['+ error_info +']'
        sba_status_info = {'status':sba_status, 'comment': comment}

        return sba_status_info
    
    def Check_date_status(self,ssh,password):
        command = 'date +%F'
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh_response = stdout.readlines()
        date_status = False
        dev_date = ssh_response[0]
        dev_date = re.sub(r"[^0-9-]","",dev_date)       #Accept only valid data chars
        date_today = str(date.today())
        if (date_today in dev_date):
            date_status=True
        date_info = {'date_status':date_status,'dev_date':dev_date, 'today': date_today}      
        return date_info        

    def device_status(self,host,port,username,password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        #Check_date_status       
        new_result = {'host':host}
        new_result.update(self.Check_date_status(ssh,password))        
        #Check_SBA_status       
        new_result.update(self.Check_SBA_status(ssh,password))
        #Check_Temperatures
        new_result.update(self.Check_temperatures(ssh,password))
        #Check disk_usage
        new_result.update(self.Check_disk(ssh,password))
        #Check disk_usage
        new_result.update(self.Check_Log_Files(ssh,password))
        ssh.close()
        return new_result
        
    @namespace.expect(status_model_data, validate=True)
    @namespace.response(code=200, description="Success")
    @namespace.response(code=400, description="Request Validation Error")
    @namespace.response(code=500, description="Internal Server Error")
    def post(self):
        """Get status information from a device given the place name and a range of dates"""
        app.logger.info(f"json = {request.json}")
        hosts = eval(request.json['hosts'])
        port = 22
        username = 'edt'#os.environ['EDT_USER']
        password = 'admin' #os.environ['EDT_PASSWORD']
        respuesta={}
        result_list = []
        for host in hosts:
            print('Processing: ',host)
            try:
                result_list.append(self.device_status(host=host,port=port,username=username,password=password))
            except Exception as e:
                exception = 'Exception'
                result_list.append({'host':host,'comment':exception})

        data_set = pd.DataFrame.from_records(result_list) #.sort_values('total_log_files')
        data_set.to_excel(str(date.today()) + '_'+hosts[0]+'-'+hosts[-1]+'_status_report.xlsx')
        print(data_set)        
        return result_list