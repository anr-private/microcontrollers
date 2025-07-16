# Simple Momentary Switch - Uncontrolled Polling  - BAD EXAMPLE!

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin 20/GP15

#load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT)  #use on board LED to show switch state

#Creat an 'object' for our actual Momentary Switch
Momentary_Sw = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)

#Polling method of handling an input
print("Ready, Set, GO!")
while True:  #run an endless loop - Typical main loop
    
    if Momentary_Sw.value() == True: #If input GP15 is HIGH
        LED.value(1)
        print("Button is pressed")
    elif Momentary_Sw.value() == False: #If input GP15 is LOW
        print("Button is not-pressed")  
        LED.value(0)
        
    utime.sleep(.01) #slow down the loop so we can see the printing
    


