# maranr_watering_system_main.py
#
# Main startup for MWS

import sys
import platform
import gc

try:
    import utime as time        #uPy
except Exception:
    import time                 #Py3 unit tests

from logger_elem.ElemLoggerABC import ElemLoggerABC, ElemLogControl
from lib2.DataBoard import DataBoard
from lib2.TimeMgr import TimeMgr
from lib2.MwsWifi import MwsWifi
from displays.MwsDisplays import MwsDisplays
from sensors.MwsButtons import MwsButtons
from sensors.MwsSensors import MwsSensors
from weblib.MwsWebServer import MwsWebServer
from utils import MWS_CONFIG
from utils import get_fs_space_string
from utils import get_memory_status_string

from mws.MaranrWateringSystem import MaranrWateringSystem

#if determine_py_platform() == "micropython":
#    sys.path.append("/http")
#else:
#    sys.path.append("../http")


# Logging functions are NOT AVAILABLE: log,logrt,logi. Use log_control.xxx()


def main():
    
    print("MAIN: MARANR Watering System starting...")
    print(f"MAIN@39  {MWS_CONFIG=}")

    # create these early on, in order. Pre-allocate to minimize heap frag.
    log_control = ElemLogControl.get_instance()
    log_control.remove_old_log_file()
    # The goal is to call get_instance() just once.
    # DataBoard is created first - it contains refs to all the other
    # major objects.
    databoard = DataBoard.get_instance()
    databoard.time_mgr = TimeMgr.get_instance()
    databoard.displays = MwsDisplays.get_instance()
    databoard.buttons = MwsButtons.get_instance()
    databoard.sensors = MwsSensors.get_instance()
    databoard.wifi = MwsWifi.get_instance()
    databoard.web_server = MwsWebServer.get_instance()

    log_control.log_and_print_one_line("===  MARANR WATERING SYSTEM  -- MWS -- BEGIN EXECUTION  =======================")

    mws = MaranrWateringSystem()
    mws.perform_pre_asyncio_setups()
    mws.run_mws()
    

if __name__ == '__main__':
    main()
    
### end ###
