# RequestHandler.py

import asyncio
import gc

from utils import show_len
from utils import get_fs_space_string
from utils import get_memory_status_string

from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib.FileUtils import FileUtils

from .HttpParser import HttpParser
from .ReplyBuilder import ReplyBuilder

# Content-Type values
# application/x-www-form-urlencoded  - posting a FORM(?)
# application/json  - posting JSON data
# multipart/form-data; boundary=--------------------------833994107218074559113347

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class RequestHandler(ElemLoggerABC):
    def __init__(self):
        self.default_file = "/pages/index.html"
        self.default_subdir = "pages"
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsSensors@25 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def handle_client_request(self, header):
        # header is str containing the header lines """
        # returns a reply, suitable for sending back to the client

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)
        ###do_gc("RH@49.after-parser-header")
        if parsed_http is None:
            print(f"RH@51 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error
            
        m1 = f"RH@54 CLIENT REQUEST   parseError: {httpParser.latest_error()}"
        m2 = f"RH@55 {parsed_http.long_string()}"
        #print(m1)
        #print(m2)
        log(m1)
        log(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            ###do_gc("RH@63.after-handle-get-req")
            if reply:
                ###print(f"RH@65 {str(reply)=}")
                return reply

        m = f"RH@68 RequestHandler @ 34 NOT IMPL YET: REQ {parsed_http=}"
        #print(m)
        log(m)
        return None #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            

    def _handle_get_request(self, parsed_http):
        req_url = parsed_http.request_url

        if req_url == "/data":#@@@@@@@@@@@@@@@@@@ data req not impl yet @@@@@@@@@@@@@@@
            pass
        else:
            reply = self._handle_file_request(parsed_http)
            if reply:
                return reply
        logi(f"RH@83  _handle_get_request REPLY=404. CANNOT HANDLE GET-REQ {parsed_http=}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(req_url)
        #log(f"RH@86 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@95 Default file requested") 
            file_path = self.default_file
        
        log(f"RH@98 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fu = FileUtils()
        if not fu.obtain_input_file(file_path, binary=True, prefix_dir=self.default_subdir, w="RH@104"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            log(f"RH@108 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
            ###print(f"RH@109  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = self._guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            log(f"RH@120 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
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
            log(f"RH@132 REPLY WITH 404.  {file_path=}  {content_type=}")
            log(f"RH@133 {m=}")
            ###print(f"RH@134  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        #@@@@@@file_content = self.read_the_page_file(file_path)
        # Read the file
        fu = FileUtils()
        file_content = fu.obtain_input_file(file_path, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@146")

        if file_content is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@152 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@153 {m=}")
            ###print(f"RH@154  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        log(f"RH@157  {file_path=} {content_type=}  len={show_len(file_content)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_content)

        ###print(f"RH@164 RequestHandler._handle_textual_file_request REPLY is ...")
        ###print(f"RH@165: {reply}")
        ###logi(f"RH@166 text-file-REPLY: {reply}")
        return reply


    def _handle_binary_file_request(self, file_path, content_type):

        #@@@@@@file_content = self.read_the_page_file(file_path)
        # Read the file
        fu = FileUtils()
        file_content = fu.obtain_input_file(file_path, 
                binary=True, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@177")

        if file_content is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@183 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@184 {m=}")
            ###print(f"RH@185  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        log(f"RH@188  {file_path=} {content_type=}  len={show_len(file_content)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_content)

        #print(f"RH@195 RequestHandler._handle_file_request REPLY is ...")
        #print(f"RH@196: {reply}")
        return reply


    def _guess_file_content_type(self, file_path):
        # parts is ".../filename", "html" etc
        parts = file_path.rsplit(".", 1)
        #log(f"RH@203 _guess_file_content_type {parts=} {file_path=} ")
        if len(parts) < 2:
            # no extension found
            return None
        ext = parts[1].lower()
        #log(f"RH@208 _guess_file_content_type {ext=} {file_path=} ")
        if ext in ["html", "htm"]:
            #@@@@ maybe use "text/html; charset=UTF-8"?
            t = "text/html"
        elif ext in ["js",]:
            t = "text/javascript"
        elif ext in ["css",]:
            t = "text/css"
        elif ext in ["ico",]:
            t = "image/x-icon"
        elif ext in ["png",]:
            t = "image/png"
        elif ext in ["jpeg", "jpg"]:
            t = "image/jpeg"
        elif ext in ["gif",]:
            t = "image/gif"
        else:
            log(r"RH@225 **ERROR** Unknow Content-Type for file '{file_path}'")
            t = None
        log(f"RH@227 _guess_file_content_type {ext=} {file_path=} guessed-type='{t}'")
        return t

def do_gc(where):
    if 1:
        mss = get_memory_status_string(do_garbage_collect=False)
        print(f"{where} MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
        gc.collect()
        mss = get_memory_status_string(do_garbage_collect=False)
        print(f"{where} MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

###

