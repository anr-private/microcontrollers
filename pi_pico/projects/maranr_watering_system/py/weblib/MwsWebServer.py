# MwsWebServer.py

import asyncio

from logger_elem.ElemLoggerABC import ElemLoggerABC
from utils import show_cc

from .HdrAccum import HdrAccum
from .ParsedHttp import ParsedHttp
from .RequestHandler import RequestHandler

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class MwsWebServer(ElemLoggerABC):
    #  top-level Server class 

    def __init__(self, host, port):
        self.host = host
        self.port = port
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsSensors@25 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        log("MWS@19.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):

        callbk = self.handle_new_client
        server = await asyncio.start_server(callbk, self.host, self.port)
        log(f"MWS@29 webserver_coro: Listening on {self.host}:{self.port}...")
        log(f"MWS@30  Server obj is {type(server)}")

        while 1:
            log(f"MWS@33 webserver_coro RUNNING idle!")
            await asyncio.sleep(5)

        ###result = "NO RESULT YET from webserver_coro"
        ###log(f"MWS@37 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        m = f"MWS@61 handle_new_client  {reader=} {writer=}  "
        print();print(m); log(m)
        
        hdrAccum = HdrAccum()
        line_num = 0
        mesg_tail = ""
        try:
            while 1:
                log(f"MWS@54 handle_new_client@54  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()
                if not new_bytes:
                    # Client disconnected
                    log(f"MWS@53 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                #@@@@m = f"MWS@56 handle_new_client@61 {line_num=} got {len(new_bytes)} bytes. "
                #@@@@print(m);
                #@@@@@log(m)
    
                line = new_bytes.decode("utf-8")
                log(f"MWS@60 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                log(f"MWS@61 handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    log(f"MWS@65 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    log(f"MWS@68 {header if header else 'NULL'}")
                    log(f"MWS@69 {mesg_tail if mesg_tail else 'NULL'}")
                    
                    httpReply = self.handle_the_request(header)
                    
                    if httpReply is None:
                        mesg = f"MWS@74  FAILED TO HANDLE REQUEST!"
                        print(mesg)
                        log(mesg)
                        break
                    m1 = f"MWS@78 HTTP-REPY is {str(httpReply)} "
                    m2 = f"MWS@79 ... reply header... --------------------"
                    m3 = f"{httpReply.get_header()}"
                    m4 = f"MWS@85  --- end of REPLY HEADER ---"  ###  {len(httpReply.get_header())}  -------------------"

                    #print(m1); print(m2); print(m3); print(m4)
                    logi(m1); logi(m2); logi(m3); logi(m4)
                    
                    writer.write(httpReply.get_header())
                    body = httpReply.get_body()
                    if body:
                        writer.write(body)
                    await writer.drain()
                    ###await writer.wait_closed()

                    break

            logi(f"MWS@97 handle_new_client done with this client!")

        except Exception as ex:
            print("$*$"*35);print("$*$"*35);print("$*$"*35);print("$*$"*35);
            log(f"MWS@101 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' ")
            ###raise
        finally:
            log("MWS@101 handle_new_client Closing client writer connection")
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed
            log("MWS@104 handle_new_client CLIENT WRITER is CLOSED")
            
            log(f"MWS@106 handle_new_client CLOSING THE CLIENT reader")
            reader.close()
            await reader.wait_closed()
            log("MWS@109 handle_new_client CLIENT READER is CLOSED")


    def handle_the_request(self, header):
        log(f"MWS@113 handle_client_request  {len(header)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(header)

        log(f"MWS@118 httpReply: {str(httpReply)}")
        return httpReply

        



###
