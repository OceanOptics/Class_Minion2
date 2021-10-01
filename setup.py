import os


print('Welcome to Minion setup !')

"""
Keep current security
It's bad practice but the minion should be alone at sea.
"""
print('Keep default user pi')
print('User pi must have sudo privilege.')
print('Sudo privilege shouldn\'t require a password')


"""
Setup WiFi for recovery mode
"""
print('You should setup known wifi networks in /etc/wpa_supplicant.conf for recovery.')


"""
Setup external software
"""
# Get updates
os.system('sudo apt update && sudo apt upgrade -y')
# Get needed packages
os.system('sudo apt-get install build-essential python-smbus i2c-tools avrdude -y')
# raspi-config
os.system('sudo raspi-config nonint do_change_locale en_US.UTF-8')
os.system('sudo raspi-config nonint do_boot_behaviour B2')
os.system('sudo raspi-config nonint do_camera 0')
os.system('sudo raspi-config nonint do_ssh 0')
os.system('sudo raspi-config nonint do_i2c 0')
os.system('sudo raspi-config nonint do_rgpio 0')
os.system('sudo raspi-config nonint do_hostname minion')


"""
Set up and sync RTC
"""
os.system("echo 'dtoverlay=i2c-rtc,pcf8523' >> /boot/config.txt")

# Might need to be done after reboot
os.system('sudo apt-get -y remove fake-hwclock')
os.system('sudo update-rc.d -f fake-hwclock remove')
os.system('sudo systemctl disable fake-hwclock')
os.system("sudo sed -i '7,9 s/^/#/' /lib/udev/hwclock-set")

# Update hwclock-set parameters
with open('/lib/udev/hwclock-set', 'r') as f :
  file = f.read()
file = file.replace('/sbin/hwclock --rtc=$dev --systz --badyear', '#/sbin/hwclock --rtc=$dev --systz --badyear')
file = file.replace('/sbin/hwclock --rtc=$dev --systz', '#/sbin/hwclock --rtc=$dev --systz')
with open('/lib/udev/hwclock-set', 'w') as f:
  f.write(file)

# Set time (assume computer was sync with internet time)
os.system('sudo hwclock -D -r')
os.system('sudo hwclock -w')


"""
Copy software at known location
"""
# Move scripts to local build
os.system('sudo cp minion.py /home/pi/Minion_script/')


"""
Setup system to boot on start
"""
# Set pi to launch rest of script after reboot
os.system("sudo sed -i '/# Print the IP/isudo python /home/pi/Minion_scripts/minion.py\n\n' /etc/rc.local")

# Reboot to finish kernel module config
os.system('sudo reboot now')