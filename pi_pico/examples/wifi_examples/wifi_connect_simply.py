# wifi_connect_simple.py
#
# Connect to wifi.
# Requires wifi credentials in file 'details.py'.
#
# Blinks the builtin LED according to the connection state:
#    Slow  - trying to connect
#    Fast  - connected ok
#
# DOES NOT CONNECT  9/3/2025  -- FIXED
#  Maybe the wifi (Ubiquity) is WPA3 only? If so Pico W firmware does not know how to do WPA3
# So set the router to WPA2/WPA3 mode(?)
# FIXED: Ubiquity was ok. This pgm was using incorrect SSID and PW.
#
#  0 (STAT_IDLE): No connection and no activity.
#  1 (STAT_CONNECTING): Connection in progress.
#  3 (STAT_GOT_IP): Connection successful, IP address obtained.
# -1 (STAT_CONNECT_FAIL): Connection failed.
# -2 (STAT_NO_AP_FOUND): No access point found.
# -3 (STAT_WRONG_PASSWORD): Incorrect password. 

import network
import os
import sys
import time
from machine import Pin

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#print("Attempting to connect...")
#wlan.connect("SSID", "PW")
    
from details import SSID, PW

ssid = SSID
password = PW

def get_builtin_led():
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
    elif "pi pico 2 w" in machine_name_lc:
        this_machine = "pi pico 2 w"
        print(f"Machine is a Pi Pico 2 W    this-machine='{this_machine}'")
    else:
        print(f"Unknown system/hardware '{machine_name_lc}'")
        this_machine = "UNKNOWN"
    print()

    # Initialize the built-in LED pin
    # For Pico W, the built-in LED is accessed using the string "LED"
    if this_machine == "pi pico w" or this_machine == "pi pico 2 w":
        # 'EXT_GPIO0'  GPIO zero on the wifi chip (not the Pico)
        led = Pin("LED", Pin.OUT)
    else:
        print(f"**ERROR**  unknown machine '{this_machine}'")
        raise RuntimeError(f"Unknown machine '{machine_name}'")
    print(f"Found built-in LED {led}")
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)
    return led

def find_wifi(led):

    wlan = network.WLAN(network.STA_IF) # Create a Wi-Fi station interface
    wlan.active(True) # Activate the Wi-Fi chip
    
    print(f"Attempting to connect: SSID={ssid}")
    wlan.connect(ssid, password) # Connect to your network

    # Wait for the connection to establish
    max_wait = 30 # Timeout in seconds
    num_tries = 0
    led.value(1)
    while num_tries < max_wait:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        num_tries += 1
        print(f"Waiting for connection...   num_tries={num_tries}  max={max_wait}")
        time.sleep(1)
        led.toggle()
    print(f"wlan.status() = {wlan.status()}")
    
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected to network')
        print('Network config:', wlan.ifconfig())
    return wlan

def monitor_wifi(wlan, led):
    ctr = 0
    while True:
        ctr += 1

        ok = wlan.isconnected()

        if 0:
            # for testing
            if ctr > 10:
                ok = False
                print("@@@@@@@@@@@@@@@@ FAKING LOST CONNECTION")

        print(f"Connected: {ok}")
        if ok:
            led.toggle()
        else:
            led.value(0)
        time.sleep(0.5)


def main(args):
    print(f"MAIN:  args={args}")
    led = get_builtin_led()

    time.sleep(2)

    wlan = find_wifi(led)

    monitor_wifi(wlan, led)


    print(f"MAIN:  wifi is {wifi}")

    time.sleep(10)


if __name__ == "__main__":
    main(sys.argv[1:])

    
### end ###
