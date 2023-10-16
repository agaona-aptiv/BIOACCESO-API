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
#          File: Proteus_Handler.py
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
import mod_ProTeUS.core.Proteus_Definitions as PD
import mod_ProTeUS.cfg.Session_ctrl_cfg as SC_cfg
from mod_ProTeUS.src.Proteus_Callout import *
from mod_ProTeUS.src.Manufacturing_Services import *
from mod_ProTeUS.src.Specific_Services import *


# -----------------------------------------------
#  Functions Definitions
# -----------------------------------------------
class ProteusHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """
            Static access method.
        """
        if ProteusHandler.__instance is None:
            ProteusHandler()
        return ProteusHandler.__instance

    def __init__(self):
        """
            Virtually private constructor.
        """
        if ProteusHandler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PD.logger.info("ProTeUS class created")
            ProteusHandler.__instance = self
            self.Security_Level_1_Unlocked = False
            self.Security_Level_2_Unlocked = False
            self.Security_Level_3_Unlocked = False
            self.Session_Started = False
            self.Current_Session = SC_cfg.SessionLevel.SESSION_0.value
            self.Service = 0
            self.SubService = 0
            self.Data_Size = 0
            self.Expiration_Timer = 0
            self.Current_Request = []

    def __Clear_Current_Request(self):
        """
            Clears all variables involved in the proteus process
        """
        self.Current_Request.clear()
        self.Service = 0
        self.SubService = 0
        self.Data_Size = 0

    def __Length_Message(self):
        """
            Determines if the received message has the number of bytes allowed(Min and Max bytes allowed)
        """
        response = False

        if (PD.MINIMUM_PARAMETERS <= len(self.Current_Request)) and (
                PD.MAX_BUFFER_SIZE >= len(self.Current_Request)):
            response = True
            PD.logger.info("Min and max length are correct")

        return response

    def __Service_Supported(self):
        """
            Determine if the Service is supported
        """
        result = False

        if self.Service in PH_cfg.Supported_Services_List:
            result = True
            PD.logger.info("Service_Supported")

        return result

    def __SubService_Supported(self):
        """
            Determine if the Sub-Service is supported
        """
        result = False

        if self.SubService in PH_cfg.Supported_Services_List[self.Service]:
            result = True
            PD.logger.info("SubService_Supported")

        return result

    def __Total_Length(self):
        """
            Determine if the number of bytes for the specific Service and Sub-service is correct
        """
        result = False

        """ 
            Special case to ignore length when getting or setting HUB URL, as it can be different
            according to every Company server
        """
        if self.Service == 0x54 and (self.SubService == 0x34 or self.SubService == 0x36):
            result = True

        elif (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                PD.SubServiceStructure.REQ_LEN.value] == len(self.Current_Request)) and (
                self.Data_Size == (
                PH_cfg.Supported_Services_List[self.Service][self.SubService][
                    PD.SubServiceStructure.REQ_LEN.value] - PD.MINIMUM_PARAMETERS)):
            result = True
            PD.logger.info("Total_Length correct")

        return result

    def __Supported_In_Active_Session(self):
        """
            Determine if the request is supported in the currect Proteus session
        """
        result = False

        if (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                PD.SubServiceStructure.SESSION.value] == self.Current_Session) or (
                PH_cfg.Supported_Services_List[self.Service][self.SubService][
                    PD.SubServiceStructure.SESSION.value] == SC_cfg.SessionLevel.SESSION_0.value):
            result = True
            PD.logger.debug("Supported_In_Active_Session")
        return result

    def __Security_Access_Unlocked(self):
        """
            Determine if the security has been unlocked for this particular request
        """
        result = False
        if (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                PD.SubServiceStructure.SECURITY.value] == SC_cfg.SecurityLevel.SEC_LEVEL_0.value) or (
                (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                     PD.SubServiceStructure.SECURITY.value] == SC_cfg.SecurityLevel.SEC_LEVEL_1.value) and (
                        True == self.Security_Level_1_Unlocked)) or (
                (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                     PD.SubServiceStructure.SECURITY.value] == SC_cfg.SecurityLevel.SEC_LEVEL_2.value) and (
                        True == self.Security_Level_2_Unlocked)) or (
                (PH_cfg.Supported_Services_List[self.Service][self.SubService][
                     PD.SubServiceStructure.SECURITY.value] == SC_cfg.SecurityLevel.SEC_LEVEL_3.value) and (
                        True == self.Security_Level_3_Unlocked)
        ):
            result = True
            PD.logger.info("Security_Access_Unlocked")

        return result

    def Process_Message(self, buffer):
        """
            Analysis and execution of the request
        """
        PD.logger.debug("Process_Message")
        self.Current_Request = buffer
        response = []

        if self.Session_Started:
            if self.__Get_Time_In_Millis() > (self.Expiration_Timer + PH_cfg.EXPIRATION_TIME):
                PD.logger.error("Timer expired")
                self.__Expired_Session()

        if self.__Length_Message():
            self.Service = self.Current_Request[0]
            self.SubService = self.Current_Request[1]
            self.Data_Size = self.Current_Request[2]

            if self.__Service_Supported():
                if self.__SubService_Supported():
                    if self.__Total_Length():
                        if self.__Supported_In_Active_Session():
                            if self.__Security_Access_Unlocked():
                                PD.logger.info("Function to be executed:")

                                response = eval('%s(%s)' % (
                                    PH_cfg.Supported_Services_List[self.Service][self.SubService][
                                        PD.SubServiceStructure.FUNCTION_NAME.value], self.Current_Request))
                            else:
                                PD.logger.error("Error in Security_Access_Unlocked")
                                response = Get_Negative_Response(self.Service, self.SubService,
                                                                 PD.ProteusResponseCode.SECURITY_ACCESS_DENIED.value)
                        else:
                            PD.logger.error("Error in Supported_In_Active_Session")
                            response = Get_Negative_Response(self.Service, self.SubService,
                                                             PD.ProteusResponseCode.NOT_ACTIVE_IN_CURRENT_SESSION.value)
                    else:
                        PD.logger.error("Error in Total_Length")
                        response = Get_Negative_Response(self.Service, self.SubService,
                                                         PD.ProteusResponseCode.INCORRECT_LENGTH.value)
                else:
                    PD.logger.error("Error in SubService_Supported")
                    response = Get_Negative_Response(self.Service, self.SubService,
                                                     PD.ProteusResponseCode.SUBSERVICE_NOT_SUPPORTED.value)
            else:
                PD.logger.error("Error in Service_Supported")
                response = Get_Negative_Response(self.Service, self.SubService,
                                                 PD.ProteusResponseCode.SERVICE_NOT_SUPPORTED.value)
        else:
            PD.logger.error("Error in Length_Message")
            response = Get_Negative_Response(self.Service, self.SubService,
                                             PD.ProteusResponseCode.INCORRECT_LENGTH.value)
        self.__Clear_Current_Request()
        self.Expiration_Timer = self.__Get_Time_In_Millis()

        return response

    def Enter_Session_0(self, buffer):
        """
            Set's the appropriate variables to the session 0 state
        """
        PD.logger.debug("Enter_Session_1")
        service = buffer[0]
        sub_service = buffer[1]
        resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
        response = []

        self.__Expired_Session()
        Send_Session_Change(self.Current_Session)
        response = Get_Positive_Response(service, sub_service, resp_size, 0)

        return response

    def Enter_Session_1(self, buffer):
        """
            Set's the appropriate variables to the session 1 state
        """
        PD.logger.debug("Enter_Session_1")
        service = buffer[0]
        sub_service = buffer[1]
        resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
        response = []

        self.Security_Level_2_Unlocked = False
        self.Security_Level_3_Unlocked = False
        self.Current_Session = SC_cfg.SessionLevel.SESSION_1.value
        self.Session_Started = True
        Send_Session_Change(self.Current_Session)
        response = Get_Positive_Response(service, sub_service, resp_size, 0)

        return response

    def Enter_Session_2(self, buffer):
        """
            Set's the appropriate variables to the session 2 state
        """
        PD.logger.debug("Enter_Session_2")
        service = buffer[0]
        sub_service = buffer[1]
        resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
        response = []

        self.Security_Level_1_Unlocked = False
        self.Current_Session = SC_cfg.SessionLevel.SESSION_2.value
        self.Session_Started = True
        Send_Session_Change(self.Current_Session)
        response = Get_Positive_Response(service, sub_service, resp_size, 0)

        return response

    def Enter_Session_3(self, buffer):
        """
            Set's the appropriate variables to the session 3 state
        """
        PD.logger.debug("Enter_Session_3")
        service = buffer[0]
        sub_service = buffer[1]
        resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
        response = []

        self.__Clear_Session_Data()
        self.Current_Session = SC_cfg.SessionLevel.SESSION_3.value
        self.Session_Started = True
        Send_Session_Change(self.Current_Session)
        response = Get_Positive_Response(service, sub_service, resp_size, 0)

        return response

    def Unlock_Security_Access_Level_1(self, buffer):
        """
            Determines if the Security Level 1 can be unlocked
        """
        PD.logger.debug('Unlock_Security_Access_Level_1')
        service = buffer[0]
        sub_service = buffer[1]
        response = []

        if Unlock_Security_Algorithm_Level_1(buffer):
            self.Security_Level_1_Unlocked = True
            resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.INVALID_KEY.value)

        return response

    def Unlock_Security_Access_Level_2(self, buffer):
        """
            Determines if the Security Level 2 can be unlocked
        """
        PD.logger.debug('Unlock_Security_Access_Level_2')
        service = buffer[0]
        sub_service = buffer[1]
        response = []

        if Unlock_Security_Algorithm_Level_2(buffer):
            self.Security_Level_2_Unlocked = True
            resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.INVALID_KEY.value)

        return response

    def Unlock_Security_Access_Level_3(self, buffer):
        """
            Determines if the Security Level 3 can be unlocked
        """
        PD.logger.debug('Unlock_Security_Acces_Level_3')
        service = buffer[0]
        sub_service = buffer[1]
        response = []

        if Unlock_Security_Algorithm_Level_3(buffer):
            self.Security_Level_3_Unlocked = True
            resp_size = PH_cfg.Supported_Services_List[service][sub_service][PD.SubServiceStructure.RESP_LEN.value]
            response = Get_Positive_Response(service, sub_service, resp_size, 0)
        else:
            response = Get_Negative_Response(service, sub_service, PD.ProteusResponseCode.INVALID_KEY.value)

        return response

    def __Get_Time_In_Millis(self):
        """
            Get the current time in milliseconds
        """
        return Get_Time_In_Millis()

    def __Expired_Session(self):
        """
            Clears all the state flags and enters to Session 0
        """
        self.Session_Started = False
        self.Current_Session = SC_cfg.SessionLevel.SESSION_0.value
        self.__Clear_Session_Data()
        Send_Session_Change(self.Current_Session)

    def __Clear_Session_Data(self):
        """
            Clears all Security level flags
        """
        self.Security_Level_1_Unlocked = False
        self.Security_Level_2_Unlocked = False
        self.Security_Level_3_Unlocked = False

    def Get_Current_Session(self):
        """
            Returns the current session of Proteus
        """
        return self.Current_Session



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
# Jan-14-2021 Edgar Hdz Meraz
#   + DBL_175
#      - Change in __Total_Length function to ignore length of string when Setting or Getting
#        the HUB URL. This is due to the URL length of HUB servers is different.
#########################################################################################
