import collections
import multiprocessing as mp
from multiprocessing import Process, Queue, Lock
import threading
from threading import Timer
from enum import Enum
from mod_EDT_AccessCTRL.EDT_AccessCTRL import EDT_AccessCTRL, Logger
from main_HMI.EDT_HMI_cfg import HMI_MESSAGES
from main_HMI.EDT_HMI_cfg import BOX_COLOR as HMI_BOX_COLOR
#nzddvp - testin HMI
import time
from datetime import datetime as dt

from Config_Test.EDT_Debug import *
from Config_Test.EDT_Statistics import *
from Config_Test.EDT_Thruput import *

def Save_User_Not_Identified_Record(no_mask_status):
    try:
        if no_mask_status:
            mask = '[N].'
        else:
            mask = '[S].'

        dt_string = '[BioAcceso] - ' + dt.now().strftime('%Y-%m-%d %H:%M:%S') + ': Intento de identificacion no exitoso, cubrebocas ' + mask
        file = open('users_not_identified.log', 'a+')
        #file.write(dt_string[:-0] + '\n')
        file.write(dt_string + '\n')
        file.close()
    except Exception as e:
        Logger('[BioAcceso] - Error al intentar guardar registro de usuario no identificado. ' + '(' + str(e) + ')' )

def Save_User_Not_Identified_Image(image, user, event):
    Images_Logger(image,user,event)

def Save_User_Identified_Image(image, user, event):
    Images_Logger(image,user,event)

def EDT_Errors_Logger(text):
    debug_line = str(currentframe().f_back.f_lineno)
    EDT_Logger('edt_errors', debug_line, text)

class AccessCTRL_States(Enum):
    DETECTION_STATE = 0
    DISPLAY_OFF_STATE = 1
    IDENTIFICATION_STATE = 2
    MASK_DETECTION_STATE = 3
    TEMPERATURE_MEASUREMENT_STATE = 4
    ALTERNATIVE_ID_STATE = 5
    EVALUATE_ACCESS_STATE = 6
    FOLLOW_UP_STATE = 7
    EXIT_STATE = 8

