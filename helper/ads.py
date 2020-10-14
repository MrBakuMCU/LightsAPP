from helper.ads1115lib import ADS1115
import time

ads = ADS1115(address=0x48)


def ads_sensor_01():
    while True:
        volt = ads.readADCSingleEnded(channel=2)
        print("{:.0f} mV measurement on (Channel=2)AN3".format(volt))
        time.sleep(1)
    return volt
