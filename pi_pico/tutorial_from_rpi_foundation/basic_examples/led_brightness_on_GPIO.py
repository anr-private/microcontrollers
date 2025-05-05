# Control the brightness of a red LED that is connected to GPIO pin 15
# Not used: green LED on GPIO 14
# Brightness steps/changes using button on GPIO 13.
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

def blink_led(led, brightnessReq, secs):
    """ brightness is 0 - 10, gets scaled to 0 - 1.0  """
    
    if (brightnessReq < 0):
        brightness = 0
    elif (brightnessReq > 10):
        brightness = 1.0
    else:
        brightness = brightnessReq / 10.0;
    print(f"Blink_led brightness set to: {brightness}      requested-brightness: {brightnessReq}")
    # Sets the brightness and turns the LED on
    led.brightness = brightness
    #led.on()
    time.sleep(secs)
    led.off()
    #led.brightness = 0.0
    time.sleep(secs/2.0)

brightness = 0
while True:
    blink_led(red_led, brightness, 0.4)
    
    brightness += 1
    ###print(f"now  {brightness}")
    
    if (brightness > 10):
        brightness = 0
    if 0:
        time.sleep(0.2)

###
