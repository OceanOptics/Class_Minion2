#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LED = 33

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

while True:
	GPIO.output(LED, 1)
	time.sleep(1)
	GPIO.output(LED, 0)
	time.sleep(1)
