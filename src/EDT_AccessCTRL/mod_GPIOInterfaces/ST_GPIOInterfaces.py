'''
Created on July, 2020
@author: Leobardo N Hernandez
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: GPIO Driver
#          Description: This script provides control of the GPIO ports.
#          Enterprise: Condumex
#          SW Developer: Leobardo N Hernandez
#
#          File: ST_GPIOInterfaces.py
#          Feature: GPIO driver
#          Design: Driagrama_Secuencia_DB_GPIO_Driver.pptx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
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
import mod_GPIOInterfaces.ST_GPIOInterfaces_cfg as gpio_interfaces_cfg

import unittest
import time
import RPi.GPIO as GPIO
from threading import Timer
from enum import Enum

#-------------------
# Defines
#-------------------
RELAY1 = gpio_interfaces_cfg.RELAY1_GPIO_INTERFACE
RELAY2 = gpio_interfaces_cfg.RELAY2_GPIO_INTERFACE
BUZZER = gpio_interfaces_cfg.BUZZER_GPIO_INTERFACE

RELAY1_ACTIVE_TIME = 5.0
RELAY2_ACTIVE_TIME = 5.0
BUZZER_ACTIVE_TIME_FOR_ACCESS = 0.200
BUZZER_ACTIVE_TIME_FOR_NOT_ACCESS = 0.125
BUZZER_ACTIVE_TIME_FOR_INVALID_TEMPERATURE = 0.050

#-----------------------
# GPIO STATE VALUES
#-----------------------
GPIO_HIGH = GPIO.HIGH
GPIO_LOW = GPIO.LOW

#-----------------------
# TYPES DEFINITION
#-----------------------
class BUZZER_SOUNDS(Enum):
    ACCESS_GRANTED = 0
    ACCESS_DENIED = 1
    ACCESS_DENIED_TEMPERATURE = 2

#-----------------------
# CLASSES DEFINITION
#-----------------------
class ST_ExternalDevices():
    __instance = None
    _gpio_interfaces = None

    _relay1TimerRunning: bool = False
    _relay2TimerRunning: bool = False
    _buzzerTimerRunning: bool = False
    _relay1Timer = None
    _relay2Timer = None
    _buzzerTimer = None

    _buzzerTimeCounter = 0
    _buzzerIsActive: bool = False
    _cyclicalBuzzerSound: bool = False

    _buzzerSoundCondition = None

    @staticmethod
    def getInstance():
        if ST_ExternalDevices.__instance is None:
            ST_ExternalDevices()
        return ST_ExternalDevices.__instance

    def __init__(self):
        if ST_ExternalDevices.__instance is not None:
            raise Exception('ST_ExternalDevices class is singleton!')
        else:
            ST_ExternalDevices.__instance = self
            self._gpio_interfaces = ST_GPIOInterfaces.getInstance()

    def Connect_External_Devices(self):
        initialization_success = False

        try:
            self._gpio_interfaces.Init_GPIO_Ports()
            initialization_success = True
        except Exception as e:
            self._gpio_interfaces.Clean_GPIO_Ports()
            #raise the GPIO initialization error

        return initialization_success

    def Activate_Relay1(self):
        activate_relay1_success = False

        try:
            if not self._relay1TimerRunning:
                self._gpio_interfaces.Set_GPIO_State(RELAY1, GPIO_LOW)
                self._relay1TimerRunning = True
            else: # Stop Timer
                self._relay1Timer.cancel()

            # Start running Timer
            self._relay1Timer = Timer(RELAY1_ACTIVE_TIME, self.Deactivate_Relay1)
            self._relay1Timer.start()
            activate_relay1_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return activate_relay1_success            

    def Deactivate_Relay1(self):
        deactivate_relay1_success = False

        try:
            self._gpio_interfaces.Set_GPIO_State(RELAY1, GPIO_HIGH)

            if self._relay1Timer is not None:
                self._relay1Timer.cancel()

            self._relay1TimerRunning = False
            deactivate_relay1_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return deactivate_relay1_success            

    def Activate_Relay2(self):
        activate_relay2_success = False

        try:
            self._gpio_interfaces.Set_GPIO_State(RELAY2, GPIO_LOW)
            activate_relay2_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return activate_relay2_success            

    def Deactivate_Relay2(self):
        deactivate_relay2_success = False

        try:
            self._gpio_interfaces.Set_GPIO_State(RELAY2, GPIO_HIGH)
            deactivate_relay2_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return deactivate_relay2_success            

    def Activate_Buzzer(self, buzzer_sound):
        activate_buzzer_success = False
        self._buzzerSoundCondition = buzzer_sound

        try:
            if not self._buzzerTimerRunning:
                self._gpio_interfaces.Set_GPIO_State(BUZZER, GPIO_HIGH)
                self._buzzerTimerRunning = True
            else: # Stop Timer
                self._buzzerTimer.cancel()

            if BUZZER_SOUNDS.ACCESS_DENIED == self._buzzerSoundCondition:
                self._cyclicalBuzzerSound = True
                self._buzzerTimeCounter = 8 # 1 second = 8 * BUZZER_ACTIVE_TIME_FOR_NOT_ACCESS
                self._buzzerTimer = Timer(BUZZER_ACTIVE_TIME_FOR_NOT_ACCESS, self.Cyclical_Buzzer)
            elif BUZZER_SOUNDS.ACCESS_DENIED_TEMPERATURE == self._buzzerSoundCondition:
                self._cyclicalBuzzerSound = True
                self._buzzerTimeCounter = 20 # 1 second = 20 * BUZZER_ACTIVE_TIME_FOR_INVALID_TEMPERATURE
                self._buzzerTimer = Timer(BUZZER_ACTIVE_TIME_FOR_INVALID_TEMPERATURE, self.Cyclical_Buzzer)
            else:
                self._cyclicalBuzzerSound = False
                self._buzzerTimer = Timer(BUZZER_ACTIVE_TIME_FOR_ACCESS, self.Deactivate_Buzzer)

            self._buzzerIsActive = True
            self._buzzerTimer.start()
            activate_buzzer_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return activate_buzzer_success            

    def Cyclical_Buzzer(self):
        cyclical_buzzer_success = False

        try:
            self._buzzerTimeCounter -= 1
            if self._buzzerIsActive:
                self._gpio_interfaces.Set_GPIO_State(BUZZER, GPIO_LOW)
                self._buzzerIsActive = False
            else:
                self._gpio_interfaces.Set_GPIO_State(BUZZER, GPIO_HIGH)
                self._buzzerIsActive = True

            if self._buzzerTimer is not None:
                self._buzzerTimer.cancel()

            if self._buzzerTimeCounter > 1:
                if BUZZER_SOUNDS.ACCESS_DENIED == self._buzzerSoundCondition:
                    self._buzzerTimer = Timer(BUZZER_ACTIVE_TIME_FOR_NOT_ACCESS, self.Cyclical_Buzzer)
                    self._buzzerTimer.start()
                elif BUZZER_SOUNDS.ACCESS_DENIED_TEMPERATURE == self._buzzerSoundCondition:
                    self._buzzerTimer = Timer(BUZZER_ACTIVE_TIME_FOR_INVALID_TEMPERATURE, self.Cyclical_Buzzer)
                    self._buzzerTimer.start()
                else:
                    pass #TODO: This case should not happen, if that, would the buzzer be stopped?
            else:
                self._buzzerTimerRunning = False
                self.Deactivate_Buzzer()
            cyclical_buzzer_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return cyclical_buzzer_success            

    def Deactivate_Buzzer(self):
        deactivate_buzzer_success = False

        try:
            self._gpio_interfaces.Set_GPIO_State(BUZZER, GPIO_LOW)
            if self._buzzerTimer is not None:
                self._buzzerTimer.cancel()

            self._buzzerTimerRunning = False
            deactivate_buzzer_success = True
        except Exception as e:
            self.Disconnect_Exterrnal_Devices()

        return deactivate_buzzer_success            

    def Disconnect_External_Devices(self):
        disconnect_success = False

        try:
            self._gpio_interfaces.Clean_GPIO_Ports()
            disconnect_success = True
        except Exception as e:
            self._gpio_interfaces.Clean_GPIO_Ports()
            #raise the GPIO clean error

        return disconnect_success


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
            #ST_GPIOInterfaces.Init_GPIO_Ports()

    @staticmethod
    def Init_GPIO_Ports():
        gpio_init_success = False

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(RELAY1,GPIO.OUT)
            GPIO.setup(RELAY2,GPIO.OUT)
            GPIO.setup(BUZZER,GPIO.OUT)
            GPIO.output(RELAY1,GPIO_HIGH)
            GPIO.output(RELAY2,GPIO_HIGH)
            GPIO.output(BUZZER,GPIO_LOW)
            gpio_init_success = True
        except Exception as e:
            print("GPIO Initialization failed! - " + str(e))
            GPIO.cleanup()

        return gpio_init_success

    @staticmethod
    def Set_GPIO_State(gpio_pin, gpio_state):
        gpio_was_set = False
        try:
            GPIO.output(gpio_pin, gpio_state)
            gpio_was_set = True
        except Exception as e:
            print("GPIO79 output exception - " + str(e))

        return gpio_was_set

    @staticmethod
    def Get_GPIO_State(gpio_pin):
        try:
            gpio_current_state = GPIO.input(gpio_pin)
        except Exception as e:
            print("GPIO79 input exception - " + str(e))
            gpio_current_state = GPIO_LOW

        return gpio_current_state

    @staticmethod
    def Clean_GPIO_Ports():
        gpio_clean_success = False

        try:
            GPIO.output(RELAY1,GPIO_HIGH)
            GPIO.output(RELAY2,GPIO_HIGH)
            GPIO.output(BUZZER,GPIO_LOW)
            GPIO.cleanup()
            gpio_clean_success = True
        except Exception as e:
            print("GPIO clean exception - " + str(e))

        return gpio_clean_success

'''
************************************************************************
**************************** Unit Test *********************************
*** https://docs.python.org/2/library/unittest.html#assert-methods *****
************************************************************************
'''
class TC001_Test_SingleTone(unittest.TestCase):
    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_1_TestSingletoneException(self):
        print('******************** test001_TestSingletone ************************')
        print('-------------------- test001_TestSingletoneException ---------------')
        gpioInterfaces = ST_GPIOInterfaces()
        exceptionFlag = False
        try:
            gpioInterfaces2 = ST_GPIOInterfaces()
        except Exception as e:
            exceptionFlag = True
        else:
            pass
        self.assertTrue(exceptionFlag, True)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_2_TestMultipleGetInstances(self):
        print('-------------------- test002_TestMultipleGetInstances ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        gpioInterfaces2 = ST_GPIOInterfaces.getInstance()
        self.assertEqual(gpioInterfaces, gpioInterfaces2)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_3_GPIO_initialization(self):
        gpio_initialization_success = False
        print('-------------------- test003_GPIO_Initialization ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        gpio_initialization_success = gpioInterfaces.Init_GPIO_Ports()
        self.assertEqual(gpio_initialization_success, True)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_4_Relay1_Set_High_State(self):
        gpio_set_result = GPIO_LOW
        print('-------------------- test004_Relay1_Set_High_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(RELAY1,GPIO_HIGH):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(RELAY1)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_HIGH)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_5_Relay1_Set_Low_State(self):
        gpio_set_result = GPIO_HIGH
        print('-------------------- test005_Relay1_Set_Low_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(RELAY1, GPIO_LOW):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(RELAY1)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_LOW)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_6_Relay2_Set_High_State(self):
        gpio_set_result = GPIO_LOW
        print('-------------------- test006_Relay2_Set_High_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(RELAY2, GPIO_HIGH):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(RELAY2)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_HIGH)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_7_Relay2_Set_Low_State(self):
        gpio_set_result = GPIO_HIGH
        print('-------------------- test007_Relay2_Set_Low_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(RELAY2, GPIO_LOW):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(RELAY2)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_LOW)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_8_Buzzer_Set_High_State(self):
        gpio_set_result = GPIO_LOW
        print('-------------------- test008_Buzzer_Set_High_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(BUZZER, GPIO_HIGH):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(BUZZER)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_HIGH)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_9_Buzzer_Set_Low_State(self):
        gpio_set_result = GPIO_HIGH
        print('-------------------- test009_Buzzer_Set_Low_State ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        if gpioInterfaces.Init_GPIO_Ports():
            if gpioInterfaces.Set_GPIO_State(BUZZER, GPIO_LOW):
                time.sleep(0.500)
                gpio_set_result = gpioInterfaces.Get_GPIO_State(BUZZER)
            gpioInterfaces.Clean_GPIO_Ports()

        self.assertEqual(gpio_set_result, GPIO_LOW)


    @unittest.skipIf(gpio_interfaces_cfg._debugTest == True, "DebugMode")
    def test001_10_GPIO_Cleanup(self):
        gpio_cleanup_success = False
        print('-------------------- test010_GPIO_Cleanup ---------------')
        gpioInterfaces = ST_GPIOInterfaces.getInstance()
        gpio_cleanup_success = gpioInterfaces.Clean_GPIO_Ports()
        self.assertEqual(gpio_cleanup_success, True)


#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Aug-07-2020 nzddvp
#   + Created initial file.
#
# Sep-08-2020 nzddvp
#   Description:
#       - Modified Set_GPIO_State() to solve the IssueID-11.
#       - Added Get_GPIO_State().
#
# Sep-25-2020 nzddvp
#   Description:
#       - Removed Init_GPIO_Ports from __init__ method.
#       - Removed the class instance from this script.
#
# Oct-08-2020 nzddvp
#   DBL_66:
#       - gpio_interface patch.
#
# Oct-21-2020 nzddvp
#   DBL_63:
#       - Added class ST_ExternalDevices().
#       - Removed unused code.
#
# Oct-21-2020 nzddvp
#   DBL_104:
#       - Added the condition to sound the buzzer every 100ms when the access control
#         detects a high temperature.
#       - Changed the buzzer sound time from 200ms to 250ms for the case when the access
#         control denies the access.
#
# Jan-28-2021 Leobardo N Hernandez
#   + DBL_205:
#      - Updated the implementation of the Activate/Deactivate functions for Relay2.
#
#########################################################################################
