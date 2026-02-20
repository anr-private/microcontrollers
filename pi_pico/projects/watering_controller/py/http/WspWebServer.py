# WspWebServer.py

import asyncio

from utils import *
from http.HdrAccum import HdrAccum
from http.ParsedHttp import ParsedHttp
from http.RequestHandler import RequestHandler

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
        m = f"WWS.handle_new_client@46  {reader=} {writer=}  "
        print();print(m); log(m)
        
        hdrAccum = HdrAccum()
        line_num = 0
        mesg_tail = ""
        try:
            while 1:
                print(f"WWS.handle_new_client@54  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()
                if not new_bytes:
                    # Client disconnected
                    print(f"handle_client_by_lines@58 GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                m = f"WWS.handle_new_client@61 {line_num=} got {len(new_bytes)} bytes. "
                print(m); log(m)
    
                line = new_bytes.decode("utf-8")
                log(f"WWS.handle_new_client@52 {line_num=} got {len(line)} chars. ")
                log(f"WWS.handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    print(f"WWS@69 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    print(f"WWS@72 {header if header else 'NULL'}")
                    print(f"WWS@73 {mesg_tail if mesg_tail else 'NULL'}")
                    
                    reply = self.handle_the_request(header)
                    
                    if reply is None:
                        mesg = f"WWS@79  FAILED TO HANDLE REQUEST!"
                        print(mesg)
                        log(mesg)
                        break
                    m1 = f"" # WWS@83  ------------------ REPLY IS  {len(reply)}  -------------------"
                    m2 = f"{reply}"
                    m3 = f"WWS@83  ------------------ end of REPLY   {len(reply)}  -------------------"
                    print(m1); print(m2); print(m3)
                    log(m1): log(m2); log(m3)
                    
                    writer.write(reply)
                    await writer.drain()
                    ###await writer.wait_closed()

                    break

            print(f"WWS.handle_new_client@95 done with this client!")
            log(f"WWS.handle_new_client done with this client!")

        except Exception as ex:
            print(f"WWS.handle_new_client@99 **FAILED**  ex={repr(ex)}  ex='{str(ex)}' ")
        ###finally:
        print('WWS.handle_new_client@101 Closing client writer connection')
        writer.close()
        await writer.wait_closed() # Wait until the stream is fully closed
        print("WWS.handle_new_client@104 CLIENT WRITER is CLOSED")
        #
        print(f"WWS.handle_new_client@106 CLOSING THE CLIENT reader")
        reader.close()
        await reader.wait_closed()
        print("WWS.handle_new_client@104 CLIENT READER is CLOSED")


    def handle_the_request(self, header):
        print(f"WWS.handle_client_request  {len(header)=}")

        reqHandler = RequestHandler()
        reply = reqHandler.handle_client_request(header)

        dbg(f"WWS@111  reply.len={len(reply) if reply else 'no-reply!'}")
        return reply





    # def SAVEDFORNOW(self, header):
        # hp = HttpParser()
# 
        # parsedHttp = hp.parse_header_data(header)
# 
        # if parsedHttp is None:
            # print(f"WS@93 REQUEST PARSE ERROR: {hp.latest_error()}")
            # #@@@@@ handle an error
# 
        # m1 = f"WWS@92 CLIENT REQUEST {hp.latest_error()=}"
        # m2 = f"WWS@93 {parsedHttp.long_string()}"
        # print(m1)
        # print(m2)
        # log(m1)
        # log(m2)

        



###
