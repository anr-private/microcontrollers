#Animated Battery Level display
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

def Battery_Level_Gauge(Delay, Value):
    A_LED.value(0)       #Turn off all LEDs
    B_LED.value(0)       
    C_LED.value(0)       
    D_LED.value(0)       
    E_LED.value(0)       
    F_LED.value(0)       
    G_LED.value(0)       
    H_LED.value(0)       
    I_LED.value(0)       
    J_LED.value(0)
    
    if (Value >= 1): J_LED.value(1)  #If in range, turn on LEDs sequentially
    utime.sleep(Delay)               #Short delay to animate the display
    if (Value >= 2): I_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 3): H_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 4): G_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 5): F_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 6): E_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 7): D_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 8): C_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 9): B_LED.value(1)
    utime.sleep(Delay)
    if (Value >= 10):A_LED.value(1)
    utime.sleep(Delay)
   
        
print("Ready, Set, GO!")
while True:
    Battery_Level_Gauge(.15, 10) #0=Dead-Red   10=Full Charge-Blue
    utime.sleep(3)

