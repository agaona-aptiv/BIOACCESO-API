import bme280
import smbus2
from time import sleep

port = 1      # Jetson Xavier port = 1
address = 0x76 # Other BME280s may be different
bus = smbus2.SMBus(port)
i = 1

calibration_params = bme280.load_calibration_params(bus,address)

while i<=5:
    i = i + 1
    bme280_data = bme280.sample(bus,address,calibration_params)
    humidity  = round(bme280_data.humidity,1)
    pressure  = round(bme280_data.pressure,1)
    ambient_temperature = round(bme280_data.temperature,1)
    print(humidity, '% |', pressure, 'mb/hPa |', ambient_temperature,'°c')
    sleep(1)
