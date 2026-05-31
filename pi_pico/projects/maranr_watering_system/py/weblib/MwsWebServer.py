# MwsWebServer.py

import asyncio
import gc

from utils import gc_collect
from lib2.DataBoard import DataBoard
from lib2.TimeMgr import TimeMgr
from logger_elem.ElemLoggerABC import ElemLoggerABC
from utils import show_cc

from .HdrAccum import HdrAccum
from .ParsedHttp import ParsedHttp
from .RequestHandler import RequestHandler

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

VALIDATE = 743520


class MwsWebServer(ElemLoggerABC):
    #  top-level webserver class 

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = MwsWebServer(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        MwsWebServer._instance = None


    def __init__(self, validate):
        if validate != VALIDATE:
            raise RuntimeError(f"MwsWebServer CTOR is private!")
        self._ipaddr = None
        self._port = 0
        self._databoard = DataBoard.get_instance()
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        log("WEBSVR@58.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):
        server = None

        while True:
            ipaddr = self._databoard.ipaddr
            port   = self._databoard.port
            log(f"WEBSVR@70 webserver_coro MONITOR CONNECTION STATUS: IP:PORT  {ipaddr} {port}")

            # default sleep time - assuming nothing has changed...
            sleep_secs = 15 #@@@$$$$$$$$$$$$

            # Do we need to stop the server?
            need_to_stop = False
            if ipaddr is None and server is not None:
                need_to_stop = True
                logi(f"WEBSVR@79  NEED TO STOP SERVER:  we do not have an IPADDR (any longer)")
            if ipaddr is not None and self._ipaddr != ipaddr:
                need_to_stop = True
                logi(f"WEBSVR@82  NEED TO STOP SERVER:  IPADDR changed: ours: {self._ipaddr}  NEW: {ipaddr}")
            if port != 0 and self._port != port:
                need_to_stop = True
                logi(f"WEBSVR@85  NEED TO STOP SERVER:  PORT changed: ours: {self._port}  NEW: {port}")

            if need_to_stop:
                if server is not None:
                    logi(f"WEBSVR@89 STOPPING THE SERVER ")
                    await self._close_the_server(server)
                    server = None
                    self._ipaddr = None
                    self._port = 0
                    self._databoard.webserver_active = False
                    sleep_secs = 10 #@@@$$$$$
                else:
                    logi(f"WEBSVR@97 STOP THE SERVER - except there is no server running")

            need_to_start = False
            if server is None:
                # No server running. Do we need to start one?  (Can we with what we have?)
                if ipaddr is not None:   # we assume therefore that port != 0:
                    need_to_start = True

            if need_to_start:
                logi(f"WEBSVR@106 (RE)STARTING THE SERVER")
                callbk = self.handle_new_client
                server = await asyncio.start_server(callbk, ipaddr, port)

                self._ipaddr = ipaddr
                self._port = port
                self._databoard.webserver_active = True
                sleep_secs = 10
                logi(f"WEBSVR@114 (RE)STARTED THE SERVER  {self._ipaddr} {self._port}")

            if sleep_secs is not None:
                await asyncio.sleep(sleep_secs)


    async def _close_the_server(self, server):
        logi(f"WEBSVR@121 CLOSE THE SERVER")
        try:
            server.close()
            logi(f"WEBSVR@124 AWAITING for the SERVER to CLOSE")
            await server.wait_closed()
        except Exception as ex:
            m = f"WEBSVR@127 *ERROR* Closing the server:  {repr(ex)}"
            logi(m)

        ###result = "NO RESULT YET from webserver_coro"
        ###log(f"WEBSVR@131 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        #m = f"WEBSVR@135 -----=====-----=====-----===== NEW CLIENT =====-----====="
        #logi(m)
        m = f"WEBSVR@137 =====___ NEW CLIENT  ___+++++___  {TimeMgr.get_formatted_date_time_string()}  ___+++++====="
        logi(m)
        #m = f"WEBSVR@139 handle_new_client  reader={repr(reader)} writer={repr(writer)}  "
        #logi(m)

        try:
            request_stg = await self._read_the_request(reader)

            if not request_stg:
                m = f"WEBSVR@146 FAILED TO READ THE REQUEST!"
                logi(m)
                return

            httpReply = self._handle_the_request(request_stg)
            del request_stg
            
            if httpReply is None:
                mesg = f"WEBSVR@154  FAILED TO HANDLE REQUEST!"
                log(mesg)
                return

            m = f"WEBSVR@158 HTTP-REPY is ... "
            logi(m)
            mlines = httpReply.get_loggable_lines(prefix="WEBSVR@160")
            for m in mlines:
                logi(m)
            del m, mlines

            self._write_the_reply(httpReply, writer)

            del httpReply

            await writer.drain()

        except Exception as ex:
            print("WEBSVR@172 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR@173 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        finally:
            log("WEBSVR@178 handle_new_client Closing client writer connection")
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed
            log("WEBSVR@181 handle_new_client CLIENT WRITER is CLOSED")
            
            log(f"WEBSVR@183 handle_new_client CLOSING THE CLIENT reader")
            reader.close()
            await reader.wait_closed()
            log("WEBSVR@186 handle_new_client CLIENT READER is CLOSED")

        m = f"WEBSVR@188 DONE WITH THIS CLIENT -- RUN THE GC COLLECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        logi(m)
        gc_collect()
        mf = gc.mem_free()
        m = f"WEBSVR@192 AFTER GC  FREE MEMORY is {mf}"
        logi(m)
        logi(f"WEBSVR@194 handle_new_client done with this client!")


    async def _read_the_request(self, reader):

        hdrAccum = HdrAccum()
        line_num = 0
        header = None
        try:
            while 1:
                #log(f"WEBSVR@204 read_the_request  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()

                if not new_bytes:
                    # Client disconnected
                    log(f"WEBSVR@209 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
    
                line = new_bytes.decode("utf-8")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    log(f"WEBSVR@217 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    log(f"WEBSVR@220 {header if header else 'NULL'}")
                    log(f"WEBSVR@221 {mesg_tail if mesg_tail else 'NULL'}")
                    if mesg_tail:
                        ###raise RuntimeError("WEBSVR@223  WE HAVE A mesg_tail: '{mesg_tail}'")
                        logi(f"WEBSVR@224 __WARNING__ we have a mesg_tail {type(mesg_tail)}")
                    #@@TODO@@  Need to handle a leftover tail string - in case of packet breakup by network
                    break
            return header

        except Exception as ex:
            print("WEBSVR@230 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR@231 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            ### return None

    def _handle_the_request(self, request_stg):
        log(f"WEBSVR@238 handle_the_request  {len(request_stg)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(request_stg)

        m = f"WEBSVR@243 httpReply: {str(httpReply)}"
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
            print("WEBSVR@260 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR@261 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TODO fix all the try/except



###
