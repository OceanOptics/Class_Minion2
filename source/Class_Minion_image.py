#!/usr/bin/env python

from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import configparser
import pickle

GPIO.setwarnings(False)

config = configparser.ConfigParser()
config.read('/home/pi/Class_Minion_scripts/Class_Minion_config.ini')

firstp = open("timesamp.pkl")
samp_time = pickle.load(firstp)
path, dirs, files = next(os.walk("/home/pi/Class_Minion_data/"))
samp_count = str(len(files)+1)
samp_time = samp_count + "-" + samp_time

i = 0
light = 12
power = 32

def flash():
        j = 0
        while j <= 1:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1



def picture():

        # Collect time value from pickle on desktop
        firstp = open("timesamp.pkl","rb")
        samp_time = pickle.load(firstp)
        pic_count = str(len(os.listdir("/home/pi/Class_Minion_pics/"))+1)
        pictime = pic_count + "-" + samp_time
        GPIO.output(light, 1)
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
    	time.sleep(10)
    	camera.capture('/home/pi/Class_Minion_pics/%s.jpg' % pictime)
    	time.sleep(5)
    	camera.stop_preview()
        GPIO.output(light, 0)

if __name__ == '__main__':

    camera = PiCamera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light, GPIO.OUT)
    GPIO.setup(power, GPIO.OUT)
    picture()
    exit(1)
