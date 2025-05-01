# simple test for picozero
from picozero import pico_led
import time

while True:
    pico_led.on()
    time.sleep(0.5)
    pico_led.off()
    time.sleep(0.5)
    
### end ###
