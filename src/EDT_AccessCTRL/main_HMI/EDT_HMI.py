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
#          Module: HMI
#          Description: This script provides control of HMI.
#          Enterprise: Condumex
#          SW Developer: Ernesto Ulises Beltran
#
#          File: EDT_HMI.py
#          Feature: HMI
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################

import os
import threading
import sys
import cv2
import datetime
import enum
import time
import main_HMI.EDT_HMI_cfg as stac_cfg
import mod_EDT_AccessCTRL.EDT_AccessCTRL_cfg as ac_cfg
from main_HMI.core import Core
from multiprocessing import Process, Queue, Lock
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer, QPoint, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor, QBrush
# nzddvp - Testing HMI and Access Control redesign
#from mod_EDT_AccessCTRL.EDT_AccessCTRL import EDT_AccessCTRL
from mod_EDT_AccessCTRL.AccessCTRL_Main import MainProcess
from datetime import datetime as dt

from inspect import currentframe
from Config_Test.EDT_Debug import EDT_Logger

VERSION = "EDT_HMI v1.00"
IMG_SIZE    = 640,480          # 640,480 or 1280,720 or 1920,1080
IMG_FORMAT  = QImage.Format_RGB888
DISP_MSEC   = 48               # Delay between display cycles
CAP_API     = cv2.CAP_ANY       # API: CAP_ANY or CAP_DSHOW etc...

camera_num  = 1                 # Default camera (first in list)
image_queue = Queue(2)          # Queue to hold images
frame_queue = Queue(1)          # Queue to hold frame
signals_queue = Queue(1)        # Queue to update signals
frame_mutex = threading.Lock()  # Mutex to synchronize frame
running     = True              # Flag to indicate thread running

STYLE_SHEET_1 = 'color:grey;background-color:rgb(191, 199, 212);border:3px solid grey;border-radius:10px;'
STYLE_SHEET_2 = 'color:green;background-color:rgb(207, 229, 191);border:3px solid green;border-radius:10px;'
STYLE_SHEET_3 = 'color:green;background-color:rgb(207, 229, 191);border:3px solid green;border-radius:10px;'
STYLE_SHEET_4 = 'color:white;background-color:rgb(34, 177, 76);font: bold 42px;'
STYLE_SHEET_5 = 'color:white;background-color:rgb(237, 28, 36);font: bold 42px;'
STYLE_SHEET_6 = 'color:blue;background-color:rgb(132, 193, 249);border:3px solid blue;border-radius:10px;'
TEXT_EMPTY = ''
TEXT_1 = 'ACCESO AUTORIZADO' #Green per excel
TEXT_2 = 'ACCESO NEGADO\nNECESITAS CUBREBOCAS' #Red Req 676 
TEXT_3 = 'ACCESO NEGADO\nACUDE A SERVICIO MEDICO' #Red per excel
TEXT_4 = 'NO RECONOCIDO\nRETIRA TU CUBREBOCAS'  #Blue Req 594 Step_2
TEXT_5 = 'COLOCATE TU CUBREBOCAS' #Blue Req 102, 595 Step_3
TEXT_6 = 'BIENVENIDO\nVISITA'   #Red Req 329
TEXT_7 = 'NO RECONOCIDO\nCENTRE ROSTRO\nPARA RECAPTURA'  #Blue Req 668
TEXT_8 = 'ADQUIRIENDO TEMPERATURA'
TEXT_9 = 'ACCESO NEGADO\nPASA A VIGILANCIA' #Red
TEXT_10 ='TEMPERATURA SOSPECHOSA\nINTENTA DE NUEVO\nY ACERCATE' #Red  Req 669
TEXT_11 ='COLOCATE EN AREA\nDE IDENTIFICACION' #Req 679 
TEXT_12 ='IDENTIFICANDO'  #Blue Step_1

def getGstVideoStr(sensor_id, framerate, in_width, in_height, out_width, out_height, flip_method):
    gstVideoStr = 'nvarguscamerasrc wbmode=1 sensor-id=' + str(sensor_id) + ' tnr-mode=2 ee-mode=2 aeantibanding=1 !'
    gstVideoStr += ' video/x-raw(memory:NVMM), framerate=' + str(framerate) + '/1, width=' + str(in_width) + ', height=' + str(in_height) + ', format=NV12 !'
    gstVideoStr += ' nvvidconv flip-method=' + str(flip_method) + ' ! video/x-raw, width=' + str(out_width) + ', height=' + str(out_height) + ', format=BGRx !'
    gstVideoStr += ' videoconvert ! video/x-raw, format=BGR ! appsink'
    return gstVideoStr

