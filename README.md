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
  


## Setup Arduino Nano
Upload Low_Power_Pi/Low_Power_Pi.ino to the Arduino Nano using Arduino IDE.
Note that depending on your version of Arduino Nano, you might have to check the (Arduino Nano (older version)) in the board parameters to prevent issues.

