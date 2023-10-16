import sys
import os
import ctypes
import pathlib


class paramsMLX90641(ctypes.Structure):
    _fields_ = [
        ("kVdd", ctypes.c_int16),
        ("vdd25", ctypes.c_int16),
        ("KvPTAT", ctypes.c_float),
        ("KtPTAT", ctypes.c_float),
        ("vPTAT25", ctypes.c_uint16),
        ("alphaPTAT", ctypes.c_float),
        ("gainEE", ctypes.c_int16),
        ("tgc", ctypes.c_float),
        ("cpKv", ctypes.c_float),
        ("cpKta", ctypes.c_float),
        ("resolutionEE", ctypes.c_uint8),
        ("calibrationModeEE", ctypes.c_uint8),
        ("KsTa", ctypes.c_float),
        ("ksTo", ctypes.c_float*8),
        ("ct", ctypes.c_int16*8),
        ("alpha", ctypes.c_uint16*192),    
        ("alphaScale", ctypes.c_uint8),
        ("offset", ctypes.c_int16*2*192),    
        ("kta", ctypes.c_int8*192),
        ("ktaScale", ctypes.c_uint8),    
        ("kv", ctypes.c_int8*192),
        ("kvScale", ctypes.c_uint8),
        ("cpAlpha", ctypes.c_float),
        ("cpOffset", ctypes.c_int16),
        ("emissivityEE", ctypes.c_float), 
        ("brokenPixel", ctypes.c_uint16)]


# uncovered functions in python:


    # int MLX90641_SynchFrame(uint8_t slaveAddr);
    # int MLX90641_TriggerMeasurement(uint8_t slaveAddr);
    # int MLX90641_GetFrameData(uint8_t slaveAddr, uint16_t *frameData);
    # void MLX90641_GetImage(uint16_t *frameData, const paramsMLX90641 *params, float *result);
    # float MLX90641_GetEmissivity(const paramsMLX90641 *mlx90641);
    # void MLX90641_BadPixelsCorrection(uint16_t pixel, float *to);

    # int MLX90641_I2CRead(uint8_t slaveAddr,uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data);
    # int MLX90641_I2CWrite(uint8_t slaveAddr,uint16_t writeAddress, uint16_t data);


class MLX90641():
    def __init__(self):
        ## Read shared libraries
        ## Change to relative paths
        current_filePath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))+'/MLX90641/c-code'
        libi2c          = ctypes.CDLL(current_filePath + '/libi2c.so', mode=ctypes.RTLD_GLOBAL)
        libmlx90641_i2c = ctypes.CDLL(current_filePath + '/libmlx90641_i2c_devtree.so', mode=ctypes.RTLD_GLOBAL)
        libmlx90641     = ctypes.CDLL(current_filePath + '/libmlx90641.so', mode=ctypes.RTLD_GLOBAL)
        
        #libi2c          = ctypes.CDLL('./mod_Temperature/MLX90641/c-code/libi2c.so', mode=ctypes.RTLD_GLOBAL)
        #libmlx90641_i2c = ctypes.CDLL('./mod_Temperature/MLX90641/c-code/libmlx90641_i2c_devtree.so', mode=ctypes.RTLD_GLOBAL)
        #libmlx90641     = ctypes.CDLL('./mod_Temperature/MLX90641/c-code/libmlx90641.so', mode=ctypes.RTLD_GLOBAL)

        ## Extract functions from shared libraries
        self.I2CInit = libmlx90641_i2c.MLX90641_I2CInit
        self.I2CInit.restype = None

        self.I2CFreqSet = libmlx90641_i2c.MLX90641_I2CFreqSet
        self.I2CFreqSet.restype = None
        self.I2CFreqSet.argtypes = [ctypes.c_int]
                
        self.dumpEE = libmlx90641.MLX90641_DumpEE
        self.dumpEE.restype = ctypes.c_int
        self.dumpEE.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]
      
        self.getFrameData = libmlx90641.MLX90641_GetFrameData
        self.getFrameData.restype = ctypes.c_int
        self.getFrameData.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]
        
        self.extractParameters = libmlx90641.MLX90641_ExtractParameters
        self.extractParameters.restype = ctypes.c_int
        self.extractParameters.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self.getVdd = libmlx90641.MLX90641_GetVdd
        self.getVdd.restype = ctypes.c_float
        self.getVdd.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self.getTa = libmlx90641.MLX90641_GetTa
        self.getTa.restype = ctypes.c_float
        self.getTa.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self.calculateTo = libmlx90641.MLX90641_CalculateTo
        self.calculateTo.restype = None
        self.calculateTo.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641), ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
        
        self.setResolution = libmlx90641.MLX90641_SetResolution
        self.setResolution.restype = ctypes.c_int
        self.setResolution.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
        
        self.getResolution = libmlx90641.MLX90641_GetCurResolution
        self.getResolution.restype = ctypes.c_int
        self.getResolution.argtypes = [ctypes.c_uint8]
        
        self.setRefreshRate = libmlx90641.MLX90641_SetRefreshRate
        self.setRefreshRate.restype = ctypes.c_int
        self.setRefreshRate.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
        
        self.getRefreshRate = libmlx90641.MLX90641_GetRefreshRate
        self.getRefreshRate.restype = ctypes.c_int
        self.getRefreshRate.argtypes = [ctypes.c_uint8]
        
        self.getSubPageNumber = libmlx90641.MLX90641_GetSubPageNumber
        self.getSubPageNumber.restype = ctypes.c_int
        self.getSubPageNumber.argtypes = [ctypes.POINTER(ctypes.c_uint16)]
        

        #self.I2CInit()
        #self.I2CFreqSet(250)

    def i2cInit(self):
        return self.I2CInit()
        
    def i2cFreqSet(self, freq):
        return self.I2CFreqSet(freq)
        
    def i2cCloseMlx90641(self):
        return self.I2CCloseMlx90641()
    
    def dumpEE(self, slaveAddr, eepromData):
        return self.dumpEE(slaveAddr, eepromData)
    
    def getFrameData(self, slaveAddr, frameData):
        return self.getFrameData(slaveAddr, frameData)
    
    def extractParameters(self, eepromData, params):
        return self.extractParameters(eepromData, params)
    
    def getVdd(self, frameData, params):
        return self.getVdd(frameData, params)
    
    def getTa(self, frameData, params):
        return self.getTa(frameData, params)
    
    def calculateTo(self, frameData, params, emissivity, tr, result):
        return self.calculateTo(frameData, params, emissivity, tr, result)

    def setResolution(self, slaveAddr, resolution):
        return  self.setResolution(slaveAddr, resolution)

    def getResolution(self, slaveAddr):
        return self.getResolution(slaveAddr)

    def setRefreshRate(self, slaveAddr, refreshRate):
        return  self.setRefreshRate(slaveAddr, refreshRate)

    def getRefreshRate(self, slaveAddr):
        return self.getRefreshRate(slaveAddr)
    
    def getSubPageNumber(self, frameData):
        return self.getSubPageNumber(frameData)
    

