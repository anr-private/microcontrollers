# ReplyBuilder.py

from utils import *

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
    "  <p>The resource {RESOURCE} you requested has not been found at the specified address.",
    "  Please check the spelling of the address.",
    "  </p>",
    " </body>",
    "</html>"
    ]


class ReplyBuilder:

    def __init__(self, *args):
        self.status_value = STATUS_OK
        self.content_type = CONTENT_HTML
        self.body = ""
        self._reply = None


    def build_page_file_reply(self, file_content):
        # build a reply that contains a /pages/xxx.html etc file body
        self.status_value = STATUS_OK
        self.content_type = CONTENT_HTML
        # a string containing the file content
        self.body = file_content

        reply = self._build_reply()

        print(f"RB.build_page_file_reply:")
        print(f" {reply}")
        return reply


    def build_reply_404(self, resource_not_found):
        self.status_value = STATUS_NO_SUCH_RESOURCE
        self.content_type = CONTENT_HTML
        # provide text - is this needed? esp for favicon.ico  @@@@@@@@@@@@@@@@@@@@@@@@@@@
        valsdict = {"RESOURCE" : resource_not_found}
        fmt_lines = []
        for line in NOT_FOUND_HTML_LINES:
            print(f"@@@RB@57  {line=}  {valsdict=}")
            line.format_map(valsdict)
            fmt_lines.append(line)
        body_lines = add_eol_to_lines(fmt_lines)
        self.body = "".join(body_lines)

        reply = self._build_reply()

        print(f"RB.build_reply_404:")
        print(f" {reply}")
        return reply

    def _build_reply(self):
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
        reply = "".join(lines)
        #for line in lines:
        #    print(f"RB@23@ {show_cc(line)}")
        #print(f"RB@23 {show_cc(reply)}")

        if self.body:
            reply += self.body
        self._reply = reply
        return self._reply

    def __str__(self):
        s = []
        s.append("status=%s" % str(self.status_value))
        s.append(",content=%s" % str(self.content_type))
        if self._body:
            s.append("body.len={len(self._body)}")
        if self._reply:
            s.append("reply.len={len(self._reply)}")
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
