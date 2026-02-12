# asyncio_blink_leds.py
#
# Blinks LEDs on pins 14,15
# and main() does some busy work
# So 3 async tasks running concurrently

import uasyncio

async def blink(led, period_ms):
    while True:
        led.on()
        await uasyncio.sleep_ms(5)
        led.off()
        await uasyncio.sleep_ms(period_ms)

async def main(led1, led2):
    uasyncio.create_task(blink(led1, 700))
    uasyncio.create_task(blink(led2, 400))
    
    # just do some 'work' in main
    ctr = 0
    while 1:
        print(f"Main: counted to {ctr}")
        ctr += 1 
        await uasyncio.sleep_ms(2_000)

# Running on a pyboard
###from pyb import LED
###uasyncio.run(main(LED(1), LED(2)))

# Running on a generic board
from machine import Pin
###uasyncio.run(main(Pin(1), Pin(2)))

led14 = Pin(14, Pin.OUT)
led15 = Pin(15, Pin.OUT)

try:
    uasyncio.run(main(led14, led15))
except KeyboardInterrupt:
    print(f"=== Interrupted by USER control-C")
print(f"Turn off the LEDs")
led14.off()
led15.off()

### end ###
