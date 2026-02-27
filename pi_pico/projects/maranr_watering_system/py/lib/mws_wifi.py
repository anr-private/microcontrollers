# mws_wifi.py
#
# handle connecting to Wifi

#@@@@@ FIXES FOR WIFI
#Disable Power-Save Mode: By default, the Pico W uses aggressive power-saving, which can cause connection drops. Use wlan.config(pm = 0xa11140) to keep the radio active.
#Robust Reconnection Loop: Do not assume wlan.connect() works permanently. Implement a while not wlan.isconnected(): loop with time.sleep() to check status and re-initiate connection.
#Handle DHCP Timeouts: The Pico W might fail to get an IP quickly. Add a timeout to your connection script; if it doesn't connect within 10-20 seconds, deactivate (wlan.active(False)) and reactivate the interface before trying again.

import network
import utime
import ntptime

from details import SSID, PW
#from utils import *
import lib.utils as utils
dbg = utils.dbg
loggg = utils.loggg

ssid = SSID
password = PW

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


def wifi_set_time_from_ntp(wlan):

    try:
        ntptime.settime()
    except Exception as ex:
        m = f"WIFI@61 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}"
        dbg(m)
        loggg(m)
        return False

    # verify the time
    current_time = utime.localtime()

    # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
    # (year, month, mday, hour, minute, second, weekday, yearday)
    # weekday is 0=Sun, etc
    print(f"TIME FROM NTP: {current_time} ") # as tuple
    year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
    print(f"{year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
    weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
    print(f"  {weekday_stg=}")

    return True

###
