# ParsedHttp.py

from utils import *

METHOD_NAMES = ("GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE")

class ParsedHttp:
    """ parsed HTTP mesg 
    Commonly:  ph = ParsedHttp(...)
    """

    def __init__(self):
        """ """

        ###@@@self.latest_error = ""

        # first line of the mesg. It's either a request or reply.
        
        # Ex:
        # Request GET / HTTP/1.1
        #         POST /api/users HTTP/1.1
        # Reply ex: HTTP/1.0 200 OK 

        self.start_line = None

        # True if this is a request; False if a reply
        # None if not yet set; if so, accessing raises exception
        self.request_flag = None

        # Method from start line. Allowable:
        # GET  HEAD  POST  PUT  DELETE  CONNECT  OPTIONS  TRACE
        self.method = None

        # "1.1", etc
        self.http_version = None

        # requested action 'GET', "POST', etc
        self.action = None
        # requested URL
        self.request_url = None

        # Reply code is "200", "404", etc.  Reply error codes numbers, as STRING
        self.reply_code = None
        # 'OK', etc.  Reply code as a string, per the reply header.
        self.reply_stg = None

        # 'raw' field values
        # Ex: 
        #  "Server"        "SimpleHTTP/0.6 Python/3.12.3"
        #  "Date"          "Sat, 07 Feb 2026 01:36:36 GMT"
        #  "Content-type"  "image/vnd.microsoft.icon"
        #  "Content-Length" "15086"
        #  "Last-Modified"  "Fri, 06 Feb 2026 02:51:34 GMT
        self._fields = {}

    def is_request_method(self, meth_name):
        """ Returns True if the arg is a known method name """
        return meth_name in METHOD_NAMES

    #@@@@@@@@@@@
    def set_as_request(self, action_stg, request_url, http_version):
        """ This is a REQUEST mesg """
        self.request_flag = True
        self.action = action_stg
        self.request_url = request_url
        self.http_version = http_version

    def set_as_reply(self, http_version, reply_code, reply_stg):
        """ This is a REPLY mesg """
        self.request_flag = False
        self.http_version = http_version
        self.reply_code = reply_code
        self.reply_stg = reply_stg

    def is_request(self):
        if self.request_flag is None:
            e = "ParsedHttp.is_request called but flag has not been set yet."
            #raise RuntimeError(e)
            #@@@@ temp: later, convert back to RuntimeError

            print("*********INTERNAL-ERROR**** "+e)
        return self.request_flag

    def is_reply(self):
        return not self.is_request()


    def add_field(self, field_name, field_value):
        if len(field_name) <= 0:
            raise ValueError("ParsedHttp.add_field Empty field name. Field-value '{}'")
        self._fields[field_name] = field_value

    def get_field(self, field_name):
        if field_name not in self._fields:
            raise KeyError(f"ParsedHttp.get_field NO SUCH FIELD '{field_name}'")
        return self._fields[field_name]


    def __str__(self):
        s = []
        s.append("requestFlag=%s" % ("REQ" if self.request_flag else "REPLY"))
        s.append("method=%s" % str(self.method))
        s.append("httpVersion=%s" % str(self.http_version))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


    def long_str(self):
        lines = []
        lines.append(f"{self.__class__.__name__}:")

        s = []
        s.append("  requestFlag=%s" % ("REQ" if self.request_flag else "REPLY"))
        s.append("method=%s" % str(self.method))
        s.append("httpVersion=%s" % str(self.http_version))
        lines.append(" ".join(s))

        for field_name in sorted(self._fields):
            s = f"  {field_name}: '{self._fields[field_name]}'"
            lines.append(s)

        return "\n".join(lines)
    long_string = long_str


### end ###
