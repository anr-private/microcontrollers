# simple_i2c_scan.py

###import machine
from machine import Pin, SoftI2C, I2C

import time

i2c_bus_number = 0
data_pin_number = 0
clock_pin_number = 1


# Ensure you use the exact pins matching your microcontroller board layout
# 100kHz (100000) is the most reliable speed for the SparkFun co-processor
i2c = I2C(i2c_bus_number, scl=Pin(clock_pin_number), sda=Pin(data_pin_number), freq=100000)

#i2c = SoftI2C(i2c_bus_number, scl=Pin(clock_pin_number), sda=Pin(data_pin_number),  freq=100000))
i2c = SoftI2C(Pin(1), Pin(0), freq=100000)

print("Starting continuous I2C loop scan...")
secs = 0
newline_ctr = 0
while True:
    secs += 5
    newline_ctr += 5
    try:
        devices = i2c.scan()
        if devices:
            print(f"\n{secs=}  Device found at address:", [hex(d) for d in devices])
        else:
            print(f"{secs=}  No device  ", end="")
            #if (secs % 20) == 0: print()
            if newline_ctr >= (5*8):
                print()
                newline_ctr = 0
    except Exception as e:
        print("Bus Error:", e)
    time.sleep(5) # Check once per second        


###
