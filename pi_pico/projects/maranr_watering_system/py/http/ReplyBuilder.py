# ReplyBuilder.py

from utils import *

from http.HttpReply import HttpReply

HTTP_PROTOCOL = "HTTP/1.1"
SERVER_ID = "Pico Watering System"

STATUS_OK = 200
STATUS_NO_SUCH_RESOURCE = 404

CONTENT_HTML = "text/html"

NOT_FOUND_HTML_LINES = [
    "<html>",
    "<head>",
    "<title>Resource Not Found</title>",
    "</head>",
    " <body>",
    "  <p>The requested resource {RESOURCE} Resource cannot be found.",
    "  Please check the URL.",
    "  </p>",
    " </body>",
    "</html>"
    ]


class ReplyBuilder:

    def __init__(self, *args):
        self.status_value = STATUS_OK
        self.content_type = CONTENT_HTML
        self.body = ""
        #@@@@@@@@@@@self._reply = None


    def build_textual_file_reply(self, content_type, body_string):
        # build a reply that contains a textual body (ie not binary)
        # Ex: /pages/xxx.html,css,js, etc. The body is a str.
        self.status_value = STATUS_OK
        self.content_type = content_type
        # a string containing the file content
        self.body = body_string

        reply = self._build_reply()

        dbg(f"RB@48 build_textual_file_reply: {str(reply)}")
        return reply


    def build_binary_file_reply(self, content_type, body_bytes):
        # build a reply that contains a textual body (ie not binary)
        # Ex: /pages/xxx.html,css,js, etc. The body is a str.
        self.status_value = STATUS_OK
        self.content_type = content_type
        # a string containing the file content
        self.body = body_bytes

        reply = self._build_reply()

        dbg(f"RB@62.build_binary_file_reply: {str(reply)}")
        return reply


    def build_reply_404(self, resource_not_found):
        self.status_value = STATUS_NO_SUCH_RESOURCE
        self.content_type = CONTENT_HTML
        # provide text - is this needed? esp for favicon.ico  @@@@@@@@@@@@@@@@@@@@@@@@@@@
        valsdict = {"RESOURCE" : resource_not_found}
        fmt_lines = []
        for line in NOT_FOUND_HTML_LINES:
            dbg(f"RB@73  {line=}  {valsdict=}")
            fmt_line = line.format(**valsdict)
            dbg(f"RB@75  {fmt_line=}  {valsdict=}")
            fmt_lines.append(fmt_line)
        body_lines = add_eol_to_lines(fmt_lines)
        self.body = "".join(body_lines)

        reply = self._build_reply()

        dbg(f"RB@82.build_reply_404: {str(reply)}")
        return reply

    def _build_reply(self):
        # returns HttpReply
        status_stg = status_string_from_value(self.status_value)
        lines = []
        lines.append(f"{HTTP_PROTOCOL} {self.status_value} {status_stg}")  
        lines.append(f"Server: {SERVER_ID}")
        lines.append(f"Content-Type: {self.content_type}")
        lines.append(f"Connection: Closed")
        if len(self.body) > 0:
            lines.append(f"Content-Length: {len(self.body)}")
        lines.append("") # end-of-header
        lines = add_eol_to_lines(lines)
        header_stg = "".join(lines)
        #for line in lines:
        #    dbg(f"RB@99 {show_cc(line)}")
        #dbg(f"RB@100 {show_cc(reply)}")

        reply = HttpReply()
        reply.set_reply(header_stg, self.body)
        self._reply = reply
        return self._reply

    def __str__(self):
        s = []
        s.append("status=%s" % str(self.status_value))
        s.append(",content=%s" % str(self.content_type))
        if self._body:
            s.append("body.len={len(self._body)}")
        #if self._reply:
        #    s.append("reply.len={len(self._reply)}")
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))

def status_string_from_value(status_value):
    status_strings = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found"
    }
    if status_value in status_strings:
        return status_strings[status_value]
    return "Invalid Status"

def add_eol_to_lines(lines):
    results = []
    for line in lines:
        results.append(line+"\r\n")
    return results

###
