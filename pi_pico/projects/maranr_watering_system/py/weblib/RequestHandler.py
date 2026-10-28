# RequestHandler.py

import asyncio
import gc
import json

try: from typing import Any
except ImportError: pass

from lib1.utils import gc_collect
from lib1.utils import len_to_str
from lib1.utils import get_fs_space_string
from lib1.utils import get_memory_status_string

from logger_elem.ElemLoggerABC import ElemLoggerABC
from logger_elem.ElemLogControl import ElemLogControl
from lib2.FileObtainer import FileObtainer
from lib2.DataBoard import DataBoard
from lib2.MwsWifi import MwsWifi
from lib2.TimeMgr import TimeMgr

from .HttpParser import HttpParser
from .ReplyBuilder import ReplyBuilder
from .RequestHandlerLog import RequestHandlerLog
from .RequestHandlerData import RequestHandlerData
from .TemplateGrinder import TemplateGrinder
from .RHUtils import RHUtils

# Content-Type values
# application/x-www-form-urlencoded  - posting a FORM(?)
# application/json  - posting JSON data
# multipart/form-data; boundary=--------------------------833994107218074559113347

# Logging functions; our parent class sets using _set_logger()
log:   Any = None
logrt: Any = None
logi:  Any = None


class RequestHandler(ElemLoggerABC):
    def __init__(self):
        self.default_file = "/pages/index.htmlp"
        self.default_subdir = "pages"
        self._grinder = TemplateGrinder.get_instance()
        self._databoard = DataBoard.get_instance()
        self._rh_data = RequestHandlerData()
        self._rh_log = RequestHandlerLog()
        self.__rhu = RHUtils()  # just to set up its logging
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def handle_client_request(self, header):
        # header is str containing the header lines """
        # returns a reply, suitable for sending back to the client

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        LL=log

        m = f"RH@66 ^^^^^  HANDLE NEW CLIENT REQUEST  ^^^^^^  {TimeMgr.get_formatted_date_time_string()} ^^^^^^^^^^^^^"
        LL(m)
        m = f"RH@68  -=-=-=  run lib/gc_collect()  -=-=-= "
        LL(m)
        gc_collect()

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)
        ###do_gc("RH@75.after-parser-header")
        if parsed_http is None:
            print(f"RH@77 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            logi(f"RH@78 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error TODO
        logi(f"RH@80 PARSED-REQUEST: {str(parsed_http)}")
        m1 = f"RH@81 CLIENT REQUEST   latest-parse-err: '{httpParser.latest_error()}' "
        m2a = parsed_http.long_str(sep="\nRH@82")
        m2 = f"RH@83 {m2a}"
        LL(m1); LL(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            if reply:
                return reply

        m = f"RH@91 RequestHandler REQUEST {parsed_http=} NOT IMPL YET.  TODO @@@ "
        logi(m)
        print(m)

        rb = ReplyBuilder()
        reply = rb.build_reply_404(parsed_http.url_path)
        logi(f"RH@97 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_get_request(self, parsed_http):
        # get just the /w/x/z without the ?parm=213&...
        url_path = parsed_http.url_path

        if url_path == "/data":
            log(f"RH@106  DATA request: {parsed_http}")
            reply = self._rh_data.handle_data_request(parsed_http)
            if reply: return reply
        elif url_path == "/log":
            log(f"RH@110  LOG request: {parsed_http}")
            reply = self._rh_log.handle_log_request(parsed_http)
            if reply: return reply
        elif url_path == "/echo":
            log(f"RH@114  ECHO request: {parsed_http}")
            reply = self._rh_data.handle_echo_request(parsed_http)
            if reply: return reply
        else:
            reply = self._handle_file_request(parsed_http)
            if reply: return reply
        # if fall through, we don't know how to handle
        logi(f"RH@121  _handle_get_request REPLY=404. CANNOT HANDLE GET-REQ {parsed_http}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        #log(f"RH@124 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply


    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@133 Default file requested") 
            file_path = self.default_file
        
        log(f"RH@136 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fu = FileObtainer()
        if not fu.obtain_input_file(file_path, binary=True, prefix_dir=self.default_subdir, w="RH@142"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            log(f"RH@146 REPLY WITH 404. '{m}' {file_path=}  len={len_to_str(reply)}")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = RHUtils.guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            log(f"RH@157 REPLY WITH 404. '{m}' {file_path=}  len={len_to_str(reply)}")
            return reply

        # handle the file depending on its Content-Type
        if content_type in ["text/html","text/css", "text/javascript" ]:
            reply = self._handle_textual_file_request(file_path, content_type)
        elif content_type in ["image/x-icon","image/png", "image/gif", "image/jpeg"]:
            reply = self._handle_binary_file_request(file_path, content_type)
        else:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to build a Reply."
            reply = rb.build_reply_404(m)
            log(f"RH@169 REPLY WITH 404.  {file_path=}  {content_type=}")
            log(f"RH@170 {m=}")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        # Read the file
        fu = FileObtainer()
        file_contents = fu.obtain_input_file(file_path, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@181")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@187 REPLY WITH 404.  {file_path=}  len={len_to_str(reply)}")
            log(f"RH@188 {m=}")
            return reply

        log(f"RH@191  {file_path=} {content_type=}  len={len_to_str(file_contents)}")
        
        if file_path.lower().endswith(".htmlp"):
            updated_file_contents = self._grinder.grind_file_contents(file_contents)
            if updated_file_contents is not None:
                file_contents = updated_file_contents
                del updated_file_contents
                gc.collect()  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_contents)

        return reply


    def _handle_binary_file_request(self, file_path, content_type):

        # Read the file
        fu = FileObtainer()
        file_contents = fu.obtain_input_file(file_path, 
                binary=True, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@214")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@220 REPLY WITH 404.  {file_path=}  len={len_to_str(reply)}")
            log(f"RH@221 {m=}")
            return reply

        log(f"RH@224  {file_path=} {content_type=}  len={len_to_str(file_contents)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_contents)

        return reply



#def do_gc(where):
#    if 1:
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
#        gc.collect()
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

###

