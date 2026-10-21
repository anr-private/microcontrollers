# maranr_watering_system_main.py
#
# Main startup for MWS

import sys
import platform
import gc

try:
    import time
except ModuleNotFoundError:
    import utime as time          # type: ignore
# THE ABOVE REPLACES THE BELOW CODE: to match other similar import usages
#    and to allow mypy to run
# try:
    # import utime as time        #uPy
# except Exception:
    # # Py3 unit tests
    # import time      # type: ignore 
                

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

    log_control = ElemLogControl.get_instance()

    # Create these early on, in order. Pre-allocate to minimize heap frag.
    # The goal is to call get_instance() just once.  HUH??
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

    if 1:
        log_control.log_and_print_one_line("\n===  MWS_CONFIG PARAMETERS  ========")
        for fig_param in sorted(MWS_CONFIG.keys()):
            fig_value = MWS_CONFIG.get(fig_param)
            m = f" {fig_param:<22}  {fig_value:<60}"
            log_control.log_and_print_one_line(m)
        log_control.log_and_print_one_line("===  end of MWS_CONFIG PARAMETERS  ========\n")


    log_control.dump_registered_loggers()

    mws = MaranrWateringSystem()
    mws.perform_pre_asyncio_setups()
    mws.run_mws()
    

if __name__ == '__main__':
    main()
    
### end ###
