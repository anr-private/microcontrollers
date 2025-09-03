# wifi_connect_simple.py
#
# DOES NOT CONNECT  9/3/2025
#  Maybe the wifi (Ubiquity) is WPA3 only? If so Pico W firmware does not know how to do WPA3
# So set the router to WPA2/WPA3 mode(?)

import network
import utime
time=utime

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#print("Attempting to connect...")
#wlan.connect("SSID", "PW")
    
ssid = @@@@
password =@@@@
    
if 1:   
    
    wlan = network.WLAN(network.STA_IF) # Create a Wi-Fi station interface
    wlan.active(True) # Activate the Wi-Fi chip
    wlan.connect(ssid, password) # Connect to your network

    # Wait for the connection to establish
    max_wait = 10 # Timeout in seconds
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected to network')
        print('Network config:', wlan.ifconfig())


if 0:
    while True:
        print(f"Connected: {wlan.isconnected()}")
        utime.sleep(1)
    
### end ###
