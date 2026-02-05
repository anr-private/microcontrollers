# wifi_simple_client.py
#
#  0 (STAT_IDLE): No connection and no activity.
#  1 (STAT_CONNECTING): Connection in progress.
#  3 (STAT_GOT_IP): Connection successful, IP address obtained.
# -1 (STAT_CONNECT_FAIL): Connection failed.
# -2 (STAT_NO_AP_FOUND): No access point found.
# -3 (STAT_WRONG_PASSWORD): Incorrect password. 
#
# dir(wlan-obj) output:
#  ['__class__', 'IF_AP', 'IF_STA', 'PM_NONE', 'PM_PERFORMANCE', 'PM_POWERSAVE', 'SEC_OPEN',
#   'SEC_WPA2_WPA3', 'SEC_WPA3', 'SEC_WPA_WPA2', 'active', 'config', 'connect', 'deinit', 'disconnect',
#   'ifconfig', 'ioctl', 'ipconfig', 'isconnected', 'scan', 'send_ethernet', 'status']

import machine
import network
import urequests
import utime
    
from details import SSID, PW

ssid = SSID
password = PW
    
VERBOSE = True
VV = VERBOSE    
    

def dbg(stg=None):
    """ output a string to the debug output """
    if not VERBOSE: return
    if stg is None: stg = ""
    print(f"DBG:{stg}")


def connect_to_wifi(show_details=True):
    """ Connect to the WIFI WLAN.
    Return a wlan obj if successful.
    Else raises exception
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
    
    return wlan


def fetch_url(url):
    try:
        response = urequests.get(url)
        print("Status Code:", response.status_code)
        print("Content:")
        print(response.text)
        response.close() # Always close the response
        return response
    
    except Exception as e:
        print("Error fetching URL:", e)
    except RuntimeError as e:
        print("FETCH_URL: " + e)
    except KeyboardInterrupt:
        print("FETCH_URL: " + e)
    print("FETCH_URL: returns NONE")

def OLD___fetchurl(url):
    try:
        wlan = connect_to_wifi()
        if wlan.isconnected():
            # Example: Fetch a test URL. Replace with your desired URL.
            test_url = "http://example.com"
            fetch_url(test_url)
        else:
            print("WiFi connection lost, cannot fetch URL")
    except RuntimeError as e:
        print(e)
    except KeyboardInterrupt:
        pass




    except RuntimeError as e:
        print(e)
    except KeyboardInterrupt:
        pass


def main():
    """ main pgm for web client """
    dbg(f"MAIN: begin  wifi_simple_client")

    try:
        wlan = connect_to_wifi()
        dbg(f"MAIN connected to wlan!")
        
        #while True:
        if 1:
            url = "http://192.168.1.215:8000"
            #url = "http://example.com"
            dbg(f"MAIN  url='{url}'")    
            if not wlan.isconnected():
                print(f"WiFi connection lost. Cannot fetch URL '{url}'")
                
            result = fetch_url(url)
            
            print("="*60)
            print(f"@@@ RESULT {result}")
            print("-"*60)


    except KeyboardInterrupt:
        print(f"INTERRUPTED BY USER ^C")
    except RuntimeError as ex:
        print(f"RUNTIME ERROR: {ex}")
    except Exception as ex:
        print(f"UNKNOWN EXCEPTION: {ex}")

    dbg(f"MAIN: exit  wifi_simple_client")
    
    # This does a Soft Reset. Equiv to control-D
    #sys.exit()
    # This does a Hard Reset: equiv to power cycle of the Pi Pico
    #machine.reset()
    
if __name__ == '__main__':
    main()


### end ###
