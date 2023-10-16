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
#          Description: This file executes the Manufacturing Service request.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#
#          File: Manufacturing_Services.py
#          Feature: Proteus
#          Design: PROTEUS_en_Dispositivo_de_Acceso_Biometrico.vsdx
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
import mod_ProTeUS.cfg.Proteus_Handler_cfg as PH_cfg
import mod_ProTeUS.cfg.Manufacturing_Services_cfg as Ms_cfg
import mod_ProTeUS.core.Proteus_Definitions as PD
from mod_ProTeUS.src.Proteus_Callout import *
from Config_Test.Manufacturing.API_MAN_Config_Cal import *
import math


# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------
def Unlock_Security_Algorithm_Level_1(buffer):
    # Algoritmo para desbloquear level
    # Return True in case security was unlock
    PD.logger.debug("Unlock_Security_Algorithm_Level_1")
    return True


def Get_SW_Version(buffer):
    """
        Sends the SW version Data
    """
    PD.logger.debug('Get SW version')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    configCal = API_MAN_Config_Cal.getInstance()
    result, data = configCal.Get_SWID()

    if result:
        # Check the SW ID is in the correct format
        numData = [int (elem) for elem in data]

        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Get_HW_Type(buffer):
    """
        Sends the Hardware type Data
    """
    PD.logger.debug('Get_HW_Type')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    configCal = API_MAN_Config_Cal.getInstance()
    result, data = configCal.Get_HWType()

    if result:
        """ In this case data is sent as a list due to Get_Positive_Response uses extend function
            to iterate values """
        numData = [int (elem) for elem in data]

        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_HW_Type(buffer):
    """
        Set's the new Hw type information
    """
    PD.logger.debug('Set_HW_Type')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3:]
    invalidChar = 0
    strData = ''
    elemIndx = 0

    for elem in data:
        # Condition modified to validate type of sensor (index 1) range from 0 to 2
        if (1 == len(str(elem)) and ((1 == elemIndx and elem >= 0 and elem <= Ms_cfg.MAX_HW_TYPE + 1)
           or (elemIndx != 1 and elem >= 0 and elem <= Ms_cfg.MAX_HW_TYPE))):
            strData = strData + str(elem)
            elemIndx = elemIndx + 1
        else:
            invalidChar = 1
            break

    if not invalidChar:
        configCal = API_MAN_Config_Cal.getInstance()
        result = configCal.Set_HWType(strData)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Serial_Number(buffer):
    """
        Sends the Serial number Data
    """
    PD.logger.debug('Get_Serial_Number')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_MAN_Config_Cal.getInstance()
    result, data = configCal.Get_SerialNumber()

    if result:
        encData = data.encode('utf-8')
        numData = [elem for elem in encData]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Serial_Number(buffer):
    """
        Set's the new Serial number information
    """
    PD.logger.debug('Set_Serial_Number')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3:]
    string_data = ''.join([chr(elem) for elem in data])

    if string_data.isalnum() and string_data[0] == 'B' \
       and (string_data[1] == 'P' or string_data[1] == '1') and \
       (1 == len(string_data[2]) and 1 == len(string_data[3]) and 1 == len(string_data[4])):
        configCal = API_MAN_Config_Cal.getInstance()
        result = configCal.Set_SerialNumber(string_data)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Mac_Address(buffer):
    """
        Gets the Mac Address
    """
    PD.logger.debug('Get_Mac_Address')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_MAN_Config_Cal.getInstance()
    result, data = configCal.Get_MacAddress()

    if result:
        encData = data.encode('utf-8')
        numData = [elem for elem in encData]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
# Nov-19-2020   Felipe Martinez
#   + DBL_140
#      - Implement the return of the Proteus response message
#
# Nov-30-2020   Edgar Hdz Meraz
#   + DBL_154
#      - Change Print statements to use logging to file instead
#
# Dec-23-2020   Edgar Hdz Meraz
#   + DBL_175
#      - Changes to validate calibration values according to new requirements
#        from spreadsheet
#
# Jan-22-2021   Edgar Hdz Meraz
#   + DBL_201
#      - Changes to get the Mac Address value
#########################################################################################
