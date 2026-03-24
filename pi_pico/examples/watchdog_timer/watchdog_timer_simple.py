# watchdog_timer_simple.py
#
# Simple example of how to use the watchdog timer

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


def show_machine_reset_cause():
    
    prev_cause = machine.reset_cause()
    print(f"PREVIOUS VALUE of machine.reset_cause() is {prev_cause}")
    
    if prev_cause == machine.PWRON_RESET:
        print(f"  ... value {prev_cause} is machine.PWRON_RESET - Pico was powered on")
    elif prev_cause == 2:
        print(f" ... value {prev_cause} means machine.reset() was called within the Micropython program")
        print(f" ...     (note there is no attrib on the 'machine' module defined for this value(!?)")
    elif prev_cause == machine.WDT_RESET:
        print(f"  ... value {prev_cause} is machine.WDT_RESET - Pico was resetarted by the Watchdog Timer.")
    else:
        print(f"  ... value {prev_cause} is machine.PWRON_RESET - Pico was powered on")
    print(f"NOTE that a soft reset does not clear/alter the machine.reset() value.")
    return
    

def show_watchdog_firing():
    # 1. Initialize WDT with a 2-second (2000ms) timeout
    # Note: On RP2040, the maximum timeout is 8,388 ms (~8.3 seconds)
    wdt = WDT(timeout=2000)

    secs = 1.0
    while True:
        # Perform your main tasks here
        # In this example, the sleep delay slowly increases
        # until the watchdog fires.
        print(f"System running...secs={secs}")
        time.sleep(secs)
        secs += 0.1
        
        # 2. "Feed the dog" to prevent a reset
        wdt.feed()

show_machine_id()
show_machine_reset_cause()
show_watchdog_firing()


###


