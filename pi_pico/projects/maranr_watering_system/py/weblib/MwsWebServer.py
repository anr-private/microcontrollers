# MwsWebServer.py

import asyncio
import gc

from lib2.DataBoard import DataBoard
from logger_elem.ElemLoggerABC import ElemLoggerABC
from utils import show_cc, get_formatted_date_time_string

from .HdrAccum import HdrAccum
from .ParsedHttp import ParsedHttp
from .RequestHandler import RequestHandler

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class MwsWebServer(ElemLoggerABC):
    #  top-level Server class 

    def __init__(self):
        #@@@@@@@@$$$$$$$$$$$$$$$$$$$
        #ipaddr = "192.168.1.49"
        #port = 8000
        #self._ipaddr = ipaddr
        #self._port = port
        self._ipaddr = None
        self._port = 0
        self._dataBoard = DataBoard.get_instance()
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsSensors@25 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        log("MWS@45.startup!")

        task = asyncio.create_task(self.webserver_coro())
        return task


    async def webserver_coro(self):
        server = None

        while True:
            ipaddr = self._dataBoard.ipaddr
            port   = self._dataBoard.port
            log(f"MWS@57 webserver_coro MONITOR CONNECTION STATUS: IP:PORT  {ipaddr} {port}")

            # default sleep time - assuming nothing has changed...
            sleep_secs = 15 #@@@$$$$$$$$$$$$

            # Do we need to stop the server?
            need_to_stop = False
            if ipaddr is None and server is not None:
                need_to_stop = True
                logi(f"MWS@66  NEED TO STOP SERVER:  we do not have an IPADDR (any longer)")
            if ipaddr is not None and self._ipaddr != ipaddr:
                need_to_stop = True
                logi(f"MWS@69  NEED TO STOP SERVER:  IPADDR changed: ours: {self._ipaddr}  NEW: {ipaddr}")
            if port != 0 and self._port != port:
                need_to_stop = True
                logi(f"MWS@72  NEED TO STOP SERVER:  PORT changed: ours: {self._port}  NEW: {port}")

            if need_to_stop:
                if server is not None:
                    logi(f"MWS@76 STOPPING THE SERVER ")
                    await self._close_the_server(server)
                    server = None
                    self._ipaddr = None
                    self._port = 0
                    self._dataBoard.webserver_active = False
                    sleep_secs = 10 #@@@$$$$$
                else:
                    logi(f"MWS@84 STOP THE SERVER - except there is no server running")

            need_to_start = False
            if server is None:
                # No server running. Do we need to start one?  (Can we with what we have?)
                if ipaddr is not None:   # we assume therefore that port != 0:
                    need_to_start = True

            if need_to_start:
                logi(f"MWS@93 (RE)STARTING THE SERVER")
                callbk = self.handle_new_client
                server = await asyncio.start_server(callbk, ipaddr, port)

                self._ipaddr = ipaddr
                self._port = port
                self._dataBoard.webserver_active = True
                sleep_secs = 10
                logi(f"MWS@101 (RE)STARTED THE SERVER  {self._ipaddr} {self._port}")

            if sleep_secs is not None:
                await asyncio.sleep(sleep_secs)


    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###    def OLDCORO(self):
