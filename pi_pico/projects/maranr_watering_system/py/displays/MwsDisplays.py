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
from lib2.DataBoard import DataBoard

from displays.lib_lcd1602_2004_with_i2c import LCD

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

# Works with 2 line and 4 line by 16 chars LCDs
NUM_ROWS = 2
#NUM_ROWS = 4


class MwsDisplays(ElemLoggerABC):
    def __init__(self):
        self._dataBoard = DataBoard.get_instance()
        self.lcd1602_sda_pin = MWS_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = MWS_CONFIG.get("lcd1602_scl_pin")
        self.lcd = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsDisplays@40 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def locate_the_lcd(self):
        # This can take several seconds and it ties up the
        # thread.
        # So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@49 locate_the_lcd: try to locate the LCD device...")
         # SoftI2C is software I2C - works on ANY GPIO pins(!)
         # 100K is default freq.  Can go higher ex 400K
         # The LCD() ctor can take several seconds to decide if it has
         # found the LCD.
        i2c_driver = SoftI2C(scl=Pin(self.lcd1602_scl_pin), 
                             sda=Pin(self.lcd1602_sda_pin), 
                             freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@94 locate_the_lcd: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@96 locate_the_lcd **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("MwsDisplays@48 start_the_task!")

        if not self.lcd:
            m = "MwsDisplays@69 No LCD available - no attempt to send data to the LCD will occur."
            logi(m)
            print(m)

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        if self.lcd is None:
            m = f"MwsDisplays@80  DID NOT FIND THE lcd!"
            logi(m)
            print(m)
        elif not not self.lcd.ok:
            self.lcd = None # disable
            m = f"MwsDisplays@58  LCD is not OK!"
            logi(m)
            print(m)
            #m = f"MwsDisplays@58  STOPPING THE displays TASK!!!!!!!!!!!!!!!!!!!!!!!"
            #logi(m)
            #print(m)

        ctr = 1
        while 1:
            if self.lcd:
                self._just_show_some_hello_lines(ctr)
                ...
            else:
                m = f"MwsDisplays@64 TEMP: RUNNING idle! COULD NOT FIND LCD!  {ctr=}"
                logi(m)
                print(m)
                await asyncio.sleep(120) # slow the logging rate
            await asyncio.sleep(5)
            ctr += 1

        ###result = "NO RESULT YET from displays_coro"
        ###print(f"MwsDisplays.displays_coro COMPLETED.  {result=}")
        ###return result

    def _just_show_some_hello_lines(self, ctr):
        print(f"MwsDisplays@100 SHOW HELLO LINES  self.lcd: {self.lcd}")

        if self.lcd is None: return

        #line1 = "LINE 1 is BAD@@@!!!"
        #try:
        #    line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"
        #    print(f"@@@@@@@@@106  LINE1 is {line1}")
        #except Exception as ex:
        #    print(f"@@@@@@@@@@@@@@@@@@@ MwsDisplays@107  EX  {repr(ex)}  {str(ex)}  {ex}")
        #
        ###@@@@@@@@@@@@@@@@@@@@@line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"

        line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"
        line2 = f"ctr={ctr}      "
        self.lcd.puts(line1, x=0,y=0)
        self.lcd.puts(line2, x=0,y=1)


###
