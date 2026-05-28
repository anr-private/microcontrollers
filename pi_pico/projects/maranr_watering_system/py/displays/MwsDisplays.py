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
from logger_elem.ElemLogControl import ElemLogControl
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

# biggest row index 0..(rows-1)
LCD_MENU_ROW_MAX = 6

# max col number 0..N-1
LCD_MENU_COL_MAX = {
    0: 3,   # network
    1: 1,   # date time
    2: 1,   # NTP status
    3: 2,   # Pico board temperature
    4: 3,   # memory
    5: 1,   # filesys 
    6: 4,   # logs info
    7: 1,   #
    8: 1,   #
    9: 1,   # 
}

# non-menu display
LCD_ACTIVE_DISPLAY_MAX = 9 #@@@@@@@@@@@@@@@@ UPDATE?

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
        self._databoard = DataBoard.get_instance()

        # LCD 1602                           
        self.lcd1602_sda_pin = MWS_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = MWS_CONFIG.get("lcd1602_scl_pin")
        self.lcd = None
        # display (when menu is not active)
        self._lcd_active_display = 0
        # menu
        self._menu_active = False
        self._menu_row = 0
        self._menu_col = 0

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
        #print(f"MwsDisplays@113 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi                 


    def _locate_lcd_soft_i2c(self):
        # Find the LCD. Use software-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@123 _locate_lcd_soft_i2c: try to locate the LCD device...")
         # SoftI2C is software I2C - works on ANY GPIO pins(!)
         # 100K is default freq.  Can go higher ex 400K
         # The LCD() ctor can take several seconds to decide if it has
         # found the LCD.
        i2c_driver = SoftI2C(scl=Pin(self.lcd1602_scl_pin), 
                             sda=Pin(self.lcd1602_sda_pin), 
                             freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@134 _locate_lcd_soft_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@137 _locate_lcd_soft_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None

    def _locate_lcd_hw_i2c(self):
        # Find the LCD. Use hardware-based I2C.
        # This can take several seconds and it ties up the
        # thread. So it is done before we start the asyncio event loop.
        print(f"MwsDisplays@144 _locate_lcd_hw_i2c: try to locate the LCD device...")
        i2c_driver = I2C(1,
                         scl=Pin(self.lcd1602_scl_pin), 
                         sda=Pin(self.lcd1602_sda_pin), 
                         freq=100000)
        self.lcd = LCD(i2c_driver, logi)
        
        if self.lcd.ok:
            print(f"MwsDisplays@152 _locate_lcd_hw_i2c: located the LCD device...")
        else:
            self.lcd = None
            print(f"MwsDisplays@155 _locate_lcd_hw_i2c **ERROR**  failed to locate the LCD device!")
        return self.lcd is not None


    def notify_btn_short_press(self, btn_name):
        # button was pressed - short press
        print(f"MwsDisplays@161 BTN SHORT: {btn_name}")
        if self._menu_active:
            if btn_name == "Down":
                new_row = self._menu_row + 1
                self._set_lcd_menu_row(new_row)
            elif btn_name == "Up":
                new_row = self._menu_row - 1
                self._set_lcd_menu_row(new_row)
            elif btn_name == "Left":
                new_col = self._menu_col - 1
                self._set_lcd_menu_col(new_col)
            elif btn_name == "Right":
                new_col = self._menu_col + 1
                self._set_lcd_menu_col(new_col)
            elif btn_name == "Center":
                self._update_menu_state(False)

        else: # menu not active
            if btn_name == "Down":
                v = self._lcd_active_display + 1
                self._set_lcd_active_display(v)
            elif btn_name == "Up":
                v = self._lcd_active_display - 1
                self._set_lcd_active_display(v)
            elif btn_name == "Center":
                self._update_menu_state(True)


    def notify_btn_long_press(self, btn_name):
        # button was pressed - long press
        print(f"MwsDisplays@191 BTN LONG: {btn_name}")
        if btn_name == "Center":
            if self._menu_active:
                self._menu_row = 0
                self._menu_col = 0
            else:
                pass # nothing in no-menu mode yet
            print(f"MwsDisplays@198 notify_btn_long_press FORCE LCD UPDATE.  prev_tick_upd={self._lcd_next_update_tick}")
            self._force_lcd_update()  # 'many ticks in the past'

    def notify_btn_double_press(self, btn_name):
        # button was pressed - double press
        print(f"MwsDisplays@203 BTN DOUBLE: {btn_name}")


    def _update_menu_state(self, active):
       if active:
           print(f"MwsDisplays@208 ACTIVATE MENU")
           self._menu_active = True
           ###self._menu_row = 0
           ###self._menu_col = 0
       else:
           print(f"MwsDisplays@213 DEACTIVATE MENU")
           self._menu_active = False
       self._force_lcd_update()


    def _set_lcd_menu_row(self, new_row):
        if new_row < 0:
            new_row = LCD_MENU_ROW_MAX
        elif new_row > LCD_MENU_ROW_MAX:
            new_row = 0
        print(f"MwsDisplays@223 _set_lcd_menu_row SET MENU ROW to {new_row}.  Was {self._menu_row}")
        self._menu_row = new_row
        print(f"MwsDisplays@225 _set_lcd_menu_row FORCE LCD UPDATE.  prev_tick_upd={self._lcd_next_update_tick}")
        self._force_lcd_update()  # 'many ticks in the past'
        

    def _set_lcd_menu_col(self, new_col):
        max_col = LCD_MENU_COL_MAX.get(self._menu_row, 1)
        print(f"MwsDisplays@231  row={self._menu_row}  {max_col=}")
        if new_col < 0:
            new_col = max_col
        elif new_col > max_col:
            new_col = 0
        print(f"MwsDisplays@236 _set_lcd_menu_col SET MENU COL to {new_col}.  Was {self._menu_col}")
        self._menu_col = new_col
        print(f"MwsDisplays@238 _set_lcd_menu_col FORCE LCD UPDATE. ")
        self._force_lcd_update()  # 'many ticks in the past'
        


    def _set_lcd_active_display(self,v):
        # Roll over if request is too big or too small
        if v < 0 :
            logi(f"MwsDisplays@246 set_active_lcd_display TOO SMALL: {v}  type={type(v)}")
            v = LCD_ACTIVE_DISPLAY_MAX
        elif v > LCD_ACTIVE_DISPLAY_MAX:
            logi(f"MwsDisplays@249 set_active_lcd_display TOO LARGE: {v}  type={type(v)}")
            v = 0
        print(f"MwsDisplays@251 set_lcd_active_display SET LCD ACTIVE DISPLAY to {v}.  Was {self._lcd_active_display}")
        self._lcd_active_display = v
        print(f"MwsDisplays@253 set_lcd_active_display FORCE LCD UPDATE.  prev_tick_upd={self._lcd_next_update_tick}")
        self._force_lcd_update()  # 'many ticks in the past'


    # Which to use? Hardware or Soft I2C?
    ####locate_the_lcd = _locate_lcd_soft_i2c
    locate_the_lcd = _locate_lcd_hw_i2c

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("MwsDisplays@263 start_the_task!")

        if not self.lcd:
            m = "MwsDisplays@266 No LCD available - no attempt to send data to the LCD will occur."
            logi(m)
            print(m)

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        if self.lcd is None:
            m = f"MwsDisplays@277  DID NOT FIND THE lcd!"
            logi(m)
            print(m)
        elif not self.lcd.ok:
            self.lcd = None # disable
            m = f"MwsDisplays@282  LCD is not OK! DISABLED the LCD"
            logi(m)
            print(m)
            #m = f"MwsDisplays@285  STOPPING THE displays TASK!!!!!!!!!!!!!!!!!!!!!!!"
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
                    m = f"MwsDisplays@301  RUNNING idle! COULD NOT FIND LCD!  {elapsed_secs=}"
                    logi(m)
                    print(m)

            led_idx = self._update_leds(led_idx)

            # tick the time
            await asyncio.sleep(0.25)
            self._timer_ticks += 1
            elapsed_secs = self._timer_ticks >>2

    def _force_lcd_update(self):
        print(f"MwsDisplays@313 _force_lcd_update FORCE UPDATE.  prev_tick_upd={self._lcd_next_update_tick}")
        self._lcd_next_update_tick = 1 # 'many ticks in the past'


    def _update_leds(self, led_idx):
        self.leds[led_idx].value(0)
        led_idx += 1
        if led_idx >= len(self.leds): led_idx = 0
        self.leds[led_idx].value(1)
        return led_idx


    def _update_lcd(self, elapsed_secs):
        ###print(f"MwsDisplays@326 UPDATE LCD LINES  {elapsed_secs=} {self._lcd_active_display=} ")
        if self._menu_active:
            self._update_lcd_menu_active(elapsed_secs)
        else:
            self._update_lcd_no_menu(elapsed_secs)


    def _update_lcd_menu_active(self, elapsed_secs):
       # Menu col > 0
        if self._menu_row == 0:
            self._lcd_show_network(self._menu_col, elapsed_secs)
        elif self._menu_row == 1:
            self._lcd_show_date_time(self._menu_col)
        elif self._menu_row == 2:
            self._lcd_show_ntp_status(self._menu_col)
        elif self._menu_row == 3:
            self._lcd_show_temperatures(self._menu_col)
        elif self._menu_row == 4:
            self._lcd_show_memory(self._menu_col)
        elif self._menu_row == 5:
            self._lcd_show_filesys(self._menu_col)
        elif self._menu_row == 6:
            self._lcd_show_logs_info(self._menu_col)
        else:
            line1 = "menu bad col"
            line2 = f"{self._menu_row}  {self._menu_col}"
            self._show_lcd_lines(line1,line2)


    def _update_lcd_no_menu(self, elapsed_secs):
        if self._lcd_active_display == 0:
            self._lcd_show_network(1, elapsed_secs)

        elif self._lcd_active_display == 1:
            self._lcd_show_date_time(1)

        elif self._lcd_active_display == 2:
            self._lcd_show_ntp_status(1)

        elif self._lcd_active_display == 3:
            self._lcd_show_temperatures(1)

        elif self._lcd_active_display == 4:
            self._lcd_show_temperatures(2)

        elif self._lcd_active_display == 5:
            self._lcd_show_memory(1)

        elif self._lcd_active_display == 6:
            self._lcd_show_memory(2)

        elif self._lcd_active_display == 7:
            self._lcd_show_memory(3)

        elif self._lcd_active_display == 8:
            self._lcd_show_filesys(1)

        elif self._lcd_active_display == 9:
            self._lcd_show_logs_info(2)

        else:
            # This should not get displayed unless debugging,
            # when LCD_ACTIVE_DISPLAY_MAX is set to a larger number
            # than there are cases above
            d = self._lcd_active_display
            line1 = f"ACTIVE DISP {d}"
            line2 = f"ACTIVE DISP={d}"
            ###self.lcd.puts(f"ACTIVE DISPLAY {d}", y=0)
            ###self.lcd.puts(f"ACTIVE DISPLAY={d}", y=1)
            self._show_lcd_lines(line1, line2)

    def _lcd_show_network(self, which, elapsed_secs):
        if which == 0:
            line1 = "Network"
            line2 = ""
        elif which == 1:
            hhmmss = seconds_to_hhmmss_string(elapsed_secs)
            line1 = f"{self._databoard.ipaddr}:{self._databoard.port}"
            line2 = f"{hhmmss}"
        elif which == 2:
            hhmmss = seconds_to_hhmmss_string(elapsed_secs)
            line1 = f"{self._databoard.ipaddr}:{self._databoard.port}"
            line2 = f"{self._databoard.wifi_restarts_counter} Wifi Restarts"
        else:
            line1 = f"{self._databoard.ipaddr}"
            line2 = f"Port: {self._databoard.port}"
        self._show_lcd_lines(line1,line2)

    def _lcd_show_date_time(self, which):
        if which == 0:
            line1 = "Date-Time"
            line2 = ""
        else:
            line1 = f"{self._databoard.time_mgr.get_formatted_local_YYYYMMDD()}"
            line2 = f"{self._databoard.time_mgr.get_formatted_local_HHMMSS()}"
        self._show_lcd_lines(line1,line2)

    def _lcd_show_ntp_status(self, which):
        if which == 0:
            line1 = "NTP Status"
            line2 = ""
        else:
            # NTP Latest update:
            line1 = f"{self._databoard.time_mgr_latest_ntp_update_secs} secs"
            line2 = f"{self._databoard.time_mgr_number_of_ntp_updates} NTP update"
        self._show_lcd_lines(line1,line2)

    def _lcd_show_temperatures(self, which):
        if which == 0:
            line1 = "Temps"
            line2 = ""
        elif which == 1:
            # Temp-F
            degs_f = self._databoard.internal_temp_f
            min_degs_f = self._databoard.internal_min_temp_f
            max_degs_f = self._databoard.internal_max_temp_f
            #         123456789.123456
            #         Pico temp 123.1F"
            line1 = f"Pico temp {degs_f:.1f}F"
            line2 = f"{min_degs_f:.1f} {max_degs_f:.1f} MinMx"

        elif which == 2:
            # Temp-C
            degs_c = self._databoard.internal_temp_c
            min_degs_c = self._databoard.internal_min_temp_c
            max_degs_c = self._databoard.internal_max_temp_c
            #         123456789.123456
            #         Pico temp 123.1C"
            line1 = f"Pico temp {degs_c:.1f}C"
            line2 = f"{min_degs_c:.1f} {max_degs_c:.1f} MinMx"
        else:
            line1 = f"UNKNOWN TEMP {which=}"
            line2 = ""
        self._show_lcd_lines(line1,line2)

    def _lcd_show_memory(self, which):
        if which == 0:
            line1 = "Memory"
            line2 = ""
        elif which == 1:
            # memory alloc
            mem_alloc = self._databoard.memory_alloc
            mem_alloc_min = self._databoard.memory_alloc_min
            mem_alloc_max = self._databoard.memory_alloc_max
            line1 = f"{mem_alloc} AllocMnMx"
            line2 = f"{mem_alloc_min} {mem_alloc_max}"

        elif which == 2:
            # memory free
            mem_free = self._databoard.memory_free
            mem_free_min = self._databoard.memory_free_min
            mem_free_max = self._databoard.memory_free_max
            line1 = f"{mem_free} FreeMinMx"
            line2 = f"{mem_free_min} {mem_free_max}"
        elif which == 3:
            # memory
            mem_free = self._databoard.memory_free
            mem_alloc = self._databoard.memory_alloc
            line1 = f"{mem_free} FreeMem"
            line2 = f"{mem_alloc} AllocMem"
        else:
            line1 = f"UNKNOWN {which=}"
            line2 = ""
        self._show_lcd_lines(line1,line2)

    def _lcd_show_filesys(self, which):
        if which == 0:
            line1 = "File Space"
            line2 = ""
        else:
            # file space
            total_space, free_space = get_flash_space()
            line1 = f"{free_space} FreeFS"
            line2 = f"{total_space} TotalFS"
        self._show_lcd_lines(line1,line2)


    def _lcd_show_logs_info(self, which):
        if which == 0:
            line1 = "Logs Info"
            line2 = ""
        elif which == 1:
            elc = ElemLogControl.get_instance()
            line1 = f"{elc.get_current_log_fpath()}"
            line2 = f"{elc.get_current_log_fsize()} bytes"
        elif which == 2:
            elc = ElemLogControl.get_instance()
            include_currently_open_file = True
            totals = elc.get_logs_totals(include_currently_open_file)
            num_logs  = totals[0]
            total_size = totals[1]
            line1 = f"{num_logs} logs"
            line2 = f"{total_size} bytes"
        elif which == 3:
            elc = ElemLogControl.get_instance()
            first_item = elc.get_log_table_item(0)
            if first_item is None:
                line1 = "No first logfile"
                line2 = " in logs-table"
            else:
                fname = first_item[0]
                fsize = first_item[1]
                line1 = f"{fname}"
                line2 = f"{fsize} 1st"
        elif which == 4:
            elc = ElemLogControl.get_instance()
            last_item = elc.get_log_table_item(-1)
            if last_item is None:
                line1 = "No last logfile"
                line2 = " in logs-table"
            else:
                fname = last_item[0]
                fsize = last_item[1]
                line1 = f"{fname}"
                line2 = f"{fsize} last"
        else:
            line1 = f"logs info"
            line2 = f"bad col# {which}"
        self._show_lcd_lines(line1,line2)


    def _show_lcd_line(self, line):
        self._show_lcd_lines(line, "")
    def _show_lcd_lines(self, line1, line2):
        s1 = f"{line1:<16}"
        s2 = f"{line2:<16}"
        self.lcd.puts(s1, y=0)
        self.lcd.puts(s2, y=1)

###
