from helper.ads1115lib import ADS1115
import time

ads = ADS1115(address=0x48)


def ads_sensor_01():
    while True:
        reading = ads.readADCSingleEnded(channel=2)
        time.sleep(1.2)
        return reading
