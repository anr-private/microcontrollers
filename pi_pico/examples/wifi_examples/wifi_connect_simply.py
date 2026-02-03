# wifi_connect_simple.py
#
# DOES NOT CONNECT  9/3/2025
#  Maybe the wifi (Ubiquity) is WPA3 only? If so Pico W firmware does not know how to do WPA3
# So set the router to WPA2/WPA3 mode(?)
#
#  0 (STAT_IDLE): No connection and no activity.
#  1 (STAT_CONNECTING): Connection in progress.
#  3 (STAT_GOT_IP): Connection successful, IP address obtained.
# -1 (STAT_CONNECT_FAIL): Connection failed.
# -2 (STAT_NO_AP_FOUND): No access point found.
# -3 (STAT_WRONG_PASSWORD): Incorrect password. 

import network
import utime
time=utime

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#print("Attempting to connect...")
#wlan.connect("SSID", "PW")
    
from details import SSID, PW

ssid = SSID
password = PW
    
if 1:   
    
    wlan = network.WLAN(network.STA_IF) # Create a Wi-Fi station interface
    wlan.active(True) # Activate the Wi-Fi chip
    
    print(f"Attempting to connect: SSID={ssid}")
    wlan.connect(ssid, password) # Connect to your network

    # Wait for the connection to establish
    max_wait = 30 # Timeout in seconds
    num_tries = 0
    while num_tries < max_wait:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        num_tries += 1
        print(f"Waiting for connection...   num_tries={num_tries}  max={max_wait}")
        time.sleep(1)
    print(f"wlan.status() = {wlan.status()}")
    
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected to network')
        print('Network config:', wlan.ifconfig())


if 1:
    while True:
        print(f"Connected: {wlan.isconnected()}")
        utime.sleep(1)
    
### end ###
