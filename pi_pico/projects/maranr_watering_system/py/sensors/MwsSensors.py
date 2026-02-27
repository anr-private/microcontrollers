# MwsSensors.py

import asyncio
import utime as time

#from utils import *
import lib.utils as utils
dbg = utils.dbg
loggg = utils.loggg


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
            print("WS.sensors_coro RUNNING - nothing impl yet")
            await asyncio.sleep(10)


###

