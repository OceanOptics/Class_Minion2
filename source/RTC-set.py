#!/usr/bin/env python

# Allows users to set the RTC while ssh'd to a local IP Class_Minion

import os
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

def flash():
	j = 0
	while j <= 2:
		GPIO.output(12, 1)
		time.sleep(.25)
		GPIO.output(12, 0)
		time.sleep(.25)
		j = j + 1

print "Connect to internet"
time.sleep(10)

ifswitch='sudo python /home/pi/Documents/Class_Minion_tools/dhcp-switch.py'

print 'switching to global internet'

net_cfg = os.popen("ls /etc/ | grep dhcpcd").read()

if ".internet" in net_cfg:
	os.system(ifswitch)

else:
	print "You are already on global internet"

ping = ""

while(ping!=0):
	ping = os.system('ping google.com -c 1')
	time.sleep(4)
	print ping

	if (ping == 0):
		print 'You have internet!'
	else:
		print 'no internet'

print 'setting clock!'

os.system('sudo hwclock -D -r')
os.system('sudo hwclock -w')

flash()

print 'connecting to Class_Minion network'

os.system(ifswitch)
