#!/usr/bin/env python3
import configparser
import time
from time import localtime

ltime_data = {
    'LIGHTTIME_01': dict(START01='11:58', STOP01='17:25', UPDATED01=time.strftime("%m/%d/%y %H:%M", localtime())),
    'LIGHTTIME_02': dict(START02='15:58', STOP02='23:25', UPDATED02=time.strftime("%m/%d/%y %H:%M", localtime()))
}

config = configparser.ConfigParser()
config.read_dict(ltime_data)

t1_start = config['LIGHTTIME_01']['START01']
t1_stop = config['LIGHTTIME_01']['STOP01']
t1_updated = config['LIGHTTIME_01']['UPDATED01']

t2_start = config['LIGHTTIME_02']['START02']
t2_stop = config['LIGHTTIME_02']['STOP02']
t2_updated = config['LIGHTTIME_02']['UPDATED02']

print("START:", {t1_start})
print('STOP:', {t1_stop})
print("UPDATED:", {t1_updated})
print("\n")
print("START:", {t2_start})
print("STOP:", {t2_stop})
print("UPDATED:", {t2_updated})

with open('../static/configs/time_config.ini', 'w') as configfile:
    config.write(configfile)