sensor_id=0
framerate=ac_cfg.FRAMERATE
in_width = ac_cfg.IN_WIDTH
in_height = ac_cfg.IN_HEIGHT
out_width = ac_cfg.OUT_WIDTH
out_height = ac_cfg.OUT_HEIGHT
flip_method = ac_cfg.FLIP_METHOD
video_input_device = getGstVideoStr(sensor_id, framerate, in_width, in_height, out_width, out_height, flip_method)
face_min_width = 360 #out_width * ac_cfg.FACE_MIN_WIDTH_FACTOR
face_min_height = 360 #out_height * ac_cfg.FACE_MIN_HEIGHT_FACTOR
centre_x = 320 #using resolusion of 640*480 @TODO: use formula  #(out_width / 2)
centre_y = 240 #using resolusion of 640*480 @TODO: use formula  #out_height / 2
delta_x = face_min_width * 0.2
delta_y = face_min_height * 0.2
det_area_frame_color = (255, 255, 0)    # Yellow

# Access Control object created here because it is used in different
# functions and methods defined in first level of script.

def Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('hmi', debug_line, text)

# Grab images from the camera (separate thread)
def grab_image(cam_num, imageq, frameq, core):
    print('START: grab_image')
    if not core.config['target']:
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
    else:
        cap = cv2.VideoCapture(video_input_device, cv2.CAP_GSTREAMER)
    while running:
        if cap.grab():
            ret, frame = cap.retrieve(0)
            if ret and frame is not None:
                #Flip the image if needed
                if not core.config['target']:
                    frame = cv2.flip(frame, flipCode=1)
                #Cropping original image to change from 486*864 to 480*640
                frame = frame[6:, 178:818] #Xavier
                #frame = frame[6:, 46:686] #Nano
                #print(frame.shape)
                #Save frame to be analyzed/shown
                if imageq.qsize() < 2:
                    imageq.put(frame)
                if not frame_mutex.locked() and frameq.empty():
                    t = (True, frame)
                    frameq.put(t)
            else:
                time.sleep(DISP_MSEC / 100.0)
        else:
            print("Error: can't grab camera image")
            break
    cap.release()
    while frame_mutex.locked() and not frameq.empty():
        time.sleep(0.01)
    t = (False, None)
    frameq.put(t)
    print('END: grab_image')

# Get signals from the queue
def process_signals(signals, signalsq):
    print('START: process_signals')
    while running:
        if not signalsq.empty():
            try:
                signals_data = signalsq.get()
                if signals_data is not None and len(signals_data) > 0:
                    #print("-- HMI recibio signals de Access Control" + ' - ' + dt.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                    det = signals_data["display_on"]
                    rec = signals_data["rectangles"]
                    acc = signals_data["user_acc_status"]
                    info = signals_data["user_info"]
                    text = signals_data["message"]
                    signals.update(det, rec, acc, info, text)
            except Exception as e:
                print(e)
        else:
            time.sleep(0.001)
    print('END: process_signals')

# Typedef for rectangles object
class Rectangles(object):
    def __init__(self, rec):
        self.rectangles = rec

# Typedef for user info object
class Info(object):
    def __init__(self, info):
        self.info = info

# Worker update implementation
class WorkerUpdate():
    def __init__(self, sig, parent=None):
        self.signals = sig
        self.detFace = False
        self.usrAcc = False
        self.text = 0

    def update(self, det, rec, acc, info, text):
        if self.detFace != det:
            self.detFace = det
            self.signals.detection_update.emit(det)
        if self.usrAcc != acc:
            self.usrAcc = acc
            if not acc: self.signals.access_update.emit()
        if det and rec is not None:
            data = Rectangles(rec)
            self.signals.rectangles_update.emit(data)
        if det and info is not None:
            data = Info(info)
            self.signals.info_update.emit(data)
        if det and text is not None:
            self.text = text
            self.signals.text_update.emit(text)
        elif det and text is None and self.text != 0:
            self.text = 0
            self.signals.text_update.emit(0)
        else:  pass

