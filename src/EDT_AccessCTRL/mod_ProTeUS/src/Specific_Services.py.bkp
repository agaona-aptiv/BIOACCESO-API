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
#          Description: This file executes the Specific Service request.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#
#          File: Specific_Services.py
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
import mod_ProTeUS.cfg.Specific_Services_cfg as Sp_cfg
import mod_ProTeUS.core.Proteus_Definitions as PD
from mod_ProTeUS.src.Proteus_Callout import *
from Config_Test.SpecificServices.API_SS_Config_Cal import *


# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------
def Unlock_Security_Algorithm_Level_2(buffer):
    # Algoritmo para desbloquear level
    # Return True in case security was unlock
    PD.logger.debug("Unlock_Security_Algorithm_Level_2")
    return True


def Unlock_Security_Algorithm_Level_3(buffer):
    # Algoritmo para desbloquear level
    # Return True in case security was unlock
    PD.logger.debug("Unlock_Security_Algorithm_Level_3")
    return True


def Get_HW_Compatibility(buffer):
    """
        Sends the Hw compatibility Data
    """
    PD.logger.debug('Get_HW_Compatibility')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_HWCompatibility()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response



def Set_HW_Compatibility(buffer):
    """
        Set's the new Hw compatibility information
    """
    PD.logger.debug('Set_HW_Compatibility')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]

    if Sp_cfg.MAX_HW_VERSION >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_HWCompatibility(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Facial_Recognition(buffer):
    """
        Sends the status of the Facial Recognition feature
    """
    PD.logger.debug('Get_Facial_Recognition')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_FacialRecognition()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Facial_Recognition(buffer):
    """
        Set's the new Facial recognition information
    """
    PD.logger.debug('Set_Facial_Recognition')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]

    if Sp_cfg.MAX_DBL_CONFIG >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_FacialRecognition(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Temp_Detection(buffer):
    """
        Sends the status of the Temperature detection feature
    """
    PD.logger.debug('Get_Temp_Detection')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_TempDetection()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Temp_Detection(buffer):
    """
        Set's the new Temperature detection information
    """
    PD.logger.debug('Set_Temp_Detection')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]
    if Sp_cfg.MAX_DBL_CONFIG >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_TempDetection(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Door_Access(buffer):
    """
        Sends the status of the door access feature
    """
    PD.logger.debug('Get_Door_Access')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_DoorAccess()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Door_Access(buffer):
    """
        Set's the new Door Access information
    """
    PD.logger.debug('Set_Door_Access')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]

    if Sp_cfg.MAX_DBL_CONFIG >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_DoorAccess(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Facemask(buffer):
    """
        Sends the status of the Facemask feature
    """
    PD.logger.debug('Get_Facemask')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_FaceMask()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response



def Set_Facemask(buffer):
    """
        Set's the new Facemask information
    """
    PD.logger.debug('Set_Facemask')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]
    if Sp_cfg.MAX_DBL_CONFIG >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_FaceMask(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Send_Info_To_HUB(buffer):
    """
        Sends the status of the Send info to HUB feature
    """
    PD.logger.debug('Get_Send_Info_To_HUB')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_SendInfoToHub()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Send_Info_To_HUB(buffer):
    """
        Set's the new Send info to HUB information
    """
    PD.logger.debug('Set_Send_Info_To_HUB')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]
    if Sp_cfg.MAX_DBL_CONFIG >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_SendInfoToHub(data)

        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_White_Balance(buffer):
    """
        Sends the status of the white balance information
    """
    PD.logger.debug('Get_White_Balance')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_WhiteBalance()

    if result:
        numData = [int(data)]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_White_Balance(buffer):
    """
        Set's the new White Balance information
    """
    PD.logger.debug('Set_White_Balance')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    data = buffer[3]
    if Sp_cfg.MAX_WHITE_BALANCE_VALUES >= data >= 0:
        configCal = API_SS_Config_Cal.getInstance()
        result = configCal.Set_WhiteBalance(data)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Upper_Temp_Limit(buffer):
    """
        Sends the Upper temp limit value
    """
    PD.logger.debug('Get_Upper_Temp_Limit')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result,data = configCal.Get_UpperTempLimit()

    if result:
        strTempVal = data.split('.')
        numData = [int(elem) for elem in strTempVal]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Upper_Temp_Limit(buffer):
    """
        Set's the new Upper temp limit information
    """
    PD.logger.debug('Set_Upper_Temp_Limit')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    integer_temperature = buffer[3]
    decimal_temperature = buffer[4]
    PD.logger.debug("integer_temperature: {0}".format(integer_temperature))
    PD.logger.debug("decimal_temperature: {0}".format(decimal_temperature))

    if ((integer_temperature >= Sp_cfg.UPPER_TEMP_LIMIT_MIN_INTEGER and decimal_temperature >= 0) and
        (integer_temperature <= Sp_cfg.UPPER_TEMP_LIMIT_MAX_INTEGER and decimal_temperature <= Sp_cfg.UPPER_TEMP_LIMIT_MAX_DECIMALS)):
        data =  [integer_temperature, decimal_temperature]
        configCal = API_SS_Config_Cal.getInstance()
        strData = '.'.join([str(elem) for elem in data])
        result = configCal.Set_UpperTempLimit(strData)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Lower_Temp_Limit(buffer):
    """
        Sends the Lower temp limit data
    """
    PD.logger.debug('Get_Lower_Temp_Limit')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_LowerTempLimit()

    if result:
        strTempVal = data.split('.')
        numData = [int(elem) for elem in strTempVal]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Lower_Temp_Limit(buffer):
    """
        Set's the new lower temperature limit information
    """
    PD.logger.debug('Set_Lower_Temp_Limit')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    integer_temperature = buffer[3]
    decimal_temperature = buffer[4]

    if ((integer_temperature >= Sp_cfg.LOWER_TEMP_LIMIT_MIN_INTEGER and decimal_temperature >= 0) and
        (integer_temperature <= Sp_cfg.LOWER_TEMP_LIMIT_MAX_INTEGER and decimal_temperature <= Sp_cfg.LOWER_TEMP_LIMIT_MAX_DECIMALS)):
        data =  [integer_temperature, decimal_temperature]
        configCal = API_SS_Config_Cal.getInstance()
        strData = '.'.join([str(elem) for elem in data])
        result = configCal.Set_LowerTempLimit(strData)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_DBA_IP(buffer):
    """
        Sends the DBA IP
    """
    PD.logger.debug('Get_DBA_IP')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_DBAIP()

    if result:
        strIPVal = data.split('.')
        numData = [int(elem) for elem in strIPVal]
        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_DBA_IP(buffer):
    """
        Set's the new DBA IP
    """
    PD.logger.debug('Set_DBA_IP')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    addP1 = buffer[3]
    addP2 = buffer[4]
    addP3 = buffer[5]
    addP4 = buffer[6]

    if (Sp_cfg.MAX_ADDRESS_VALUE >= addP1 >= Sp_cfg.MIN_ADDRESS_VALUE) and (Sp_cfg.MAX_ADDRESS_VALUE >= addP2 >= Sp_cfg.MIN_ADDRESS_VALUE) and (
            Sp_cfg.MAX_ADDRESS_VALUE >= addP3 >= Sp_cfg.MIN_ADDRESS_VALUE) and (Sp_cfg.MAX_ADDRESS_VALUE >= addP4 >= Sp_cfg.MIN_ADDRESS_VALUE):
        configCal = API_SS_Config_Cal.getInstance()
        strData =  str(addP1) + '.' + str(addP2) + '.' + str(addP3) + '.' + str(addP4)
        result = configCal.Set_DBAIP(strData)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_HUB_URL(buffer):
    """
        Sends the HUB URL
    """
    PD.logger.debug('Get_HUB_URL')
    service = buffer[0]
    sub_service = buffer[1]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_HUBURL()
    resp_size = len(data)

    if result:
            encData = data.encode('utf-8')
            data = [int(elem) for elem in encData]
            response = Get_Positive_Response(service, sub_service, resp_size, data)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_HUB_URL(buffer):
    """
        Set's the new HUB URL
    """
    PD.logger.debug('Set_HUB_URL')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    try:
        data = buffer[3:]
        string_data = ''.join([chr(elem) for elem in data])

        if len(string_data) <=  Sp_cfg.MAX_URL_LENGTH:
            configCal = API_SS_Config_Cal.getInstance()
            result = configCal.Set_HUBURL(string_data)

            if result:
                response = Get_Positive_Response(service, sub_service, resp_size, 0)
            else:
                response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    except Exception as e:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Get_Face_Recognition_Rate(buffer):
    """
        Sends the Face recognition rate
    """
    PD.logger.debug('Get_Face_Recognition_Rate')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []
    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_FaceRecognitionRate()

    if result:
        numData = []
        strRateVal = data.split('.')
        numData.insert(0, int(strRateVal[0]))
        numData.insert(1, int(strRateVal[1]))

        if resp_size == len(numData):
            response = Get_Positive_Response(service, sub_service, resp_size, numData)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Face_Recognition_Rate(buffer):
    """
        Set's the new Face recognition Rate value
    """
    PD.logger.debug('Set_Face_Recognition_Rate')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    strUnits = str(buffer[3])
    units = buffer[3]
    strDec = str (buffer[4])
    invalidChar = 0

    if (not (1 == len(strUnits)) or units < 0 or units > 1 or not (1 == len(strDec))):
        invalidChar = 1

    if not invalidChar:
        configCal = API_SS_Config_Cal.getInstance()
        string_data = strUnits + '.' + strDec
        result = configCal.Set_FaceRecognitionRate(string_data)
        if result:
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


