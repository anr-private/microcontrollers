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
    await uasyncio.sleep_ms(10_000)

# Running on a pyboard
###from pyb import LED
###uasyncio.run(main(LED(1), LED(2)))

# Running on a generic board
from machine import Pin
###uasyncio.run(main(Pin(1), Pin(2)))
uasyncio.run(main(Pin(14), Pin(15)))

### end ###
