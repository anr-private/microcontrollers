# maranr_watering_system_main.py
#


import asyncio
import sys
import platform
import gc

try:
    import utime as time        #uPy
except Exception:
    import time                 #Py3 unit tests

from logger_elem.ElemLoggerABC import ElemLoggerABC, ElemLogControl

#from displays.MwsDisplays import MwsDisplays
#from sensors.MwsSensors import MwsSensors
#from lib2.MwsWifi import MwsWifi
#from weblib.MwsWebServer import MwsWebServer
from utils import MWS_CONFIG
from utils import get_formatted_local_time
from utils import get_fs_space_string
from utils import get_memory_status_string
from utils import get_formatted_local_time

from mws.MaranrWateringSystem import MaranrWateringSystem

#if determine_py_platform() == "micropython":
#    sys.path.append("/http")
#else:
#    sys.path.append("../http")


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None





def main():
    
    print("MAIN: MARANR Watering System starting...")

    print(f"MAIN@48  {MWS_CONFIG=}")

    
    log_control = ElemLogControl.get_instance()
    log_control.remove_old_log_file()

    log_control.log_one_line("===  MARANR WATERING SYSTEM  -- MWS -- BEGIN EXECUTION  =======================")


    mws = MaranrWateringSystem()
    mws.run_mws()
    

if __name__ == '__main__':
    main()
    
### end ###
