''' This is a demo program featuring a digital sound sensor.
The sound sensor is inexpensive and can be purchased here...
https://www.amazon.com/HiLetgo-Sensor-Module-Detect-Control/dp/B00LW14ZEI
While advertised as a "Voice Detect", don't expect much in that way.

The device has a Trimmer Pot to set the threshold between Quiet and LOUD
We will monitor the output to see if the sound level is low or high with
digital input of the PICO.

'''

import machine
import time

#Create an 'object' for our digital pin
Sound_Sensor = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
pS = 0
cntr = 0
        
while True:
    if (Sound_Sensor.value() == 0) & (pS == 1):   #Now Quiet, was Loud
        print("***")
        pS = 0                                    #Set previous state to low
    elif (Sound_Sensor.value() == 1) & (pS == 0): #Now Loud, was Quiet
        print("*************",cntr) 
        pS = 1                                    #Set previous state to high
        cntr += 1
    time.sleep(.005) 
  