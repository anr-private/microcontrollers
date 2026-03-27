# HdrAccum.py

#import utils
from utils import show_cc
from logger_elem.ElemLoggerABC import ElemLoggerABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class HdrAccum(ElemLoggerABC):

    def __init__(self):
        self._mesg = ""
        self._end_of_hdr_pos = -1
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def accum_header_line(self, line):
        log(f"ACCUMLINE@16 '{show_cc(line)}'")
        self._mesg += line
        # found the end of the header?  
        pos = self._mesg.find("\r\n\r\n")
        if pos >= 0:
            # keep the two '\r\n' sequences
            self._end_of_hdr_pos = pos + 4

    def found_end_of_header(self):
        return self._end_of_hdr_pos >= 0

    def get_header(self):
        if not self.found_end_of_header():
            return None
        return self._mesg[0:self._end_of_hdr_pos]

    def get_tail(self):
        if not self.found_end_of_header():
            return None
        return self._mesg[self._end_of_hdr_pos:]

###
