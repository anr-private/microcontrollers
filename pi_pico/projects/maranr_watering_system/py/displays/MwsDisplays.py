# MwsDisplays.py

import asyncio
try:
    import utime as time
except Exception:
    import time
from machine import Pin
from machine import I2C    # hardware driver
###from machine import SoftI2C # software driver

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

VALIDATE = 857395


class MwsDisplays(ElemLoggerABC):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = MwsDisplays(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        MwsDisplays._instance = None


    def __init__(self,validate):
        if validate != VALIDATE:
            raise RuntimeError(f"MwsDisplays CTOR is private!")
        self._dataBoard = DataBoard.get_instance()
        # LCD 1602                           
        self.lcd1602_sda_pin = MWS_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = MWS_CONFIG.get("lcd1602_scl_pin")
        self.lcd = None
        # LEDs
        self.led_red1   = Pin( 6, Pin.OUT)
        self.led_green1 = Pin( 7, Pin.OUT)
        self.led_white1 = Pin( 8, Pin.OUT)
        self.led_red2   = Pin( 9, Pin.OUT)
        self.led_green2 = Pin(10, Pin.OUT)
        self.led_white2 = Pin(11, Pin.OUT)
        self.leds = (
            self.led_red1, self.led_green1, self.led_white1,
            self.led_red2, self.led_green2, self.led_white2) 

        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsDisplays@73 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi                 


    def _locate_lcd_soft_i2c(self):
        # Find the LCD. Use software-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@83 _locate_lcd_soft_i2c: try to locate the LCD device...")
         # SoftI2C is software I2C - works on ANY GPIO pins(!)
         # 100K is default freq.  Can go higher ex 400K
         # The LCD() ctor can take several seconds to decide if it has
         # found the LCD.
        i2c_driver = SoftI2C(scl=Pin(self.lcd1602_scl_pin), 
                             sda=Pin(self.lcd1602_sda_pin), 
                             freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@94 _locate_lcd_soft_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@97 _locate_lcd_soft_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    def _locate_lcd_hw_i2c(self):
        # Find the LCD. Use hardware-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@104 _locate_lcd_hw_i2c: try to locate the LCD device...")
        i2c_driver = I2C(1,
                         scl=Pin(self.lcd1602_scl_pin), 
                         sda=Pin(self.lcd1602_sda_pin), 
                         freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@112 _locate_lcd_hw_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@115 _locate_lcd_hw_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    # Which to use? Hardware or Soft I2C?
    ####locate_the_lcd = _locate_lcd_soft_i2c
    locate_the_lcd = _locate_lcd_hw_i2c

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("MwsDisplays@124 start_the_task!")

        if not self.lcd:
            m = "MwsDisplays@127 No LCD available - no attempt to send data to the LCD will occur."
            logi(m)
            print(m)

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        if self.lcd is None:
            m = f"MwsDisplays@138  DID NOT FIND THE lcd!"
            logi(m)
            print(m)
        elif not self.lcd.ok:
            self.lcd = None # disable
            m = f"MwsDisplays@143  LCD is not OK!"
            logi(m)
            print(m)
            #m = f"MwsDisplays@146  STOPPING THE displays TASK!!!!!!!!!!!!!!!!!!!!!!!"
            #logi(m)
            #print(m)

        lcd_secs_next = 0
        led_idx = 0
        secs = 0
        while 1:
            lcd_secs_next = self._update_lcd(secs, lcd_secs_next)

            # if secs >= lcd_secs_next:
                # lcd_secs_next += 5  # every 5 secs
                # 
                # if self.lcd:
                    # self._just_show_some_hello_lines(secs)
                    # ...
                # else:
                    # m = f"MwsDisplays@163 TEMP: RUNNING idle! COULD NOT FIND LCD!  {secs=}"
                    # logi(m)
                    # print(m)
                    # ###await asyncio.sleep(120) # slow the logging rate

            led_idx = self._update_leds(led_idx)

            # self.leds[led_idx].value(0)
            # led_idx =+ 1
            # if led_idx >= len(self.leds): led_idx = 0
            # self.leds[led_idx].value(1)

            await asyncio.sleep(1)
            secs += 1

    def _update_lcd(self, secs, lcd_secs_next):
            if self.lcd:
                if secs < lcd_secs_next:
                    return lcd_secs_next
                lcd_secs_next += 5  # every 5 secs

                self._just_show_some_hello_lines(secs)
                ...
                return lcd_secs_next
            else:
                m = f"MwsDisplays@188 TEMP: RUNNING idle! COULD NOT FIND LCD!  {secs=}"
                logi(m)
                print(m)
                ###await asyncio.sleep(120) # slow the logging rate

    def _update_leds(self, led_idx):
        self.leds[led_idx].value(0)
        led_idx += 1
        if led_idx >= len(self.leds): led_idx = 0
        self.leds[led_idx].value(1)
        return led_idx






        ###result = "NO RESULT YET from displays_coro"
        ###print(f"MwsDisplays.displays_coro COMPLETED.  {result=}")
        ###return result

    def _just_show_some_hello_lines(self, secs):
        print(f"MwsDisplays@210 SHOW HELLO LINES  self.lcd: {self.lcd}")

        if self.lcd is None: return

        #line1 = "LINE 1 is BAD@@@!!!"
        #try:
        #    line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"
        #    print(f"@@@@@@@@@106  LINE1 is {line1}")
        #except Exception as ex:
        #    print(f"@@@@@@@@@@@@@@@@@@@ MwsDisplays@219  EX  {repr(ex)}  {str(ex)}  {ex}")
        #
        ###@@@@@@@@@@@@@@@@@@@@@line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"

        line1 = f"{self._dataBoard.ipaddr}:{self._dataBoard.port}"
        line2 = f"secs={secs}      "
        self.lcd.puts(line1, x=0,y=0)
        self.lcd.puts(line2, x=0,y=1)


###
