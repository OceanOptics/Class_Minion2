#!/usr/bin/env python
import os

import RPi.GPIO as GPIO

wifi = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wifi, GPIO.OUT)
GPIO.output(wifi, 1)

def yes_no(answer):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
     
    while True:
        choice = raw_input(answer).lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print "Please respond with 'yes' or 'no'\n"

os.system('sudo apt-get -y remove fake-hwclock')
os.system('sudo update-rc.d -f fake-hwclock remove')
os.system('sudo systemctl disable fake-hwclock')

os.system("sudo sed -i '7,9 s/^/#/' /lib/udev/hwclock-set")

with open('/lib/udev/hwclock-set', 'r') as file :
  Class_Minion_RTC = file.read()

Class_Minion_RTC = Class_Minion_RTC.replace('/sbin/hwclock --rtc=$dev --systz --badyear', '#/sbin/hwclock --rtc=$dev --systz --badyear')
Class_Minion_RTC = Class_Minion_RTC.replace('/sbin/hwclock --rtc=$dev --systz', '#/sbin/hwclock --rtc=$dev --systz')

# Write the file out again
with open('/lib/udev/hwclock-set', 'w') as file:
  file.write(Class_Minion_RTC)

# Set time
os.system('sudo hwclock -D -r')
os.system('sudo hwclock -w')

# Write deployment scripts to rc.local

os.system("sudo sed -i '/# Print the IP/isudo python /home/pi/Class_Minion_scripts/Class_Minion_DeploymentHandler.py &\n' /etc/rc.local")
os.system("sudo sed -i '/# Print the IP/i#sudo python /home/pi/Class_Minion_scripts/Keep_Me_Alive.py \n' /etc/rc.local")


# Remove self from rc.local and configure deployment
with open('/etc/rc.local', 'r') as file :
  rclocal = file.read()
# Replace the RTC string
rclocal = rclocal.replace('sudo python /home/pi/Class_Minion_scripts/Class_Minion_finish_install.py', '')
with open('/etc/rc.local', 'w') as file:
  file.write(rclocal)

os.system('sudo python /home/pi/Class_Minion_tools/dhcp-switch.py')

os.system('sudo reboot now')

print "DONE!"
