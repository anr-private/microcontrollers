# wifi_connect__w_lcd.py
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
from machine import SoftI2C, Pin
from lib_lcd1602_2004_with_i2c import LCD

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#print("Attempting to connect...")
#wlan.connect("SSID", "PW")
    
from details import SSID, PW

ssid = SSID
password = PW

LCD_SDA_PIN = 2
LCD_SCL_PIN = 3
print(f"LCD:   Data=GPIO{LCD_SDA_PIN}  Clock=GPIO{LCD_SCL_PIN} ")

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
    if 1:
        time.sleep(1)
        led.value(0)
        time.sleep(1)
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
    return led


def setup_lcd():
    print(f"setup_lcd: try to locate the LCD device...")
     # SoftI2C is software I2C - works on ANY GPIO pins(!)
     # 100K is default freq.  Can go higher ex 400K
    lcd = LCD(SoftI2C(sda=Pin(LCD_SDA_PIN), scl=Pin(LCD_SCL_PIN), freq=100000))
    print(f"setup_lcd: ... located the LCD device...")
    lcd.puts(" "*16)
    lcd.puts("  lcd is ready  ", y=1)
    return lcd


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


def monitor_wifi(wlan, led, lcd):
    ctr = 0
    secs = 0
    ipaddr = "no-ipaddr"
    prev_ip_addr = None

    while True:
        ctr += 1

        ###if ctr >=32:
        ###    print(f"@136 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FAKE A DISCONNECT @@@@@@@@@@@@@@@@@@@@")
        ###    wlan.disconnect()

        ok = wlan.isconnected()

        if 0:
            # for testing
            if ctr > 10:
                ok = False
                print("@@@@@@@@@@@@@@@@ FAKING LOST CONNECTION")

        ###print(f"@142   ctr&7 is {ctr & 7}")
        if ctr & 7 == 0:
            secs = ctr >> 1  # 2 counts per second
            ###ctr_shown = ctr >> 3
            print(f"Connected: {ok}      {secs=}  loop-ctr={ctr} ")
            is_conn = "conn " if ok else "NOCONN"
            lcd.puts(f"{is_conn} secs={secs}  ")

        if ok:
            info = wlan.ifconfig()
            if info:
                ipaddr = info[0]
            else:
                ipaddr = "NO IP ADDR!"
            led.toggle()
        else:
            ipaddr = "NOT CONNECTED"
            led.value(0)

        if prev_ip_addr != ipaddr:
            prev_ip_addr = ipaddr
            lcd.puts(ipaddr+"      ", y=1)

        time.sleep(0.5)


def main(args):
    print(f"MAIN:  args={args}")

    wlan = None
    lcd = None

    try:
        led = get_builtin_led()

        lcd = setup_lcd()

        print(f"MAIN@155  lcd is {lcd}")

        ##@@@@@@time.sleep(1.5)

        lcd.puts("Finding wifi...")
        lcd.puts("                ", y=1)

        wlan = find_wifi(led)

        lcd.puts("Found wifi       ")

        #print(f"@157 DIR WLAN is ...")
        #print(dir(wlan))
    
        monitor_wifi(wlan, led, lcd)
    
    except KeyboardInterrupt:
        print("  MAIN:  keyboard interrupt")
    finally:
        if wlan is not None:
            print("MAIN: disconnect the WLAN ")
            wlan.disconnect()
        if lcd is not None:
            lcd.clear()

    #print(f"MAIN:  wifi is {wifi}")

    #time.sleep(10)


if __name__ == "__main__":
    main(sys.argv[1:])

    
### end ###
