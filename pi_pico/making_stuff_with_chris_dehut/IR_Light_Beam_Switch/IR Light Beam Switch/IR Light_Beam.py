'''
This is a demonstration program utilizing the "Light Beam" switch from Adafruit P/N 6167

This is a typical light emitter/detector device.
When the light reaches the detector, switch is "ON"
When the light beam breaks, switch is "OFF"

'''
import machine
import utime

#Create an output object for use as our LED
LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show "Light Beam" switch state

#Create an 'object' for our "Light beam" switch
LB_Switch = machine.Pin(16,machine.Pin.IN,machine.Pin.PULL_UP)

 
LED.value(0)     #Turn Off LED
utime.sleep(1)   
print("Ready, Set, Go!")
while True:                              #run an endless loop - Typical main loop
    if (LB_Switch.value() == True):      #If light reaches detector - switch is ON
        LED.value(1)                     #Turn on the LED
        print("SW ON")
    elif (LB_Switch.value() != True):    #If light is not reaching detector - Switch is OFF
        LED.value(0)                     #Turn off the LED
        print("SW OFF")
    utime.sleep(.2)                      #slow down the loop to mimic other processing activities
        

        



