# MwsWebServer.py

import asyncio
import gc

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
        log("MWS@38.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):

        callbk = self.handle_new_client
        server = await asyncio.start_server(callbk, self.host, self.port)
        log(f"MWS@48 webserver_coro: Listening on {self.host}:{self.port}...")
        log(f"MWS@49  Server obj is {type(server)}")

        while 1:
            log(f"MWS@52 webserver_coro RUNNING idle!")
            await asyncio.sleep(5)

        ###result = "NO RESULT YET from webserver_coro"
        ###log(f"MWS@56 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        m = f"MWS@60 handle_new_client  {reader=} {writer=}  "
        print(); logi(m)

        try:
            request_stg = await self._read_the_request(reader)

            if not request_stg:
                m = f"MWS@67 FAILED TO READ THE REQUEST!"
                print(m)
                logi(m)
                return

            httpReply = self._handle_the_request(request_stg)
            del request_stg
            
            if httpReply is None:
                mesg = f"MWS@76  FAILED TO HANDLE REQUEST!"
                print(mesg)
                log(mesg)
                return

            m1 = f"MWS@81 HTTP-REPY is {str(httpReply)} "
            m2 = f"MWS@82 ... reply header... --------------------"
            m3 = f"{httpReply.get_header()}"
            m4 = f"MWS@84  --- end of REPLY HEADER ---"  ###  {len(httpReply.get_header())}  -------------------"
            print(m1); print(m2); print(m3); print(m4)
            logi(m1); logi(m2); logi(m3); logi(m4)

            self._write_the_reply(httpReply, writer)

            del httpReply

            await writer.drain()

        except Exception as ex:
            print("MWS@95 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@96 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        finally:
            log("MWS@101 handle_new_client Closing client writer connection")
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed
            log("MWS@104 handle_new_client CLIENT WRITER is CLOSED")
            
            log(f"MWS@106 handle_new_client CLOSING THE CLIENT reader")
            reader.close()
            await reader.wait_closed()
            log("MWS@109 handle_new_client CLIENT READER is CLOSED")

        m = "MWS@111 RUN THE GC COLLECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(m)
        logi(m)
        gc.collect()
        mf = gc.mem_free()
        m = "MWS@116 AFTER GC  FREE MEMORY is {mf}"
        print(m)
        logi(m)
        logi(f"MWS@119 handle_new_client done with this client!")


    async def _read_the_request(self, reader):

        hdrAccum = HdrAccum()
        line_num = 0
        try:
            while 1:
                #log(f"MWS@128 read_the_request  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()

                if not new_bytes:
                    # Client disconnected
                    log(f"MWS@133 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                ####m = f"MWS@136 handle_new_client@61 {line_num=} got {len(new_bytes)} bytes. "
                ####print(m);
                ####log(m)
    
                line = new_bytes.decode("utf-8")
                #log(f"MWS@141 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                #log(f"MWS@142 handle_new_client@52 {line_num=} {show_cc(line)}")
                #print(f"MWS@143 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                #print(f"MWS@144 handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    log(f"MWS@148 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    log(f"MWS@151 {header if header else 'NULL'}")
                    log(f"MWS@152 {mesg_tail if mesg_tail else 'NULL'}")
                    if mesg_tail:
                        ###raise RuntimeError("MWS@154  WE HAVE A mesg_tail: '{mesg_tail}'")
                        logi(f"MWS@155 __WARNING__ we have a mesg_tail {type(mesg_tail)}")
                    #@@TODO@@  Need to handle a leftover tail string - in case of packet breakup by network
                    break
            return header

        except Exception as ex:
            print("MWS@161 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@162 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            ### return None

    def _handle_the_request(self, request_stg):
        log(f"MWS@169 handle_the_request  {len(request_stg)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(request_stg)

        m = f"MWS@174 httpReply: {str(httpReply)}"
        print(m)
        logi(m)

        return httpReply


    def _write_the_reply(self, httpReply, writer):
        try:           
            writer.write(httpReply.get_header())
            body = httpReply.get_body()
            if body:
                writer.write(body)
            ###caller does these:
            ###await writer.drain()
            ###await writer.wait_closed()

        except Exception as ex:
            print("MWS@192 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@193 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



###
