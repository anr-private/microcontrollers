#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example1-GetReadings.py
#
# Simple Example for the Qwiic Soil Moisture Device
#
# Written by  SparkFun Electronics, May 2019
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
# More information on qwiic is at https://www.sparkfun.com/qwiic

import qwiic_soil_moisture_sensor
import time
import sys

def runExample():

	address = 0x37	 # default for capacitive sensor

	print(f"\nSparkFun Qwiic Soil Moisture Sensor Example 1	 address=0x{address:02X}\n")
	mySoilSensor = qwiic_soil_moisture_sensor.QwiicSoilMoistureSensor(address=address)

	if mySoilSensor.is_connected() == False:
		print("The Qwiic Soil Moisture Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySoilSensor.begin()

	print("Initialized.")

	while True:
		mySoilSensor.read_moisture_level()
		print (mySoilSensor.level)
		mySoilSensor.led_on()
		time.sleep(1)
		mySoilSensor.led_off()
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


###
