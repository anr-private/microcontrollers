# pushbuttons_5btns_uses_asyncio.py
#
# Test program for the 5 pushbuttons on the Maranr Watering System
# prototype board/system/setup.
# 
# This is based on the initial tests found here:
#  ~/git/microcontrollers/pi_pico/examples/async_Peter_Hinch/...
#    pushbutton_examples/pushbutton_w_coro__5_btns_ex.py
#
#
# There are 5 pushbuttons arranged and connected like this and numbered as such:
#          UP                       1
#  LEFT  CENTER  RIGHT         2    3    4
#         DOWN                      5
#
# Button     GPIO Pin
#     1        14        U    up
#     2        15        L    left
#     3        20        C    center
#     4        21        R    right
#     5        22        D    down
#
#
# Uses coroutines (coro's).
# This allows the handler(s) to do things like await on a sleep()
# and not stall the main loop (or other async tasks, for that matter.)
#
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#46-suppress-mode

from machine import Pin
import asyncio
import time

from primitives import Pushbutton
from primitives import set_global_exception

UP_BUTTON_GPIO_PIN     = 14
LEFT_BUTTON_GPIO_PIN   = 15
CENTER_BUTTON_GPIO_PIN = 20
RIGHT_BUTTON_GPIO_PIN  = 21
DOWN_BUTTON_GPIO_PIN   = 22


TASK_1_CTR = 0  # fake task

SHORT_CTR = 0
DOUBLE_CTR = 0
LONG_CTR = 0

async def handle_short(btn, btn_name):
    global SHORT_CTR
    SHORT_CTR += 1
    print(f"@31  SHORT PRESS  btn={btn} {btn_name}")
    if 1:
        print(f"@33    WAITing in handle_short() - should not stall the main loop!")
        await asyncio.sleep(3)
        print(f"@35    DONE-WAITing in handle_short()")
        

async def handle_double(btn, btn_name):
    global DOUBLE_CTR
    DOUBLE_CTR += 1
    print(f"@18 DOUBLE PRESS  btn={btn} {btn_name}")

async def handle_long(btn, btn_name):
    global LONG_CTR
    LONG_CTR += 1
    print(f"@21  LONG PRESS  btn={btn} {btn_name}")


async def task_1(): # fake task
    global TASK_1_CTR
    TASK_1_CTR = 0
    while 1:
        TASK_1_CTR += 1
        if TASK_1_CTR % 500 == 0:
            print(f"@10 task_1  ctr={TASK_1_CTR}")
        await asyncio.sleep(0)


def init_one_button(btn, btn_name):
    pb = Pushbutton(btn, suppress=True)
    pb.release_func(handle_short, (btn, btn_name))
    pb.double_func(handle_double, (btn, btn_name))
    pb.long_func(handle_long, (btn, btn_name))
    return pb


async def main():
    print(f"MAIN@24 STARTed  Buttons are:")
    print(f"  UP      {UP_BUTTON_GPIO_PIN}")
    print(f"  LEFT    {LEFT_BUTTON_GPIO_PIN}")
    print(f"  CENTER  {CENTER_BUTTON_GPIO_PIN}")
    print(f"  RIGHT   {RIGHT_BUTTON_GPIO_PIN}")
    print(f"  DOWN    {DOWN_BUTTON_GPIO_PIN}")
    
    # set a global exception handler - for debugging an async program.
    # (not really needed for this simple test)
    ###set_global_exception()
    
    up_btn     = Pin(UP_BUTTON_GPIO_PIN, Pin.IN, Pin.PULL_UP)
    left_btn   = Pin(LEFT_BUTTON_GPIO_PIN, Pin.IN, Pin.PULL_UP)
    center_btn = Pin(CENTER_BUTTON_GPIO_PIN, Pin.IN, Pin.PULL_UP)
    right_btn  = Pin(RIGHT_BUTTON_GPIO_PIN, Pin.IN, Pin.PULL_UP)
    down_btn   = Pin(DOWN_BUTTON_GPIO_PIN, Pin.IN, Pin.PULL_UP)

    if 1:
        # slow down the polling
        Pushbutton.debounce_ms *= 2
    print(f"@32  Pushbutton.debounce_ms is {Pushbutton.debounce_ms}")

    # pb = Pushbutton(btn, suppress=True)
    # pb.release_func(handle_short, (btn,))
    # pb.double_func(handle_double, (btn,))
    # pb.long_func(handle_long, (btn,))

    up_pb     = init_one_button(up_btn, "Up")
    left_pb   = init_one_button(left_btn, "Left")
    center_pb = init_one_button(center_btn, "Center")
    right_pb  = init_one_button(right_btn, "Right")
    down_pb   = init_one_button(down_btn, "Down")

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
