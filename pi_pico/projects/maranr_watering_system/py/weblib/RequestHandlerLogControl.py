# RequestHandlerLogControl.py
#
# Requests and replies for controlling logging and loggers


import asyncio
import gc
import json

from utils import show_len
from utils import get_fs_space_string
from utils import get_memory_status_string
from utils import get_formatted_date_time_string

from logger_elem.ElemLoggerABC import ElemLoggerABC
from logger_elem.ElemLogControl import ElemLogControl
from lib2.FileObtainer import FileObtainer
from lib2.DataBoard import DataBoard
from lib2.MwsWifi import MwsWifi

from .HttpParser import HttpParser
from .ReplyBuilder import ReplyBuilder
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


class RequestHandlerLogControl(ElemLoggerABC):
    def __init__(self):
        self.default_file = "/pages/index.htmlp"
        self.default_subdir = "pages"
        self._grinder = TemplateGrinder()
        self._data_board = DataBoard.get_instance()
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsSensors@25 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def handle_log_request(self, parsed_http):
        log(f"RHLOG@199  _handle_log_request  ph={parsed_http}")

        params = parsed_http.url_query_parameters

        if "settings" in params:
            return self._handle_log_settings_request(parsed_http, params)


        rel_line_number_stg = params.get("linenumber")
        num_lines_stg = params.get("numlines")
        if rel_line_number_stg is None: rel_line_number_stg = "40"
        if num_lines_stg is None: num_lines_stg = rel_line_number_stg

        try:
            relative_line_number = int(rel_line_number_stg)
            numlines = int(num_lines_stg)
        except (TypeError,ValueError) as ex:
            m = f"RHLOG@212 Failed to convert params {params=} to int {parsed_http.request_url} ex={ex}"
            print(m)
            logi(m)
            #return None
            # use some defaults
            relative_line_number = 20
            numlines = 20
        print(f"RHLOG@219  {relative_line_number=}  {numlines=}")
        elc = self._get_control_instance()

        lines = elc.get_lines_from_log_file(relative_line_number, numlines)
        print(f"RHLOG@223 len={len(lines) if lines is not None else 'no-lines!'} {lines=}")
        if lines is None: return None


        html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>Logger File Lines</title>",
        "</head>",
        "<body>",
        f"LOG LINES   -{relative_line_number} to -{(relative_line_number-numlines+1)} &nbsp;  at end of log file.<br>",
        "<p> ",
           " &nbsp; <a href=\"log?linenumber=40&numlines=40\">last-40 to end-of-log</a> "
           " &nbsp; <a href=\"log?linenumber=80&numlines=40\">-80 to -40</a>",
           " &nbsp; <a href=\"log?linenumber=120&numlines=40\">-120 to -80</a>",
           " &nbsp; <a href=\"log?linenumber=160&numlines=40\">-160 to -120</a>",
        "</p>",
            ]
        html_tail = [
        "  </p>",
        " <p><a href=\"index.htmlp\">BACK</a></p>",
        "</body>",
        "</html>",
            ]

        for line in lines:
            line = line.replace('\n', '')
            line += "<br>"
            html_lines.append(line)
        lines = None
        html_lines.extend(html_tail)
        body_string = "\n".join(html_lines)
        del html_lines

        print(f"RHLOG@258 body_string:...")  
        print(body_string)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = RHUtils.guess_file_content_type("X.html")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, body_string)

        m = f"RHLOG@270 HTTP REPLY to LOG request "
        print(m)
        logi(m)
        m = f"RHLOG@273  {reply.long_string()}"
        print(m)
        logi(m)
        return reply


    def _handle_log_settings_request(self, parsed_http, params):
        # JSON request  EX: /log?settings&whatever=123
        print(f"RHLOG@303 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOG SETTINGS")
        print(f"RHLOG@303 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOG SETTINGS")
        print(f"RHLOG@303 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOG SETTINGS")
        print(f"RHLOG@303 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOG SETTINGS")
        print(f"RHLOG@303 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOG SETTINGS")

        print(f"RHLOG@118  LOG-SETTINGS-REQ  params={params}")

        data_dict = {"datetime": get_formatted_date_time_string() }

        classes = ElemLogControl.get_instance().get_registered_classes()
        classes_dict = dict()
        i = 0
        for class_name in classes:
            classes_dict[class_name] = i
            i += 1
        data_dict["classes"] = classes_dict

        json_stg = json.dumps(data_dict)
        print(f"RHLOG@315 body: JSON-string:...")  
        print(json_stg)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = RHUtils.guess_file_content_type("X.json")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, json_stg)

        m = f"RHLOG@327  HTTP REPLY to DATA REQUEST:"
        print(m)
        logi(m)
        m = f"RHLOG@330 {reply.long_string()}"
        print(m)
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

