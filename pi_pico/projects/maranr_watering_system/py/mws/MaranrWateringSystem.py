# MaranrWateringSystem.py

import asyncio
import machine  # probably not needed
import sys

try:
    import utime as time        #uPy
except Exception:
    import time                 #Py3 unit tests

from logger_elem.ElemLoggerABC import ElemLoggerABC, ElemLogControl
from lib2.DataBoard import DataBoard
from lib2.MwsWifi import MwsWifi
from lib2.TimeMgr import TimeMgr
from displays.MwsDisplays import MwsDisplays
from sensors.MwsSensors import MwsSensors
from weblib.MwsWebServer import MwsWebServer
from utils import determine_machine_type
from utils import get_fs_space_string
from utils import get_memory_status_string


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class MaranrWateringSystem(ElemLoggerABC):

    def __init__(self):
        self._onboard_led = None
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi

    def perform_pre_asyncio_setups(self):
        # Perform any setups that must be done before we start the
        # main_task. These are typically setups that require
        # relatively long time periods to get completed.
        
        displays = MwsDisplays()
        ok = displays.locate_the_lcd()
        if not ok:
            m = "MWSMAIN@50 FAILED TO LOCATE THE LCD."
            logi(m)
            print(m)


    async def main_task(self):
        logi(f"MWSMAIN@40  MAIN TASK STARTED {TimeMgr.get_formatted_date_time_string()}");

        # Create this first: most other classes use it immediately
        dataBoard = DataBoard.get_instance()
        logi(f"MWSMAIN@44 Created DataBoard. state=...\n{dataBoard.long_string()} ")

        self._onboard_led = self._get_onboard_led()
        self._toggle_onboad_led()


        wifi = MwsWifi.get_instance()
        wifi_task = asyncio.create_task(wifi.wifi_task())
        logi(f"MWSMAIN@52 wifi task is {wifi_task} ")

        sensors = MwsSensors()
        sensors_task = sensors.start_the_task()
        logi(f"MWSMAIN@56 {sensors_task=}")
        
        displays = MwsDisplays()
        displays_task = displays.start_the_task()
        logi(f"MWSMAIN@60 {displays_task=}")

        webserver = MwsWebServer() 
        webserver_task = webserver.start_the_task()
        logi(f"MWSMAIN@64 {webserver_task=}")
    
        sleep_secs = 3
        logging_ctr = 999
        logging_ctr_limit = 60 / sleep_secs  # log the time every 60 seconds
        while 1:
            log(f"MWSMAIN@67 MAIN TASK running TopOfLoop   ")

            logging_ctr += 1
            if logging_ctr >= logging_ctr_limit:
                logging_ctr = 0
                fss = get_fs_space_string()
                logi(f"{TimeMgr.get_formatted_date_time_string()} =_=_=_==_=_=_==_=_=_==_=_=_==_=_=_==_=_=_==_=_=_=  {fss}")
            ####logi(f"{TimeMgr.get_formatted_date_time_string()} @@@@@@@@@@@@@@@@@@@@@@@@@@@=_=_=_==_=_=_==_=_=_==_=_=_==_=_=_==_=_=_==_=_=_=")

            webserver_done = webserver_task.done()
            sensors_done = sensors_task.done()
            displays_done = displays_task.done()
    
#MAIN@96 FS: TOTAL SPACE 868,352 bytes, 848.00 KB, 0.83 MB   FREE SPACE 507,904 bytes, 496.00 KB, 0.48 MB
#MAIN@97 MEMORY:  gc.mem_alloc()=90240   gc.mem_free()=115328
#MAIN@99 MEMORY AFTER GC:  gc.mem_alloc()=64464   gc.mem_free()=141104


            _=""" #$$$$$ TODO finish this
            log(f"  Who is done:  web={webserver_task.done()}  "+\
                   f"displays={displays_task.done()}  sensors={sensors_task.done()}")
            pr int(f"MWSMAIN@80 FS: {get_fs_space_string()}")
            pr int(f"MWSMAIN@81 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
            gc.collect()
            pr int(f"MWSMAIN@83 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

            #log(f"   state: {sensors_task.state}")  # bool
            #log(f"   data: {sensors_task.data}")    # None
            
            # not impl in micropython
            ###done, pending = await asyncio.wait(tasks, timeout=1)
    
            if webserver_done and sensors_done and displays_done:
                log("MWSMAIN@92  MAIN_TASK: all tasks are done!")
                break
            """

            log(f"MWSMAIN@96  MAIN TASK running  SLEEP 3  ")
            await asyncio.sleep(sleep_secs)
            self._toggle_onboad_led()


    def run_mws(self):

        logi("--- MaranrWateringSystem --- BEGIN run_mws()  =======================")

        #pr int(f"MWSMAIN@105 FS: {get_fs_space_string()}")
        #pr int(f"MWSMAIN@106 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
        #pr int(f"MWSMAIN@107  +++++ DO GC COLLECT   ++++++++++++++++++")
        #gc.collect()
        #pr int(f"MWSMAIN@109 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

        ###@@@host,port = self.connect_to_wifi()
        logi("MWSMAIN@112  START THE MAIN TASK")
        try:
            # Start the event loop and run the main server coroutine
            asyncio.run(self.main_task())

        except KeyboardInterrupt:
            #@@@@@@@@ TODO Handle keyboard in MWS main
            #date_stg, time_stg = get_formatted_local_time()
            #m = f"MWSMAIN@120 {date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
            #logi(m)
            print("MWSMAIN@122 interrupt from keyboard")

        finally:
            # Clean up the event loop (optional, but good practice)
            asyncio.new_event_loop()

    def _toggle_onboad_led(self):
        if self._onboard_led is not None:
            self._onboard_led.toggle()

    def _get_onboard_led(self):
        this_machine = determine_machine_type()

        if this_machine in ["pi pico w", "pi pico 2 w"]:
            # 'EXT_GPIO0'  GPIO zero on the wifi chip (not the Pico)
            led = machine.Pin("LED", machine.Pin.OUT)
        else:
            logi(f"**ERROR**  unknown machine '{this_machine}'")
            led = machine.Pin(25, machine.Pin.OUT)
        return led

### end ###
