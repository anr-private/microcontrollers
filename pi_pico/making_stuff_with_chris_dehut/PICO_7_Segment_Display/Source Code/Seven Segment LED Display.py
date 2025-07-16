# 7 Segment LED display - Common cathode
# Turn on and off each segment

#ALSO REQUIRED!!!
#220 ohm resistor for each Segment
#Wire according to information provided on associated video on YouTube

#Check the data sheet for your display, adjust connections as needed
#Connect Common Cathode pins to GND pins on PICO
#Connect the segment LEDS to these pins

#A_LED  to pin 21/GP16
#B_LED  to pin 22/GP17
#DP_LED to pin 25/GP19
#C_LED  to pin 26/GP20

#D_LED to pin 16/GP12
#E_LED to pin 17/GP13
#G_LED to pin 19/GP14
#F_LED to pin 20/GP15

#load libraries
import machine
import utime

A_LED  = machine.Pin(16,machine.Pin.OUT)  #Create an output pin for each segment
B_LED  = machine.Pin(17,machine.Pin.OUT)  
DP_LED = machine.Pin(19,machine.Pin.OUT)  
C_LED  = machine.Pin(20,machine.Pin.OUT)  

D_LED  = machine.Pin(12,machine.Pin.OUT)  
E_LED  = machine.Pin(13,machine.Pin.OUT)  
G_LED  = machine.Pin(14,machine.Pin.OUT)  
F_LED  = machine.Pin(15,machine.Pin.OUT)  

print("Ready, Set, GO!")
Seq_Del = .1
while True:
    A_LED.value(1)       #Turn ON A LED segment
    utime.sleep(Seq_Del) #Pause a bit
    B_LED.value(1)       
    utime.sleep(Seq_Del) 
    DP_LED.value(1)       
    utime.sleep(Seq_Del) 
    C_LED.value(1)       
    utime.sleep(Seq_Del) 
    D_LED.value(1)       
    utime.sleep(Seq_Del) 
    E_LED.value(1)       
    utime.sleep(Seq_Del) 
    G_LED.value(1)       
    utime.sleep(Seq_Del) 
    F_LED.value(1)       
    utime.sleep(Seq_Del) 

    utime.sleep(1) 
    
    A_LED.value(0)       #Turn OFF A LED segment
    utime.sleep(Seq_Del) #Pause a bit
    B_LED.value(0)       
    utime.sleep(Seq_Del) 
    DP_LED.value(0)       
    utime.sleep(Seq_Del) 
    C_LED.value(0)       
    utime.sleep(Seq_Del) 
    D_LED.value(0)       
    utime.sleep(Seq_Del) 
    E_LED.value(0)       
    utime.sleep(Seq_Del) 
    G_LED.value(0)       
    utime.sleep(Seq_Del) 
    F_LED.value(0)       
    utime.sleep(Seq_Del) 

    utime.sleep(1) 
