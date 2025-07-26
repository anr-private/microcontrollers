from machine import Pin
import utime
import os

print("=== DETERMINE THE SYSTEM TYPE =========")
print(f"os.uname={os.uname()}  type={type(os.uname())}")
os_uname = os.uname()
for x in os_uname:
    print(f"   {x}")
##print(os_uname["machine"])

machine_name = os_uname[4]
machine_name_lc = machine_name.lower()
print(f"  machine_name_lc={machine_name_lc}")
if "pi pico w" in machine_name_lc:
    this_machine = "pi pico w"
    print(f"Machine is a Pi Pico W    this-machine='{this_machine}'")
else:
    print(f"Unknown system/hardware '{machine_name_lc}'")
print()


# Initialize the built-in LED pin
# For Pico W, the built-in LED is accessed using the string "LED"
if this_machine == "pi pico w":
    # 'EXT_GPIO0'  GPIO zero on the wifi chip (not the Pico)
    led = Pin("LED", Pin.OUT)
else:
    print(f"**ERROR**  unknown machine '{this_machine}'")
    raise RuntimeError(f"Unknown machine '{machine_name}'")
print(f"Blink the built-in LED {led}")
    
# Infinite loop to continuously blink the LED
try:
    while True:
        led.value(1)  # Turn the LED on (set pin value to high)
        utime.sleep(0.5)  # Pause for 0.5 seconds
        led.value(0)  # Turn the LED off (set pin value to low)
        utime.sleep(0.5)  # Pause for another 0.5 seconds
except (KeyboardInterrupt):
    led.value(0)
    print("... end of BLINK program ...")

### end ###
