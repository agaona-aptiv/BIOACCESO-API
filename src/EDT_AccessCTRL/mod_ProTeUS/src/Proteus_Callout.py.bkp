# ==============================================================================
#
# @file Proteus_Callout.py
#
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
#          Description: This file send the response of the Proteus request.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#
#          File: Proteus_Callout.py
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
import mod_ProTeUS.core.Proteus_Definitions as PD
import datetime


# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------
def Get_Positive_Response(service, subService, size, data):
    """
        Returns the positive response of the request
    """
    PD.logger.debug("Get_Positive_Response")
    response = [service, (subService + 1)]

    if 0 == size:
        response.append(1)  # size
        response.append(PD.ProteusResponseCode.NO_ERROR.value)  # Error code
    else:
        response.append((1 + size))  # size
        response.append(PD.ProteusResponseCode.NO_ERROR.value)  # Error code
        """ extend used to iterate on data with several values, such as 'Access Code', 
            'Serial Number' and all of those having more than 1 byte in length. For
            data having only 1 byte, it is necessary to pass the data values as list
            [data] """
        response.extend(data)

    return response


def Get_Negative_Response(service, subService, error):
    """
        Returns the negative response of the request
    """
    PD.logger.debug("Get_Negative_Response")
    response = [service, subService, 1, error]

    return response


def Get_Time_In_Millis():
    """
        Returns the current time in milliseconds
    """
    return int(round(datetime.datetime.now().timestamp() * 1000))

def Send_Session_Change(Session):
    """
        Sends the Session change to the appropriate module
    """
    PD.logger.debug("Send_Session_Change")

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
# Nov-30-2020   Edgar Hernandez
#   + DBL_154
#      - Change Print statements to use logging to file instead
#
# Dec-23-2020   Edgar Hdz Meraz
#   + DBL_175
#      - Changes to add comment about the use of the extend function in
#        Get_Positive_Response
#########################################################################################

