# MwsWebServer.py

import asyncio

from utils import *
from http.HdrAccum import HdrAccum
from http.ParsedHttp import ParsedHttp
from http.RequestHandler import RequestHandler

class MwsWebServer:
    """ top-level Server class """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        dbg("WWS@19.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):

        callbk = self.handle_new_client
        server = await asyncio.start_server(callbk, self.host, self.port)
        dbg(f"WWS@29 webserver_coro: Listening on {self.host}:{self.port}...")
        dbg(f"WWS@30  Server obj is {type(server)}")

        while 1:
            dbg(f"WWS@33 webserver_coro RUNNING idle!")
            await asyncio.sleep(5)

        ###result = "NO RESULT YET from webserver_coro"
        ###dbg(f"WWS@37 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        m = f"WWS@46 handle_new_client  {reader=} {writer=}  "
        print();print(m); log(m)
        
        hdrAccum = HdrAccum()
        line_num = 0
        mesg_tail = ""
        try:
            while 1:
                dbg(f"WWS@54 handle_new_client@54  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()
                if not new_bytes:
                    # Client disconnected
                    dbg(f"WWS@53 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                m = f"WWS@56 handle_new_client@61 {line_num=} got {len(new_bytes)} bytes. "
                print(m); log(m)
    
                line = new_bytes.decode("utf-8")
                log(f"WWS@60 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                log(f"WWS@61 handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    dbg(f"WWS@65 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    dbg(f"WWS@68 {header if header else 'NULL'}")
                    dbg(f"WWS@69 {mesg_tail if mesg_tail else 'NULL'}")
                    
                    httpReply = self.handle_the_request(header)
                    
                    if httpReply is None:
                        mesg = f"WWS@74  FAILED TO HANDLE REQUEST!"
                        print(mesg)
                        log(mesg)
                        break
                    m1 = f"WWS@78 HTTP-REPY is {str(httpReply)} "
                    m2 = f"WWS@79 ... reply header... ----------------------------"
                    m3 = f"{httpReply.get_header()}"
                    m4 = f"WWS@85  ------------------ end of REPLY HEADER   {len(httpReply.get_header())}  -------------------"
                    print(m1); print(m2); print(m3); print(m4)
                    log(m1); log(m2); log(m3); log(m4)
                    
                    writer.write(httpReply.get_header())
                    body = httpReply.get_body()
                    if body:
                        writer.write(body)
                    await writer.drain()
                    ###await writer.wait_closed()

                    break

            dbg(f"WWS@95 handle_new_client done with this client!")
            log(f"WWS@95 handle_new_client done with this client!")

        except Exception as ex:
            dbg(f"WWS@99 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' ")
        ###finally:
        dbg("WWS@101 handle_new_client Closing client writer connection")
        writer.close()
        await writer.wait_closed() # Wait until the stream is fully closed
        dbg("WWS@104 handle_new_client CLIENT WRITER is CLOSED")
        
        dbg(f"WWS@106 handle_new_client CLOSING THE CLIENT reader")
        reader.close()
        await reader.wait_closed()
        dbg("WWS@109 handle_new_client CLIENT READER is CLOSED")


    def handle_the_request(self, header):
        dbg(f"WWS@113 handle_client_request  {len(header)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(header)

        dbg(f"WWS@118 httpReply: {str(httpReply)}")
        return httpReply

        



###
