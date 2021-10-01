#!/usr/bin/env pyhton
"""
Minion Camera Single Script Executable

MIT License

Rewritten by: Nils Haentjens
Past versions from: Melissa Omand Lab
"""
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import os


__version__ = '3.0.0'


"""
Parameters
"""
deployment_duration = 10 * 24 + 12  # hours
sample_rate = 4                     # number/hour  (programmed on micro-controller)
PICTURES_PER_BURST = 5              # number of picture during burst
BURST_SLEEP = 2                     # seconds between pictures during burst
PICTURE_WITH_LIGHT = True           # Turn on light during picture (consumes more battery)
PATH_TO_PICTURES = '/home/pi/Minion_pics'
MAX_SAMPLES = deployment_duration * sample_rate * PICTURES_PER_BURST
# MAX_SAMPLES = 1000


"""
Hardware specific configuration
"""
# Valid for Minion Teach Hardware 1606696
PIN_LIGHT = 12
PIN_WIFI = 38
PIN_OVER = 40


"""
Functions
"""


def parse_wpa_supplicant(filename='/etc/wpa_supplicant/wpa_supplicant.conf'):
    with open(filename) as f:
        lines = f.read().split('\n')
        # Remove indentation and skip first and last line
        lines = [line.strip() for line in lines[1:-1]]
        # Parse all parameters up to ssid
        ssid = []
        for line in lines:
            foo = line.split('=')
            if len(foo) == 2:
                key, value = foo[0], foo[1]
            else:
                key = foo[0]
                value = "=".join(foo[1:])
            # opts[key] = value
            if key == 'ssid':
                ssid.append(value[1:-1])
            # return value[1:-1]  # remove quotes
    return ssid


def wifi_connected():
    iwlist = 'sudo iwlist wlan0 scan | grep "SSID"'
    scan_ssids = os.popen(iwlist).read()
    known_ssids = parse_wpa_supplicant()
    for ssid in known_ssids:
        if ssid in scan_ssids:
            return True
    return False


def flash():
    j = 0
    while j <= 2:
        GPIO.output(PIN_LIGHT, 1)
        sleep(.25)
        GPIO.output(PIN_LIGHT, 0)
        sleep(.25)
        j = j + 1


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (2592, 1944)
        self.camera.framerate = 15
        if not os.path.exists(PATH_TO_PICTURES):
            os.mkdir(PATH_TO_PICTURES)

    def warm_up(self):
        # TODO Verify that warm up is required to adjust camera light level
        if PICTURE_WITH_LIGHT:
            print('Minion: Disco on!')
            GPIO.output(PIN_LIGHT, 1)
        self.camera.start_preview()
        sleep(10)

    def picture(self):
        picture_id = str(len(os.listdir(PATH_TO_PICTURES)) + 1)
        picture_time = os.popen("sudo hwclock -u -r").read().split('.', 1)[0].replace("  ", "_").replace(" ",
                                                                                                         "_").replace(
            ":", "-")
        picture_name = picture_id + "-" + picture_time + '.jpg'
        print('Minion: Taking selfie (' + picture_name + ').')
        self.camera.capture(os.path.join(PATH_TO_PICTURES, picture_name))

    def cool_down(self):
        # TODO Verify this step is required
        sleep(5)
        self.camera.stop_preview()
        if PICTURE_WITH_LIGHT:
            print('Minion: Disco off.')
            GPIO.output(PIN_LIGHT, 0)


def shutdown_pi():
    print('Minion: Kanpai!')
    GPIO.output(PIN_WIFI, 0)
    sleep(2)  # Twice more than update frequency of MCU
    os.system('sudo shutdown now')
    exit()


"""
Main code
"""
if __name__ == '__main__':
    print('Minion: Pwede na?')

    # Setup Pinout
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_LIGHT, GPIO.OUT)
    GPIO.setup(PIN_WIFI, GPIO.OUT)
    GPIO.setup(PIN_OVER, GPIO.OUT)
    GPIO.output(PIN_OVER, 1)
    GPIO.output(PIN_WIFI, 1)

    # Check if recovered based on wifi
    if wifi_connected():
        print('Minion: Bee-do! Bee-do!')
        flash()
        exit()  # Keep system alive

    # Check number of samples and go to sleep for ever if too many
    if os.path.exists(PATH_TO_PICTURES) and len(os.listdir(PATH_TO_PICTURES)) > MAX_SAMPLES:
        print('Minion: Trip is over.')
        GPIO.output(PIN_OVER, 0)
        shutdown_pi()

    # Take pictures
    cam = Camera()
    cam.warm_up()
    for i in range(PICTURES_PER_BURST):
        cam.picture()
        sleep(BURST_SLEEP)
    cam.cool_down()

    # Check if recovered again (in case wifi didn't got a fix yet)
    if wifi_connected():
        print('Minion: Bee-do! Bee-do!')
        flash()  # Keep system alive
    else:
        shutdown_pi()
