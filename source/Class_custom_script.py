#!/usr/bin/env python

import configparser
import pickle

# Collect time value from pickle on desktop
firstp = open("timesamp.pkl","rb")
timestamp = pickle.load(firstp)

config = configparser.ConfigParser()
config.read('/home/pi/Documents/Class_Minion_scripts/Class_Minion_config.ini')

inicus = bool(config['Sampling_scripts']['Custom'])

# This is an empty file used for adding extra routines

def main():
	print("Add software you wish to include here!")



if __name__ == "__main__":

	main()
