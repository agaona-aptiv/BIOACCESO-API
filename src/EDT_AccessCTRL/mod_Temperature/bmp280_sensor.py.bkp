
from bmp280 import BMP280
from time import sleep

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# Initialise the BMP280

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
i = 1

while i<=5:
    i = i + 1
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    print('{:05.2f}*C {:05.2f}hPa'.format(temperature, pressure))
    sleep(1)