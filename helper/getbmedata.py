from bme280 import bme280


def getBMEData1():
    temperature, pressure, humidity = bme280.readBME280All(addr=0x76)

    if humidity is not None and temperature is not None and pressure is not None:
        humidity = round(humidity, 1)
        temperature = round(temperature, 1)
        pressure = round(pressure, 1)

    return temperature, humidity, pressure