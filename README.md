# Class Minion 2.0

## Setup RPi
Class Minion runs with python 2.7

  1. Setup Raspbian Lite on an SD card and boot RPI Zero
  2. Update distribution `sudo apt-get update && sudo apt-get upgrade -y`   
  3. Configure local, wifi, and enable ssh
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

    # Execute installation script
    cd Class_Minion2
    sudo python Class_Minion_install.py
  

When the RPi is turned on the script Class_Minion_DeploymentHandler.py is called. This script takes a picture and other measurements (optional), it then check if a known wifi is in range. If a wifi is in range it stays on, otherwise it turns off. This can result in a blocking behaviour if the wifi of choice is not available preventing to offload the data from the deployment. To test such behaviour the last line of Class_Minion_DeploymentHandler.py can be commented to prevent the halt to happen.

    # turn on wifi
    sudo ifconfig wlan0 up
    # turn off wifi
    sudo ifconfig wlan0 down
    # run script to see if it finds wifi to connect and prevent halt of system
    sudo python ~/Class_Minion_scripts/Class_Minion_DeploymentHandler.py

## Setup Arduino Nano
Upload Low_Power_Pi/Low_Power_Pi.ino to the Arduino Nano using Arduino IDE.
Note that depending on your version of Arduino Nano, you might have to check the (Arduino Nano (older version)) in the board parameters to prevent issues.