class AccessCTRL_FSM:
    def __init__(self): #, frame_queue, signals_queue, frame_mutex):
        # self._frameQueue = frame_queue
        # self._signalsQueue =  signals_queue
        # self._frameMutex = frame_mutex
        self._accessCtrl = EDT_AccessCTRL()
    
        self._currentState = AccessCTRL_States.DETECTION_STATE
        self._lastState = AccessCTRL_States.DISPLAY_OFF_STATE

        self._algoThreads = None  # Pool
        self._identificationActive = False  # Identification state running
        self._idAccuracyPercentage = 0.5

        # Variables to manipulate the Face identification and Mask Detection threads (or processes)
        self._identificationActive = False
        self._faceIdComplete = False
        self._faceIdResult = None

        self._maskDetectionActive = False  # @todo: it is not being used, remove?
        self._maskDetectionComplete = False
        self._maskDetectionResult = False

        # Variables to manipulate the Face identification and Mask Detection threads (or processes)
        self._faceToIdentify = "Eustacio"
        self._contProcess = True

        self._faceIdSuccess = False  # @todo: it is not being used, remove?
        self._usersIdList = []
        self._userID = '0000'
        self._maskStatus = False
        self._tempStatus = False

        self._noFaceTimer = Timer(10, self.NoFaceTimeout)
        self._stateTimer = Timer(5, self.StateTimeout)
        self._identificacionModelTimer = Timer(10,self.IdentificationModelTimeout)
        
        self._noFaceTimeout = False
        self._stateTimeout = False
        self._identificationModelTimeout = False

        # New variables
        self._identificationAttemptsCtr = 0
        self._MAX_IDENTIFICATION_ATTEMPTS = 2                   #DBL_323_PostServiceProcess
        self._alternativeIdNoMaskStatus = False
        self._alternativeIdFailAttempts = 0
        self._MAX_ALTERNATIVE_ID_FAIL_ATTEMPTS = 3
        self._evaluationDone = False
        self._display_on = True
        self.userInfo = None
        self._followUp = False
        self._aut = None
        self._name = None
        self._last_name = None
        self._monID = None
        self._temp = None
        self.StartIdentificationModelTimer(10)

        self._states = {
            AccessCTRL_States.DETECTION_STATE : self.DetectionState,
            AccessCTRL_States.DISPLAY_OFF_STATE : self.DisplayOffState,
            AccessCTRL_States.IDENTIFICATION_STATE : self.IdentificationState,
            AccessCTRL_States.MASK_DETECTION_STATE : self.MaskDetectionState,
            AccessCTRL_States.TEMPERATURE_MEASUREMENT_STATE : self.TemperatureMeasurementState,
            AccessCTRL_States.ALTERNATIVE_ID_STATE : self.AlternativeIdState,
            AccessCTRL_States.EVALUATE_ACCESS_STATE : self.EvaluateAccessState,
            AccessCTRL_States.FOLLOW_UP_STATE : self.FollowUpState,
            AccessCTRL_States.EXIT_STATE : self.ExitState
        }
        
        self._stateTimeLimits = {
            AccessCTRL_States.DETECTION_STATE : 60,
            AccessCTRL_States.DISPLAY_OFF_STATE : 0,
            AccessCTRL_States.IDENTIFICATION_STATE : 5,
            AccessCTRL_States.MASK_DETECTION_STATE : 5,
            AccessCTRL_States.TEMPERATURE_MEASUREMENT_STATE : 3,
            AccessCTRL_States.ALTERNATIVE_ID_STATE : 5,
            AccessCTRL_States.EVALUATE_ACCESS_STATE : 0,
            AccessCTRL_States.FOLLOW_UP_STATE : 2,
            AccessCTRL_States.EXIT_STATE: 0
        }
        self._HMImessage = None

        # Variables for debugging
        self._dbgFaceIdCounter = 0

    def DetectionState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Detection state")
                Logger("******************************")
                if AccessCTRL_States.DISPLAY_OFF_STATE == self._lastState:    # DBL_205
                    self._accessCtrl.TurnOnAuxiliaryLamp()
                self.StartStateTimer(900) # Stay 15 minutes in this state if no faces are detected
                self._lastState = self._currentState
                self._accessCtrl.ResetValues()
                self.StopNoFaceTimer()
                self._HMImessage = None
                self._display_on = True
                self.userInfo = None

            if self._accessCtrl.HasFaceToIdentify():
                Logger("DETECTION MSG: FACE DETECTED IN IDENTIFICATION AREA, TRANSITION TO IDENTIFICATION_STATE")
                self.StopStateTimer()
                # @TODO: Pintar cuadro azul al rostro a identificar
                self._currentState = AccessCTRL_States.IDENTIFICATION_STATE
            elif self._accessCtrl.HasFacesToDetect():
                Logger("DETECTION MSG: FACES IN DETECTION RANGE")
                self._HMImessage = HMI_MESSAGES.ACERCAR_A_ZONA_DE_ID.value
                self.StopStateTimer()
                # Paint blue squares
                # self.ResetTimers(60)
            elif self._stateTimeout:
                Logger("DETECTION MSG: STATE TIMEOUT, TRANSITION TO DISPLAY_OFF_STATE")
                self._currentState = AccessCTRL_States.DISPLAY_OFF_STATE
            else:
                #Logger("DETECTION MSG: NO FACES IN THE FRAME")
                self._HMImessage = None
                if not self._stateTimer.isAlive():
                    # Reinit the timer to stay 15 minutes in this state if no faces are detected
                    self.StartStateTimer(900) 
            if self._identificationModelTimeout:
                self._accessCtrl.UpdateIdentificationModel()
                self.StartIdentificationModelTimer(10)
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN DETECTION_STATE: " + str(e))

    def DisplayOffState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Display Off State")
                Logger("******************************")
                self._accessCtrl.TurnOffAuxiliaryLamp()    # DBL_205 
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                self.StopStateTimer()
                self._HMImessage = None
                self._display_on = False

            if self._accessCtrl.HasFacesToDetect():
                Logger("DISPLAY OFF_STATE MSG: FACES IN DETECTION RANGE, TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN DISPLAY_OFF_STATE: " + str(e))
    
    def IdentificationState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Identification State")
                Logger("******************************")
                self.StartStateTimer(3) # @TODO: State Timeout - Confirm the max time to complete an identification 
                self._lastState = self._currentState
                self._identificationAttemptsCtr = 0
                self._usersIdList = []
                self._userID = '0000'
                self._faceIdSuccess = False
                self.StopNoFaceTimer()
                self._HMImessage = None
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_INIT, time.time())
                Set_Thruput_Time(IDENTIFICATION_THRUPUT, THRUPUT_INIT, time.time())
                Update_Statistics(EDT_STATISTIC.ID_ATTEMPT, self._userID)
                # ------------------------------------------------------------------------------
                
            if self._stateTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(IDENTIFICATION_THRUPUT, THRUPUT_END, time.time())
                # ------------------------------------------------------------------------------
                Logger("IDENTIFICATION_STATE MSG: STATE TIMEOUT, TRANSITION TO ALTERNATIVE_ID_STATE")
                self._currentState = AccessCTRL_States.ALTERNATIVE_ID_STATE
            elif self._noFaceTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(IDENTIFICATION_THRUPUT, THRUPUT_END, time.time())
                Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_END, time.time())
                Save_Thruput()
                # ------------------------------------------------------------------------------
                Logger("EvaluateNoFaceTimer MSG: TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
            elif self._accessCtrl.HasFaceToIdentify():
                Logger("IDENTIFICATION_STATE MSG: IDENTIFYING...")
                self._HMImessage = HMI_MESSAGES.IDENTIFICANDO.value
                # @TODO: INIT NO FACES TIMER
                #self.ResetTimers(5)
                self.StopNoFaceTimer()
                self._usersIdList.append(self._accessCtrl.IdentifyUser())
                self._identificationAttemptsCtr = self._identificationAttemptsCtr + 1
                if self._identificationAttemptsCtr >= self._MAX_IDENTIFICATION_ATTEMPTS:
                    self._userID = self.GetIdentifiedUser()
                    Logger("ID: {0}, ID LIST {1}".format(self._userID, self._usersIdList))
                    if self._userID != '0000':
                        Logger("IDENTIFICATION_STATE MSG: SUCCESSFUL IDENTIFICATION, TRANSITION TO TEMPERATURE_MEASUREMENT_STATE")
                        # ------------------------------------------------------------------------------
                        Update_Statistics(EDT_STATISTIC.SUCCESSFUL_ID, self._userID)
                        # ------------------------------------------------------------------------------
                        self._faceIdSuccess = True
                        self._currentState = AccessCTRL_States.TEMPERATURE_MEASUREMENT_STATE
                        Save_User_Identified_Image(self._accessCtrl._frame,self._userID,'user_identified')
                    else:
                        Logger("IDENTIFICATION_STATE MSG: USER COULD NOT BE IDENTIFIED, TRANSITION TO ALTERNATIVE_ID_STATE")
                        self._currentState = AccessCTRL_States.ALTERNATIVE_ID_STATE
                        self._usersIdList = []
                        self._identificationAttemptsCtr = 0
                    # ------------------------------------------------------------------------------
                    Set_Thruput_Time(IDENTIFICATION_THRUPUT, THRUPUT_END, time.time())
                    # ------------------------------------------------------------------------------
            else:
                Logger("IDENTIFICATION_STATE MSG:: NO FACE TO IDENTIFY IN THE FRAME")
                if not self._noFaceTimer.isAlive():
                    Logger("EvaluateNoFaceTimer MSG: Start _noFaceTimer")
                    self.StartNoFaceTimer()
                else:
                    # Do nothing, keep in this state.    
                    Logger("EvaluateNoFaceTimer MSG: NO FACES TIMER RUNNING")
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN IDENTIFICATION_STATE: " + str(e))

    def MaskDetectionState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Mask Detection State")
                Logger("******************************")
                self.StartStateTimer(5)
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                self._maskStatus = False
                self._HMImessage = None
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(MASK_THRUPUT, THRUPUT_INIT, time.time())
                # ------------------------------------------------------------------------------

            if self._stateTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(MASK_THRUPUT, THRUPUT_END, time.time())
                # ------------------------------------------------------------------------------
                Logger("MASK_DETECTION_STATE MSG: STATE TIMEOUT, TRANSITION TO EVALUATE_ACCESS_STATE")
                self._currentState = AccessCTRL_States.EVALUATE_ACCESS_STATE
            elif self._noFaceTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(MASK_THRUPUT, THRUPUT_END, time.time())
                Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_END, time.time())
                Save_Thruput()
                Update_Statistics(EDT_STATISTIC.ABORTED_ID, self._userID)
                # ------------------------------------------------------------------------------
                Logger("EvaluateNoFaceTimer MSG: TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
            elif self._accessCtrl.HasFaceToIdentify():
                Logger("MASK_DETECTION_STATE MSG: DETECTING MASK...")
                self.StopNoFaceTimer()
                # @TODO: INIT NO FACES TIMER
                #self.ResetTimers(5)
                self._maskStatus = self._accessCtrl.GetMask(85.0)

                if not self._maskStatus:
                    Logger("MASK_DETECTION_STATE MSG: USER IS NOT WEARING A MASK")
                    self._HMImessage = HMI_MESSAGES.PUT_MASK.value

                Logger("MASK_DETECTION_STATE MSG: TRANSITION TO EVALUATE_ACCESS_STATE")
                self._currentState = AccessCTRL_States.EVALUATE_ACCESS_STATE    # DBL_211
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(MASK_THRUPUT, THRUPUT_END, time.time())
                # ------------------------------------------------------------------------------
            else:
                Logger("MASK_DETECTION_STATE MSG:: NO FACE TO IDENTIFY IN THE FRAME")
                if not self._noFaceTimer.isAlive():
                    Logger("EvaluateNoFaceTimer MSG: Start _noFaceTimer")
                    self.StartNoFaceTimer()
                else:
                    # Do nothing, keep in this state.    
                    Logger("EvaluateNoFaceTimer MSG: NO FACES TIMER RUNNING")
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN MASK_DETECTION_STATE: " + str(e))
            
    def TemperatureMeasurementState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Temperature Measurement State")
                Logger("******************************")
                self.StartStateTimer(1)
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                self._tempStatus = False
                self._accessCtrl._temperature = 0
                self._HMImessage = None
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(TEMPERATURE_THRUPUT, THRUPUT_INIT, time.time())
                # ------------------------------------------------------------------------------

            self._HMImessage = HMI_MESSAGES.ACERCAR_ROSTRO_PARA_TEMPERATURA.value
            if self._stateTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(TEMPERATURE_THRUPUT, THRUPUT_END, time.time())
                # ------------------------------------------------------------------------------
                Logger("TEMPERATURE_MEASUREMENT_ST MSG: STATE TIMEOUT, TRANSITION TO MASK_DETECTION_STATE")
                self._currentState = AccessCTRL_States.MASK_DETECTION_STATE
            elif self._noFaceTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(TEMPERATURE_THRUPUT, THRUPUT_END, time.time())
                Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_END, time.time())
                Save_Thruput()
                Update_Statistics(EDT_STATISTIC.ABORTED_ID, self._userID)
                # ------------------------------------------------------------------------------
                Logger("EvaluateNoFaceTimer MSG: TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
            # elif self._accessCtrl.HasFaceToIdentify(): @TODO: Check for HasFaceToIdentify when temp detection process change
            else:
                Logger("TEMPERATURE_MEASUREMENT_ST: MEASURING TEMPERATURE...")
                #self.StopNoFaceTimer()
                # @TODO: INIT NO FACES TIMER
                # self.ResetTimers(5)
                self._tempStatus = self._accessCtrl.GetTemperature(self._userID)

                if self._tempStatus:
                    # ------------------------------------------------------------------------------
                    Set_Thruput_Time(TEMPERATURE_THRUPUT, THRUPUT_END, time.time())
                    # ------------------------------------------------------------------------------
                    Logger("TEMPERATURE_MEASUREMENT_ST: SUCCESSFUL TEMPERATURE MEASUREMENT, TRANSITION TO MASK_DETECTION_STATE")
                    self._currentState = AccessCTRL_States.MASK_DETECTION_STATE
                # TODO: Uncomment next section when verifying HasFaceToIdentify
            """else: 
                print("MASK_DETECTION_STATE MSG:: NO FACE TO IDENTIFY IN THE FRAME")
                if not self._noFaceTimer.isAlive():
                    print("EvaluateNoFaceTimer MSG: Start _noFaceTimer")
                    self.StartNoFaceTimer()
                else:
                    # Do nothing, keep in this state.    
                    print("EvaluateNoFaceTimer MSG: NO FACES TIMER RUNNING")"""
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN TEMPERATURE_STATE: " + str(e))

    def AlternativeIdState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Alternative Id State")
                Logger("******************************")
                self.StartStateTimer(5)
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                self._identificationAttemptsCtr = 0
                self._usersIdList = []
                self._userID = '0000'
                self._faceIdSuccess = False
                self._alternativeIdFailAttempts = 0
                self. _alternativeIdNoMaskStatus = False
                self._HMImessage = None
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(ALTERNATIVE_THRUPUT, THRUPUT_INIT, time.time())
                # ------------------------------------------------------------------------------

            if self._stateTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(ALTERNATIVE_THRUPUT, THRUPUT_END, time.time())
                # ------------------------------------------------------------------------------
                Logger("ALTERNATIVE_ID_STATE MSG: STATE TIMEOUT, TRANSITION TO EVALUATE_ACCESS_STATE")
                self._currentState = AccessCTRL_States.EVALUATE_ACCESS_STATE
                Save_User_Not_Identified_Record(self._alternativeIdNoMaskStatus)
                Save_User_Not_Identified_Image(self._accessCtrl._frame,self._userID,'user_not_identified')
                # ------------------------------------------------------------------------------
                Update_Statistics(EDT_STATISTIC.UNSUCCESSFUL_ID, self._userID)
                # ------------------------------------------------------------------------------
            elif self._noFaceTimeout:
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(ALTERNATIVE_THRUPUT, THRUPUT_END, time.time())
                Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_END, time.time())
                Save_Thruput()
                # ------------------------------------------------------------------------------
                Logger("EvaluateNoFaceTimer MSG: TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
            elif self._accessCtrl.HasFaceToIdentify():
                self.StopNoFaceTimer()
                # @TODO: INIT NO FACES TIMER
                # self.ResetTimers(5)

                # @TODO: Should this verification be run all time?
                if not self._alternativeIdNoMaskStatus:
                    Logger("ALTERNATIVE_ID_STATE MSG: DETECTING MASK...")
                    if self._accessCtrl.GetMask(85.0):
                        Logger("ALTERNATIVE_ID_STATE MSG: USER IS WEARING A MASK, REQUEST TO REMOVE IT")
                        self._HMImessage = HMI_MESSAGES.REMOVE_MASK.value
                    else:
                        Logger("ALTERNATIVE_ID_STATE MSG: USER IS NOT WEARING A MASK, RETRY IDENTIFICATION")
                        self._alternativeIdNoMaskStatus = True
                        self.StartStateTimer(5)
                        # @TODO: Should the timer be reset????
                else:
                    # User has been removed the mask
                    Logger("ALTERNATIVE_ID_STATE MSG: IDENTIFYING...")
                    self._HMImessage = HMI_MESSAGES.IDENTIFICANDO_METODO_ALTERNO.value
                    self._usersIdList.append(self._accessCtrl.IdentifyUser())
                    self._identificationAttemptsCtr = self._identificationAttemptsCtr + 1
                    if self._identificationAttemptsCtr >= self._MAX_IDENTIFICATION_ATTEMPTS:
                        self._userID = self.GetIdentifiedUser()
                        Logger("ID: {0}, ID LIST {1}".format(self._userID, self._usersIdList))
                        if self._userID != '0000':
                            # ------------------------------------------------------------------------------
                            Set_Thruput_Time(ALTERNATIVE_THRUPUT, THRUPUT_END, time.time())
                            # ------------------------------------------------------------------------------
                            Logger("ALTERNATIVE_ID_STATE MSG: SUCCESSFUL IDENTIFICATION, TRANSITION TO TEMPERATURE_MEASUREMENT_STATE")
                            # ------------------------------------------------------------------------------
                            Update_Statistics(EDT_STATISTIC.ALTERNATIVE_ID, self._userID)
                            # ------------------------------------------------------------------------------
                            self._faceIdSuccess = True
                            self._currentState = AccessCTRL_States.TEMPERATURE_MEASUREMENT_STATE
                            Save_User_Identified_Image(self._accessCtrl._frame,self._userID,'user_identified')
                        elif self._alternativeIdFailAttempts < self._MAX_ALTERNATIVE_ID_FAIL_ATTEMPTS:
                            self._alternativeIdFailAttempts = self._alternativeIdFailAttempts + 1
                            Logger("ALTERNATIVE_ID_STATE MSG: FAIL IDENTIFICATION ATTEMPT {0}".format(self._alternativeIdFailAttempts))
                            # Reset values to start a new identification attempt
                            self._identificationAttemptsCtr = 0
                            self._usersIdList = []
                            self._userID = '0000'
                            self._faceIdSuccess = False
                        else:
                            # ------------------------------------------------------------------------------
                            Set_Thruput_Time(ALTERNATIVE_THRUPUT, THRUPUT_END, time.time())
                            # ------------------------------------------------------------------------------
                            Logger("ALTERNATIVE_ID_STATE MSG: FAIL IDENTIFICATION ATTEMPT {0}".format(self._alternativeIdFailAttempts))
                            Logger("ALTERNATIVE_ID_STATE MSG: USER COULD NOT BE IDENTIFIED, TRANSITION TO EVALUATE_ACCESS_STATE")
                            self._currentState = AccessCTRL_States.EVALUATE_ACCESS_STATE
                            Save_User_Not_Identified_Record(self._alternativeIdNoMaskStatus)
                            Save_User_Not_Identified_Image(self._accessCtrl._frame,self._userID,'user_not_identified')
                            # ------------------------------------------------------------------------------
                            Update_Statistics(EDT_STATISTIC.UNSUCCESSFUL_ID, self._userID)
                            # ------------------------------------------------------------------------------
            else:
                Logger("ALTERNATIVE_ID_STATE MSG: NO FACE TO IDENTIFY IN THE FRAME")
                if not self._noFaceTimer.isAlive():
                    Logger("EvaluateNoFaceTimer MSG: Start _noFaceTimer")
                    self.StartNoFaceTimer()
                else:
                    # Do nothing, keep in this state.
                    Logger("EvaluateNoFaceTimer MSG: NO FACES TIMER RUNNING")
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN ALTERNATIVE_ID_STATE: " + str(e))

    def EvaluateAccessState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Evaluate Access State")
                Logger("******************************")
                #self.StartStateTimer(5)
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                #self._accessCtrl.GetUserInfoFromDB()
                self._accessCtrl.GetUserInfoFromDB(self._userID)
                if self._userID=='12636_12636':
                    self._userID='------'

                self._evaluationDone = False
                #self._HMImessage = None
                # ------------------------------------------------------------------------------
                Set_Thruput_Time(EVALUATION_THRUPUT, THRUPUT_INIT, time.time())
                Update_Statistics(EDT_STATISTIC.COMPLETED_ID, self._userID)
                # ------------------------------------------------------------------------------

            Logger("EVALUATE_ACCESS_STATE MSG: EVALUATING ACCESS...")
            # self.ResetTimers(5)
            self._HMImessage = self._accessCtrl.EvaluateAccess(self._userID).value
            Logger("EVALUATE_ACCESS_STATE MSG: ACCESS DETERMINED")
            self._aut = self._accessCtrl._userInfo['authorized']
            self._name = self._accessCtrl._userInfo['name']
            self._last_name = self._accessCtrl._userInfo['last_name']
            self._monID = self._accessCtrl._userInfo['monitor_id']
            self._temp = round(self._accessCtrl._temperature,1)
            self._evaluationDone = True
            # ------------------------------------------------------------------------------
            Set_Thruput_Time(EVALUATION_THRUPUT, THRUPUT_END, time.time())
            Set_Thruput_Time(TOTAL_THRUPUT, THRUPUT_END, time.time())
            Save_Thruput()
            # ------------------------------------------------------------------------------
            self._currentState = AccessCTRL_States.FOLLOW_UP_STATE
            Logger("EVALUATE_ACCESS_STATE MSG: TRANSITION TO FOLLOW_UP_STATE")
            #Get info to send to HMI
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN EVALUATION_STATE: " + str(e))

    def FollowUpState(self):
        try:
            if(self._currentState != self._lastState):
                Logger("******************************")
                Logger("Follow Up State")
                Logger("******************************")
                self.StartStateTimer(2)            
                self._lastState = self._currentState
                self.StopNoFaceTimer()
                self._followUp = True
                #self._HMImessage = None
            #time.sleep(0.5)
            #self._currentState = AccessCTRL_States.DETECTION_STATE
            # self._accessCtrl.FollowUpUser()
            if self._accessCtrl._userInfo['box_position'] is not None:    #DBL_120
                if self._aut:
                    self._accessCtrl._highlightFace[0][4] = HMI_BOX_COLOR.GREEN.value
                else:
                    self._accessCtrl._highlightFace[0][4] = HMI_BOX_COLOR.RED.value

            if self._stateTimeout:
            #     self._lastState = self._currentState
                Logger("FOLLOW_UP_STATE MSG: STATE TIMEOUT, TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
                self._aut = False
                self._name = None
                self._last_name = None
                self._userID = None
                self._monID = None
                self._temp = None
                self._maskStatus = None
                self._followUp = False
                self._evaluationDone = False
                #self.userInfo = None
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN FOLLOW_UP_STATE: " + str(e))

    def ExitState(self):
        Logger("******************************")
        Logger("Exit State")
        Logger("******************************")

    def Shutdown(self):
        try:
            # @todo: stop threads if running, finish pending post and then call shutdown
            # or only set flag to false and call shutdown in MainProcess
            self._accessCtrl.Shutdown()
            self._contProcess = False
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN SHUTDOWN: " + str(e))

    def Default(self, frame):
        try:
            # TODO: Send frame to EDT_AccessCTRL ... setFrame(frame) ??
            self._accessCtrl.GetFaces(frame)
            if not self._accessCtrl.HasFacesToDetect():
                if self._noFaceTimer is None:
                    self._noFaceTimer = Timer(10, self.NoFaceTimeout)
                    self._noFaceTimer.start()
            # self._accessCtrl.GetMask(0.85)
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN DEFAULT: " + str(e))

    def GetIdentifiedUser(self):
        user_id = '0000'
        try:
            user_id_counters = collections.Counter(self._usersIdList)
            most_common_user = user_id_counters.most_common(1)

            for uid, identifications in most_common_user:
                # @todo: should ACCURACY_PERCENTAGE be part of the class?
                if identifications >= round(len(self._usersIdList) * self._idAccuracyPercentage):
                    user_id = uid
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN GET IDENTIFIED USER: " + str(e))

        return user_id

    def StartNoFaceTimer(self, timeLimit=2):
        try:
            self.StopNoFaceTimer()
            if timeLimit > 0:
                self._noFaceTimer = Timer(timeLimit, self.NoFaceTimeout)
                self._noFaceTimer.start()
                Logger('Starting new no face timer with limit {0}'.format(timeLimit))
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN START NO FACE TIMER: " + str(e))

    def StopNoFaceTimer(self):
        try:
            self._noFaceTimeout = False
            if self._noFaceTimer.isAlive():
                Logger('No Face timer is alive, stoping it')
                self._noFaceTimer.cancel()
                self._noFaceTimer.join()
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN STOP NO FACE TIMER: " + str(e))

    def EvaluateNoFaceTimer(self):
        try:
            if self._noFaceTimeout:
                Logger("EvaluateNoFaceTimer MSG: TRANSITION TO DETECTION_STATE")
                self._currentState = AccessCTRL_States.DETECTION_STATE
            elif not self._noFaceTimer.isAlive():
                Logger("EvaluateNoFaceTimer MSG: Start _noFaceTimer")
                self.StartNoFaceTimer()
            else:
                # Do nothing, keep in this state.    
                Logger("EvaluateNoFaceTimer MSG: NO FACES TIMER RUNNING")
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN EVALUATE NO FACE TIMER: " + str(e))

    def StartStateTimer(self, timeLimit):
        try:
            self.StopStateTimer()
            if timeLimit > 0:
                self._stateTimer = Timer(timeLimit, self.StateTimeout)
                self._stateTimer.start()
                Logger('Starting new state timer with limit {0}'.format(timeLimit))
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN START STATE TIMER: " + str(e))

    def StopStateTimer(self):
        try:
            self._stateTimeout = False
            if self._stateTimer.isAlive():
                Logger('State timer is alive, stoping it')
                self._stateTimer.cancel()
                self._stateTimer.join()
        except Exception as e:
            self._currentState = AccessCTRL_States.DETECTION_STATE
            self._HMImessage = None
            EDT_Errors_Logger("ERROR IN STOP STATE TIMER: " + str(e))

    def NoFaceTimeout(self):
        Logger("No face timeout")
        self._noFaceTimeout = True

    def StateTimeout(self):
        Logger("State timeout")
        self._stateTimeout = True

    def IdentificationModelTimeout(self):
        self._identificationModelTimeout = True

    def StartIdentificationModelTimer(self, timeLimit):
        try:
            self.StopIdentificationModelTimer()
            if timeLimit > 0:
                self._identificacionModelTimer = Timer(timeLimit,self.IdentificationModelTimeout)
                self._identificacionModelTimer.start()
        except Exception as e:
            EDT_Errors_Logger('ERROR AL INTENTAR INICIALIZAR EL TIMER PARA ACTUALIZAR EL MODELO DE IDENTIFICACION' + str(e))

    def StopIdentificationModelTimer(self):
        try:
            self._identificationModelTimeout = False
            if self._identificacionModelTimer.isAlive():
                self._identificacionModelTimer.cancel()
                self._identificacionModelTimer.join()
        except Exception as e:
            EDT_Errors_Logger('ERROR AL DETENER EL TIMER PARA ACTUALIZAR EL MODELO DE IDENTIFICACION' + str(e))
def MainProcess(frame_queue, signals_queue, frame_mutex):
    Logger('***** Starting MainProcess *****')
    frameQueue = frame_queue
    signalsQueue = signals_queue
    frameMutex = frame_mutex
    toggle_info = False
    user_info = {'aut': False,
                   'name': 'Cargando',
                   'last_name': '',
                   'usrID': '------',
                   'monID': '------',
                   'temp': 35.0,
                   'mask': False}
    hmi_signals = {'display_on': False, 'rectangles': None, 'user_acc_status': True,    # DBL_194
                       'user_info': user_info, 'message': None}
    signalsQueue.put(hmi_signals)

    fsm = AccessCTRL_FSM()
    user_info = None

    while fsm._contProcess:
        if not frameQueue.empty():
            frameMutex.acquire()
            try:
                cont, my_frame = frameQueue.get()
                if cont:
                    fsm.Default(my_frame)
                    state_function = fsm._states.get(fsm._currentState, lambda: None)
                    state_function()
                    num_faces = len(fsm._accessCtrl._faces)

                    if fsm._evaluationDone:
                        user_info = {'aut': fsm._aut,
                                       'name': fsm._name,
                                       'last_name': fsm._last_name,
                                       'usrID': fsm._userID,
                                       'monID': fsm._monID,
                                       'temp': fsm._temp,
                                       'mask': fsm._maskStatus}
                        acc_status = True
                        fsm._followUp = True
                    else:
                        user_info = None
                        acc_status = False

                    hmi_message = fsm._HMImessage if fsm._HMImessage is not None else None
                    hmi_signals = {'display_on': fsm._display_on,
                                   'rectangles': fsm._accessCtrl._highlightFace,
                                   'user_acc_status': acc_status, 
                                   'user_info': user_info,
                                   'message':  hmi_message}
                    signalsQueue.put(hmi_signals)
                else:
                    fsm._contProcess = False
            finally:
                frameMutex.release()
        else:
            time.sleep(0.001)
    fsm._accessCtrl.Shutdown()
    Logger('END: MainProcess')

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Dec-01-2020 Leobardo N Hernandez / Lucero Buenrostro / Jonatan Uresti
#   + DBL_196:
#      -Created initial file.
#
# Jan-27-2021 Leobardo N Hernandez
#   + DBL_196:
#      - Updated the time for transition from Detection to Display Off.
#
# Jan-28-2021 Leobardo N Hernandez
#   + DBL_205:
#      - Updated Detection state to turn on the auxiliary lamp when previous state has
#        been Display Off.
#      - Updated Display Off state to turn off the auxiliary lamp.
#
# Feb-02-2021 Leobardo N Hernandez
#   + DBL_209:
#      - Added Save_User_Not_Identified_Record() function to save the record when a
#        user was not identified.
#
# Feb-09-2021 Leobardo N Hernandez
#   + DBL_211:
#      - Updated Identification and AlternativeId states to get temperature once the
#        user has been identified.
#
# Feb-17-2021 Leobardo N Hernandez
#   + DBL_222:
#      - Updated Identification and AlternativeId states to provide the id of the
#        identified user to the temperature function.
#
# Feb-17-2021 Leobardo N Hernandez
#   + DBL_211:
#      - Updated Identification and AlternativeId states to transition to temperature
#        state instead of mask detection state once the user has been identified.
#
# Feb-17-2021 Leobardo N Hernandez
#   + DBL_120:
#      - Updated Follow Up state to update the box color of the face evaluated.
#
# Feb-18-2021 Leobardo N Hernandez
#   + DBL_225
#      - Updated most of the text sent to Logger.
#
# Feb-19-2021 Leobardo N Hernandez
#   + DBL_226
#      - Created function Save_User_Not_Identified_Image to save the frame when the 
#        user could not be identified.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_230
#      - Added image logger to save identified users.
#      - Added loggers to save identification statistics and performance of the device in
#        the identification process.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_231
#      - Updated Follow Up state to set proper color to face identified.
#      - Updated him_signals in MainProcess.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_232
#      - Added timer functions to update the identification model periodically.
#
# Mar-05-2021 Leobardo N Hernandez
#   + DBL_234
#      - Updated temperature state to display the HMI message again.
#
# Mar-26-2021 Lucia B Chavez
#   + DBL_247
#      - Added ABORTED_ID statistic in case the identification process is aborted due
#        to the timeout for no_face expired in temperature and mask detection states.
# Mar-24-2021 Leobardo N Hernandez
#   + DBL_244
#      - Updated MaskDetectionState function.
#
# Febrero-2022 Arturo Gaona
#   + DBL_323_PostServiceProcess Is_alive issue
#       - self._MAX_IDENTIFICATION_ATTEMPTS = 2
#
#########################################################################################