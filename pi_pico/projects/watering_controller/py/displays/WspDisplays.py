# WspDisplays.py

import asyncio
import utime as time

from utils import *
from machine import Pin, SoftI2C
from lib_lcd1602_2004_with_i2c import LCD

class WspDisplays:
    """ top-level Server class """

    def __init__(self, *args):
        self.lcd1602_sda_pin = WSP_CONFIG.get("lcd1602_sda_pin")
        self.lcd1602_scl_pin = WSP_CONFIG.get("lcd1602_scl_pin")
        ...

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("WD.startup!")

        task = asyncio.create_task(self.displays_coro())
        return task


    async def displays_coro(self):

        while 1:
            print(f"WD.displays_coro RUNNING idle!")
            await asyncio.sleep(5)

        ###result = "NO RESULT YET from displays_coro"
        ###print(f"WspDisplays.displays_coro COMPLETED.  {result=}")
        ###return result



###
