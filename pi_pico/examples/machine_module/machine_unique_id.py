# machine_unique_id.py
#
# How to get the unique ID of the Pico

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


