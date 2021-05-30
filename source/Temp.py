#!/usr/bin/python
import time
import os
import configparser
import pickle

config = configparser.ConfigParser()
config.read('/home/pi/Documents/Class_Minion_scripts/Class_Minion_config.ini')

Stime = config['Data_Sample']['Class_Minion_sample_time']

try :
    float(test_string)
    Stime = float(Stime)
except :
    Stime = float(.25)

Srate = float(config['Data_Sample']['Class_Minion_sample_rate'])

Sf = 1/Srate

if __name__ == "__main__":

    import tsys01

    sensor_temp = tsys01.TSYS01()

    i = 0

    Sample_number = (Stime*60)*Srate

    # We must initialize the sensor before reading it
    if not sensor_temp.init():
        print("Error initializing sensor")
        exit(1)

    # Collect time value from pickle on desktop
    firstp = open("timesamp.pkl","rb")
    samp_time = pickle.load(firstp)
    path, dirs, files = next(os.walk("/home/pi/Documents/Class_Minion_data/"))
    samp_count = str(len(files)+1)
    samp_time = samp_count + "-" + samp_time

    file_name = "/home/pi/Documents/Class_Minion_data/%s_Temp.txt" % samp_time

    file = open(file_name,"w+")

    file.write("Temperature @ %s\r\n" % samp_time)
    file.write("Sample Rate: %s \n" % Srate)

    # Spew readings
    while Sample_number > i:

        if not sensor_temp.read():
            print("Error reading sensor")
            iniTmp = False
            exit(1)

        print("Temperature_accurate: %0.2f C" % sensor_temp.temperature())

        file.write(str(sensor_temp.temperature()) + "\r\n")

        i = i + 1

        time.sleep(Sf)

    file.close()
