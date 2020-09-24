#!/usr/bin/env python

# Written to make switching wireless networks easier!
# Be careful, as you need to be in .Class in order to retain your static IP

# import needed libraries for scanning and executing
import glob, os
import time

# Iterator
i = 0

# User defined loop for style points
def plz_wait():
	for i in range(0,3):
		print "_____________________"
		time.sleep(1)
		i = i + 1

# Filenames of interest
Class = "dhcpcd.Class"
internet = "dhcpcd.internet"
# Target Directory
os.chdir("/etc")
# List of dhcpcd.* files
files = []
# Scan for files
for file in glob.glob("dhcpcd.*"):
	files.append(file)

#If you wanna see the output
#print files

# Decide what to do with this information
# IF Else decision type
# Copy the .conf to the missing file and move the alt to .conf

if Class in files:
	os.system('sudo cp /etc/dhcpcd.conf /etc/dhcpcd.internet')
	print "Copying .conf to .internet"
	#plz_wait()
	os.system('sudo cp /etc/dhcpcd.Class /etc/dhcpcd.conf')
	print "Copying .Class to .conf"
	#plz_wait()
	os.system('sudo rm -rf /etc/dhcpcd.Class')
	print "Now you have ClassS!"

elif internet in files:
        os.system('sudo cp /etc/dhcpcd.conf /etc/dhcpcd.Class')
        print "Copying .conf to .Class"
        #plz_wait()
        os.system('sudo cp /etc/dhcpcd.internet /etc/dhcpcd.conf')
        print "Copying .internet to .conf"
        #plz_wait()
	os.system('sudo rm -rf /etc/dhcpcd.internet')
	print "Now you have internet!"


# Cheaky response when things are bad
else:
	print "Things aren't right here... expect spies."

time.sleep(1)
# Restart network interfaces for actions to take effect
os.system('sudo service dhcpcd restart')

print "Done!"

# yay.

