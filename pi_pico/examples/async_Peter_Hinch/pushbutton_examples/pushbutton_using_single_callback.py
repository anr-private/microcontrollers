# pushbutton_using_single_callback.py
#
# Expansion of the 'simple' Peter Hinch async Pushbutton example.
# Uses a single simple function to handle presses.
# Does not uses coroutine(s) (coro's).
#
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#46-suppress-mode

from machine import Pin
import asyncio
from primitives import Pushbutton
import time

def handle_btn(press_type, btn):
    print(f"@15  handle_btn  press_type={press_type}  btn={btn}")
    # This is NOT a coroutine!
    # This sleep delays the async event loop!
    if 1:
        print("@19     Sleeping in the handler  -- DELAYS THE EVENT LOOP!")
        time.sleep(3) # delays

async def main():
    print("MAIN@23 STARTed")
    btn = Pin(18, Pin.IN, Pin.PULL_UP)  # Adapt for your hardware

    pb = Pushbutton(btn, suppress=True)
    pb.release_func(handle_btn, ("SHORT", btn) )
    pb.double_func(handle_btn, ("DOUBLE", btn) )
    pb.long_func(handle_btn, ("LONG", btn) )

    elapsed = 0
    start_time = time.time()
    while elapsed < 60:  # Run for one minute
        elapsed += 1
        actual_elapsed = time.time() - start_time
        print(f"@36                                MAIN: waited {elapsed} secs  ACTUAL delay: {actual_elapsed} secs")
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("@42    KEYBOARD interrupt")
finally:
    print("@44 << Create a new event loop, as cleanup >>")
    asyncio.new_event_loop()

###
