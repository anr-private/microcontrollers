# Simple Single Color LED
# Turn on and off in a timed loop

# pin 4/GP2 for LED output

#ALSO REQUIRED!!!
#120 ~ 330 ohm resistor
#Red LED 
#Wire according to information provided on associated video on YouTube


#load libraries
import machine
import utime

LED = machine.Pin(2,machine.Pin.OUT)  #use pin 4/GP2 for LED output

print("Ready, Set, GO!")
while True:
    LED.value(1)    #Turn ON LED
    utime.sleep(1) #Pause 1 second while on
    LED.value(0)    #Turn OFF LED
    utime.sleep(.25) #Pause .25 second while off
   


