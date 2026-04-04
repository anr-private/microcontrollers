# pushbutton_using_coro_ex.py
#
# Expansion of the 'simple' Peter Hinch async Pushbutton example.
# Uses coroutines (coro's) instead of the simple 'print' callable
# used by Hinch's example.
#
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#46-suppress-mode

from machine import Pin
import asyncio
from primitives import Pushbutton
import time

async def handle_short(btn):
    print(f"@15  handle_short SHORT PRESS  btn={btn}")

async def handle_double(btn):
    print(f"@18 handle_double DOUBLE PRESS  btn={btn}")

async def handle_long(btn):
    print(f"@21  handle_long LONG PRESS  btn={btn}")

async def main():
    print("MAIN@24 STARTed")
    btn = Pin(18, Pin.IN, Pin.PULL_UP)  # Adapt for your hardware

    pb = Pushbutton(btn, suppress=True)
    pb.release_func(handle_short, (btn,))
    pb.double_func(handle_double, (btn,))
    pb.long_func(handle_long, (btn,))

    elapsed = 0
    start_time = time.time()
    while elapsed < 60:  # Run for one minute
        elapsed += 1
        actual_elapsed = time.time() - start_time
        print(f"@37                                MAIN: waited {elapsed} secs  ACTUAL delay: {actual_elapsed} secs")
        await asyncio.sleep(1)

asyncio.run(main())

###
