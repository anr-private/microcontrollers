# LED_gpio_2.py
#
# Test program to load onto new Pi Pico or Pico W
# Blinks GPIO pin 2 (physical pin 4)
# Connect an LED + resistor to physical pins 3 and 4
# Physical 3 is GND.  Physical 4 is GPIO 2.
# Normally installed as 'main.py' so it boots when Pico is powered.

import machine
import utime

# GPIO 25 (no board pin) is 'internal led' - does not appear to work on the clone W boards I bought
# board pin 3 is GND
# board pin 20 is GPIO 15
#pin = 25
#pin = 15
pin=2
LED = machine.Pin(pin, machine.Pin.OUT)

while True:
    #print("  blink the internal LED")
    LED.value(1) #Turn on LED
    utime.sleep(.5) 
    LED.value(0) #Turn off LED
    utime.sleep(.25)

