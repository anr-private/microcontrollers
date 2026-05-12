# MwsDisplays.py

import asyncio
import gc
try:
    import utime as time
except Exception:
    import time
from machine import Pin
from machine import I2C    # hardware driver
###from machine import SoftI2C # software driver

from utils import MWS_CONFIG
from utils import seconds_to_hhmmss_string
from utils import get_flash_space
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

    LCD_ACTIVE_DISPLAY_MAX = 8 #@@@@@@@@@@@@@@@@ UPDATE?


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
        self._databoard = DataBoard.get_instance()

        # LCD 1602                           
        self.lcd1602_sda_pin = MWS_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = MWS_CONFIG.get("lcd1602_scl_pin")
        self.lcd = None
        self._lcd_active_display = 0
        # timer to control updating rates for displays
        # _timer_ticks is the current 'elapsed time in ticks'
        # _lcd_next_update_tick is the tick (some future time) at which
        #   we will update the LCD.
        #   This gets updated/advanced every so many seconds, but may
        #   get 'pushed back' to the current tick if the LCD should
        #   be updated ASAP (such as when the display is changed).
        # Currently: 1 sec is 4 ticks
        self._timer_ticks = 0
        self._lcd_next_update_tick = 0

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
        #print(f"MwsDisplays@87 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi                 


    def _locate_lcd_soft_i2c(self):
        # Find the LCD. Use software-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@97 _locate_lcd_soft_i2c: try to locate the LCD device...")
         # SoftI2C is software I2C - works on ANY GPIO pins(!)
         # 100K is default freq.  Can go higher ex 400K
         # The LCD() ctor can take several seconds to decide if it has
         # found the LCD.
        i2c_driver = SoftI2C(scl=Pin(self.lcd1602_scl_pin), 
                             sda=Pin(self.lcd1602_sda_pin), 
                             freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@108 _locate_lcd_soft_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@111 _locate_lcd_soft_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    def _locate_lcd_hw_i2c(self):
        # Find the LCD. Use hardware-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@118 _locate_lcd_hw_i2c: try to locate the LCD device...")
        i2c_driver = I2C(1,
                         scl=Pin(self.lcd1602_scl_pin), 
                         sda=Pin(self.lcd1602_sda_pin), 
                         freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@126 _locate_lcd_hw_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@129 _locate_lcd_hw_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    def get_lcd_active_display(self):
        return self._lcd_active_display

    def set_lcd_active_display(self,v):
        # v is an int 0..n
        if not isinstance(v, int):
            logi("MwsDisplays@138 set_active_lcd_display BAD VALUE: {v}  type={type(v)}")
            v = 0

        # Roll over if request is too big or too small
        if v < 0 :
            logi("MwsDisplays@142 set_active_lcd_display TOO SMALL: {v}  type={type(v)}")
            v = self.LCD_ACTIVE_DISPLAY_MAX
        elif v > self.LCD_ACTIVE_DISPLAY_MAX:
            logi("MwsDisplays@142 set_active_lcd_display TOO LARGE: {v}  type={type(v)}")
            v = 0

        print(f"MwsDisplays@145 set_lcd_active_display SET LCD ACTIVE DISPLAY to {v}.  Was {self._lcd_active_display}")
        self._lcd_active_display = v
        print(f"MwsDisplays@147 set_lcd_active_display FORCE LCD UPDATE.  prev_tick_upd={self._lcd_next_update_tick}")
        self._lcd_next_update_tick = 1  # 'many ticks in the past'


    # Which to use? Hardware or Soft I2C?
    ####locate_the_lcd = _locate_lcd_soft_i2c
    locate_the_lcd = _locate_lcd_hw_i2c

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("MwsDisplays@157 start_the_task!")

        if not self.lcd:
            m = "MwsDisplays@160 No LCD available - no attempt to send data to the LCD will occur."
            logi(m)
            print(m)

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        if self.lcd is None:
            m = f"MwsDisplays@171  DID NOT FIND THE lcd!"
            logi(m)
            print(m)
        elif not self.lcd.ok:
            self.lcd = None # disable
            m = f"MwsDisplays@176  LCD is not OK! DISABLED the LCD"
            logi(m)
            print(m)
            #m = f"MwsDisplays@179  STOPPING THE displays TASK!!!!!!!!!!!!!!!!!!!!!!!"
            #logi(m)
            #print(m)

        led_idx = 0
        elapsed_secs = 0
        ###self._timer_ticks = 0
        while 1:
            # Handle the LCD update
            if self._timer_ticks >= self._lcd_next_update_tick:
                if self.lcd is not None:
                    self._lcd_next_update_tick = self._timer_ticks + (5 <<2) #  5 secs (20 ticks)
                    self._update_lcd(elapsed_secs)
                else:
                    # LCD is disabled. (slow the logging rate)
                    self._lcd_next_update_tick += (5*60) <<1 #  5 mins
                    m = f"MwsDisplays@195  RUNNING idle! COULD NOT FIND LCD!  {elapsed_secs=}"
                    logi(m)
                    print(m)

            led_idx = self._update_leds(led_idx)

            # tick the time
            await asyncio.sleep(0.25)
            self._timer_ticks += 1
            elapsed_secs = self._timer_ticks >>2


    def _update_leds(self, led_idx):
        self.leds[led_idx].value(0)
        led_idx += 1
        if led_idx >= len(self.leds): led_idx = 0
        self.leds[led_idx].value(1)
        return led_idx


    def _update_lcd(self, elapsed_secs):
        ###print(f"MwsDisplays@216 UPDATE LCD LINES  {elapsed_secs=} {self._lcd_active_display=} ")

        #line1 = "LINE 1 is BAD@@@!!!"
        #try:
        #    line1 = f"{self._databoard.ipaddr}:{self._databoard.port}"
        #    print(f"@@@@@@@@@106  LINE1 is {line1}")
        #except Exception as ex:
        #    print(f"@@@@@@@@@@@@@@@@@@@ MwsDisplays@223  EX  {repr(ex)}  {str(ex)}  {ex}")
        #
        ###@@@@@@@@@@@@@@@@@@@@@line1 = f"{self._databoard.ipaddr}:{self._databoard.port}"

        if self._lcd_active_display == 0:
            # 123456789.123456
            hhmmss = seconds_to_hhmmss_string(elapsed_secs)
            line1 = f"{self._databoard.ipaddr}:{self._databoard.port}"
            line2 = f"{hhmmss}"
            ###self.lcd.puts(line1, x=0,y=0)
            ###self.lcd.puts(line2, x=0,y=1)

        elif self._lcd_active_display == 1:
            line1 = f"{self._databoard.time_mgr.get_formatted_local_YYYYMMDD()}"
            line2 = f"{self._databoard.time_mgr.get_formatted_local_HHMMSS()}"


        elif self._lcd_active_display == 2:
            # NTP Latest update:
            line1 = f"{self._databoard.time_mgr_latest_ntp_update_secs} secs"
            line2 = f"{self._databoard.time_mgr_number_of_ntp_updates} NTP update"

        elif self._lcd_active_display == 3:
            # Temp-F
            degs_f = self._databoard.internal_temp_f
            min_degs_f = self._databoard.internal_min_temp_f
            max_degs_f = self._databoard.internal_max_temp_f
            #         123456789.123456
            #         Pico temp 123.1F"
            line1 = f"Pico temp {degs_f:.1f}F"
            line2 = f"{min_degs_f:.1f} {max_degs_f:.1f} MinMx"

        elif self._lcd_active_display == 4:
            # Temp-C
            degs_c = self._databoard.internal_temp_c
            min_degs_c = self._databoard.internal_min_temp_c
            max_degs_c = self._databoard.internal_max_temp_c
            #         123456789.123456
            #         Pico temp 123.1C"
            line1 = f"Pico temp {degs_c:.1f}C"
            line2 = f"{min_degs_c:.1f} {max_degs_c:.1f} MinMx"

        elif self._lcd_active_display == 5:
            # memory
            mem_free = self._databoard.memory_free
            mem_alloc = self._databoard.memory_alloc
            line1 = f"{mem_free} FreeMem"
            line2 = f"{mem_alloc} AllocMem"

        elif self._lcd_active_display == 6:
            # memory free
            mem_free = self._databoard.memory_free
            mem_free_min = self._databoard.memory_free_min
            mem_free_max = self._databoard.memory_free_max
            line1 = f"{mem_free} FreeMinMx"
            line2 = f"{mem_free_min} {mem_free_max}"

        elif self._lcd_active_display == 7:
            # memory alloc
            mem_alloc = self._databoard.memory_alloc
            mem_alloc_min = self._databoard.memory_alloc_min
            mem_alloc_max = self._databoard.memory_alloc_max
            line1 = f"{mem_alloc} AllocMnMx"
            line2 = f"{mem_alloc_min} {mem_alloc_max}"

        elif self._lcd_active_display == 8:
            # file space
            total_space, free_space = get_flash_space()
            line1 = f"{free_space} FreeFS"
            line2 = f"{total_space} TotalFS"

        else:
            d = self._lcd_active_display
            line1 = f"ACTIVE DISP {d}"
            line2 = f"ACTIVE DISP={d}"
            ###self.lcd.puts(f"ACTIVE DISPLAY {d}", y=0)
            ###self.lcd.puts(f"ACTIVE DISPLAY={d}", y=1)
        s1 = f"{line1:<16}"
        s2 = f"{line2:<16}"
        self.lcd.puts(s1, y=0)
        self.lcd.puts(s2, y=1)

###
