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
#          File: ST_GPIOInterfaces.py
#          Feature: Stubs
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################
# packages
# sudo -H pip3 install Jetson.GPIO
# sudo -H groupadd -f -r gpio
# sudo -H usermod -a -G gpio "user_name"
# sudo -H
# sudo -H


# All imported modules must be added after config file
# Avoid use of 'cfg' as alias because all modules contain a config file
import mod_UserServices.ST_GPIOInterfaces_cfg as gpio_interfaces_cfg

import os
import cv2
import time
from threading import Timer
import sys

#-------------------
# Defines
#-------------------
RELAY1 = gpio_interfaces_cfg.RELAY1_GPIO_INTERFACE
RELAY2 = gpio_interfaces_cfg.RELAY2_GPIO_INTERFACE
BUZZER = gpio_interfaces_cfg.BUZZER_GPIO_INTERFACE

#-----------------------
# GPIO STATE VALUES
#-----------------------
GPIO_HIGH = True
GPIO_LOW = False

#-----------------------
# GLOBAL VARIABLES
#-----------------------
relay1TimerRunning = False
buzzerTimerRunning = False
relay1Timer = None
buzzerTimer = None

#-----------------------
# FUNCTIONS
#-----------------------
'''
def Start_Running_Relay1Timer():
    global relay1TimerRunning
    relay1TimerRunning = True

def Start_Running_BuzzerTimer():
    global buzzerTimerRunning
    buzzerTimerRunning = True

def Stop_Running_Relay1Timer():
    global relay1TimerRunning
    relay1TimerRunning = False

def Stop_Running_BuzzerTimer():
    global buzzerTimerRunning
    buzzerTimerRunning = False
'''

def Activate_RELAY1():
    global relay1TimerRunning
    gpio_interface.Set_GPIO_State(RELAY1, GPIO_LOW)
    relay1TimerRunning = True

def Activate_BUZZER():
    global buzzerTimerRunning
    gpio_interface.Set_GPIO_State(BUZZER, GPIO_HIGH)
    buzzerTimerRunning = True

def Deactivate_RELAY1():
    global relay1TimerRunning
    gpio_interface.Set_GPIO_State(RELAY1, GPIO_HIGH)
    if relay1Timer is not None:
        relay1Timer.cancel()
    relay1TimerRunning = False

def Deactivate_BUZZER():
    global buzzerTimerRunning
    gpio_interface.Set_GPIO_State(BUZZER, GPIO_LOW)
    if buzzerTimer is not None:
        buzzerTimer.cancel()
    buzzerTimerRunning = False

def startRelay1Timer():
    global relay1Timer
    relay1Timer = Timer(5.0,Deactivate_RELAY1)
    relay1Timer.start()

def startBuzzerTimer():
    global buzzerTimer
    buzzerTimer = Timer(0.2,Deactivate_BUZZER)
    buzzerTimer.start()

def cancelRelay1Timer():
    global relay1Timer
    relay1Timer.cancel()

def cancelBuzzerTimer():
    global buzzerTimer
    buzzerTimer.cancel()

class ST_GPIOInterfaces:
    __instance = None

    @staticmethod
    def getInstance():
        if ST_GPIOInterfaces.__instance is None:
            ST_GPIOInterfaces()
        return ST_GPIOInterfaces.__instance

    def __init__(self):
        if ST_GPIOInterfaces.__instance is not None:
            raise Exception('This class is singleton!')
        else:
            ST_GPIOInterfaces.__instance = self
            ST_GPIOInterfaces.Init_GPIO_Ports()

    @staticmethod
    def Init_GPIO_Ports():
        pass

    @staticmethod
    def Set_GPIO_State(gpio_pin, gpio_state):
        gpio_was_set = True
        return gpio_was_set

    @staticmethod
    def Get_GPIO_State(gpio_pin):
        gpio_current_state = GPIO_LOW
        return gpio_current_state

    @staticmethod
    def Clean_GPIO_Ports():
        pass

gpio_interface = ST_GPIOInterfaces.getInstance()

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
#########################################################################################
