#!/usr/bin/env python

import RPi.GPIO as GPIO

wifi = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(wifi, GPIO.OUT)
GPIO.output(wifi, 1)