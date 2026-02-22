# watering_project_main.py
#
# main program for the watering project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import asyncio
import sys
import platform
import utime

from displays.MwsDisplays import MwsDisplays
from sensors.MwsSensors import MwsSensors
from lib import mws_wifi
from utils import *
from http.MwsWebServer import MwsWebServer

log_start()

log("===  WATERING PROJECT -- BEGIN EXECUTION  =======================")


if determine_py_platform() == "micropython":
    sys.path.append("/http")
else:
    sys.path.append("../http")


async def main_task(host, port):

    webserver = MwsWebServer(host, port) 
    webserver_task = webserver.start_the_task()
    dbg(f"MWSMAIN@37 {webserver_task=}")

    sensors = MwsSensors()
    sensors_task = sensors.start_the_task()
    dbg(f"MWSMAIN@47 {sensors_task=}")
    
    displays = MwsDisplays()
    displays_task = displays.start_the_task()
    dbg(f"MWSMAIN@50 {displays_task=}")
    
    while 1:
        dbg(f"MWSMAIN@50  MAIN TASK running    {host=}   {port=} ")
        webserver_done = webserver_task.done()
        sensors_done = sensors_task.done()
        displays_done = displays_task.done()

        dbg(f"  Who is done:  web={webserver_task.done()}  "+\
               f"displays={displays_task.done()}  sensors={sensors_task.done()}")
        #dbg(f"   state: {sensors_task.state}")  # bool
        #dbg(f"   data: {sensors_task.data}")    # None
        
        # not impl in micropython
        ###done, pending = await asyncio.wait(tasks, timeout=1)

        if webserver_done and sensors_done and displays_done:
            dbg("MWSMAIN@65  MAIN_TASK: all tasks are done!")
            break
        
        await asyncio.sleep(11)
        
    if 0:   # NOT IMPL
        dbg(f"MWSMAIN@71 webserver result={webserver_task.result()}")
        dbg(f"MWSMAIN@72 sensors   result={sensors_task.result()}")
        dbg(f"MWSMAIN@73 displays  result={displays_task.result()}")
    

def main():

    wlan, ip_addr = mws_wifi.connect_to_wifi()


    MAX_RETRIES = 10
    num_retries = 0
    while num_retries < MAX_RETRIES:
        ok = mws_wifi.wifi_set_time_from_ntp(wlan)
        if ok:
            m = "MWSMAIN@94  SUCCESSFULLY UPDATED SYSTEM TIME from NTP"
            dbg(m)
            log(m)
            break
        m = "MWSMAIN@94  **ERROR** FAILED TO UPDATE SYSTEM TIME from NTP. {num_retries=}")
        time.sleep(1)

    date_stg, time_stg = get_formatted_local_time()
    m = f"MWSMAIN@88 MAIN  CONNECTED TO WIFI.  local date,time: {date_stg}  {time_stg} "
    dbg(m)
    log(m)
    m = f"MWSMAIN@88 MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}"
    dbg(m)
    log(m)

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
        date_stg, time_stg = get_formatted_local_time()
        m = f"MWSMAIN@107 {date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
        dbg(m)
        log(m)
    finally:
        # Clean up the event loop (optional, but good practice)
        asyncio.new_event_loop()

if __name__ == '__main__':
    main()
    
### end ###

