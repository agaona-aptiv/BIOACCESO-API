'''
Created on October, 2020
@author: Felipe Martinez
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: Proteus
#          Description: This file validates the Proteus request and calls for the appropriate API to execute it.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#
#          File: Unit_Test.py
#          Feature: Proteus
#          Design: PROTEUS_en_Dispositivo_de_Acceso_Biometrico.vsdx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#          Important: This module creates a configuration file for Manufacturing calibrations
#          and another one for Specific Services with default values. So, first, please make
#          sure to backup or delete any existing configuration file in paths:
#           \EDT_AccessCTRL\Config_Test\Manufacturing\MAN_CFG.txt
#           \EDT_AccessCTRL\Config_Test\SpecificServices\SS_CFG.txt
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
import unittest
from mod_ProTeUS.core.Proteus_Handler import *


# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------

class Test_0_Proteus_Class(unittest.TestCase):

    def test_0_TestMultipleGetInstances(self):
        # Preconditions for test
        py = ProteusHandler.getInstance()
        py2 = ProteusHandler.getInstance()

        self.assertTrue(py, py2)


class Tests_1_Manufacturing_Services(unittest.TestCase):

    def test_1_Enter_Manufacturing_Session(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x10, 0x02, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x02, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x03, 0x01, 0x02])

    def test_2_Unlock__Security_Level_1(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x10, 0x06, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x06, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x06, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x07, 0x01, 0x02])

    def test_3_Manufacturing_to_Default_Session(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x10, 0x04, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x04, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x05, 0x01, 0x02])

    def test_4_Get_SW_ID(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x08, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x08, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x08, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x09, 0x05, 0x02, 0x00, 0x00, 0x00, 0x00])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_5_Get_HW_Type(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x0A, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0A, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x0A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0B, 0x04, 0x02, 0x09, 0x09, 0x09])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_6_Set_HW_Type(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x0C, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0C, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x10, 0x0C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0C, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x10, 0x0C, 0x03, 0x01, 0x00, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0C, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x10, 0x06, 0x00]  # unlock security level 1
        rsp = py.Process_Message(request)

        request = [0x10, 0x0C, 0x03, 0xFF, 0x00, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0C, 0x01, 0x05])

        # Test: Correct request
        request = [0x10, 0x0C, 0x03, 0x01, 0x00, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0D, 0x01, 0x02])

        # Verify that the value 101 was set in config file by calling the Get function
        request = [0x10, 0x0A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0B, 0x04, 0x02, 0x01, 0x00, 0x01])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_7_Get_Serial_Number(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x0E, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0E, 0x01, 0x04])

        request = [0x10, 0x0E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0F, 0x06, 0x02, 0x42, 0x30, 0x30, 0x30, 0x30])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_8_Set_Serial_Number(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x10, 0x01, 0x27]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x10, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x10, 0x10, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x10, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x10, 0x10, 0x05, 0x42, 0x31, 0x30, 0x30, 0x30]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x10, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x10, 0x06, 0x00]  # unlock security level 1
        rsp = py.Process_Message(request)

        request = [0x10, 0x10, 0x05, 0x43, 0x30, 0x30, 0x30, 0x30]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x10, 0x01, 0x05])

        # Test: Correct request
        request = [0x10, 0x10, 0x05, 0x42, 0x31, 0x30, 0x30, 0x30]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x11, 0x01, 0x02])

        # Verify that the value B1000 was set in config file by calling the Get function
        request = [0x10, 0x0E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x0F, 0x06, 0x02, 0x42, 0x31, 0x30, 0x30, 0x30])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_9_Get_Mac_Address(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x10, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x10, 0x12, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x12, 0x01, 0x04])

        # Test: Correct request
        request = [0x10, 0x12, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x10, 0x13, 0x12, 0x02, 0x31, 0x32, 0x3A, 0x42, 0x33, 0x3A, 0x30, 0x37, 0x3A, 0x37, 0x36, 0x3A, 0x44, 0x36, 0x3A, 0x32, 0x32])

        # End test
        # Return to session 0
        request = [0x10, 0x04, 0x00]
        rsp = py.Process_Message(request)


class Tests_2_Specific_Services(unittest.TestCase):

    def test_01_Enter_Specific_Session(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x54, 0x02, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x02, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x03, 0x01, 0x02])

    def test_02_Unlock_Security_Level_2(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x54, 0x08, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x08, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x08, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x09, 0x01, 0x02])

    def test_03_Unlock_Security_Level_3(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x54, 0x0A, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0A, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x0A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0B, 0x01, 0x02])

    def test_04_Specific_to_Default_Session(self):
        # Pre-conditions for the test
        py = ProteusHandler.getInstance()

        # Test: Request with incorrect length
        request = [0x54, 0x04, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x04, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x05, 0x01, 0x02])

    def test_05_Get_HW_Compatibility(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x0C, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0C, 0x01, 0x04])

        request = [0x54, 0x0C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0D, 0x02, 0x02, 0x63])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_06_Set_HW_Compatibility(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x0E, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0E, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x0E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0E, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x0E, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0E, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        request = [0x54, 0x0E, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0E, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x0E, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0F, 0x01, 0x02])

        # Verify that the value 1 was set in config file by calling the Get function
        request = [0x54, 0x0C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x0D, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_07_Get_Facial_Recognition(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x10, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x10, 0x01, 0x04])

        request = [0x54, 0x10, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x11, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_08_Set_Facial_Recognition(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x12, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x12, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x12, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x12, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x12, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x12, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x12, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x12, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x12, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x13, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x10, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x11, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_09_Get_Temp_Detection(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x14, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x14, 0x01, 0x04])

        request = [0x54, 0x14, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x15, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_10_Set_Temp_Detection(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x16, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x16, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x16, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x16, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x16, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x16, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x16, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x16, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x16, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x17, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x14, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x15, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_11_Get_Door_Access(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x18, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x18, 0x01, 0x04])

        request = [0x54, 0x18, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x19, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_12_Set_Get_Door_Access(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x1A, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1A, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x1A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1A, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x1A, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1A, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x1A, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1A, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x1A, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1B, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x18, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x19, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_13_Get_Facemask(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x1C, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1C, 0x01, 0x04])

        request = [0x54, 0x1C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1D, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_14_Set_Facemask(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x1E, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1E, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x1E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1E, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x1E, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1E, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x1E, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1E, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x1E, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1F, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x1C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x1D, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_15_Get_Send_Info_To_HUB(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x20, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x20, 0x01, 0x04])

        request = [0x54, 0x20, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x21, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_16_Set_Send_Info_To_HUB(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x22, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x22, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x22, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x22, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x22, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x22, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x22, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x22, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x22, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x23, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x20, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x21, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_17_Get_White_Balance(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x24, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x24, 0x01, 0x04])

        request = [0x54, 0x24, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x25, 0x02, 0x02, 0x01])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_18_Set_White_Balance(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x26, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x26, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x26, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x26, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x26, 0x01, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x26, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        request = [0x54, 0x26, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x26, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x26, 0x01, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x27, 0x01, 0x02])

        # Verify that the value 0 was set in config file by calling the Get function
        request = [0x54, 0x24, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x25, 0x02, 0x02, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_19_Get_Upper_Temp_Limit(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x28, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x28, 0x01, 0x04])

        request = [0x54, 0x28, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x29, 0x03, 0x02, 0x25, 0X05])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_20_Set_Upper_Temp_Limit(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x2A, 0x01, 0x26]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2A, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x2A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2A, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x2A, 0x02, 0x26, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2A, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x2A, 0x02, 0x27, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2A, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x2A, 0x02, 0x26, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2B, 0x01, 0x02])

        # Verify that the value 38.0 (0x26, 0x00) was set in config file by calling the Get function
        request = [0x54, 0x28, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x29, 0x03, 0x02, 0x26, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_21_Get_Lower_Temp_Limit(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x2C, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2C, 0x01, 0x04])

        request = [0x54, 0x2C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2D, 0x03, 0x02, 0x22, 0X05])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_22_Set_Lower_Temp_Limit(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x2E, 0x01, 0x24]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2E, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x2E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2E, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x2E, 0x02, 0x24, 0x09]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2E, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x08, 0x00]  # unlock security level 2
        rsp = py.Process_Message(request)

        request = [0x54, 0x2E, 0x02, 0x25, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2E, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x2E, 0x02, 0x23, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2F, 0x01, 0x02])

        # Verify that the value 35.0 (0x23, 0x00) was set in config file by calling the Get function
        request = [0x54, 0x2C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x2D, 0x03, 0x02, 0x23, 0x00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_23_Get_DBA_IP(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x30, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x30, 0x01, 0x04])

        request = [0x54, 0x30, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x31, 0x05, 0x02, 0xFF, 0xFF, 0xFF, 0xFF])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_24_Set_DBA_IP(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x32, 0x01, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x32, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x32, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x32, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x32, 0x04, 0xFF, 0xFF, 0xFF, 0xFF]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x32, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        request = [0x54, 0x32, 0x04, 0xFF, 0xFF, 0xFF, 0x010A]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x32, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x32, 0x04, 0xFE, 0xFE, 0xFE, 0xFE]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x33, 0x01, 0x02])

        # Verify that the value 254.254.254.254 (0xFE, 0xFE, 0xFE, 0xFE) was set in config file by calling the Get function
        request = [0x54, 0x30, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x31, 0x05, 0x02, 0xFE, 0xFE, 0xFE, 0xFE])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    """ Note: For HUB URL Unit Tests, no verification is done about the length of data 
              due to it may change according to the server name of the company """
    def test_25_Get_HUB_URL(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        request = [0x54, 0x34, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x35, 0x4F, 0x02, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x6d, 0x69, 0x73, 0x61, 0x70, 0x6c, 0x69, 0x63, 0x61, 0x63, 0x69, 0x6f, 0x6e, 0x65, 0x73, 0x2e, 0x63, 0x69, 0x64, 0x65, 0x63, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x2f, 0x73, 0x62, 0x61, 0x5f, 0x68, 0x75, 0x62, 0x2f, 0x41, 0x50, 0x49, 0x2f, 0x70, 0x75, 0x62, 0x6c, 0x69, 0x63, 0x2f, 0x69, 0x6e, 0x64, 0x65, 0x78, 0x2e, 0x70, 0x68, 0x70, 0x2f, 0x61, 0x70, 0x69, 0x2f, 0x76, 0x31, 0x2f, 0x68, 0x75, 0x62, 0x61, 0x70, 0x69])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_26_Set_HUB_URL(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Correct request but no security unlocked
        request = [0x54, 0x36, 0x1A, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x36, 0x01, 0x09])

        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        # Test: Length of URL more than 255 characters
        request = [0x54, 0x36, 0x100, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x64, 0x75, 0x6d, 0x65, 0x78,
                   0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x76, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x76, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e,
                   0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x00, 0x00, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x36, 0x1A, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x37, 0x01, 0x02])

        # Verify that the value http://www.condumex.com.mx was set in config file by calling the Get function
        request = [0x54, 0x34, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x35, 0x1B, 0x02, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x63, 0x6f, 0x6e, 0x64, 0x75, 0x6d, 0x65, 0x78, 0x2e, 0x63, 0x6f, 0x6d, 0x2e, 0x6d, 0x78])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_27_Get_Face_Recognition_Rate(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x38, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x38, 0x01, 0x04])

        request = [0x54, 0x38, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x39, 0x03, 0x02, 0x00, 0X00])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_28_Set_Face_Recognition_Rate(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x3A, 0x03]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3A, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x3A, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3A, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x3A, 0x02, 0x00, 0x02]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3A, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        request = [0x54, 0x3A, 0x02, 0x02, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3A, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x3A, 0x02, 0x00, 0x02]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3B, 0x01, 0x02])

        # Verify that the value 0.2 (0x00, 0x02) was set in config file by calling the Get function
        request = [0x54, 0x38, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x39, 0x03, 0x02, 0x00, 0x02])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_29_Get_Access_Code(self):
        # Pre-conditions for the test
        # Obtain instance of the class an enter to Specific session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        #Write a specific access code
        request = [0x54, 0x3E, 0x40, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x3C, 0x01]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3C, 0x01, 0x04])

        # Test: Correct request
        request = [0x54, 0x3C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3D, 0x41, 0x02, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)

    def test_30_Set_Access_Code(self):
        # Pre-conditions for the test
        # Obtain instance of the class and enter to manufacturing session
        py = ProteusHandler.getInstance()
        request = [0x54, 0x02, 0x00]
        rsp = py.Process_Message(request)

        # Initialize testing
        # Test: Request with incorrect length
        request = [0x54, 0x3E, 0x40]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3E, 0x01, 0x04])

        # Test: Request with incorrect length
        request = [0x54, 0x3E, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3E, 0x01, 0x04])

        # Test: Correct request but no security unlocked
        request = [0x54, 0x3E, 0x40, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3E, 0x01, 0x09])

        # Test: Correct request but data out of range
        request = [0x54, 0x0A, 0x00]  # unlock security level 3
        rsp = py.Process_Message(request)

        request = [0x54, 0x3E, 0x40, 0x00, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3E, 0x01, 0x05])

        # Test: Correct request
        request = [0x54, 0x3E, 0x40, 0x31, 0x34, 0x34, 0x34, 0x34, 0x34, 0x34, 0x34, 0x31, 0x36, 0x33, 0x65, 0x63, 0x31, 0x63, 0x36, 0x33, 0x34, 0x34, 0x66, 0x30, 0x66, 0x32, 0x34, 0x32, 0x36, 0x36, 0x66, 0x32, 0x34, 0x66, 0x34, 0x31, 0x39, 0x38, 0x62, 0x30, 0x66, 0x39, 0x37, 0x33, 0x65, 0x62, 0x39, 0x66, 0x61, 0x32, 0x66, 0x34, 0x30, 0x65, 0x30, 0x39, 0x65, 0x36, 0x64, 0x33, 0x30, 0x35, 0x34, 0x61, 0x63, 0x35, 0x65]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3F, 0x01, 0x02])

        # Verify that the value 14444444163ec1c6344f0f24266f24f4198b0f973eb9fa2f40e09e6d3054ac5e
        # was set in config file by calling the Get function
        request = [0x54, 0x3C, 0x00]
        rsp = py.Process_Message(request)
        self.assertEqual(rsp, [0x54, 0x3D, 0x41, 0x02, 0x31, 0x34, 0x34, 0x34, 0x34, 0x34, 0x34, 0x34, 0x31, 0x36, 0x33, 0x65, 0x63, 0x31, 0x63, 0x36, 0x33, 0x34, 0x34, 0x66, 0x30, 0x66, 0x32, 0x34, 0x32, 0x36, 0x36, 0x66, 0x32, 0x34, 0x66, 0x34, 0x31, 0x39, 0x38, 0x62, 0x30, 0x66, 0x39, 0x37, 0x33, 0x65, 0x62, 0x39, 0x66, 0x61, 0x32, 0x66, 0x34, 0x30, 0x65, 0x30, 0x39, 0x65, 0x36, 0x64, 0x33, 0x30, 0x35, 0x34, 0x61, 0x63, 0x35, 0x65])

        # End test
        # Return to session 0
        request = [0x54, 0x04, 0x00]
        rsp = py.Process_Message(request)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)


#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
# Dec-23-2020   Edgar Hdz Meraz
#   + DBL_175
#      - Changes to modify test cases to check against default values of configuration
#        files and to add tests to set wrong and correct values of calibrations, acco-
#        rding to calibrations spreadsheet
#
# Jan-22-2021   Edgar Hdz Meraz
#   + DBL_201
#      - Changes to test sub-service 0x12 of manufacturing, in order to check read of
#        Mac Address value
#########################################################################################