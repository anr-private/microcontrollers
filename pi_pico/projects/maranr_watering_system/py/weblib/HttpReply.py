# HttpReply.py

from logger_elem.ElemLoggerABC import ElemLoggerABC
from utils import show_cc

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class HttpReply(ElemLoggerABC):

    def __init__(self):
        # header should be a str and should end with \r\n\r\n
        self._header = None
        self._body = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"HttpReply@23 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi

    def set_reply(self, header, body):

        # header should be a str and should end with \r\n\r\n
        ###@@@@@@@if typ e(header) is not str:
        if not isinstance(header, str):
            raise RuntimeError(f"HttpReply.set_reply header is not str: {type(header)}")
        # header should have at least "HTTP/1.0 200 OK\r\n\r\n"
        if len(header) < 10:
            raise RuntimeError(f"HttpReply.set_reply header is too short: len={len(header)} hdr='{header}'")
        if header[-4:] != "\r\n\r\n":
            raise RuntimeError(f"HttpReply.set_reply header does not end with CR/LF/CR/LF: {show_cc(header)}")
            

        self._header = header

        self._body = body

    def get_header(self):
        return self._header

    def get_body(self):
        return self._body

    def __str__(self):
        if self._header is None:
            hdr_len_stg = "None"
        else:
            hdr_len_stg = len(self._header)

        if self._body is None:
            body_len_stg = "None"
        elif isinstance(self._body, str):
            body_len_stg = f"{len(self._body)}-chars"
        elif isinstance(self._body, bytes):
            body_len_stg = f"{len(self._body)}-bytes"         
        else:
            body_len_stg = f"{type(self._body)}-unknown-len"
        #except Exception as ex:
        #    return "HttpReply ctor not finished, cannot use str() ex={repr(ex)}  {str(ex)}"
        s = []
        s.append("hdr.len=%s" % hdr_len_stg)
        s.append("body.len=%s" % body_len_stg)
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))

###
