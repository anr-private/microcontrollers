'''
This is a demonstration program to show some capabilities of the MCP23017 chip
This chip is a 16 pin port expander chip allowing each pin to be either a input or output
Eight of these devices can be connected to a single bus providing 128 additional I/O Pins!!!!
This demo sets up the 'A' port (pins 0 ~ 7) as outputs
Then sequences them on, then off.
The inputs are then configured on 'B' port (pins 8 ~ 15)
Depending on the state of the input, an LED will be set to the same state
Input #15 controls LED on pin 0, etc.

Requires a library --- mcp23017.py which can be obtained from here
https://github.com/mcauser/micropython-mcp23017
Mike's excellant work on this library makes the MCP23017 easy
for us to use - THANK YOU MIKE!

Caution must be used to to make sure too much current isn't pulled from the PICO.
An external power supply is often required at the MCP23017
Also be aware of the current limitation of the MCP23017 - it is NOT A DRIVER!

'''
from machine import Pin, I2C
import mcp23017
import time
sdaPIN=machine.Pin(20)  #Configure the i2c pins
sclPIN=machine.Pin(21)
i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000) #Configure i2c settings
mcp = mcp23017.MCP23017(i2c, 0x20)  #Create an object for using the chip

Dwell = .05
p = 0
while p <=7 :               #Turn all LEDs ON sequentially
    mcp[p].output(1)        #Turn ON pin
    time.sleep(Dwell)
    p += 1

p = 0
while p <=7 :              #Turn all LEDs OFF sequentially
    mcp[p].output(0)       #Turn OFF pin
    time.sleep(Dwell)
    p += 1    


ip = 8
while ip <=15:             #Set other port up as inputs pulled HIGH
    mcp[ip].input()        #Configure as input
    mcp[ip].input(pull=1)  #Turn on interal pull up resistor
    ip += 1


while True:
    ip = 8
    port_s = ""                        
    while ip <= 15:                #scan input port, pins 8 ~ 15
        if mcp[ip].value() == 1:   #if pin is high, it is ON
            p = ip - 8             #Calculate pin# of an output 
            mcp[p].output(1)       #Turn on the LED 
            port_s = port_s + "1"  #Create a visual representation of the port state
        elif mcp[ip].value() == 0:
            p = ip - 8
            mcp[p].output(0)
            port_s = port_s + "0"  
        ip += 1
    print(ip, port_s)              #print the port state showing all inputs
    time.sleep(.25)
            