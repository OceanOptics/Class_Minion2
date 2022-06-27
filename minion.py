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
CAMERA_MODE = 'VIDEO'               # VIDEO or PICTURE
VIDEO_LENGTH = 30                   # length of video in seconds (only for mode='VIDEO_*')
PICTURES_PER_BURST = 5              # number of pictures during burst (only for mode='PICTURE')
BURST_SLEEP = 2                     # seconds between pictures during burst (only for mode='PICTURE')
WITH_LIGHT = False                   # Turn on light during shot (consumes more battery)
PATH_TO_DATA = '/home/pi/Minion_pics'
MAX_SAMPLES = 10000


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
    def __init__(self, mode='PICTURE'):
        self.camera = PiCamera()
        self.mode = mode
        # Assume camera module V2
        # if mode == 'VIDEO_HD_LFPS':
        #     # Full field of view (4:3), FPS < 15
        #     self.camera.resolution = (3280, 2464)
        #     self.camera.framerate = 15
        if mode == 'VIDEO':
            # Full field of view (4:3), FPS < 40
            self.camera.resolution = (1640, 1232)
            self.camera.framerate = 30
        elif mode == 'PICTURE':
            self.camera.resolution = (3280, 2464)
            self.camera.framerate = 15
        if not os.path.exists(PATH_TO_DATA):
            os.mkdir(PATH_TO_DATA)

    def warm_up(self):
        # TODO Verify that warm up is required to adjust camera light level
        if WITH_LIGHT:
            print('Minion: Disco on!')
            GPIO.output(PIN_LIGHT, 1)
        self.camera.start_preview()
        sleep(10)

    def capture(self):
        if self.mode.startswith('VIDEO'):
            self.video()
        else:
            self.timelapse()

    def timelapse(self):
        for i in range(PICTURES_PER_BURST):
            self.picture()
            sleep(BURST_SLEEP)

    def picture(self):
        picture_id = str(len(os.listdir(PATH_TO_DATA)) + 1)
        picture_time = os.popen("sudo hwclock -u -r").read().split('.', 1)[0] \
            .replace("  ", "_").replace(" ", "_").replace(":", "-")
        picture_name = picture_id + "-" + picture_time + '.jpg'
        print('Minion: Taking selfie (' + picture_name + ').')
        self.camera.capture(os.path.join(PATH_TO_DATA, picture_name))

    def video(self):
        video_id = str(len(os.listdir(PATH_TO_DATA)) + 1)
        video_time = os.popen("sudo hwclock -u -r").read().split('.', 1)[0] \
            .replace("  ", "_").replace(" ", "_").replace(":", "-")
        video_name = video_id + "-" + video_time + '.h264'
        print('Minion: Recording video (' + video_name + ').')
        self.camera.start_recording(os.path.join(PATH_TO_DATA, video_name))
        self.camera.wait_recording(VIDEO_LENGTH)
        self.camera.stop_recording()

    def cool_down(self):
        self.camera.stop_preview()
        if WITH_LIGHT:
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
    if os.path.exists(PATH_TO_DATA) and len(os.listdir(PATH_TO_DATA)) > MAX_SAMPLES:
        print('Minion: Trip is over.')
        GPIO.output(PIN_OVER, 0)
        shutdown_pi()

    # Take pictures
    cam = Camera(CAMERA_MODE)
    cam.warm_up()
    cam.capture()
    cam.cool_down()

    # Check if recovered again (in case wifi didn't got a fix yet)
    if wifi_connected():
        print('Minion: Bee-do! Bee-do!')
        flash()  # Keep system alive
    else:
        shutdown_pi()
