# RequestHandler.py
#
# LINEMARKER=HRQH

import asyncio
import gc
import json

try: from typing import Any
except ImportError: pass

from lib1.utils import len_to_str
from lib1.gc_utils import gc_collect, get_memory_status_string
from lib1.file_system_utils import get_fs_space_string

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

        m = f"HRQH$67 ^^^^^  HANDLE NEW CLIENT REQUEST  ^^^^^^  {TimeMgr.get_formatted_date_time_string()} ^^^^^^^^^^^^^"
        LL(m)
        m = f"HRQH$69  -=-=-=  run lib/gc_collect()  -=-=-= "
        LL(m)
        gc_collect()

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)
        ###do_gc("HRQH$76.after-parser-header")
        if parsed_http is None:
            print(f"HRQH$78 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            logi(f"HRQH$79 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error TODO
        logi(f"HRQH$81 PARSED-REQUEST: {str(parsed_http)}")
        m1 = f"HRQH$82 CLIENT REQUEST   latest-parse-err: '{httpParser.latest_error()}' "
        m2a = parsed_http.long_str(sep="\n"+"HRQH$83")
        m2 = f"HRQH$84 {m2a}"
        LL(m1); LL(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            if reply:
                return reply

        m = f"HRQH$92 RequestHandler REQUEST {parsed_http=} NOT IMPL YET.  TODO @@@ "
        logi(m)
        print(m)

        rb = ReplyBuilder()
        reply = rb.build_reply_404(parsed_http.url_path)
        logi(f"HRQH$98 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_get_request(self, parsed_http):
        # get just the /w/x/z without the ?parm=213&...
        url_path = parsed_http.url_path

        if url_path == "/data":
            log(f"HRQH$107  DATA request: {parsed_http}")
            reply = self._rh_data.handle_data_request(parsed_http)
            if reply: return reply
        elif url_path == "/log":
            log(f"HRQH$111  LOG request: {parsed_http}")
            reply = self._rh_log.handle_log_request(parsed_http)
            if reply: return reply
        elif url_path == "/echo":
            log(f"HRQH$115  ECHO request: {parsed_http}")
            reply = self._rh_data.handle_echo_request(parsed_http)
            if reply: return reply
        else:
            reply = self._handle_file_request(parsed_http)
            if reply: return reply
        # if fall through, we don't know how to handle
        logi(f"HRQH$122  _handle_get_request REPLY=404. CANNOT HANDLE GET-REQ {parsed_http}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        #log(f"HRQH$125 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply


    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"HRQH$134 Default file requested") 
            file_path = self.default_file
        
        log(f"HRQH$137 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fob = FileObtainer()
        if not fob.obtain_entire_binary_file_contents(
                                            file_path, 
                                            prefix_dir=self.default_subdir, 
                                            w="HRQH$146"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            log(f"HRQH$150 REPLY WITH 404. '{m}' {file_path=}  len={len_to_str(reply)}")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = RHUtils.guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            log(f"HRQH$161 REPLY WITH 404. '{m}' {file_path=}  len={len_to_str(reply)}")
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
            log(f"HRQH$173 REPLY WITH 404.  {file_path=}  {content_type=}")
            log(f"HRQH$174 {m=}")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        # Read the file
        fob = FileObtainer()
        file_contents = fob.obtain_entire_text_file_contents(
                                            file_path, 
                                            prefix_dir=self.default_subdir, 
                                            w="HRQH$187")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"HRQH$193 REPLY WITH 404.  {file_path=}  len={len_to_str(reply)}")
            log(f"HRQH$194 {m=}")
            return reply

        log(f"HRQH$197  {file_path=} {content_type=}  len={len_to_str(file_contents)}")
        
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
        fob = FileObtainer()
        file_contents = fob.obtain_entire_binary_file_contents(
                                                file_path, 
                                                prefix_dir=self.default_subdir, 
                                                w="HRQH$221")
        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"HRQH$226 REPLY WITH 404.  {file_path=}  len={len_to_str(reply)}")
            log(f"HRQH$227 {m=}")
            return reply

        log(f"HRQH$230  {file_path=} {content_type=}  len={len_to_str(file_contents)}")
        
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

