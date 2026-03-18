# MaranrWateringSystem.py

import asyncio
import sys

try:
    import utime as time        #uPy
except Exception:
    import time                 #Py3 unit tests

from logger_elem.ElemLoggerABC import ElemLoggerABC, ElemLogControl
from lib2.DataBoard import DataBoard
from lib2.MwsWifi import MwsWifi
from displays.MwsDisplays import MwsDisplays
from sensors.MwsSensors import MwsSensors
from weblib.MwsWebServer import MwsWebServer


class MaranrWateringSystem(ElemLoggerABC):

    def __init__(self):
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        print(f"MWSMAIN@22 _set_logger: {repr(logger)}")
        print(f"MWSMAIN@23 _set_logger: {str(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def main_task(self):
        print(f"MWSMAIN@31  in main_task");

        # Create this first: most other classes use it immediately
        dataBoard = DataBoard.get_instance()
        print(f"MWSMAIN@36 Created DataBoard. state=...\n{dataBoard.long_string()} ")

        wifi = MwsWifi.get_instance()
        wifi_task = asyncio.create_task(wifi.wifi_task())
        print(f"MWSMAIN@46 wifi task is {wifi_task} ")

        sensors = MwsSensors()
        sensors_task = sensors.start_the_task()
        log(f"MWSMAIN@39 {sensors_task=}")
        
        displays = MwsDisplays()
        displays_task = displays.start_the_task()
        log(f"MWSMAIN@43 {displays_task=}")

        webserver = MwsWebServer() 
        webserver_task = webserver.start_the_task()
        log(f"MWSMAIN@35 {webserver_task=}")
    
        while 1:
            print(f"MWSMAIN@49 MAIN TASK running TopOfLoop   ")
            webserver_done = webserver_task.done()
            sensors_done = sensors_task.done()
            displays_done = displays_task.done()
    
#MAIN@96 FS: TOTAL SPACE 868,352 bytes, 848.00 KB, 0.83 MB   FREE SPACE 507,904 bytes, 496.00 KB, 0.48 MB
#MAIN@97 MEMORY:  gc.mem_alloc()=90240   gc.mem_free()=115328
#MAIN@99 MEMORY AFTER GC:  gc.mem_alloc()=64464   gc.mem_free()=141104


            _=""" #$$$$$
            log(f"  Who is done:  web={webserver_task.done()}  "+\
                   f"displays={displays_task.done()}  sensors={sensors_task.done()}")
            print(f"MWSMAIN@65 FS: {get_fs_space_string()}")
            print(f"MWSMAIN@66 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
            gc.collect()
            print(f"MWSMAIN@68 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

            #log(f"   state: {sensors_task.state}")  # bool
            #log(f"   data: {sensors_task.data}")    # None
            
            # not impl in micropython
            ###done, pending = await asyncio.wait(tasks, timeout=1)
    
            if webserver_done and sensors_done and displays_done:
                log("MWSMAIN@77  MAIN_TASK: all tasks are done!")
                break
            """

            print(f"MWSMAIN@81  MAIN TASK running  SLEEP 3  ")
            await asyncio.sleep(3)


    def run_mws(self):

        logi("--- MaranrWateringSystem --- BEGIN run_mws()  =======================")

        #print(f"MWSMAIN@89 FS: {get_fs_space_string()}")
        #print(f"MWSMAIN@90 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
        #print(f"MWSMAIN@91  +++++ DO GC COLLECT   ++++++++++++++++++")
        #gc.collect()
        #print(f"MWSMAIN@93 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

        ###@@@host,port = self.connect_to_wifi()
        print("MWSMAIN@96  START THE MAIN TASK")
        try:
            # Start the event loop and run the main server coroutine
            #$$$asyncio.run(self.main_task(host, port))
            print("MWSMAIN@100  START THE MAIN TASK")
            asyncio.run(self.main_task())
            print("MWSMAIN@102  START THE MAIN TASK")

        except KeyboardInterrupt:
            #@@@@@@@@
            #date_stg, time_stg = get_formatted_local_time()
            #m = f"MWSMAIN@107 {date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
            #log(m)
            #logi(m)
            print("MWSMAIN@110 interrupt from keyboard")

        finally:
            # Clean up the event loop (optional, but good practice)
            asyncio.new_event_loop()



### end ###
