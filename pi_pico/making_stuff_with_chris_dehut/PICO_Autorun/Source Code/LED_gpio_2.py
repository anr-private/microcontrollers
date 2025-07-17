# LED.py  
# blink GPIO 25 internal LED    ANR
# Does not work with the 'clone' Pico W(?) brand DVOZVO boards

import machine
import utime

# GPIO 25 (no board pin) is 'internal led' - does not appear to work on the clone W boards I bought
# board pin 3 is GND
# board pin 20 is GPIO 15
pin = 25
pin = 15
pin=2
LED = machine.Pin(pin, machine.Pin.OUT) #Set pin 25 as output

while True:
    print("  blink the internal LED")
    LED.value(1) #Turn on LED
    utime.sleep(.5) 
    LED.value(0) #Turn off LED
    utime.sleep(.25)
