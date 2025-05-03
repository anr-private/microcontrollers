# Blink a red LED that is connected to GPIO pin 15
# Control green LED on GPIO 14 using button on GPIO 13.
# GPIO 15 is the lower left pin looking from top of Pico
# with USB at the top.
# GPIO 14 is just above 15 (ie towards the USB socket)
# GPIO is TWO (2) pins above 14
#   there is a GND between 14 and 13.
#
# Uses connections:
#  GPIO 15 to resistor  (220 or 330 ohms; min 50 ohms)
#  resistor to LED anode (long lead)
#  LED cathode (short lead) to gnd (negative)
#  GPIO 14 to resistor  (220 or 330 ohms; min 50 ohms)
#  resistor to LED anode (long lead)
#  LED cathode (short lead) to gnd (negative)
#  Button goes GPIO 13 to gnd

import time
from picozero import LED, Button

GPIO_15 = 15
GPIO_14 = 14
GPIO_13 = 13

red_led = LED(GPIO_15)
green_led = LED(GPIO_14)
btn = Button(GPIO_13)

pico_led = red_led

def blink_red_led(secs):
    pico_led.on()
    time.sleep(secs)
    pico_led.off()
    time.sleep(secs)

def fancy_blink():
    while True:
        blink_red_led(0.4)
        blink_red_led(0.4)
        time.sleep(0.65)
        blink_red_led(0.15)
        blink_red_led(0.15)
        
        time.sleep(1.5)


btn.when_pressed = green_led.toggle

fancy_blink()

###
