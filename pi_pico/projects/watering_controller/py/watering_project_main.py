# watering_project_main.py
#
# main program for the watering project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import asyncio
import sys
import platform

from lib import anr_wifi
from utils import *


if determine_py_platform() == "micropython":
    sys.path.append("/anr_http")
else:
    sys.path.append("../anr_http")
#print(f"{sys.path=}")





async def main_task(host, port):
    while 1:
        print(f"MAIN TASK running    {host=}   {port=} ")
        await asyncio.sleep(1)


def main():
    wlan, ip_addr = anr_wifi.connect_to_wifi()

    print(f"MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}")

    # You will likely need to replace '0.0.0.0' with your device's actual IP address
    # after connecting it to a network.
    # '0.0.0.0' makes the server listen on all available network interfaces.
    ### ANR host = '0.0.0.0'
    host = ip_addr
    port = 8000

    try:
        # Start the event loop and run the main server coroutine
        asyncio.run(main_task(host, port))
    except KeyboardInterrupt:
        print('Server stopped by user KeyboardInterrupt.')
    finally:
        # Clean up the event loop (optional, but good practice)
        asyncio.new_event_loop()

### OLD code
# from AnrHttpServer import AnrHttpServer
# server = AnrHttpServer()
# server.run()

if __name__ == '__main__':
    main()
    
    #TEST_for_making_the_reply()

### end ###

