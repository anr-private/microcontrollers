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
    print(f"@@@37 {webserver_task=}")
    #webserver_task = asyncio.create_task(independent_task("webserver", 7))

    ###sensors_task = asyncio.create_task(independent_task("sensors", 4))
    sensors = MwsSensors()
    sensors_task = sensors.start_the_task()
    print(f"@@@47 {sensors_task=}")
    
    displays = MwsDisplays()
    displays_task = displays.start_the_task()
    print(f"@@@50 {displays_task=}")
    #displays_task = asyncio.create_task(independent_task("displays-update", 5))
    #print(f"@@@@@@@@@@@ {dir(sensors_task)}")
    #['__class__', '__next__', 'cancel', 'coro', 'data', 'done', 'ph_key', 'state']
    
    while 1:
        print(f"MAIN TASK running    {host=}   {port=} ")
        webserver_done = webserver_task.done()
        sensors_done = sensors_task.done()
        displays_done = displays_task.done()

        print(f"  Who is done:  web={webserver_task.done()}  "+\
               f"displays={displays_task.done()}  sensors={sensors_task.done()}")
        #print(f"   state: {sensors_task.state}")  # bool
        #print(f"   data: {sensors_task.data}")    # None
        
        # not impl in micropython
        ###done, pending = await asyncio.wait(tasks, timeout=1)
        ###print(f"MAIN_TASK  done={done}   pending={pending}")

        if webserver_done and sensors_done and displays_done:
            print("MAIN_TASK: all tasks are done!")
            break
        
        await asyncio.sleep(11)
        
    if 0:   # NOT IMPL
        print(f"MAIN webserver result={webserver_task.result()}")
        print(f"MAIN sensors   result={sensors_task.result()}")
        print(f"MAIN displays  result={displays_task.result()}")
    
# def mainOLDSTUFF():
#     lines = ["line 1", "line {RESOURCE} 2", "lin33"]
#     valsdict = {"RESOURCE" : "NOTFOUND!!++"}
#     fmt_lines = []
#     for line in lines:
#         print(f"@@@RB@57  {line=}  {valsdict=}")
#         new_line = line.format(**valsdict)
#         fmt_lines.append(new_line)
#     print(f"{fmt_lines}")
     
def main():
    wlan, ip_addr = mws_wifi.connect_to_wifi()

    mws_wifi.wifi_set_time_from_ntp(wlan)

    date_stg, time_stg = get_formatted_local_time()
    m = f"MAIN  CONNECTED TO WIFI.  local date,time: {date_stg}  {time_stg} "
    print(m)
    log(m)
    m = f"MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}"
    print(m)
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
        m = f"{date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
        print(m)
        log(m)
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

