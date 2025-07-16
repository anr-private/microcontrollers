# Bargraph LED display - 10 segment, multi color, Common cathode
# Turn on and off each segment

#ALSO REQUIRED!!!
#220 ohm resistor for each Segment - connect to ground
#Wire according to information provided on associated video on YouTube

#Find pin #1 - usually the corner that has a chamfer
#pin 1 to pin 21/GP16
#Continue down this side connecting the pins as such
#pin 2 to pin 22/GP17
#pin 3 to pin 24/GP18
#pin 4 to pin 25/GP19
#pin 5 to pin 26/GP20
#pin 6 to pin 27/GP21
#pin 7 to pin 29/GP22
#pin 8 to pin 31/GP26
#pin 9 to pin 32/GP27
#pin 10 to pin 34/G28
#Connect all the pins on the opposite side to ground through a 220 Ohm resistor

#load libraries
import machine
import utime

A_LED = machine.Pin(16,machine.Pin.OUT)  #Create an output pin for each segment
B_LED = machine.Pin(17,machine.Pin.OUT)  
C_LED = machine.Pin(18,machine.Pin.OUT)  
D_LED = machine.Pin(19,machine.Pin.OUT)  
E_LED = machine.Pin(20,machine.Pin.OUT)  
F_LED = machine.Pin(21,machine.Pin.OUT)  
G_LED = machine.Pin(22,machine.Pin.OUT)  
H_LED = machine.Pin(26,machine.Pin.OUT)  
I_LED = machine.Pin(27,machine.Pin.OUT)  
J_LED = machine.Pin(28,machine.Pin.OUT)  

print("Ready, Set, GO!")
Seq_Del = .1
while True:
    A_LED.value(1)       #Turn ON LED Bars in sequence
    utime.sleep(Seq_Del) #Pause a bit
    B_LED.value(1)       
    utime.sleep(Seq_Del) 
    C_LED.value(1)       
    utime.sleep(Seq_Del) 
    D_LED.value(1)       
    utime.sleep(Seq_Del) 
    E_LED.value(1)       
    utime.sleep(Seq_Del) 
    F_LED.value(1)       
    utime.sleep(Seq_Del) 
    G_LED.value(1)       
    utime.sleep(Seq_Del) 
    H_LED.value(1)       
    utime.sleep(Seq_Del) 
    I_LED.value(1)       
    utime.sleep(Seq_Del) 
    J_LED.value(1)       
    utime.sleep(Seq_Del) 

    utime.sleep(1) 
    
    A_LED.value(0)        #Turn OFF LED Bars in same sequence
    utime.sleep(Seq_Del)
    B_LED.value(0)
    utime.sleep(Seq_Del)
    C_LED.value(0)
    utime.sleep(Seq_Del)
    D_LED.value(0)
    utime.sleep(Seq_Del)
    E_LED.value(0)
    utime.sleep(Seq_Del)
    F_LED.value(0)
    utime.sleep(Seq_Del)
    G_LED.value(0)
    utime.sleep(Seq_Del)
    H_LED.value(0)
    utime.sleep(Seq_Del)
    I_LED.value(0)
    utime.sleep(Seq_Del)
    J_LED.value(0)
    utime.sleep(Seq_Del)

    utime.sleep(1) 
