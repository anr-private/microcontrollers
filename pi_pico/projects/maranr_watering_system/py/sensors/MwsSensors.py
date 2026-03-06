# MwsSensors.py

import asyncio
import gc
import utime as time

#from utils import *
###import lib.utils as utils
#from utils import get_flash_space
from utils import get_fs_space_string
from utils import get_memory_status_string


class MwsSensors:
    """ sensors and effectors """

    def __init__(self, *args):
        #self.SOME_THING = MWS_CONFIG.get("config-param-name-here")
        ...


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("WS.startup!")

        task = asyncio.create_task(self.sensors_coro())
        return task


    async def sensors_coro(self):

        while 1:
            if 0:
                fss = get_fs_space_string()
                print(f"WS.sensors_coro RUNNING: {fss}")
            if 1:
                mss = get_memory_status_string(do_garbage_collect=False)
                print(f"WS.sensors_coro MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
                gc.collect()
                mss = get_memory_status_string(do_garbage_collect=False)
                print(f"WS.sensors_coro MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

            await asyncio.sleep(4)

#    def make_space_stg(self):
#        ts, fs = get_flash_space()
#
#        tss = convert_fs_space_to_string(ts)
#        fss = convert_fs_space_to_string(fs)
#
#        s = f"TOTAL SPACE {tss}   FREE SPACE {fss}"
#        return s
#
###

