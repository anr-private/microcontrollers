# RequestHandlerData.py

import asyncio
import gc
import json

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
from .RequestHandlerLogControl import RequestHandlerLogControl
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


class RequestHandlerData(ElemLoggerABC):
    def __init__(self):
        self.default_file = "/pages/index.htmlp"
        self.default_subdir = "pages"
        self._grinder = TemplateGrinder()
        self._data_board = DataBoard.get_instance()
        self.__rhu = RHUtils()  # just to set up its logging
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def handle_data_request(self, parsed_http):
        params = parsed_http.url_query_parameters

        logi(f"RHD@122  DATA REQ  params={params}")

        #     '{"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}'
        ###json_stg = f'{"age": 1, "name": "Bob", "datetime": {TimeMgr.get_formatted_date_time_string()} }'
        data_dict = {"age": 1, "name": "Bob", "datetime": TimeMgr.get_formatted_date_time_string() }

        if "sensors" in params:
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@self._data_board.set_internal_temps(123.5,87.1)
            degs_f, degs_c = self._data_board.get_internal_temps_one_dec_place()
            data_dict["internal_temp_f"] = degs_f
            data_dict["internal_temp_c"] = degs_c
        if "debug" in params:
            lines = self._data_board.status_lines()
            hlines = "<br>\n".join(lines)
            data_dict["databoard_status"] = hlines
            data_dict["wifi_state"] = str(MwsWifi.state)
        if "settings" in params:
            data_dict["wifi_ip_and_port"] = MwsWifi.get_ip_and_port()

        json_stg = json.dumps(data_dict)
        log(f"RHD@142 body: JSON-string:...")  
        log(json_stg)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = RHUtils.guess_file_content_type("X.json")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, json_stg)

        m = f"RHD@154  HTTP REPLY to DATA REQUEST:"
        logi(m)
        m = f"RHD@156 {reply.long_string()}"
        logi(m)

        return reply

            
    def handle_echo_request(self, parsed_http):
        log(f"RHD@163  _handle_echo_request  ph={parsed_http}")

        params = parsed_http.url_query_parameters

        html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
        "  <title>Echoes the Query Parameters</title>",
        "</head>",
        "<body>",
        f"<h2>Echoed Query Parameters:</h2>",
        "<p> ",
            ]
        html_tail = [
        "  </p>",
        " <p><a href=\"index.htmlp\">BACK</a></p>",
        "</body>",
        "</html>",
            ]

        params_lines = []
        for k,v in params.items():
            line = f" &nbsp; {k}  {v}  <br>"
            params_lines.append(line)
       
        html_lines.extend(params_lines)
        html_lines.extend(html_tail)
        body_string = "\n".join(html_lines)
        del html_lines

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = RHUtils.guess_file_content_type("X.html")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, body_string)

        m = f"RHD@205 HTTP REPLY to ECHO request "
        logi(m)
        m = f"RHD@207  {reply.long_string()}"
        logi(m)
        return reply





#def do_gc(where):
#    if 1:
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
#        gc.collect()
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

###

