# WspWebServer.py

import asyncio


class WspWebServer:
    """ top-level Server class """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("WspWebServer.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):
        while 1:
            print(f"WspWebServer.webserver_coro RUNNING!")
            await asyncio.sleep(1)

        ###result = "NO RESULT YET from webserver_coro"
        ###print(f"WspWebServer.webserver_coro COMPLETED.  {result=}")
        ###return result



###
