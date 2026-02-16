# HdrAccum.py

from utils import *

# unit tests:
#  /home/art/git/art/src/python3/pico_support_tests/watering_controller/http/unit_tests/TestHdrAccum.py

class HdrAccum:

    def __init__(self):
        ###self._lines = []
        self._mesg = ""
        self._end_of_hdr_pos = -1

    def accum_header_line(self, line):
        print(f"ACCUMLINE '{show_cc(line)}'")
        ###self._lines.append(line)
        ###print(f"  Lines: {self._lines}")
        self._mesg += line
        #print(f" mesg: '{show_cc(self._mesg)} ")
        # found the end of the header?  
        pos = self._mesg.find("\r\n\r\n")
        if pos >= 0:
            # keep the two '\r\n' sequences
            self._end_of_hdr_pos = pos + 4
            print(f"Found the end of header {self._end_of_hdr_pos=} ")

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
