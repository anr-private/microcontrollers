# RequestHandler.py

import asyncio
import gc

from utils import show_len
from utils import get_fs_space_string
from utils import get_memory_status_string
from utils import get_formatted_date_time_string

from logger_elem.ElemLoggerABC import ElemLoggerABC
from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib2.FileObtainer import FileObtainer

from .HttpParser import HttpParser
from .ReplyBuilder import ReplyBuilder
from .TemplateGrinder import TemplateGrinder

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
        self._templateGrinder = TemplateGrinder()
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

        m = f"RH@50 ^^^^^  HANDLE NEW CLIENT REQUEST  ^^^^^^  {get_formatted_date_time_string()} ^^^^^^^^^^^^^"
        print(m)
        logi(m)
        m = f"RH@53  -=-=-=  do gc.collect()  -=-=-= "
        print(m)
        logi(m)
        gc.collect()

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)
        ###do_gc("RH@61.after-parser-header")
        if parsed_http is None:
            print(f"RH@63 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error
        m1 = f"RH@65 CLIENT REQUEST   latest-parse-err: '{httpParser.latest_error()}' "
        m2 = f"RH@66 {parsed_http.long_string()}"
        #print(m1)
        #print(m2)
        logi(m1)
        logi(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            ###do_gc("RH@74.after-handle-get-req")
            if reply:
                ###print(f"RH@76 {str(reply)=}")
                return reply

        m = f"RH@79 RequestHandler REQUEST {parsed_http=} NOT IMPL YET."
        logi(m)
        print(m)
        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        #log(f"RH@84 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_get_request(self, parsed_http):
        # get just the /w/x/z without the ?parm=213&...
        url_path = parsed_http.url_path

        if url_path == "/data":
            print(f"RH@93  DATA request: {parsed_http}")
            reply = self._handle_data_request(parsed_http)
            if reply: return reply
        elif url_path == "/log":
            print(f"RH@97  LOG request: {parsed_http}")
            reply = self._handle_log_request(parsed_http)
            if reply: return reply
        elif url_path == "/echo":
            print(f"RH@101  ECHO request: {parsed_http}")
            reply = self._handle_echo_request(parsed_http)
            if reply: return reply
        else:
            reply = self._handle_file_request(parsed_http)
            if reply: return reply
        # if fall through, we don't know how to handle
        logi(f"RH@108  _handle_get_request REPLY=404. CANNOT HANDLE GET-REQ {parsed_http}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(url_path)
        #log(f"RH@111 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply


    def _handle_data_request(self, parsed_http):
        params = parsed_http.url_query_parameters

        print(f"RH@118  DATA REQ  params={params}")

        #     '{"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}'
        json_stg = '{"age": 1, "name": "Bob"}'

        print(f"RH@123 body: JSON-string:...")  
        print(json_stg)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = self._guess_file_content_type("X.json")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, json_stg)

        m = f"RH@135  HTTP REPLY to DATA REQUEST:"
        print(m)
        logi(m)
        m = f"RH@135 {reply.long_string()}"
        print(m)
        logi(m)

        return reply

            
    def _handle_echo_request(self, parsed_http):
        log(f"RH@143  _handle_echo_request  ph={parsed_http}")

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

        #print(f"RH@174 body_string:...")  
        #print(body_string)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = self._guess_file_content_type("X.html")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, body_string)

        m = f"RH@186 HTTP REPLY to ECHO request "
        print(m)
        logi(m)
        m = f"RH@186  {reply.long_string()}"
        print(m)
        logi(m)
        return reply


    def _handle_log_request(self, parsed_http):
        log(f"RH@199  _handle_log_request  ph={parsed_http}")

        params = parsed_http.url_query_parameters

        rel_line_number_stg = params.get("linenumber")
        num_lines_stg = params.get("numlines")
        if rel_line_number_stg is None: rel_line_number_stg = "40"
        if num_lines_stg is None: num_lines_stg = rel_line_number_stg

        try:
            relative_line_number = int(rel_line_number_stg)
            numlines = int(num_lines_stg)
        except (TypeError,ValueError) as ex:
            m = f"RH@212 Failed to convert params {params=} to int {parsed_http.request_url} ex={ex}"
            print(m)
            logi(m)
            #return None
            # use some defaults
            relative_line_number = 20
            numlines = 20
        print(f"RH@219  {relative_line_number=}  {numlines=}")
        elc = self._get_control_instance()

        lines = elc.get_lines_from_log_file(relative_line_number, numlines)
        print(f"RH@223 len={len(lines) if lines is not None else 'no-lines!'} {lines=}")
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

        print(f"RH@258 body_string:...")  
        print(body_string)

        # Build a reply that provides the log lines
        rb = ReplyBuilder()

        # use html's content type
        content_type = self._guess_file_content_type("X.html")

        # content type: use 
        reply = rb.build_textual_file_reply(content_type, body_string)

        m = f"RH@270 HTTP REPLY to LOG request "
        print(m)
        logi(m)
        m = f"RH@273  {reply.long_string()}"
        print(m)
        logi(m)
        return reply


        return reply


    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@280 Default file requested") 
            file_path = self.default_file
        
        log(f"RH@283 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fu = FileObtainer()
        if not fu.obtain_input_file(file_path, binary=True, prefix_dir=self.default_subdir, w="RH@289"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            log(f"RH@293 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = self._guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            log(f"RH@304 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
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
            log(f"RH@316 REPLY WITH 404.  {file_path=}  {content_type=}")
            log(f"RH@317 {m=}")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        # Read the file
        fu = FileObtainer()
        file_contents = fu.obtain_input_file(file_path, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@328")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@334 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@335 {m=}")
            return reply

        log(f"RH@338  {file_path=} {content_type=}  len={show_len(file_contents)}")
        
        if file_path.lower().endswith(".htmlp"):
            updated_file_contents = self._templateGrinder.grind_file_contents(file_contents)
            if updated_file_contents is not None:
                file_contents = updated_file_contents
                del updated_file_contents
                gc.collect()  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_contents)

        ###print(f"RH@352 RequestHandler._handle_textual_file_request REPLY is ...")
        ###print(f"RH@353: {reply}")
        ###logi(f"RH@354 text-file-REPLY: {reply}")
        return reply


    def _handle_binary_file_request(self, file_path, content_type):

        # Read the file
        fu = FileObtainer()
        file_contents = fu.obtain_input_file(file_path, 
                binary=True, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@364")

        if file_contents is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            log(f"RH@370 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            log(f"RH@371 {m=}")
            return reply

        log(f"RH@374  {file_path=} {content_type=}  len={show_len(file_contents)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_contents)

        #print(f"RH@381 RequestHandler._handle_file_request REPLY is ...")
        #print(f"RH@382: {reply}")
        return reply


    def _guess_file_content_type(self, file_path):
        # parts is ".../filename", "html" etc
        parts = file_path.rsplit(".", 1)
        #log(f"RH@389 _guess_file_content_type {parts=} {file_path=} ")
        if len(parts) < 2:
            # no extension found
            return None
        ext = parts[1].lower()
        #log(f"RH@394 _guess_file_content_type {ext=} {file_path=} ")
        if ext in ["html", "htm", "htmlp"]:
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
        elif ext in ["json",]:
            t = "application/json"
        else:
            log(r"RH@413 **ERROR** Unknow Content-Type for file '{file_path}'")
            t = None
        log(f"RH@415 _guess_file_content_type {ext=} {file_path=} guessed-type='{t}'")
        return t

#def do_gc(where):
#    if 1:
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
#        gc.collect()
#        mss = get_memory_status_string(do_garbage_collect=False)
#        print(f"{where} MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

###

