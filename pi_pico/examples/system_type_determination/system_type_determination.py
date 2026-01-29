# system_type_determination
#
# How to tell which kind of Pi PICO you have

from machine import Pin
import utime
import os

def determine_machine_name(verbose=False):
    """ determine the type of Pi PICO on which are running
    Returns one of these:
        "pi pico w"         Pi PICO-W
        "unknown"           Unknown system type
    """
    
    if verbose:
        print("=== DETERMINE THE SYSTEM TYPE =========")
        print(f"os.uname={os.uname()}  type={type(os.uname())}")
        
    os_uname = os.uname()

    if verbose:
        for x in os_uname:
            print(f"   {x}")
        ##print(os_uname["machine"])

    raw_machine_name = os_uname[4]
    raw_machine_name_lc = raw_machine_name.lower()
    if verbose: print(f"  machine_name_lc={machine_name_lc}")

    if "pi pico w" in raw_machine_name_lc:
        machine_name = "pi pico w"
    else:
        machine_name = "unknown"
    return machine_name

def main():
    machine_name = determine_machine_name()
    
    if "pi pico w" in machine_name:
        print(f"Machine is a Pi Pico W    machine_name='{machine_name}'")
    else:
        print(f"Unknown system/hardware   machine_name='{machine_name}'")
    print()

main()

### end ###

