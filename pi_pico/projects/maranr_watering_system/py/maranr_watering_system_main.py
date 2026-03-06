# maranr_watering_system_main.py
#
# main program for the MARANR watering system (MWS) project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import asyncio
import sys
import platform
import gc

try:
    import utime as time        #uPy
except Exception:
    import time                 #Py3 unit tests
import utils  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

from trivlog.TrivlogABC import TrivlogABC

from displays.MwsDisplays import MwsDisplays
from sensors.MwsSensors import MwsSensors
from MwsWifi import MwsWifi
from weblib.MwsWebServer import MwsWebServer
from utils import MWS_CONFIG
from utils import get_formatted_local_time
from utils import get_fs_space_string
from utils import get_memory_status_string

#if determine_py_platform() == "micropython":
#    sys.path.append("/http")
#else:
#    sys.path.append("../http")


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


print(f"@@@MAIN@42  {MWS_CONFIG=}")


class MaranrWateringSystem(TrivlogABC):

    def __init__(self):
        super().__init__()

    @classmethod
    def _get_logger(cls): global log; return log
    @classmethod
    def _get_logger_name(cls): global log_name_; return log_name_
    @classmethod
    def _set_logger(cls, newlog, new_name):
        global log, log_name_; log = newlog; log_name_ = new_name
    @classmethod
    def _set_logger_rt(cls, newlog_rt):
        global logrt; logrt = newlog_rt
    @classmethod
    def _set_logger_important(cls, newlog_important):
        global logi; logi = newlog_important

    def _get_log_functions(self): 
        return (log, logrt, logi)
    def _set_log_functions(self, log_arg, logrt_arg, logi_arg):
        global log, logrt, logi
        print(f"MAIN@68.set_log_functions  {log_arg=}  {log_arg=}  {log_arg=}")
        log = log_arg
        logrt = logrt_arg
        logi = logi_arg


    async def main_task(self, host, port):
    
        webserver = MwsWebServer(host, port) 
        webserver_task = webserver.start_the_task()
        log(f"MWSMAIN@78 {webserver_task=}")
    
        sensors = MwsSensors()
        sensors_task = sensors.start_the_task()
        log(f"MWSMAIN@82 {sensors_task=}")
        
        displays = MwsDisplays()
        displays_task = displays.start_the_task()
        log(f"MWSMAIN@86 {displays_task=}")
        
        while 1:
            log(f"MWSMAIN@89  MAIN TASK running    {host=}   {port=} ")
            webserver_done = webserver_task.done()
            sensors_done = sensors_task.done()
            displays_done = displays_task.done()
    
            log(f"  Who is done:  web={webserver_task.done()}  "+\
                   f"displays={displays_task.done()}  sensors={sensors_task.done()}")
            print(f"MAIN@96 FS: {get_fs_space_string()}")
            print(f"MAIN@97 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
            gc.collect()
            print(f"MAIN@99 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

            #log(f"   state: {sensors_task.state}")  # bool
            #log(f"   data: {sensors_task.data}")    # None
            
            # not impl in micropython
            ###done, pending = await asyncio.wait(tasks, timeout=1)
    
            if webserver_done and sensors_done and displays_done:
                log("MWSMAIN@59  MAIN_TASK: all tasks are done!")
                break
            
            await asyncio.sleep(11)
            
        if 0:   # NOT IMPL
            log(f"MWSMAIN@114 webserver result={webserver_task.result()}")
            log(f"MWSMAIN@115 sensors   result={sensors_task.result()}")
            log(f"MWSMAIN@116 displays  result={displays_task.result()}")
        
    
    def connect_to_wifi(self):

        mws_wifi = MwsWifi.get_instance()

        wlan, ip_addr = mws_wifi.connect_to_wifi()
    
    
        MAX_RETRIES = 10
        num_retries = 0
        while num_retries < MAX_RETRIES:
            ok = mws_wifi.wifi_set_time_from_ntp(wlan)
            print(f"@@@@@@@@@ MAIN@130  set time returnned {ok=}")
            if ok:
                m = "MWSMAIN@132  SUCCESSFULLY UPDATED SYSTEM TIME from NTP"
                log(m)
                logi(m)
                break
            num_retries += 1
            m = "MWSMAIN@86  **ERROR** FAILED TO UPDATE SYSTEM TIME from NTP. {num_retries=}"
            time.sleep(1)
    
        date_stg, time_stg = get_formatted_local_time()
        m = f"MWSMAIN@141 MAIN  CONNECTED TO WIFI.  local date,time: {date_stg}  {time_stg} "
        log(m)
        logi(m)
        m = f"MWSMAIN@144 MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}"
        log(m)
        logi(m)
    
        # You will likely need to replace '0.0.0.0' with your device's actual IP address
        # after connecting it to a network.
        # '0.0.0.0' makes the server listen on all available network interfaces.
        ### ANR host = '0.0.0.0'
        host = ip_addr
        port = 8000
    
        return host,port

    def run_mws(self):

        #@@@@@_log_start()

        logi("===  MARANR WATERING SYSTEM  -- MWS -- BEGIN EXECUTION  =======================")

        print(f"MAIN@163 FS: {get_fs_space_string()}")
        print(f"MAIN@164 MEMORY: {get_memory_status_string(do_garbage_collect=False)}")
        print(f"MAIN@165  +++++ DO GC COLLECT   ++++++++++++++++++")
        gc.collect()
        print(f"MAIN@167 MEMORY AFTER GC: {get_memory_status_string(do_garbage_collect=False)}")

        host,port = self.connect_to_wifi()

        try:
            # Start the event loop and run the main server coroutine
            asyncio.run(self.main_task(host, port))
        except KeyboardInterrupt:
            date_stg, time_stg = utils.get_formatted_local_time()
            m = f"MWSMAIN@176 {date_stg} {time_stg}  Server stopped by user KeyboardInterrupt."
            log(m)
            logi(m)
        finally:
            # Clean up the event loop (optional, but good practice)
            asyncio.new_event_loop()


#@@@@@@@@@@@@@@@ REMOVE - move to logging
#def _log_start():
#    try:
#        os.remove(LOG_FNAME)
#    except Exception as ex:
#        print(f"log_start no log file exists {LOG_FNAME=}")




if __name__ == '__main__':
    mws = MaranrWateringSystem()
    mws.run_mws()

### end ###

