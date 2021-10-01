# Minion 3.0

## Setup RPi
Class Minion runs with python 2.7

  1. Setup Raspbian Lite on an SD card and boot RPI Zero
  2. Update distribution `sudo apt-get update && sudo apt-get upgrade -y`   
  3. Configure local, Wi-Fi, and enable ssh
  4. Connect to the pi over ssh and try:

    # Install pip (required for installation of Minion's drivers)
    # sudo apt install python3-pip
    sudo apt install python-pip

    # Install picamera (not available by default raspian lite)
    # sudo apt install python3-picamera
    sudo apt install python-picamera
    
    # Change default python version system-wide (not needed, keep 2.7)
    # sudo update-alternatives --install $(which python) python $(readlink $(which python2)) 1
    # sudo update-alternatives --install $(which python) python $(readlink $(which python3)) 2

    # Download software repository (git need to be installed on raspian lite)
    sudo apt install git
    git clone https://github.com/OceanOptics/Class_Minion2

    # Read installation script and run it by hand step by step (might need to reboot half-way through)
    sudo python setup.py

## Setup Arduino Nano
Upload MinionSleepMCU/MinionSleepMCU.ino to the Arduino Nano using Arduino IDE.
Note that depending on your version of Arduino Nano, you might have to check the (Arduino Nano (older version)) in the board parameters to prevent issues.

## System Behaviour
When the RPi is turned on the script `minion.py` is called. The script's logic is as follows:

  1. Check if known Wi-Fi in range:
     1. If available, the script stops and keep the RPi alive;
     2. Otherwise, it continues
  2. Check if the maximum number of pictures was captured:
     1. If true, the script stops and the system goes into sleep forever. A power cycle is needed to boot the system.
     2. Otherwise, it continues
  3. It takes a burst of pictures.
  4. Check if known Wi-Fi in range again
     1. If available, the script stops and keep the RPi alive;
     2. Otherwise, the system goes into deep sleep: powering off the RPi; which will be waked up by the Arduino X minutes later.
     

## Tips
Test camera

    raspistill -o picture.jpg

Test flash
    
    python Class_Minion_tools/flasher.py

Set Real-Time Clock (Assume computer time is synchronized with internet time)
    
    sudo hwclock -D -r
    sudo hwclock -w

Test Real-Time Clock (get time)

    sudo hwclock -r

Turn on Wi-Fi

      sudo ifconfig wlan0 up

Turn off Wi-Fi

      sudo ifconfig wlan0 down