def Get_Access_Code(buffer):
    """
        Sends the Access code
    """
    PD.logger.debug('Get_Access_Code')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    configCal = API_SS_Config_Cal.getInstance()
    result, data = configCal.Get_AccessCode()

    if result:
        if resp_size == len(data):
            encData = data.encode('utf-8')
            data = [int(elem) for elem in encData]
            response = Get_Positive_Response(service, sub_service, resp_size, data)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    else:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)

    return response


def Set_Access_Code(buffer):
    """
        Set's the new Access code  value
    """
    PD.logger.debug('Set_Access_Code')
    service = buffer[0]
    sub_service = buffer[1]
    resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
    response = []

    try:
        data = buffer[3:]

        # Check if access code is alphanumeric and has no uppercase characters
        invalidChar = 0
        string_data = ''
        for elem in data:
            strElem = chr(elem)
            if (not strElem.isalnum()) or (strElem.isalpha() and strElem.isupper()):
                invalidChar = 1
                break
            else:
                string_data = string_data + strElem

        if not invalidChar:
            configCal = API_SS_Config_Cal.getInstance()
            result = configCal.Set_AccessCode(string_data)

            if result:
                response = Get_Positive_Response(service, sub_service, resp_size, 0)
            else:
                response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.GENERAL_FAILURE.value)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)
    except Exception as e:
        response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.DATA_OUT_OF_RANGE.value)

    return response


#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
# Oct-23-2020   Felipe Martinez
#   + DBL_101
#      - Add read/write API's for Access code variable.
#
# Nov-19-2020   Felipe Martinez
#   + DBL_140
#      - Implement the return of the Proteus response message
#
# Nov-30-2020   Edgar Hdz Meraz
#   + DBL_154
#      - Change Print statements to use logging to file instead
#
# Dec-20-2020   Edgar Hdz Meraz
#   + DBL_175
#      - Changes to use API calls in setters and getters
#########################################################################################
