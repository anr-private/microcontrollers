# MwsDisplays.py

import asyncio
try:
    import utime as time
except Exception:
    import time
from machine import Pin, SoftI2C

###@@@from lib import *
#from lib import utils
#from lib.utils import loggg
from lib.utils import MWS_CONFIG
from logger_elem.ElemLoggerABC import ElemLoggerABC

from displays.lib_lcd1602_2004_with_i2c import LCD

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

# Works with 2 line and 4 line by 16 chars LCDs
NUM_ROWS = 2
#NUM_ROWS = 4


class MwsDisplays(ElemLoggerABC):
    # top-level Server class
    def __init__(self):
        super().__init__()

        self.lcd1602_sda_pin = MWS_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = MWS_CONFIG.get("lcd1602_scl_pin")
        self.lcd = None


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsDisplays@40 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("WD.startup!")

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        self.locate_the_lcd()

        ctr = 1
        while 1:
            if self.lcd:
                self.just_show_some_hello_lines(ctr)
                ...
            else:
                print(f"WD.displays_coro RUNNING idle  COULD NOT FIND LCD!")

            await asyncio.sleep(5)
            ctr += 1

        ###result = "NO RESULT YET from displays_coro"
        ###print(f"MwsDisplays.displays_coro COMPLETED.  {result=}")
        ###return result

    def locate_the_lcd(self):
        print(f"WD.locate_the_lcd: try to locate the LCD device...")
         # SoftI2C is software I2C - works on ANY GPIO pins(!)
         # 100K is default freq.  Can go higher ex 400K
        self.lcd = LCD(SoftI2C(scl=Pin(self.lcd1602_scl_pin), sda=Pin(self.lcd1602_sda_pin), freq=100000))
        
        if self.lcd:
            print(f"WD.locate_the_lcd: located the LCD device...")
        else:
            print(f"WD.locate_the_lcd **ERROR**  failed to locate the LCD device!")
    
    
    def just_show_some_hello_lines(self, ctr):
        if self.lcd is None: return
        line1 = "The Display LCD!"
        line2 = f"ctr={ctr}      "
        self.lcd.puts(line1, x=0,y=0)
        self.lcd.puts(line2, x=0,y=1)


###