# Image widget
class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None
        self.rectangles = None

    def setImage(self, image):
        #Draw the main image rectangle
        if self.rectangles is not None:
            for rec in self.rectangles:
                cv2.rectangle(image, (rec[0], rec[1]),
                            (rec[0] + rec[2], rec[1] + rec[3]), 
                            self.getColor(rec[4]), ac_cfg.LINE_THICKNESS)
        #Draw the target position rectangle
        cv2.rectangle(image, (int(centre_x-(face_min_width/2)), 
                            int(centre_y-(face_min_height/2))), 
                            (int(centre_x+(face_min_width/2)), 
                            int(centre_y+(face_min_height/2))), 
                            det_area_frame_color, 7)
        #@todo: remove sensor reference?
        #cv2.rectangle(image, (int(centre_x-2), int(centre_y-42)), 
                            #(int(centre_x+2),  int(centre_y-38)), 
                            #det_area_frame_color, 7) #Beta1
        cv2.rectangle(image, (int(centre_x-2), int(centre_y-86)), 
                            (int(centre_x+2),  int(centre_y-82)), 
                            det_area_frame_color, 7) #Beta2
        #Convert to Qt image format and update rendering
        disp_size = image.shape[1], image.shape[0]
        disp_bpl = disp_size[0] * 3
        self.image = QImage(image.data, disp_size[0], disp_size[1], 
                            disp_bpl, IMG_FORMAT)
        self.update()

    def setRectangles(self, rec):
        self.rectangles = rec

    def getColor(self, color):
        switcher = {'green':(0,255,0),'red':(255,0,0)}
        return switcher.get(color, (0,0,255))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(0, 0, self.image, 20, 40, 600, 400)
        qp.end()

# Defines the signals available
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    # Detection update signal
    detection_update = pyqtSignal(int)
    # User Access status signal
    access_update = pyqtSignal()
    # Rectangles array update signal
    rectangles_update = pyqtSignal(Rectangles)
    # User Info update signal
    info_update = pyqtSignal(Info)
    # User Text message update signal
    text_update = pyqtSignal(int)

