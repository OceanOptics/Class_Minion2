#!/usr/bin/python
import time
import os
import configparser
import pickle

config = configparser.ConfigParser()
config.read('/home/pi/Class_Minion_scripts/Class_Minion_config.ini')

Stime = config['Data_Sample']['Class_Minion_sample_time']

try :
    float(test_string)
    Stime = float(Stime)
except :
    Stime = float(.25)

Srate = float(config['Data_Sample']['Class_Minion_sample_rate'])

Sf = 1/Srate

if __name__ == "__main__":

	import ms5837

	sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

	i = 0

	Sample_number = (Stime*60)*Srate

	if not sensor.init():
	        print "Sensor could not be initialized"
	        exit(1)

	# We have to read values from sensor to update pressure and temperature
	if not sensor.read():
	    print "Sensor read failed!"
	    exit(1)

	freshwaterDepth = sensor.depth() # default is freshwater
	sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
	saltwaterDepth = sensor.depth() # No nead to read() again
	sensor.setFluidDensity(1000) # kg/m^3

	time.sleep(1)

	# Collect time value from pickle on desktop
	firstp = open("timesamp.pkl","rb")
	samp_time = pickle.load(firstp)
	path, dirs, files = next(os.walk("/home/pi/Class_Minion_data/"))
	samp_count = str(len(files)+1)
	samp_time = samp_count + "-" + samp_time

	file_name = "/home/pi/minion_data/%s_T+P.txt" % samp_time

	file = open(file_name,"w+")

	file.write("%s\r\n" % samp_time)
	file.write("Pressure(mbar),Temp(C) at %s Hz \r\n" % Srate)

	# Spew readings
	while Sample_number > i:

	    if sensor.read():
	        print("P: %0.1f mbar  %0.3f atm\tT: %0.2f C") % (
	        sensor.pressure(), # Default is mbar (no arguments)
	        sensor.pressure(ms5837.UNITS_atm), # Request psi
	        sensor.temperature()) # Default is degrees C (no arguments)

	        pressure = sensor.pressure()
	        temp1 = sensor.temperature()

	        pressure = str(pressure)
	        temp1 = str(temp1)

	        file.write(pressure + "," + temp1 + "\r\n")

	    else:
	        file.write('Sensor Failure!')
	        iniTpp = False
	        exit(1)

		i = i + 1

		time.sleep(Sf)

	file.close()
