# simple test for picozero
# does not work very well - blinks so fast it just looks like the LED
# is dimmed and flakey

from picozero import pico_led
import time

while True:
    pico_led.blink()
    
### end ###
