# MwsWebServer.py
#
# LINEMARKER=WEBSVR

import asyncio
import gc

from lib1.gc_utils import gc_collect
from lib2.DataBoard import DataBoard
from lib2.TimeMgr import TimeMgr
from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib1.utils import show_cc

from .HdrAccum import HdrAccum
from .ParsedHttp import ParsedHttp
from .RequestHandler import RequestHandler

try: from typing import Callable, Any
except ImportError: pass

# Logging functions; our parent class sets using _set_logger()
log:   Any = None
logrt: Any = None
logi:  Any = None

VALIDATE = 743520


class MwsWebServer(ElemLoggerABC):
    #  top-level webserver class 

    _instance: "MwsWebServer"|None = None

    @classmethod
    def get_instance(cls) -> "MwsWebServer":
        if cls._instance is not None: return cls._instance
        cls._instance = MwsWebServer(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        MwsWebServer._instance = None


    def __init__(self, validate: int) -> None:
        if validate != VALIDATE:
            raise RuntimeError(f"MwsWebServer CTOR is private!")
        self._ipaddr: str = "" #####@@@@@@@ None
        self._port:int = 0
        self._databoard: DataBoard = DataBoard.get_instance()
        super().__init__()

    def _set_logger(self, logger: Any) -> None:
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    #@@@@@@@@@@ TODO better annotation for the result
    def start_the_task(self) -> Any:
        """ creates,starts the coro. Returns task."""
        log("WEBSVR$64.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):

        server = None

        while True:
            # annotations b/c these are args to asyncio.start_server
            # and it's annotations are too broad
            ipaddr:str = self._databoard.ipaddr
            port:int   = self._databoard.port
            log(f"WEBSVR$79 webserver_coro MONITOR CONNECTION STATUS: IP:PORT  {ipaddr!r}:{port!r}")

            # default sleep time - assuming nothing has changed...
            sleep_secs = 15 #@@@$$$$$$$$$$$$

            # Do we need to stop the server?
            need_to_stop = False
            #@@@@@@@@@@@@@@@@@if ip addr is None and server is not None:
            if not ipaddr and server is not None:
                need_to_stop = True
                logi(f"WEBSVR$89  NEED TO STOP SERVER:  we do not have an IPADDR (any longer)")
            #@@@@@@@@@@if ip addr is not None and self._ipaddr != ipaddr:
            if ipaddr and self._ipaddr != ipaddr:
                need_to_stop = True
                logi(f"WEBSVR$93  NEED TO STOP SERVER:  IPADDR changed: ours: {self._ipaddr!r}  NEW: {ipaddr!r}")
            if port != 0 and self._port != port:
                need_to_stop = True
                logi(f"WEBSVR$96  NEED TO STOP SERVER:  PORT changed: ours: {self._port}  NEW: {port}")

            if need_to_stop:
                if server is not None:
                    logi(f"WEBSVR$100 STOPPING THE SERVER ")
                    await self._close_the_server(server)
                    server = None
                    self._ipaddr = ""
                    self._port = 0
                    self._databoard.webserver_active = False
                    sleep_secs = 10 #@@@$$$$$ TODO
                else:
                    logi(f"WEBSVR$108 STOP THE SERVER - except there is no server running")

            need_to_start = False
            if server is None:
                # No server running. Do we need to start one? 
                # Can we run with what we have? We need an IP and port.
                if ipaddr:   # we assume therefore that port != 0:
                    need_to_start = True

            if need_to_start:
                logi(f"WEBSVR$118 (RE)STARTING THE SERVER")
                #  s/w defect if occurs:
                if (not ipaddr):
                    logi(f"WEBSVR$121 INTERNAL ERROR: ipaddr is null: {ipaddr!r}. Cannot start_server")
                    continue
                if (not port):
                    logi(f"WEBSVR$124 INTERNAL ERROR: port is zero(?): {port!r} is null. Cannot start_server")
                    continue

                callbk = self.handle_new_client
                server = await asyncio.start_server(callbk, ipaddr, port)

                self._ipaddr = ipaddr
                self._port = port
                self._databoard.webserver_active = True
                sleep_secs = 10
                logi(f"WEBSVR$134 (RE)STARTED THE SERVER  {self._ipaddr} {self._port}")

            if sleep_secs is not None:
                await asyncio.sleep(sleep_secs)


    async def _close_the_server(self, server):
        logi(f"WEBSVR$141 CLOSE THE SERVER")
        try:
            server.close()
            logi(f"WEBSVR$144 AWAITING for the SERVER to CLOSE")
            await server.wait_closed()
        except Exception as ex:
            m = f"WEBSVR$147 *ERROR* Closing the server:  {repr(ex)}"
            logi(m)

        ###result = "NO RESULT YET from webserver_coro"
        ###log(f"WEBSVR$151 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        print(f"WEBSVR$155 ______________________________________ handle_new_client CALLED _____________")
        LL=log

        #m = f"WEBSVR$161 -----=====-----=====-----===== NEW CLIENT =====-----====="
        #logi(m)
        m = f"WEBSVR$163 =====___ NEW CLIENT  ___+++++___  {TimeMgr.get_formatted_date_time_string()}  ___+++++====="
        LL(m)
        #m = f"WEBSVR$165 handle_new_client  reader={repr(reader)} writer={repr(writer)}  "
        #LL(m)

        try:
            request_stg = await self._read_the_request(reader)

            if not request_stg:
                m = f"WEBSVR$172 FAILED TO READ THE REQUEST!"
                logi(m)
                return

            httpReply = self._handle_the_request(request_stg)
            del request_stg
            
            if httpReply is None:
                mesg = f"WEBSVR$180  FAILED TO HANDLE REQUEST!"
                log(mesg)
                return

            m = f"WEBSVR$184 HTTP-REPY is ... "
            LL(m)
            mlines = httpReply.get_loggable_lines(prefix="WEBSVR$186")
            for m in mlines:
                LL(m)
            del m, mlines

            self._write_the_reply(httpReply, writer)

            del httpReply

            await writer.drain()

        except Exception as ex:
            print("WEBSVR$198 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR$199 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        finally:
            log("WEBSVR$204 handle_new_client Closing client writer connection")
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed
            log("WEBSVR$207 handle_new_client CLIENT WRITER is CLOSED")
            
            log(f"WEBSVR$209 handle_new_client CLOSING THE CLIENT reader")
            reader.close()
            await reader.wait_closed()
            log("WEBSVR$212 handle_new_client CLIENT READER is CLOSED")

        m = f"WEBSVR$214 DONE WITH THIS CLIENT -- RUN THE GC COLLECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        LL(m)
        gc_collect()
        mf = gc.mem_free()
        m = f"WEBSVR$218 AFTER GC  FREE MEMORY is {mf}"
        LL(m)
        LL(f"WEBSVR$220 handle_new_client done with this client!")


    async def _read_the_request(self, reader):
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        LL=log

        hdrAccum = HdrAccum()
        line_num = 0
        header = None
        try:
            while 1:
                #log(f"WEBSVR$232 read_the_request  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()

                if not new_bytes:
                    # Client disconnected
                    log(f"WEBSVR$237 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
    
                line = new_bytes.decode("utf-8")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    log(f"WEBSVR$245 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    log(f"WEBSVR$248 {header if header else 'NULL'}")
                    log(f"WEBSVR$249 {mesg_tail if mesg_tail else 'NULL'}")
                    if mesg_tail:
                        ###raise RuntimeError("WEBSVR$251  WE HAVE A mesg_tail: '{mesg_tail}'")
                        logi(f"WEBSVR$252 __WARNING__ we have a mesg_tail {type(mesg_tail)}")
                    #@@TODO@@  Need to handle a leftover tail string - in case of packet breakup by network
                    break
            return header

        except Exception as ex:
            print("WEBSVR$258 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR$259 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            ### return None

    def _handle_the_request(self, request_stg):
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        LL=log

        log(f"WEBSVR$269 handle_the_request  {len(request_stg)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(request_stg)

        m = f"WEBSVR$274 httpReply: {str(httpReply)}"
        LL(m)

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
            print("WEBSVR$291 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"WEBSVR$292 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TODO fix all the try/except



###
