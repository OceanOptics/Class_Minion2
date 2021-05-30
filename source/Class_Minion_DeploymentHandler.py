#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import math
import configparser
import sys
import pickle

def flash():
        j = 0
        while j <= 2:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def check_wifi():

	if "Class_Minion_Hub" in os.popen(iwlist).read():
		print("WIFI!!")
		status = "Connected"
		net_status = os.popen(net_cfg).read()
		if ".Class" in net_status:
			os.system(ifswitch)
		else:
			print("You have Class_Minions!")

	else:
		print("No WIFI found.")
		status = "Not Connected"

	print(status)

	return status

# Get telemetry from scripts
# sys.path.append('/media/Data/')
sys.path.append('/home/pi/Class_Minion_scripts')

samp_time = os.popen("sudo hwclock -u -r").read()
samp_time = samp_time.split('.',1)[0]
samp_time = samp_time.replace("  ","_")
samp_time = samp_time.replace(" ","_")
samp_time = samp_time.replace(":","-")

firstp = open("timesamp.pkl","wb")
pickle.dump(samp_time, firstp)
firstp.close()

i = 0
light = 12
wifi = 7
Press_IO = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(wifi, GPIO.OUT)
GPIO.setup(Press_IO, GPIO.OUT)
GPIO.output(Press_IO, 1)
GPIO.output(wifi, 1)

config = configparser.ConfigParser()
config.read('/home/pi/Class_Minion_scripts/Class_Minion_config.ini')

Ddays = int(config['Deployment_Time']['days'])
Dhours = int(config['Deployment_Time']['hours'])

Stime = config['Data_Sample']['Class_Minion_sample_time']

try:
    float(test_string)
    Stime = float(Stime)
except:
    Stime = float(.25)

Srate = float(config['Sleep_cycle']['Class_Minion_sleep_cycle'])

iniImg = str2bool(config['Sampling_scripts']['Image'])
iniTmp = str2bool(config['Sampling_scripts']['Temperature'])
iniTpp = str2bool(config['Sampling_scripts']['TempPres'])
inicus = str2bool(config['Sampling_scripts']['Custom'])


def parse_wpa_supplicant(filename='/etc/wpa_supplicant/wpa_supplicant.conf'):
	with open(filename) as f:
		lines = f.read().split('\n')
		# Remove indentation and skip first and last line
		lines = [l.strip() for l in lines[1:-1]]
		# Parse all parameters up to ssid
		# opts = dict()
		for l in lines:
			foo = l.split('=')
			if len(foo) == 2:
				key, value = foo[0], foo[1]
			else:
				key = foo[0]
				value = "=".join(foo[1:])
			# opts[key] = value
			if key == 'ssid':
				return value[1:-1]  # remove quotes
	return None

wifi_ssid = parse_wpa_supplicant()

TotalSamples = (((Ddays*24)+Dhours))/Srate

ifswitch = "sudo python /home/pi/Class_Minion_tools/dhcp-switch.py"
iwlist = 'sudo iwlist wlan0 scan | grep "%s"' % wifi_ssid
net_cfg = "ls /etc/ | grep dhcp"
ping_hub = "ping 192.168.0.1 -c 1"
ping_google = "ping google.com -c 1"
subpkill = "sudo killall python"
ps_test = "pgrep -a python"
scriptNames = ["Temp.py", "TempPres.py", "Class_custom_script.py", "Class_Minion_image.py"]

if __name__ == '__main__':

	if len(os.listdir('/home/pi/Class_Minion_pics')) >= TotalSamples or len(os.listdir('/home/pi/Class_Minion_data')) >= TotalSamples:
        	GPIO.output(Press_IO, 0)

	else:
		if iniTmp == True:
			os.system('sudo python /home/pi/Class_Minion_scripts/Temp.py &')

		if iniTpp == True:
			os.system('sudo python /home/pi/Class_Minion_scripts/TempPres.py &')

		if inicus == True:
			os.system('sudo python /home/pi/Class_Minion_scripts/Class_custom_script.py &')

		if iniImg == True:
			os.system('sudo python /home/pi/Class_Minion_scripts/Class_Minion_image.py &')

	while(any(x in os.popen(ps_test).read() for x in scriptNames)) == True:
		if check_wifi() == "Connected":
			# Stop sampling
			flash()
			os.system(subpkill)
			exit(1)
		else:
			# Sampling
			time.sleep(5)

	print('Goodbye')
	GPIO.output(wifi, 0)
	time.sleep(5)
	os.system('sudo shutdown now')
