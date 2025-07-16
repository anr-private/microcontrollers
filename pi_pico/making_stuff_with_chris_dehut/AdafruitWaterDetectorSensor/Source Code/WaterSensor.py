'''
Water Sensor/Detector Demo

This sensor outputs a positive voltage when wet
and 0 volts when dry

'''

import machine
import time

Water  = machine.Pin(16,machine.Pin.IN,machine.Pin.PULL_DOWN)  #Create a Digital input to read


while True:                        #Endless main loop
    if (Water.value() == 1):       #Test if sensor is ON
        print("WET")                #If on then wet 
    elif (Water.value() == 0):     #Test if sensor is OFF
        print("DRY")               #If off then dry
    time.sleep(1)




    