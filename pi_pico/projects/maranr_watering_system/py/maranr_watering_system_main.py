# maranr_watering_system_main.py
#
# main program for the MARANR watering system (MWS) project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import asyncio
import sys
import platform

try:
    import utime          #uPy
except Exception:
    import time as utime  # Py3 simulate 'utime' uPy pkg

from logger.LoggerABC import LoggerABC
from displays.MwsDisplays import MwsDisplays
from sensors.MwsSensors import MwsSensors
from lib import mws_wifi
from lib import utils
from lib.utils import loggg
from lib.utils import dbg
###from lib.utils import *
from http.MwsWebServer import MwsWebServer

#if determine_py_platform() == "micropython":
#    sys.path.append("/http")
#else:
#    sys.path.append("../http")

print(f"@@@MAIN@28  {utils.MWS_CONFIG=}")


class MaranrWateringSystem:

    def __init__(self):
        pass


    async def main_task(self, host, port):
    
        webserver = MwsWebServer(host, port) 
        webserver_task = webserver.start_the_task()
        dbg(f"MWSMAIN@34 {webserver_task=}")
    
        sensors = MwsSensors()
        sensors_task = sensors.start_the_task()
        dbg(f"MWSMAIN@38 {sensors_task=}")
        
        displays = MwsDisplays()
        displays_task = displays.start_the_task()
        dbg(f"MWSMAIN@42 {displays_task=}")
        
        while 1:
            dbg(f"MWSMAIN@45  MAIN TASK running    {host=}   {port=} ")
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
                dbg("MWSMAIN@59  MAIN_TASK: all tasks are done!")
                break
            
            await asyncio.sleep(11)
            
        if 0:   # NOT IMPL
            dbg(f"MWSMAIN@65 webserver result={webserver_task.result()}")
            dbg(f"MWSMAIN@66 sensors   result={sensors_task.result()}")
            dbg(f"MWSMAIN@67 displays  result={displays_task.result()}")
        
    
    def connect_to_wifi(self):

        wlan, ip_addr = mws_wifi.connect_to_wifi()
    
    
        MAX_RETRIES = 10
        num_retries = 0
        while num_retries < MAX_RETRIES:
            ok = mws_wifi.wifi_set_time_from_ntp(wlan)
            print(f"@@@@@@@@@ MAIN  set time returnned {ok=}")
            if ok:
                m = "MWSMAIN@81  SUCCESSFULLY UPDATED SYSTEM TIME from NTP"
                dbg(m)
                loggg(m)
                break
            num_retries += 1
            m = "MWSMAIN@86  **ERROR** FAILED TO UPDATE SYSTEM TIME from NTP. {num_retries=}"
            time.sleep(1)
    
        date_stg, time_stg = utils.get_formatted_local_time()
        m = f"MWSMAIN@90 MAIN  CONNECTED TO WIFI.  local date,time: {date_stg}  {time_stg} "
        dbg(m)
        loggg(m)
        m = f"MWSMAIN@93 MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}"
        dbg(m)
        loggg(m)
    
        # You will likely need to replace '0.0.0.0' with your device's actual IP address
        # after connecting it to a network.
        # '0.0.0.0' makes the server listen on all available network interfaces.
        ### ANR host = '0.0.0.0'
        host = ip_addr
        port = 8000
    
        return host,port

    def run_mws(self):

        utils.log_start()

        loggg("===  MARANR WATERING SYSTEM  -- MWS -- BEGIN EXECUTION  =======================")

        host,port = self.connect_to_wifi()

        try:
            # Start the event loop and run the main server coroutine
            asyncio.run(self.main_task(host, port))
        except KeyboardInterrupt:
            date_stg, time_stg = utils.get_formatted_local_time()
            m = f"MWSMAIN@109 {date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
            dbg(m)
            loggg(m)
        finally:
            # Clean up the event loop (optional, but good practice)
            asyncio.new_event_loop()

if __name__ == '__main__':
    mws = MaranrWateringSystem()
    mws.run_mws()

### end ###

