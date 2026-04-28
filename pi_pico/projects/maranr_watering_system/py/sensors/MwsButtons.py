# MwsButtons.py

import asyncio
import gc
import time  #import utime as time
from machine import Pin

from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib2.DataBoard import DataBoard
from primitives import Pushbutton
from primitives import set_global_exception
from utils import gc_collect
from utils import get_fs_space_string
from utils import get_memory_status_string

log = None
logrt = None
logi = None

###UP_BUTTON_GPIO_PIN     = 14
###LEFT_BUTTON_GPIO_PIN   = 15
###CENTER_BUTTON_GPIO_PIN = 20
###RIGHT_BUTTON_GPIO_PIN  = 21
###DOWN_BUTTON_GPIO_PIN   = 22

VALIDATE = 804146

#@@@@ DEBUG ONLY ??
SHORT_CTR = 0
DOUBLE_CTR = 0
LONG_CTR = 0


class MwsButtons(ElemLoggerABC):
    """ pushbuttons """

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = MwsButtons(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        MwsButtons._instance = None


    def __init__(self, validate):
        if validate != VALIDATE:
            raise RuntimeError(f"MwsButtons CTOR is private!")
        # GPIO pins
        self.up_pin     = None
        self.left_pin   = None
        self.center_pin = None
        self.right_pin  = None
        self.down_pin   = None
        # Pushbutton objs
        self.up_pb     = None
        self.left_pb   = None
        self.center_pb = None
        self.right_pb  = None
        self.down_pb   = None
                              
        self._data_board = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        logi("MwsButtons.start_the_task  STARTING THE BUTTONS TASK!")

        self._data_board = DataBoard.get_instance()

        task = asyncio.create_task(self.buttons_coro())
        return task


    async def buttons_coro(self):

        # Buttons are connected to these GPIO pins
        self.up_pin     = Pin(14, Pin.IN, Pin.PULL_UP)
        self.left_pin   = Pin(15, Pin.IN, Pin.PULL_UP)
        self.center_pin = Pin(20, Pin.IN, Pin.PULL_UP)
        self.right_pin  = Pin(21, Pin.IN, Pin.PULL_UP)
        self.down_pin   = Pin(22, Pin.IN, Pin.PULL_UP)

        if 1:
            # slow down the polling
            Pushbutton.debounce_ms *= 2
        print(f"BTNS@95  Pushbutton.debounce_ms is {Pushbutton.debounce_ms}")

        self.up_pb     = self.init_one_button(self.up_pin, "Up")
        self.left_pb   = self.init_one_button(self.left_pin, "Left")
        self.center_pb = self.init_one_button(self.center_pin, "Center")
        self.right_pb  = self.init_one_button(self.right_pin, "Right")
        self.down_pb   = self.init_one_button(self.down_pin, "Down")

    async def handle_short(self, btn, btn_name):
        global SHORT_CTR
        SHORT_CTR += 1
        print(f"BTNS@106  SHORT PRESS  btn={btn} {btn_name}")
        if 1:
            print(f"BTNS@108    WAITing in handle_short() - should not stall the main loop!")
            await asyncio.sleep(3)
            print(f"BTNS@110    DONE-WAITing in handle_short()")
            
    
    async def handle_double(self, btn, btn_name):
        global DOUBLE_CTR
        DOUBLE_CTR += 1
        print(f"BTNS@116 DOUBLE PRESS  btn={btn} {btn_name}")
    
    async def handle_long(self, btn, btn_name):
        global LONG_CTR
        LONG_CTR += 1
        print(f"BTNS@121  LONG PRESS  btn={btn} {btn_name}")
    

    def init_one_button(self, pin, btn_name):
        pb = Pushbutton(pin, suppress=True)
        pb.release_func(self.handle_short, (pin, btn_name))
        pb.double_func(self.handle_double, (pin, btn_name))
        pb.long_func(self.handle_long, (pin, btn_name))
        return pb

    
###        elapsed = 0
###        start_time = time.time()
###        while elapsed < 60:  # Run for one minute
###            elapsed += 1
###            actual_elapsed = time.time() - start_time
###            print(f"BTNS@137                     MAIN: waited {elapsed} secs  ACTUAL delay: {actual_elapsed} secs  short={SHORT_CTR}  double={DOUBLE_CTR}  long={LONG_CTR}")
###            await asyncio.sleep(1)

###        use_logi = True
###        log_limit_ctr = 0
###        while 1:
###            if 0:
###                fss = get_fs_space_string()
###                log(f"BTNS@145.buttons_coro RUNNING: {fss}")
###            if 0:
###                mss = get_memory_status_string(do_garbage_collect=False)
###                log(f"BTNS@148.buttons_coro MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
###                gc_collect()
###                mss = get_memory_status_string(do_garbage_collect=False)
###                log(f"BTNS@151.buttons_coro MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")
###
###            # Reduce logging volume/freq
###            if 0:
###                log_limit_ctr += 1
###                if log_limit_ctr >= 6:
###                    log_limit_ctr = 0
###                    use_logi = True
###                else:
###                    use_logi = False
###
###            if 0:
###                ma_before = gc.mem_alloc()
###                mf_before = gc.mem_free()
###                gc.collect()
###                ma_after = gc.mem_alloc()
###                mf_after = gc.mem_free()
###                ma_diff = ma_after - ma_before
###                mf_diff = mf_after - mf_before
###                m1 = f"BTNS@170  ++++++++++  Alloc:  {ma_after} - {ma_before}  ==>  DIFF: {ma_diff} +++++++++++++++++++++++++++++++++++++++"
###                m2 = f"BTNS@171  ++++++++++  Free:   {mf_after} - {mf_before}  ==>  DIFF: {mf_diff}  +++++++++++++++++++++++++++++++++++++++"
###                if use_logi:
###                    logi(m1); logi(m2)
###                else:
###                    log(m1); log(m2)
###
###
###            await asyncio.sleep(10)

    # async def task_1(): # fake task
        # global TASK_1_CTR
        # TASK_1_CTR = 0
        # while 1:
            # TASK_1_CTR += 1
            # if TASK_1_CTR % 500 == 0:
                # print(f"BTNS@186 task_1  ctr={TASK_1_CTR}")
            # await asyncio.sleep(0)



###