###        server = None
###        while True:
###
###            # If we lose our IP, shut down the server and wait for a new IP.
###            if not ipaddr and self._ipaddr is not None:
###                sleep_secs = 0
###                if server is not None:
###                    logi("MWS@116  LOST WIFI CONNECTION!  closing the server")
###                    await self._close_the_server(server)
###                    sleep_secs = 5
###                server = None
###                self._ipaddr = None
###                self._port = 0
###                self._dataBoard.webserver_active = False
###                if sleep_secs:
###                    await asyncio.sleep(sleep_secs)
###
###            # Did the ip or port change?
###            if ipaddr != self._ipaddr or port != self._port:
###                m = f"MWS@128 IP / PORT changed: old: {self._ipaddr} {self._port}  NEW: {ipaddr} {port}"
###                print(m)
###                logi(m)
###                if server is not None:
###                    logi("MWS@132  IP/PORT CHANGED: closing the server")
###                    await self._close_the_server(server)
###                    server = None
###                    self._dataBoard.webserver_active = False
###
###            logi(f"MWS@137 (RE)Start the server on {ipaddr}:{port}")
###
###            callbk = self.handle_new_client
###            server = await asyncio.start_server(callbk, ipaddr, port)
###
###            self._ipaddr = ipaddr
###            self._port = port
###            self._dataBoard.webserver_active = True
###
###            log(f"MWS@146 webserver_coro: Listening on {self._ipaddr}:{self._port}...")
###            log(f"MWS@147  Server obj is {type(server)}")
###                
###            await asyncio.sleep(5)


    async def _close_the_server(self, server):
        logi(f"MWS@153 CLOSE THE SERVER")
        try:
            server.close()
            logi(f"MWS@156 AWAITING for the SERVER to CLOSE")
            await server.wait_closed()
        except Exception as ex:
            m = f"MWS@159 *ERROR* Closing the server:  {repr(ex)}"
            print(m)
            logi(m)

        ###result = "NO RESULT YET from webserver_coro"
        ###log(f"MWS@164 webserver_coro COMPLETED.  {result=}")
        ###return result

    async def handle_new_client(self, reader, writer):
        m = f"-----"
        print(m); logi(m)
        m = f"MWS@170 =====___ NEW CLIENT  ___+++++___  {get_formatted_date_time_string()}  ___+++++=====__________=====+++++-----+++++====="
        print(m); logi(m)
        m = f"\nMWS@172 handle_new_client  reader={repr(reader)} writer={repr(writer)}  "
        print(m); logi(m)

        try:
            request_stg = await self._read_the_request(reader)

            if not request_stg:
                m = f"MWS@179 FAILED TO READ THE REQUEST!"
                print(m)
                logi(m)
                return

            httpReply = self._handle_the_request(request_stg)
            del request_stg
            
            if httpReply is None:
                mesg = f"MWS@188  FAILED TO HANDLE REQUEST!"
                print(mesg)
                log(mesg)
                return

            m1 = f"MWS@193 HTTP-REPY is {str(httpReply)} "
            m2 = f"MWS@194 ... reply header... --------------------"
            m3 = f"{httpReply.get_header()}"
            m4 = f"MWS@196  --- end of REPLY HEADER ---"  ###  {len(httpReply.get_header())}  -------------------"
            print(m1); print(m2); print(m3); print(m4)
            logi(m1); logi(m2); logi(m3); logi(m4)

            self._write_the_reply(httpReply, writer)

            del httpReply

            await writer.drain()

        except Exception as ex:
            print("MWS@207 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@208 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        finally:
            log("MWS@213 handle_new_client Closing client writer connection")
            writer.close()
            await writer.wait_closed() # Wait until the stream is fully closed
            log("MWS@216 handle_new_client CLIENT WRITER is CLOSED")
            
            log(f"MWS@218 handle_new_client CLOSING THE CLIENT reader")
            reader.close()
            await reader.wait_closed()
            log("MWS@221 handle_new_client CLIENT READER is CLOSED")

        m = f"MWS@223 DONE WITH THIS CLIENT -- RUN THE GC COLLECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(m)
        logi(m)
        gc.collect()
        mf = gc.mem_free()
        m = f"MWS@228 AFTER GC  FREE MEMORY is {mf}"
        print(m)
        logi(m)
        logi(f"MWS@231 handle_new_client done with this client!")


    async def _read_the_request(self, reader):

        hdrAccum = HdrAccum()
        line_num = 0
        header = None
        try:
            while 1:
                #log(f"MWS@241 read_the_request  ======  READ A LINE  =================================")
                new_bytes = await reader.readline()

                if not new_bytes:
                    # Client disconnected
                    log(f"MWS@246 handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                    break
                line_num += 1
                ####m = f"MWS@249 handle_new_client@61 {line_num=} got {len(new_bytes)} bytes. "
                ####print(m);
                ####log(m)
    
                line = new_bytes.decode("utf-8")
                #log(f"MWS@254 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                #log(f"MWS@255 handle_new_client@52 {line_num=} {show_cc(line)}")
                #print(f"MWS@256 handle_new_client@52 {line_num=} got {len(line)} chars. ")
                #print(f"MWS@257 handle_new_client@52 {line_num=} {show_cc(line)}")

                hdrAccum.accum_header_line(line)
                if hdrAccum.found_end_of_header():
                    log(f"MWS@261 >>>--->>>  found EOHdr   hdrlen={len(hdrAccum.get_header())}")
                    header = hdrAccum.get_header()
                    mesg_tail = hdrAccum.get_tail()
                    log(f"MWS@264 {header if header else 'NULL'}")
                    log(f"MWS@265 {mesg_tail if mesg_tail else 'NULL'}")
                    if mesg_tail:
                        ###raise RuntimeError("MWS@267  WE HAVE A mesg_tail: '{mesg_tail}'")
                        logi(f"MWS@268 __WARNING__ we have a mesg_tail {type(mesg_tail)}")
                    #@@TODO@@  Need to handle a leftover tail string - in case of packet breakup by network
                    break
            return header

        except Exception as ex:
            print("MWS@274 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@275 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            ### return None

    def _handle_the_request(self, request_stg):
        log(f"MWS@282 handle_the_request  {len(request_stg)=}")

        reqHandler = RequestHandler()
        httpReply = reqHandler.handle_client_request(request_stg)

        m = f"MWS@287 httpReply: {str(httpReply)}"
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
            print("MWS@305 {'$*$'*35}");print("$*$"*35);print("$*$"*35);print("$*$"*35);
            m = f"MWS@306 handle_new_client **FAILED**  ex={repr(ex)}  ex='{str(ex)}' "
            print(m)
            logi(m)
            raise #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



###
