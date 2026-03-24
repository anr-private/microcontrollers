# machine_unique_id.py
#
# How to get the unique ID of the Pico

# dir(machine):
#  ['__class__', '__name__',
#   'ADC', 'I2C', 'I2CTarget', 'I2S', 'PWM', 'PWRON_RESET', 'Pin',
#   'RTC', 'SPI', 'Signal', 'SoftI2C', 'SoftSPI', 'Timer', 'UART',
#   'USBDevice', 'WDT', 'WDT_RESET', '__dict__', 'bitstream', 'bootloader',
#   'deepsleep', 'dht_readinto', 'disable_irq', 'enable_irq', 'freq',
#   'idle', 'lightsleep', 'mem16', 'mem32', 'mem8', 'reset', 'reset_cause',
#   'soft_reset', 'time_pulse_us', 'unique_id']

import sys
from machine import WDT
import time
import ubinascii

def show_machine_id():
    raw_id = machine.unique_id()
    ###print(machine.unique_id())
    hex_id = ubinascii.hexlify(raw_id)
    print(f"Hexified raw id: '{hex_id}'")
    hex_stg = hex_id.decode("utf-8")
    print(f"    UTF-8 decoded: '{hex_stg}'")

def show_machine_module_attributes():
    ##print(machine.unique_id().decode("utf-8"))
    ###print(dir(machine))
    
    for p in dir(machine):
        print()
        print(p)
        if p =="unique_id":
            print("   !!! SKIP !!!")
            continue
        v = getattr(machine, p)
        #print(type(v))
        if not isinstance(v, int): continue
        print(f" {p}  {v}")

show_machine_id()

###


