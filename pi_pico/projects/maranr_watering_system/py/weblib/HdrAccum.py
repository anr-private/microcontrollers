# HdrAccum.py

#import utils
from utils import show_cc
from trivlog.TrivlogABC import TrivlogABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class HdrAccum(TrivlogABC):

    def __init__(self):
        super().__init__()

        self._mesg = ""
        self._end_of_hdr_pos = -1

    def _get_log_functions(self): 
        return (log, logrt, logi)
    def _set_log_functions(self, log_arg, logrt_arg, logi_arg):
        global log, logrt, logi
        #print(f"HdrAccum@34.set_log_functions  {log_arg=}  {log_arg=}  {log_arg=}")
        log = log_arg
        logrt = logrt_arg
        logi = logi_arg


    def accum_header_line(self, line):
        log(f"ACCUMLINE@16 '{show_cc(line)}'")
        ###self._lines.append(line)
        ###print(f"  Lines: {self._lines}")
        self._mesg += line
        #print(f" mesg: '{show_cc(self._mesg)} ")
        # found the end of the header?  
        pos = self._mesg.find("\r\n\r\n")
        if pos >= 0:
            # keep the two '\r\n' sequences
            self._end_of_hdr_pos = pos + 4
            ###print(f"Found the end of header {self._end_of_hdr_pos=} ")

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
