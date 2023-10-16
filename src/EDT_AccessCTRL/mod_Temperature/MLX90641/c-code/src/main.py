import sys
from MLX90640.mlx90640 import *
import ctypes

def main():
    slaveAddr = 0x33
    dev = MLX90640()

    dev.i2cInitMlx90640()
    dev.setRefreshRate(slaveAddr, 5)

    RR = dev.getRefreshRate(slaveAddr)
    print (RR)

    eepromdata = (ctypes.c_uint16*832)()
    frameData = (ctypes.c_uint16*834)()
    params = paramsMLX90640()
    mlx90640To = (ctypes.c_float * 768)()

    dev.dumpEE(slaveAddr, ctypes.cast(eepromdata, ctypes.POINTER(ctypes.c_uint16)))
    dev.extractParameters(eepromdata, ctypes.byref(params))

    for i in range(0,10):
        dev.getFrameData(slaveAddr, ctypes.cast(frameData, ctypes.POINTER(ctypes.c_uint16)))
        Ta = dev.getVdd(frameData, params)-8.0

        dev.calculateTo(frameData, params, 1, Ta, mlx90640To)

        for i in range(0,1):
            print(mlx90640To[i])
    dev.i2cCloseMlx90640()



if __name__ == "__main__":
    main()