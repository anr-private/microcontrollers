# Mimic a VU (Volume Unit) Meter display
# Bargraph LED display - 10 segment, multi color, Common cathode

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
import random   #used to get random numbers

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

  
def VU_Animated_Display(Delay, Value):
    if (Value >= 10):        #If Value in range - turn it on
        J_LED.value(1)       #Turn bar (LED) ON
        utime.sleep(Delay)   #Short pause to create animation
    else:                    #Value not in range to be on
        J_LED.value(0)       #turn the bar (LED) OFF
        
    if (Value >= 9):
        I_LED.value(1)
        utime.sleep(Delay)
    else:
        I_LED.value(0)
  
    if (Value >= 8):
        H_LED.value(1)
        utime.sleep(Delay)
    else:
        H_LED.value(0)
    
    if (Value >= 7):
        G_LED.value(1)
        utime.sleep(Delay)
    else:
        G_LED.value(0)
    
    if (Value >= 6):
        F_LED.value(1)
        utime.sleep(Delay)
    else:
        F_LED.value(0)
    
    if (Value >= 5):
        E_LED.value(1)
        utime.sleep(Delay)
    else:
        E_LED.value(0)
    
    if (Value >= 4):
        D_LED.value(1)
        utime.sleep(Delay)
    else:
        D_LED.value(0)
    
    if (Value >= 3):
        C_LED.value(1)
        utime.sleep(Delay)
    else:
        C_LED.value(0)
    
    if (Value >= 2):
        B_LED.value(1)
        utime.sleep(Delay)
    else:
        B_LED.value(0)
        
    if (Value >= 1):
        A_LED.value(1)
        utime.sleep(Delay)
    else:
        A_LED.value(0)
        
        
        
print("Ready, Set, GO!")
while True:
    Value = random.randint(0, 10)  #Create a random integer in range 0 to 10
    VU_Animated_Display(.005, Value)
    utime.sleep(.05)

