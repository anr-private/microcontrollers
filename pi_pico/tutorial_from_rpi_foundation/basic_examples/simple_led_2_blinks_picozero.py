# simple test for picozero
# Does 2 slow blinks, 2 fast blinks, pause.
# Uses onboard LED.

from picozero import pico_led
import time

def blink_led(secs):
    pico_led.on()
    time.sleep(secs)
    pico_led.off()
    time.sleep(secs)


while True:
    blink_led(0.4)
    blink_led(0.4)
    time.sleep(0.65)
    blink_led(0.15)
    blink_led(0.15)
    
    time.sleep(1.5)
    
### end ###

