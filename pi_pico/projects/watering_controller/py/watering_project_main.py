# watering_project_main.py
#
# main program for the watering project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import asyncio
import sys
import platform

from displays.WspDisplays import WspDisplays
from lib import wsp_wifi
from utils import *
from http.WspWebServer import WspWebServer


if determine_py_platform() == "micropython":
    sys.path.append("/http")
else:
    sys.path.append("../http")


async def independent_task(name, duration):
    print(f"Task {name} started and will run for {duration} seconds independently.")
    await asyncio.sleep(duration)
    print(f"+++  Task {name} finished.   +++")
    return f"this is the result from independent_task {name=}"




async def main_task(host, port):

    webserver = WspWebServer(host, port) 
    webserver_task = webserver.start_the_task()
    print(f"@@@37 {webserver_task=}")
    #webserver_task = asyncio.create_task(independent_task("webserver", 7))

    sensors_task = asyncio.create_task(independent_task("sensors", 4))

    displays = WspDisplays()
    displays_task = displays.start_the_task()
    print(f"@@@44 {displays_task=}")
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
    


def main():
    wlan, ip_addr = wsp_wifi.connect_to_wifi()

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

