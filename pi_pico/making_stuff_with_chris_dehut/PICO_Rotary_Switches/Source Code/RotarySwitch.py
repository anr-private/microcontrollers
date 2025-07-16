# Rotary ON-OFF Switch - Simple Polling using compare
# Check state and print it from within a loop

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin GP15   

#load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT)  #use on board LED to show switch state

#Create 'objects' for our actual Switch
Rotary_Sw = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)

#Polling method using compare to handle an ON-OFF switch
print("Ready, Set, GO!")
while True:  #run an endless loop
    if Rotary_Sw.value() == True: #If input GP15 is HIGH
        LED.value(1)
        print("ON")
    elif Rotary_Sw.value() == False: #If input GP15 is HIGH
        print("OFF")  
        LED.value(0)
       
    utime.sleep(.1) #slow down the loop so we can see the printing
    


