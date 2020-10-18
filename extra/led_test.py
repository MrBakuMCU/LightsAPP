#!/usr/bin/python3.5
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)


for i in range(50):
    time.sleep(0.075)
    print("LED on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(0.075)
    print("LED off")
    GPIO.output(18, GPIO.LOW)
    time.sleep(0.075)
