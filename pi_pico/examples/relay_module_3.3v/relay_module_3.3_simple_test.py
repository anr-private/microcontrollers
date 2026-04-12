# relay_module_3.3_simple_test.py
# 
# Turn relay on relay module PC board on and off  - like an LED.
#
# See:
#  ~/git/microcontrollers/components/relay_module_3.3v/relay_board.txt

from machine import Pin
import time
import os

# print("=== DETERMINE THE SYSTEM TYPE =========")
# print(f"os.uname={os.uname()}  type={type(os.uname())}")
# os_uname = os.uname()
# for x in os_uname:
    # print(f"   {x}")
##print(os_uname["machine"])

# machine_name = os_uname[4]
# machine_name_lc = machine_name.lower()
# print(f"  machine_name_lc={machine_name_lc}")
# if "pi pico w" in machine_name_lc:
    # this_machine = "pi pico w"
    # print(f"Machine is a Pi Pico W    this-machine='{this_machine}'")
# else:
    # print(f"Unknown system/hardware '{machine_name_lc}'")
# print()


# Initialize the built-in LED pin
# For Pico W, the built-in LED is accessed using the string "LED"
# if this_machine == "pi pico w":
    # # 'EXT_GPIO0'  GPIO zero on the wifi chip (not the Pico)
    # led = Pin("LED", Pin.OUT)
# else:
    # print(f"**ERROR**  unknown machine '{this_machine}'")
    # raise RuntimeError(f"Unknown machine '{machine_name}'")
# print(f"Blink the built-in LED {led}")

gp16 = machine.Pin(16, machine.Pin.OUT)

# Infinite loop to continuously turn relay on and off
try:
    while True:
        print("LOOP: toggle the RELAY state")
        gp16.value(1)  # Turn on (set pin value to high)
        time.sleep(1)  # Pause for 1 seconds
        gp16.value(0)  # Turn off (set pin value to low)
        time.sleep(1)  # Pause for 1 seconds
except (KeyboardInterrupt):
    gp16.value(0)
    print("... end of BLINK program ...")

### end ###

