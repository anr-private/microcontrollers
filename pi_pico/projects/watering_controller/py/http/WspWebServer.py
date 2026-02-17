# WspWebServer.py

import asyncio

from utils import *
from http.HdrAccum import HdrAccum
from http.ParsedHttp import ParsedHttp
from http.HttpParser import HttpParser

class WspWebServer:
    """ top-level Server class """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        print("WWS.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):

        callbk = self.handle_new_client
        server = await asyncio.start_server(callbk, self.host, self.port)
        print(f'WWS.webserver_coro: Listening on {self.host}:{self.port}...')
        print(f"  Server obj is {type(server)}")
        # print(f"  server module {server.__module__}")
        # print(f"   dir(server)")
        # print(f"   {dir(server)}")



        while 1:
            print(f"WWS.webserver_coro RUNNING idle!")
            await asyncio.sleep(5)

        ###result = "NO RESULT YET from webserver_coro"
        ###print(f"WspWebServer.webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        dbg(f"WWS.handle_new_client  {reader=} {writer=}  ")
        log(f"WWS.handle_new_client  {reader=} {writer=}  ")

        hdrAccum = HdrAccum()
        line_num = 0
        try:
            while 1:
                print(f"WWS.handle_new_client@45  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()
                if not new_bytes:
                    # Client disconnected
                    print(f"handle_client_by_lines@86 GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                print(f"WWS.handle_new_client@52 {line_num=} got {len(new_bytes)} bytes. ")
                log(f"WWS.handle_new_client@52 {line_num=} got {len(new_bytes)} bytes. ")
    
                line = new_bytes.decode("utf-8")
                log(f"WWS.handle_new_client@52 {line_num=} got {len(line)} chars. ")
                log(f"WWS.handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    print(f"WWS@67 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    print(f"WWS@70 {header=}")
                    print(f"WWS@70 {mesg_tail=}")
                    self.handle_client_request(header)

            print(f"WWS.handle_new_client done with this client!")
            log(f"WWS.handle_new_client done with this client!")

        except Exception as ex:
            print(f'WWS.handle_new_client client {ex}')
        finally:
            print('WWS.handle_new_client Closing client connection')
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed

    def handle_client_request(self, header):
        print(f"WWS.handle_client_request  {len(header)=}")
        hp = HttpParser()
        parsedHttp = hp.parse_header_data(header)
        print(f"WWS.handle_client_request  {hp.latest_error()=}")
        print(f"WWS.handle_client_request  {parsedHttp=}")


###
