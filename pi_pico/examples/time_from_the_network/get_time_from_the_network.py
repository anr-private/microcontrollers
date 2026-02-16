#get_time_from_the_network.py

import network
import utime
import ntptime
import machine
import sys

from details import *

ssid = SSID
password = PW

DEBUG = True
def dbg(stg=None):
    """ output a string to the debug output """
    if not DEBUG: return
    if stg is None: stg = ""
    print(f"DBG:{stg}")


def connect_to_wifi(show_details=True):
    """ Connect to the WIFI WLAN.
    Return a wlan obj if successful else exception.
    """
    
    dbg(f"CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
    
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    dbg(f"  Connect to wifi: ssid='{ssid}'")
    wlan.connect(ssid, password)

    max_wait = 30 # Timeout in seconds
    num_tries = 0
    while num_tries < max_wait:
        wlan_status = wlan.status()
        dbg(f"waiting...  wlan_status={wlan_status}")
        if wlan_status < 0 or wlan_status >= 3:
            break
        num_tries += 1
        print(f"Waiting for connection...   num_tries={num_tries}  max={max_wait}")
        utime.sleep(1)
    dbg(f"wlan.status() = {wlan.status()}")
    
    if wlan.status() != 3:
        wlan.disconnect() # ignored if not connected
        raise RuntimeError(f"Network connection failed. wlan.status={wlan_status}")

    if show_details:
        print(f"Connected to wlan {ssid}")
        info = wlan.ifconfig()
        ip_addr = info[0]
        print(f"  IP={ip_addr}")
        # typical output: INFO: ('192.168.1.49', '255.255.255.0', '192.168.1.1', '192.168.1.1')
        ###print(f"  INFO: {info}")
    
    return wlan, ip_addr

def set_time_manually():
    """ Set the time from a hard-coded set of values"""
    # Set the date and time manually: (year, month, day, weekday, hour, minute, second, subsecond)
    # Weekday is 0-6 for Mon-Sun (though the 8-tuple uses 0-6 for Mon-Sun as well)
    rtc = machine.RTC()
    rtc.datetime((2026, 2, 16, 4, 11, 4, 0, 0))
    print(f"set_time_manually TIME set manually")


def show_current_time():

    current_time = utime.localtime()

    # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
    # (year, month, mday, hour, minute, second, weekday, yearday)
    # weekday is 0=Sun, etc
    print(current_time) # as tuple
    year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
    print(f"{year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
    weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
    print(f"  {weekday_stg=}")
    
    
def main(args):
    """ """

    wlan, ip_addr = connect_to_wifi(True)
    print(f"MAIN: {wlan=}  {ip_addr=}")

    if 0:
        # Set the time from an NTP server
        ntptime.settime()
        print("Time synced")
    else:
        # manual
        set_time_manually()

    show_current_time()



_="""
# Connect to WiFi (replace with your credentials)
ssid = "YOUR_SSID"
pw = "YOUR_PASSWORD"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)

while not wifi.isconnected():
    pass
print("Connected. Syncing time...")

# Set the time from an NTP server
ntptime.settime()
print("Time synced")

import machine
# Set the date and time manually: (year, month, day, weekday, hour, minute, second, subsecond)
# Weekday is 0-6 for Mon-Sun (though the 8-tuple uses 0-6 for Mon-Sun as well)
rtc = machine.RTC()
rtc.datetime((2024, 2, 16, 4, 11, 4, 0, 0))


import utime
current_time = utime.localtime()
print(current_time)
# Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
# (year, month, mday, hour, minute, second, weekday, yearday)


import utime

now = utime.localtime()

# Format the date as "YYYY-MM-DD" and time as "HH:MM:SS"
date_str = "Date: {}-{}-{}".format(now[0], now[1], now[2])
time_str = "Time: {}:{}:{}".format(now[3], now[4], now[5])

print(date_str)
print(time_str)

# Combined formatted print (as a single line)
# Note the use of slicing and concatenation for a clean format
timestring = "%04d-%02d-%02d %02d:%02d:%02d" % (now[0:3] + now[3:6])
print(timestring)
# Example output: 2024-02-16 11:04:30

"""



if __name__ == "__main__":
    main(sys.argv[1:])
