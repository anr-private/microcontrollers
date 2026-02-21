# ParsedHttp.py

from utils import *

METHOD_NAMES = ("GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE")

# Example ParsedHttp  long_string():
#  requestFlag=REQ method=GET req-url=/ httpVersion=1.1
#  Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#  Accept-Encoding: 'gzip, deflate'
#  Accept-Language: 'en-US,en;q=0.9'
#  Cache-Control: 'no-cache'
#  Connection: 'keep-alive'
#  Host: '192.168.1.49:8000'
#  Pragma: 'no-cache'
#  Priority: 'u=0, i'
#  Upgrade-Insecure-Requests: '1'
#  User-Agent: 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0'


class ParsedHttp:
    """ parsed HTTP mesg 
    Commonly:  ph = ParsedHttp(...)

 ParsedHttp:
  requestFlag=REQ method=GET req-url=/ httpVersion=1.1
  Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  Accept-Encoding: 'gzip, deflate'
  Accept-Language: 'en-US,en;q=0.9'
  Cache-Control: 'no-cache'
  Connection: 'keep-alive'
  Host: '192.168.1.49:8000'
  Pragma: 'no-cache'
  Priority: 'u=0, i'
  Upgrade-Insecure-Requests: '1'
  User-Agent: 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0'
    """

    def __init__(self):
        """ """

        # first line of the mesg. It's either a request or reply.
        # Ex:
        # Request GET / HTTP/1.1
        #         POST /api/users HTTP/1.1
        # Reply ex: HTTP/1.0 200 OK 

        self.start_line = None

        # True if this is a request; False if a reply
        # None if not yet set; if so, accessing raises exception
        self.request_flag = None

        # "1.1", etc
        self.http_version = None


        # Request method: GET  HEAD  POST  PUT  DELETE  CONNECT  OPTIONS  TRACE
        self.method = None

        # requested URL
        self.request_url = None

        # url parsed into its parts: path, params, '#'-bookmark
        # ex: /some-file.html
        self.url_path = ""
        # ex: {'a': '123', 'bbb': 'xyz'}
        self.url_parameters = {}
        # ex: bookmark (from '#' in url)
        self.url_bookmark = ""

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

    def set_as_request(self, method, request_url, 
                       url_path, url_query_params, url_bookmark,
                       http_version):
        """ This is a REQUEST mesg """
        self.request_flag = True
        self.method = method
        self.request_url = request_url
        self.url_path = url_path
        self.url_query_params = url_query_params
        self.url_bookmark = url_bookmark
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
            m = f"PH@115 *********INTERNAL-ERROR**** "+e
            print(m)
            log(m)
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
        if self.method: s.append("method=%s" % str(self.method))
        if self.request_url: s.append("req-url=%s" % str(self.request_url))
        s.append("httpVersion=%s" % str(self.http_version))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


    def long_str(self):
        lines = []
        lines.append(f"{self.__class__.__name__}:")

        s = []
        s.append("  requestFlag=%s" % ("REQ" if self.request_flag else "REPLY"))
        if self.method: s.append("method=%s" % str(self.method))
        if self.request_url: s.append("req-url=%s" % str(self.request_url))
        s.append("httpVersion=%s" % str(self.http_version))
        lines.append(" ".join(s))

        for field_name in sorted(self._fields):
            s = f"  {field_name}: '{self._fields[field_name]}'"
            lines.append(s)

        return "\n".join(lines)
    long_string = long_str


### end ###
