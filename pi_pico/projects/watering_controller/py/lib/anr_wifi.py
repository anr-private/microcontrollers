# wsp_wifi.py
#
# handle connecting to Wifi

import network
import utime

from details import SSID, PW
from utils import *

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


###