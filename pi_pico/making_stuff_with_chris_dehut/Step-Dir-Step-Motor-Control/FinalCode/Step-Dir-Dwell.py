'''
STEP-DIR Stepper Motor Drive Method

This example shows how to control a stepper motor using
a Step & Direction drive.  Velocity is controled by
specifying the time delay between steps.

Motor is 200 steps / rev
Stepping is set to 8 microsteps
200 * 8 = 1600 steps per revolution
'''

import machine
from time import sleep_us

#assign output pins for driver
Step_P = machine.Pin(14,machine.Pin.OUT) #Connect to PUL+
Dir_P  = machine.Pin(15,machine.Pin.OUT) #Connect to DIR+
LED    = machine.Pin(25,machine.Pin.OUT) #On PICO LED

def Make_Step():
    Step_P.value(1)     #Set step pin high
    sleep_us(3)         #Sleep for a very short time
    Step_P.value(0)     #Set step pin to LOW - thus creating a "pulse"
    LED.toggle()        #Toggle the LED
    
    
Dir_P.value(0)   #Set direction pin LOW
sleep_us(5)     

Steps = 0
print("Start run")
while Steps < 1600:   # run for 1 revolution
    Steps += 1        # Increment number of steps counter
    Make_Step()
    sleep_us(250)     # Sleep microseconds!!!!
    print(Steps)
    
    