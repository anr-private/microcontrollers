# Blink an LED that is connected to GPIO pin 15
# GPIO 15 is the lower left pin looking from top of Pico
# with USB at the top.
# Uses connections:
#  GPIO 15 to resistor  (220 or 330 ohms; min 50 ohms)
#  resistor to LED anode (long lead)
#  LED cathode (short lead) to gnd (negative)

import time
from picozero import LED

GPIO_15 = 15

led = LED(GPIO_15)

# ORIGINAL example
# The blink() method produces fast, erratic blinking
def original_blink():
    while True:
        led.blink()
    
    
pico_led = led

def blink_led(secs):
    pico_led.on()
    time.sleep(secs)
    pico_led.off()
    time.sleep(secs)

def fancy_blink():
    while True:
        blink_led(0.4)
        blink_led(0.4)
        time.sleep(0.65)
        blink_led(0.15)
        blink_led(0.15)
        
        time.sleep(1.5)

# pick one:
#original_blink()
fancy_blink()

###
