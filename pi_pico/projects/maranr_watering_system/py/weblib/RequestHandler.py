# RequestHandler.py

import asyncio
import gc
import json

from lib import gc_collect
from utils import show_len
from utils import get_fs_space_string
from utils import get_memory_status_string

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

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class RequestHandler(ElemLoggerABC):
    def __init__(self):
        self.default_file = "/pages/index.htmlp"
        self.default_subdir = "pages"
        self._grinder = TemplateGrinder.get_instance()
        self._data_board = DataBoard.get_instance()
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

        m = f"RH@59 ^^^^^  HANDLE NEW CLIENT REQUEST  ^^^^^^  {TimeMgr.get_formatted_date_time_string()} ^^^^^^^^^^^^^"
        logi(m)
        m = f"RH@61  -=-=-=  run lib/gc_collect()  -=-=-= "
        logi(m)
        gc_collect()

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)
        ###do_gc("RH@68.after-parser-header")
        if parsed_http is None:
            print(f"RH@70 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            logi(f"RH@71 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error TODO
        m1 = f"RH@73 CLIENT REQUEST   latest-parse-err: '{httpParser.latest_error()}' "
        m2 = f"RH@74 {parsed_http.long_string()}"
        logi(m1); logi(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            ###do_gc("RH@79.after-handle-get-req")
            if reply:
                ###print(f"RH@81 {str(reply)=}")
                return reply

        m = f"RH@84 RequestHandler REQUEST {parsed_http=} NOT IMPL YET."
        logi(m)
        print(m)

        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        logi(f"RH@90 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_get_request(self, parsed_http):
        # get just the /w/x/z without the ?parm=213&...
        url_path = parsed_http.url_path

        if url_path == "/data":
            log(f"RH@99  DATA request: {parsed_http}")
            reply = self._rh_data.handle_data_request(parsed_http)
            if reply: return reply
        elif url_path == "/log":
            log(f"RH@103  LOG request: {parsed_http}")
            reply = self._rh_log.handle_log_request(parsed_http)
            if reply: return reply
        elif url_path == "/echo":
            log(f"RH@107  ECHO request: {parsed_http}")
            reply = self._rh_data.handle_echo_request(parsed_http)
            if reply: return reply
        else:
            reply = self._handle_file_request(parsed_http)
            if reply: return reply
        # if fall through, we don't know how to handle
        logi(f"RH@114  _handle_get_request REPLY=404. CANNOT HANDLE GET-REQ {parsed_http}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        #log(f"RH@117 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply


#    def _handle_data_request(self, parsed_http):
#        params = parsed_http.url_query_parameters
#
#        logi(f"RH@124  DATA REQ  params={params}")
#
#        #     '{"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}'
#        ###json_stg = f'{"age": 1, "name": "Bob", "datetime": {TimeMgr.get_formatted_date_time_string()} }'
#        data_dict = {"age": 1, "name": "Bob", "datetime": TimeMgr.get_formatted_date_time_string() }
#
#        if "sensors" in params:
#            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@self._data_board.set_internal_temps(123.5,87.1)
#            degs_f, degs_c = self._data_board.get_internal_temps_one_dec_place()
#            data_dict["internal_temp_f"] = degs_f
#            data_dict["internal_temp_c"] = degs_c
#        if "debug" in params:
#            lines = self._data_board.status_lines()
#            hlines = "<br>\n".join(lines)
#            data_dict["databoard_status"] = hlines
#            data_dict["wifi_state"] = str(MwsWifi.state)
#        if "settings" in params:
#            data_dict["wifi_ip_and_port"] = MwsWifi.get_ip_and_port()
#
#        json_stg = json.dumps(data_dict)
#        log(f"RH@144 body: JSON-string:...")  
#        log(json_stg)
#
#        # Build a reply that provides the log lines
#        rb = ReplyBuilder()
#
#        # use html's content type
#        content_type = RHUtils.guess_file_content_type("X.json")
#
#        # content type: use 
#        reply = rb.build_textual_file_reply(content_type, json_stg)
#
#        m = f"RH@156  HTTP REPLY to DATA REQUEST:"
#        logi(m)
#        m = f"RH@158 {reply.long_string()}"
#        logi(m)
#
#        return reply
#
#            
#    def _handle_echo_request(self, parsed_http):
#        log(f"RH@165  _handle_echo_request  ph={parsed_http}")
#
#        params = parsed_http.url_query_parameters
#
#        html_lines = [
#        "<!DOCTYPE html>",
#        "<html>",
#        "<head>",
#        "  <meta charset=\"UTF-8\">",
#        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
#        "  <title>Echoes the Query Parameters</title>",
#        "</head>",
#        "<body>",
#        f"<h2>Echoed Query Parameters:</h2>",
#        "<p> ",
#            ]
#        html_tail = [
#        "  </p>",
#        " <p><a href=\"index.htmlp\">BACK</a></p>",
#        "</body>",
#        "</html>",
#            ]
#
#        params_lines = []
#        for k,v in params.items():
#            line = f" &nbsp; {k}  {v}  <br>"
#            params_lines.append(line)
#       
#        html_lines.extend(params_lines)
#        html_lines.extend(html_tail)
#        body_string = "\n".join(html_lines)
#        del html_lines
#
#        # Build a reply that provides the log lines
#        rb = ReplyBuilder()
#
#        # use html's content type
#        content_type = RHUtils.guess_file_content_type("X.html")
#
#        # content type: use 
#        reply = rb.build_textual_file_reply(content_type, body_string)
#
#        m = f"RH@207 HTTP REPLY to ECHO request "
#        logi(m)
#        m = f"RH@209  {reply.long_string()}"
#        logi(m)
#        return reply


    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@219 Default file requested") 
            file_path = self.default_file
        
        log(f"RH@222 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fu = FileObtainer()
        if not fu.obtain_input_file(file_path, binary=True, prefix_dir=self.default_subdir, w="RH@228"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            log(f"RH@232 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = RHUtils.guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            log(f"RH@243 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
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
            log(f"RH@255 REPLY WITH 404.  {file_path=}  {content_type=}")
            log(f"RH@256 {m=}")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        # Read the file
        fu = FileObtainer()
        file_contents = fu.obtain_input_file(file_path, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@267")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@273 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@274 {m=}")
            return reply

        log(f"RH@277  {file_path=} {content_type=}  len={show_len(file_contents)}")
        
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
                prefix_dir=self.default_subdir, w="RH@300")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@306 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@307 {m=}")
            return reply

        log(f"RH@310  {file_path=} {content_type=}  len={show_len(file_contents)}")
        
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

