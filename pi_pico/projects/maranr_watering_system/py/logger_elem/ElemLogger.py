# ElemLogger.py
#
# Elementary logger
# LINEMARKER=ELOG

import os
import sys

try: from typing import Callable, Any
except ImportError: pass

PRT=False
def prt(s:str) -> None:
    if PRT: print (s)


#@@@@@@@@@@@@ TODO better handling of enabling log, logi?

class ElemLogger:

    def __init__(self, log_control: Any, simplified_class_name: str) -> None:
        self.class_name: str = simplified_class_name
        self.log_enabled: bool = True #  False #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self._log_control: Any = log_control
        prt(f"ELOG$23 init {self.class_name=}")


    def is_enabled(self) -> bool:
        return self.log_enabled

    def enable_log(self, enabled: bool) -> None:
        # control whether the class using this logger generates log mesgs 
        # affects only the log() method so far
        self.log_enabled = not not enabled
            

    def log(self, mesg: str) -> None:
        if self.log_enabled:
            #print(f"ELOG$37.log '{mesg=}' ")
            print(f"LOG: {mesg}")
            self._log_control.log_one_line(mesg)

    def logrt(self, mesg: str) -> None:
        ###print(f"ELOG$42.logrt '{mesg=}' ")
        print(f"LOGRT: {mesg}")
        self._log_control.log_one_line(mesg)
        raise RuntimeError(mesg)

    def logi(self, mesg: str) -> None:
        #print(f"ELOG$48.logi '{mesg=}' ")
        print(mesg)
        self._log_control.log_one_line(mesg)


    def __str__(self) -> str:
        s = []
        s.append("cls=%s" % str(self.class_name))
        s.append("logEnabled=%s" % str(self.log_enabled))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))




###
