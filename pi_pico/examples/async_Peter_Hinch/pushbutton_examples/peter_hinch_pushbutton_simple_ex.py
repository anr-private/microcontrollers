# peter_hinch_pushbutton_simple_ex.py
#
# basic example use of Peter Hinch async Pushbutton class
#
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#46-suppress-mode

from machine import Pin
import asyncio
from primitives import Pushbutton

btn = Pin(18, Pin.IN, Pin.PULL_UP)  # Adapt for your hardware

async def main():
    print("MAIN@14 STARTed")
    pb = Pushbutton(btn, suppress=True)
    pb.release_func(print, ("SHORT",))
    pb.double_func(print, ("DOUBLE",))
    pb.long_func(print, ("LONG",))
    await asyncio.sleep(60)  # Run for one minute

asyncio.run(main())

###
