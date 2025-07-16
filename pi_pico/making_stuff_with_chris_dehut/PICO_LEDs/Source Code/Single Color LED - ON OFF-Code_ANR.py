# Simple Single Color LED
# Communicating a message in Morses code  ANR

# pin 4/GP2 for LED output

#ALSO REQUIRED!!!
#120 ~ 330 ohm resistor
#LED 


#load libraries
import machine
import utime

LED = machine.Pin(2,machine.Pin.OUT)  #use pin 4/GP2 for LED output
LED.value(0)    #Turn OFF LED

def Coded_Msg(msg):
    #msg will consist of 4 characters that are either of the letters S or L
    #The total duration for a single character is 2 seconds...
    #S = Short on-blink  --> on for .25 seconds then off for 1.75 seconds
    #L = Long on-blink   --> on for .75 seconds then off for 1.25 seconds
    #Example: LSSL - long-on, short-on, short-on, long-on
    Short_Delay = .25 #seconds
    Long_Delay  = 1.0 #seconds
    
    L = 3
    while L > 0:                         #Flash the LED on and off rapidly to indicate msg start
        LED.value(1)    #Turn ON LED
        utime.sleep(.05)
        LED.value(0)    #Turn OFF LED
        utime.sleep(.05)
        L -= 1
    
    utime.sleep(1)
    if len(msg) < 4:
        print("Message must be 4 characters long!")
    else:
        for c in msg:
            if c == "L":
                print(c)
                LED.value(1)    #Turn ON LED
                utime.sleep(Long_Delay) #Pause 1 second while on
                LED.value(0)    #Turn OFF LED
                Off_Delay = 2 - Long_Delay
                utime.sleep(Off_Delay) #Pause 1 second while on
            elif c == "S":
                print(c)
                LED.value(1)    #Turn ON LED
                utime.sleep(Short_Delay) #Pause 1 second while on
                LED.value(0)    #Turn OFF LED
                Off_Delay = 2 - Short_Delay
                utime.sleep(Off_Delay) #Pause 1 second while on
    utime.sleep(.5)
                
                
                

Coded_Msg("LSLS")  #code for good or whatever you want it to be
print("next coded msg")
Coded_Msg("LLLL") #make up any combination you want, just inform the user what the code means


        
        
        
        
        
        
        
        
    




   


