'''
Created on November, 2020
@author: Lucero Buenrostro
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: Request Handler
#          Description: This script provides an interface to Proteus services
#          Enterprise: Condumex
#          SW Developer: Lucero Buenrostro
#
#          File: Handler.py
#          Feature: Request handler
#          Design:
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#
#########################################################################################
from multiprocessing.connection import Listener, Client
import socket
import socketserver
import multiprocessing as mp
from sys import platform
import signal
from mod_ProTeUS.core.Proteus_Handler import *
from threading import Thread
import threading
import time
import logging


# -------------------
# Defines
# -------------------
try:
    HOST_ADDRESS = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
    if HOST_ADDRESS == '':
        HOST_ADDRESS = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
except Exception as e:
    logger.info("The IP of the device could not be read: " + str(e))
    HOSTNAME = socket.gethostname()
    HOST_ADDRESS = socket.gethostbyname(HOSTNAME + ".local")

TCP_PORT = 9518
LOCAL_PORT = 6000
SEVER_PASSWORD = b'password'
CLOSE_CONNECTION = b'close'
INACTIVE_CLOSE_CONNECTION = b'inactive'
TCP_TIMEOUT = 300             #seconds (5 minutes)
PROTEUS_TIMEOUT = 305         #seconds (5 minutes 5 seconds) (Must be greater than TCP_TIMEOUT)
LOGGER_NAME ='LoggerHandler'
LOG_NAME = 'Handler.log'
LOG_LEVEL = logging.DEBUG

# TCP Server response values
TCP_CLOSE_CONNECTION = b'close'
SERVER_BUSY = [0, 0, 0, 0]
CANT_PROCESS_REQUEST = [1, 1, 1, 1]
SERVER_ERROR = [2, 2, 2, 2]

# -----------------------
#Logger
# -----------------------
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(LOG_LEVEL)
print (logger)
ch1 = logging.FileHandler(LOG_NAME)
ch1.setLevel(logging.WARNING)
ch2 = logging.StreamHandler()
ch2.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch1.setFormatter(formatter)
ch2.setFormatter(formatter)
logger.addHandler(ch1)
logger.addHandler(ch2)

# -----------------------
# FUNCTIONS
# -----------------------
def Get_Time():
    """
        Returns the current time in seconds
    """
    return int(round(datetime.datetime.now().timestamp()))


class TCPRequestHandler(socketserver.StreamRequestHandler):
    """
            Handles TCP requests and connects to local server (Proteus server)
    """
    def handle(self):
        # Print client address and current process ID
        logger.info("Client connected: " + str(self.client_address))
        #print("TCP Process: " + str(mp.current_process()))
        conn = None
        #Set timeout, max waiting time for a request before closing the connection
        self.request.settimeout(TCP_TIMEOUT)
        try:

            while not self.server.starTCPServerShutdown.is_set():
                TCPdata = self.request.recv(1024)
                if self.server.ProteusClosed.is_set():
                    self.request.sendall(bytes(SERVER_ERROR))
                    self.server.ProteusClosed.clear()
                    break
                #ti = time.perf_counter()
                logger.debug('TCP request'+ str(TCPdata))
                try:
                    # Connect with Proteus server
                    if not conn:
                        address = ('localhost', LOCAL_PORT)
                        conn = Client(address, authkey=SEVER_PASSWORD)
                except Exception as e:
                    # If connection was not susccessful send TCP response "Server busy/not available"
                    logger.debug(str("Proteus server is busy " + str(e)))
                    # TODO (1): Definir respuesta negativa general, para errores de la herramienta
                    self.request.sendall(bytes(SERVER_BUSY))
                    break

                # If connection with Proteus server was successful send request to Proteus server and wait for response

                # If request to close conecction, send request to close connection to Proteus server and finish TCP connnection
                if TCPdata == TCP_CLOSE_CONNECTION:
                    conn.send(CLOSE_CONNECTION)
                    break
                else:
                    conn.send(TCPdata)
                    # Receive response from Proteus server
                    list_response = conn.recv()
                    if list_response == CLOSE_CONNECTION:
                        self.request.sendall(bytes(TCP_CLOSE_CONNECTION))
                        break
                    TCPresponse = bytes(list_response)
                    self.request.sendall(TCPresponse)
                    logger.debug("Proteus server response:" + str(list_response))
                    #tf = time.perf_counter()
                    #measured_time = tf - ti
                    #print(measured_time)
                    #time.sleep(22)
            # Request to close process has been received
            else:
                logger.debug("Shutting down actions...")
                self.request.recv(1024)
                self.request.sendall(bytes(TCP_CLOSE_CONNECTION))
                if not self.server.ProteusClosed.is_set():
                    logger.debug("Closing Proteus connection")
                    conn.send(CLOSE_CONNECTION)
                else:
                    self.server.ProteusClosed.clear()
                self.server.TCPServerShutdownReady.set()



        except (ConnectionResetError,BrokenPipeError, EOFError) as e:
            logger.info("Lost connection/reset (client): " + str(e))
            if not self.server.ProteusClosed.is_set():
                conn.send(CLOSE_CONNECTION)
            else:
                self.server.ProteusClosed.clear()
        except ConnectionAbortedError as e:
            logger.info("lost Connection: " + str(e))
            if not self.server.ProteusClosed.is_set():
                conn.send(CLOSE_CONNECTION)
            else:
                self.server.ProteusClosed.clear()
        except socket.timeout as e:
            logger.info(str("Inactive TCP client. Closing connection:: " + str(e)))
            if not self.server.ProteusClosed.is_set():
                conn.send(CLOSE_CONNECTION)
            else:
                self.server.ProteusClosed.clear()

        except Exception as e:
            logger.warning("General error" + str(e))
            self.request.sendall(bytes(SERVER_ERROR))
            if not self.server.ProteusClosed.is_set():
                conn.send(CLOSE_CONNECTION)
            else:
                self.server.ProteusClosed.clear()


class RequestTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    def __init__(self,*args, **kwargs):
        super().__init__( *args, **kwargs)
        self.starTCPServerShutdown = mp.Event()
        self.TCPServerShutdownReady = mp.Event()
        self.ProteusClosed = mp.Event()

    def server_activate(self):
        # Activate server
        socketserver.TCPServer.server_activate(self)
        logger.info("TCP server waiting for connection:" + str(self.server_address))
        return

    def service_actions(self):
        """Called by the serve_forever() loop"""
        #print("service actions:" + str(mp.current_process()))
        pass

    def verify_request(self, request, client_address):
        # Verify the request.
        # Return True if we should proceed with this request.
        connection_accepted = True
        return connection_accepted


class ProteusServer:

    def proteus_request_handler(self, conn, proteus, ProteusStartShutdown, ProteusShutdownReady,ProteusClosed):
        """Process requests to Proteus"""
        ti = Get_Time()
        while not ProteusStartShutdown.is_set():

            #Process requests
            if conn.poll():
                try:
                    # Receive request

                    request = conn.recv()
                    ti = Get_Time()
                    logger.debug("Proteus server request: " + str(request))
                    if request == CLOSE_CONNECTION:
                        conn.close()
                        break
                    else:
                        # Format request as required by Proteus
                        request = list(request)
                        if all(isinstance(elem, int) for elem in request):
                            logger.debug("Proteus module request: " + str(request))
                            # Proteus response
                            proteus_response = proteus.Process_Message(request)
                            conn.send(bytes(proteus_response))
                            logger.debug("Proteus response: " + str(proteus_response))
                        else:
                            logger.info("Invalid data type")
                            conn.send(bytes(CANT_PROCESS_REQUEST))

                except (ConnectionAbortedError, EOFError, ConnectionResetError, OSError, BrokenPipeError) as e:
                    logger.info(str("Lost connection with client (Proteus server): " + str(e)))
                    break
                except Exception as e:
                    logger.warning("General error: " + str(e))
                    if conn:
                        conn.send(CLOSE_CONNECTION)
                        conn.close()
                    break
            else:# If timeout has expired, close connection
                if Get_Time() >= (ti + PROTEUS_TIMEOUT):
                    #print(Get_Time())
                    #print(ti + PROTEUS_TIMEOUT)
                    logger.debug("Inactive Proteus client. Closing connection")
                    if conn:
                        conn.close()
                    ProteusClosed.set()
                    break
        # Request to close process has been received
        else:
            logger.debug("Shutting down actions (Proteus)...")
            if conn:
                conn.close()
            logger.debug("Closing Proteus connection")
            ProteusClosed.set()
            ProteusShutdownReady.set()


class RequestHandler:

    def __init__(self):
        # Processes setup
        self.TCPStartShutdown = mp.Event()
        self.TCPShutdownReady = mp.Event()
        self.ProteusClosed = mp.Event()
        self.ProteusStartShutdown = mp.Event()
        self.ProteusShutdownReady = mp.Event()
        self.TCPSeverProcess = mp.Process(target=self.setup_TCP_server, args=(self.TCPStartShutdown, self.TCPShutdownReady, self.ProteusClosed))
        self.localSeverProcess = mp.Process(target=self.setup_Proteus_server, args=(self.ProteusStartShutdown, self.ProteusShutdownReady, self.ProteusClosed))

    def init_processes(self):
        # Initialize processes for TCP and Process Servers
        self.localSeverProcess.daemon = True
        self.localSeverProcess.start()
        self.TCPSeverProcess.daemon = True
        self.TCPSeverProcess.start()


    def setup_TCP_server(self,StarTCPShudown,TCPShutdownReady, ProteusClosed):
        # Create TCP server
        with RequestTCPServer((HOST_ADDRESS, TCP_PORT), TCPRequestHandler) as server:
            server.starTCPServerShutdown = StarTCPShudown
            server.TCPServerShutdownReady = TCPShutdownReady
            server.ProteusClosed = ProteusClosed
            server.starTCPServerShutdown.clear()
            server.TCPServerShutdownReady.clear()
            #server.allow_reuse_address = True
            # Activate the server
            server.serve_forever()


    def setup_Proteus_server(self,ProteusStartShutDown, ProteusShutdownReady, ProteusClosed):
        address = ('localhost', LOCAL_PORT)  # family  'AF_INET'
        proteus = ProteusHandler.getInstance()
        proteusS = ProteusServer()
        newthread = Thread()
        while True:
            with Listener(address, authkey=SEVER_PASSWORD) as listener:
                if not newthread.isAlive():
                    logger.info('Proteus server waiting for connection')
                    conn = listener.accept()
                    if conn:
                        ProteusClosed.clear()
                        ProteusStartShutDown.clear()
                        ProteusShutdownReady.clear()
                        logger.info('Proteus server connected to: ' + str(listener.last_accepted))
                        newthread = Thread(target=proteusS.proteus_request_handler, args=(conn, proteus, ProteusStartShutDown, ProteusShutdownReady,ProteusClosed, ))
                        newthread.start()


    def shutdown(self):
        logger.debug("Shutting down servers")
        self.ProteusStartShutdown.set()
        self.ProteusShutdownReady.wait(0.01)
        logger.debug("Proteus Shutdown ready: " + str(self.ProteusShutdownReady.is_set()))
        self.TCPStartShutdown.set()
        self.TCPShutdownReady.wait(0.01)
        logger.debug("TCP Shutdown ready: "+ str(self.TCPShutdownReady.is_set()))
        logger.debug("Terminate handler processes")
        if 'linux' == platform or 'linux2' == platform:
            pid1 = self.TCPSeverProcess.pid
            os.kill(int(pid1), signal.SIGTERM)
            pid2 = self.localSeverProcess.pid
            os.kill(int(pid2), signal.SIGTERM)
        elif 'win32' == platform:
            self.TCPSeverProcess.terminate()
            self.localSeverProcess.terminate()
        else:
            logger.warning("Error while terminating request handler processes")
        # Wait process to finish
        n=0
        while self.TCPSeverProcess.is_alive() or self.localSeverProcess.is_alive():
            n += 1
            if n >= 2:
                if 'linux' == platform or 'linux2' == platform:
                    logger.warning("Killing handler processes")
                    pid1 = self.TCPSeverProcess.pid
                    os.kill(int(pid1), signal.SIGKILL)
                    pid2 = self.localSeverProcess.pid
                    os.kill(int(pid2), signal.SIGKILL)
                elif 'win32' == platform:
                    logger.warning("Killing handler processes")
                    self.TCPSeverProcess.kill()
                    self.localSeverProcess.kill()
                else:
                    logger.warning("Error while killing request handler processes")
            time.sleep(0.01)

        logger.debug('TCP server process is alive: ' + str(self.TCPSeverProcess.is_alive()))
        logger.debug('Proteus server process is alive: ' + str(self.localSeverProcess.is_alive()))


if __name__ == "__main__":
    mp.freeze_support()
    requestHandler = RequestHandler()
    requestHandler.init_processes()

    while True:
        # print(requestHandler.server_attributes)
        #print("main")
        #print(mp.current_process())
        #print(requestHandler.TCPSeverProcess.is_alive())
        time.sleep(2)
    requestHandler.shutdown()

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Nov-12-2020 gzvndk
#   + Created initial file.
# Dec-01-2020 gzvndk
#   + Changed prints to logging. Modified terminate processes. Added timeout for requests.
#
# Mar-08-2021 Leobardo N Hernandez
#   +DBL_233 
#     - The code to read the IP was updated.
#     - Fix an indentation error
#
#########################################################################################
