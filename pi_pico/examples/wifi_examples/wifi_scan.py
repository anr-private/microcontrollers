# wifi_scan.py
#
# This finds the wifi lan but has 'unknown' security type.

import network
import rp2

# Set the country for the Wi-Fi module (optional but recommended)
rp2.country('US') # Use your relevant country code

# Initialize the Wi-Fi interface (station mode)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Scan for nearby Wi-Fi networks
print("Scanning for Wi-Fi networks...")
networks = wlan.scan()

# Check if any networks were found
if not networks:
    print("No Wi-Fi networks found.")
else:
    print(f"Found {len(networks)} network(s):")
    # Sort by RSSI (strongest first) for better usability (optional)
    networks.sort(key=lambda x: x[3], reverse=True)

    print("--------------------------------------------------")
    print(f"{'SSID':<20} {'Channel':<7} {'RSSI':<5} {'Security'}")
    print("--------------------------------------------------")

    for net in networks:
        ssid = net[0].decode('utf-8', 'ignore') # Decode SSID
        channel = net[2]
        rssi = net[3]
        security_byte = net[4]

        # Decode security type (0: None, 1: WEP, 2: WPA-PSK, 3: WPA2-PSK, 4: WPA/WPA2-PSK)
        security_map = {0: "Open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        security = security_map.get(security_byte, f"Unknown ({security_byte})")

        # Only print if SSID is not empty (some networks might be hidden)
        if ssid:
            print(f"{ssid:<20} {channel:<7} {rssi:<5} {security}")
    print("--------------------------------------------------")
