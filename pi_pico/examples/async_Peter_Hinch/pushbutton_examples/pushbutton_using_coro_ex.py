# pushbutton_using_coro_ex.py
#
# Expansion of the 'simple' Peter Hinch async Pushbutton example.
# Uses coroutines (coro's) instead of the simple 'print' callable
# used by Hinch's example.
#
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#46-suppress-mode

from machine import Pin
import asyncio
import time

from primitives import Pushbutton
from primitives import set_global_exception

TASK_1_CTR = 0

SHORT_CTR = 0
DOUBLE_CTR = 0
LONG_CTR = 0

async def handle_short(btn):
    global SHORT_CTR
    SHORT_CTR += 1
    print(f"@15  SHORT PRESS  btn={btn}")

async def handle_double(btn):
    global DOUBLE_CTR
    DOUBLE_CTR += 1
    print(f"@18 DOUBLE PRESS  btn={btn}")

async def handle_long(btn):
    global LONG_CTR
    LONG_CTR += 1
    print(f"@21  LONG PRESS  btn={btn}")


async def task_1(): # fake task
    global TASK_1_CTR
    TASK_1_CTR = 0
    while 1:
        TASK_1_CTR += 1
        if TASK_1_CTR % 500 == 0:
            print(f"@10 task_1  ctr={TASK_1_CTR}")
        await asyncio.sleep(0)


async def main():
    print("MAIN@24 STARTed")
    
    # set a global handler - not really needed for this simple test
    ###set_global_exception()
    
    btn = Pin(18, Pin.IN, Pin.PULL_UP)  # Adapt for your hardware

    if 1:
        # slow down the polling
        Pushbutton.debounce_ms *= 2
    print(f"@32  Pushbutton.debounce_ms is {Pushbutton.debounce_ms}")

    pb = Pushbutton(btn, suppress=True)
    pb.release_func(handle_short, (btn,))
    pb.double_func(handle_double, (btn,))
    pb.long_func(handle_long, (btn,))

    elapsed = 0
    start_time = time.time()
    while elapsed < 60:  # Run for one minute
        elapsed += 1
        actual_elapsed = time.time() - start_time
        print(f"@44                     MAIN: waited {elapsed} secs  ACTUAL delay: {actual_elapsed} secs  short={SHORT_CTR}  double={DOUBLE_CTR}  long={LONG_CTR}")
        await asyncio.sleep(1)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("@53    KEYBOARD interrupt")
finally:
    print("@55   <<<  Create a new event loop, as cleanup >>>")
    asyncio.new_event_loop()
    
###