# Main window
class MyWindow(QtWidgets.QDialog):
    # Create main window
    def __init__(self, core, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("Camera number %u" % camera_num)
        print("Camera size %u x %u" % IMG_SIZE)
        #Setup app objects
        print('target: %d' % core.config['target'])
        print('width: %d' % core.config['width'])
        print('height: %d' % core.config['height'])
        if core.config['target']:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        uic.loadUi(core.path('ui_main.ui'), self)
        self.core = core
        self.width = core.config['width']
        self.height = core.config['height']
        self._timer = None
        self.signals = WorkerSignals()
        self.image = ImageWidget(self)
        self.update = WorkerUpdate(self.signals)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.icon1 = []
        self.icon2 = []
        self.icon3 = []
        self.icon4 = []
        self.icon5 = []
        #Setup app widgets configuration
        self.setGeometry(0, 0, self.width, self.height)
        self.image.setGeometry(0, 124, 600, 400)
        #Create temperature indication label
        self.label_temp = QLabel(self)
        self.label_temp.setGeometry(0, 62, 600, 60)
        self.label_temp.hide()
        #Create Exit button
        self.button = QPushButton(self)
        self.button.clicked.connect(self.close)
        self.button.setStyleSheet("font: bold 34px;color: #e6e9ed;background-color:#495a75;")
        self.button.setGeometry(450, 0, 150, 50)
        self.button.setText('Exit')
        #self.button.show()
        self.button.hide()
        #Load icon1 (Bad Temperature) resources
        icon = QtGui.QIcon("./main_HMI/resources/256_Temp_Bad_Off.png")
        self.icon1.append(icon.pixmap(QtCore.QSize(130, 127)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Temp_Bad_On.png")
        self.icon1.append(icon.pixmap(QtCore.QSize(130, 127)))
        #Load icon2 (Good Temperature) resources
        icon = QtGui.QIcon("./main_HMI/resources/256_Temp_Good_Off.png")
        self.icon2.append(icon.pixmap(QtCore.QSize(130, 127)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Temp_Good_On.png")
        self.icon2.append(icon.pixmap(QtCore.QSize(130, 127)))
        #Load icon3 (Good Mask Detection) resources
        icon = QtGui.QIcon("./main_HMI/resources/256_Mask_Good_Off.png")
        self.icon3.append(icon.pixmap(QtCore.QSize(130, 127)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Mask_Good_On2.png")
        self.icon3.append(icon.pixmap(QtCore.QSize(130, 127)))
        #Load icon4 (Bad Mask Detection) resources
        icon = QtGui.QIcon("./main_HMI/resources/256_Mask_Bad_Off.png")
        self.icon4.append(icon.pixmap(QtCore.QSize(130, 127)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Mask_Bad_On.png")
        self.icon4.append(icon.pixmap(QtCore.QSize(130, 127)))
        #Load icon5 (Card icon) resources
        icon = QtGui.QIcon("./main_HMI/resources/256_Card_Off.png")
        self.icon5.append(icon.pixmap(QtCore.QSize(103, 78)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Card_On.png")
        self.icon5.append(icon.pixmap(QtCore.QSize(103, 78)))
        icon = QtGui.QIcon("./main_HMI/resources/256_Card_Bad.png")
        self.icon5.append(icon.pixmap(QtCore.QSize(103, 78)))
        self.label_5.setPixmap(self.icon5[0])
        self.label_5.show()
        #Load logo resources
        icon = QtGui.QIcon("./main_HMI/resources/logo.png")
        self.label_2.setPixmap(icon.pixmap(QtCore.QSize(305, 154)))
        self.label_2.show()
        #Set background color for widgets
        self.label_2.setStyleSheet("background-color:transparent;")
        self.label_5.setStyleSheet("background-color:transparent;")
        self.label_6.setStyleSheet("background-color:transparent;")
        self.label_7.setStyleSheet("background-color:transparent;")
        self.label_11.setStyleSheet("color:black;background-color:transparent;")
        self.label_15.setStyleSheet("color:black;background-color:transparent;")
        self.label_12.setStyleSheet("background-color:transparent;")
        self.label_13.setStyleSheet("color:black;background-color:transparent;")
        #Create Screen Disable label
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color:black;")
        self.label.setGeometry(0, 0, self.width, self.height)
        self.label.show()
        # Signals connection
        self.signals.detection_update.connect(self.update_detection)
        self.signals.access_update.connect(self.update_access)
        self.signals.rectangles_update.connect(self.update_rectangles)
        self.signals.info_update.connect(self.update_info)
        self.signals.text_update.connect(self.update_text)
        #init Steps icons
        self.hide_steps()

    def hide_steps(self):   
        self.label_Step1.hide()
        self.label_Step2.hide()
        self.label_Step3.hide()
        self.label_Step4.hide()

    # Start image capture & display
    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: 
                    self.show_image(image_queue, self.image))
        self.timer.start(DISP_MSEC)         # Timer to trigger display         

        self.capture_thread = threading.Thread(target=grab_image, 
                    args=(camera_num, image_queue, frame_queue, self.core))
        self.capture_thread.start()         # Thread to grab images

        self.signals_thread = threading.Thread(target=process_signals,
                    args=(self.update, signals_queue))
        self.signals_thread.start()        # Thread to update signals
        self.access_ctrl_thread = threading.Thread(target=MainProcess,
                    args=(frame_queue, signals_queue, frame_mutex))
        self.access_ctrl_thread.start()  # Thread for access control

    # Fetch camera image from queue, and display it
    def show_image(self, imageq, display):
        if not imageq.empty():
            image = imageq.get()
            if image is not None and len(image) > 0:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                display.setImage(img)

    # Kill time and date timer
    def kill_info_timer(self):
        if self._timer:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None

    # Start time and date timer
    def start_info_timer(self):
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self.disable_info)
            self._timer.setSingleShot(True)
            self._timer.start(3000)

    # Update detection related widgets
    @pyqtSlot(int)
    def update_detection(self, detection):
        print('Detection: %d' % detection)
        if detection:
            self.label.hide()
        else:
            self.label.show()
            self.label_6.hide()
            self.label_7.hide()
            self.label_11.hide()
            self.label_15.hide()
            self.label_temp.hide()
            self.label_5.setPixmap(self.icon5[0])
            self.label_13.setText('SAP : ------\nFCS : ------')
            self.label_4.setStyleSheet(STYLE_SHEET_1)
            self.label_4.setText(TEXT_EMPTY)
            self.hide_steps()

    # Update user access related widgets
    @pyqtSlot()
    def update_access(self):
        self.disable_info()

    # Update the rectangle detetections widgets
    @pyqtSlot(Rectangles)
    def update_rectangles(self, data):
        self.image.setRectangles(data.rectangles)

    # Update user info widgets
    @pyqtSlot(Info)
    def update_info(self, data):
        #Update autorization info
        auto = data.info['aut']
        mask = data.info['mask']
        self.update_authorized(auto, mask)
        #Update user and monitor info
        name = data.info[ac_cfg.NAME]
        last_name = data.info[ac_cfg.LAST_NAME]
        usrID = data.info['usrID']
        monID = data.info['monID']
        self.update_userInfo(name, last_name, usrID, monID)
        #Update temperature info
        temp = data.info['temp']
        self.update_temperature(auto, temp)
        #Start info timer
        #self.start_info_timer()

    # Update text message
    @pyqtSlot(int)
    def update_text(self, message):
        #Evaluate text zone information
        self.hide_steps()
        if message == 1:
            self.label_4.setStyleSheet(STYLE_SHEET_3)
            self.label_4.setText(TEXT_1)
        elif message == 2:
            self.label_4.setStyleSheet(STYLE_SHEET_2)
            self.label_4.setText(TEXT_2)
        elif message == 3:
            self.label_4.setStyleSheet(STYLE_SHEET_2)
            self.label_4.setText(TEXT_3)
        elif message == 4:
            self.label_4.setStyleSheet(STYLE_SHEET_6)
            self.label_4.setText(TEXT_4)
            self.label_Step1.show()
            self.label_Step2.show()         
        elif message == 5:
            self.label_4.setStyleSheet(STYLE_SHEET_3)
            self.label_4.setText(TEXT_5)
        elif message == 6:
            self.label_4.setStyleSheet(STYLE_SHEET_2)
            self.label_4.setText(TEXT_6)
            self.label_5.setPixmap(self.icon5[2])
        elif message == 7:
            self.label_4.setStyleSheet(STYLE_SHEET_6)
            self.label_4.setText(TEXT_7)
        elif message == 8:
            self.label_4.setStyleSheet(STYLE_SHEET_6)
            self.label_4.setText(TEXT_8)
            self.label_Step1.show()         
            self.label_Step2.show()         
            self.label_Step3.show()         
        elif message == 9:
            self.label_4.setStyleSheet(STYLE_SHEET_2)
            self.label_4.setText(TEXT_9)
        elif message == 10:
            self.label_4.setStyleSheet(STYLE_SHEET_2)
            self.label_4.setText(TEXT_10)
        elif message == 11:
            self.label_4.setStyleSheet(STYLE_SHEET_6)
            self.label_4.setText(TEXT_11)
        elif message == 12:
            self.label_4.setStyleSheet(STYLE_SHEET_6)
            self.label_4.setText(TEXT_12)
            self.label_Step1.show()
        elif message == 13:
            self.label_4.setStyleSheet(STYLE_SHEET_6)    # DBL_186
            self.label_4.setText(TEXT_12)
            self.label_Step1.show()
            self.label_Step2.show()
        else:
            self.disable_info()

    # Update autorization widgets
    def update_authorized(self, auto, mask):
        #Evaluate authorization rights
        if auto:
            print('--Authorized')
            self.label_6.setPixmap(self.icon2[1])
            self.label_6.show()
        elif mask:   #Show bad temperature icon only if mask was ok
            print('--Denied')
            self.label_6.setPixmap(self.icon1[1])
            self.label_6.show()
        #Evaluate Mask detection
        if mask:
            print('##Mask detected')
            self.label_7.setPixmap(self.icon3[1])
            self.label_7.show()
        else:
            print('##No Mask detected')
            self.label_7.setPixmap(self.icon4[1])
            self.label_7.show()

    # Update user and monitor info widgets
    def update_userInfo(self, name, last_name, usrID, monID):
        text = name.split(' ',1)
        self.label_11.setText('%s' % text[0])
        self.label_11.show()
        text = last_name.split(' ',1)
        self.label_15.setText('%s' % text[0])
        self.label_15.show()
        self.label_13.setText('SAP : %s\nFCS : %s' % (usrID,monID))
        if usrID == '0000' or last_name == 'Desconocido':
            self.label_5.setPixmap(self.icon5[1])   # Green ID CARD icon
        else:
            self.label_5.setPixmap(self.icon5[1])   # Green ID CARD icon

    # Update temperature info widgets
    def update_temperature(self, auto, temp):
        if int(float(temp)) > 0:
            style = STYLE_SHEET_4 if auto else STYLE_SHEET_5
            self.label_temp.setStyleSheet(style)
            self.label_temp.setText('%s C' % temp)
            self.label_temp.setAlignment(QtCore.Qt.AlignCenter)
            self.label_temp.show()
        # DBL_216
        if auto:
            self.label_5.setPixmap(self.icon5[1])   # Green ID CARD icon
        else:
            self.label_5.setPixmap(self.icon5[2])   # Red ID CARD icon

    # Disable user info widgets
    def disable_info(self):
        self.kill_info_timer()
        self.label_temp.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_11.hide()
        self.label_11.setText(TEXT_EMPTY)
        self.label_15.hide()
        self.label_15.setText(TEXT_EMPTY)
        self.label_5.setPixmap(self.icon5[0])
        self.label_13.setText('SAP : ------\nFCS : ------')
        self.label_4.setStyleSheet(STYLE_SHEET_1)
        self.label_4.setText(TEXT_EMPTY)
        self.hide_steps()

    # Update time and date info widgets
    def update_time(self):
        now = datetime.datetime.now()
        self.label_12.setText(now.strftime("%d/%m/%Y    %H:%M"))

    # Window is closing: stop video capture
    def closeEvent(self, event):
        global running
        running = False
        #self.access_ctrl.Shutdown()
        self.capture_thread.join()
        self.signals_thread.join()
        self.access_ctrl_thread.join()
        #access_ctrl.Shutdown()
        print('closeEvent')

#if __name__ == '__main__':
def app(core):
    # Main execution
    if camera_num < 1:
        print("Invalid camera number '%s'" % sys.argv[1])
    else:
        app = QApplication(sys.argv)
        win = MyWindow(core)
        win.setWindowTitle(VERSION)
        win.show()
        win.start()
        sys.exit(app.exec_())

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
# Oct-09-2020 Eduardo Gunter
#   + DBL_69:
#      -Updated text messages per new requirement.
#
# Oct-09-2020 Jonatan Uresti
#   + DBL_70:
#      -Updated identification area.
#
# Oct-15-2020 Ernesto Ulises Beltran, Eduardo Gunter
#   + DBL_93:
#      -Updated graphic interface and data flow.
#
# Oct-20-2020 Ernesto Ulises Beltran, Eduardo Gunter
#   + DBL_99:
#      -Updated data flow, robustness changes and fix
#       frame less window for target issue.
#
# Oct-27-2020 Eduardo Gunter
#   + DBL_69:
#      -Update messages per requirement change.
#      -Inculdes DBL_106
#
# Oct-29-2020 Eduardo Gunter
#   + DBL_109:
#      -Add blue box for info messages, remove word TEMP, 
#       show temp only if above 0
#
# Oct-30-2020 Cinthia Valdez / Jonatan Uresti
#   DBL_54:
#       - Redisign of Access Control
#       - Includes DBL_13, DBL_23, DBL_75, DBL_83, DBL_84, DBL_86, DBL_89, DBL_91,
#          DBL_92, DBL_102*, DBL_103, DBL_104, DBL_107
#
# Nov-05-2020 Ernesto Santos / Eduardo Gunter
#   + DBL_115:
#      -Change position of message box, Name, icons & ID fields.
#       Add red ID icon; Show only one name an one last name in separate lines
#       Update text messages per new requirements. Add robustness changes.
#
#13-11-2020 Lucia Chavez
#      -Change thicknes yellow and blue squares
#
# Nov-23-2020 Eduardo Gunter
#   + DBL_151:
#      -Add icons 1,2,3,4 to indicate steps sequence in the recognition process
#       Remove unnecesarry labels 8 and 9
#
# Dec-17-2020 Eduardo Gunter
#   + DBL_167:
#      -Change text_10 per new requirement SBASIS_669
#
# Dec-10-2020 Lucero Buenrostro
#   + DBL_TBD:
#      -Add queue for signals and thread for Access Control
#
# Jan-04-2021 Leobardo N Hernandez
#   + DBL_186
#      - Updated function update_text() to add the condition for hmi message 13.
# Jan-07-2021 Eduardo Gunter
#   + DBL_192:
#      - Set ID Card icon in red for an unknown user or invalid SAP number 
#
# 3 Feb 2021
#   + DBL_210:
#      - Changed message Text_8 for temperature
#
# Feb-15-2021 Leobardo N Hernandez
#   + DBL_216
#      - Updated function update_temperature().
#
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225
#      - Updated function Logger().
#
# Mar-10-2021 Leobardo N Hernandez
#   + DBL_234
#      - Updated function update_text().
#
# Mar-24-2021 Leobardo N Hernandez
#   + DBL_244
#      - Updated update_text function to do not show steps when message value is 5
#        (COLOCATE TU CUBREBOCAS).
#
#########################################################################################