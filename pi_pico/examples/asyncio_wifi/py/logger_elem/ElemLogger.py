# ElemLogger.py
#
# Elementary logger

import os
import sys


PRT=False
def prt(s):
    if PRT: print (s)



class ElemLogger:

    def __init__(self, log_control, simplified_class_name):
        self.class_name = simplified_class_name
        self._log_enabled = False #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self._log_control = None # see below
        prt(f"ELOG@21 init {self.class_name=}")
        self._log_control = log_control


    def enable_log(self, enabled):
        self._log_enabled = not not enabled
            

    def log(self, mesg):
        if self._log_enabled:
            #print(f"ELOG@31.log '{mesg=}' ")
            print(f"LOG: {mesg}")
            self._log_control.log_one_line(mesg)
    def logrt(self, mesg):
        ###print(f"ELOG@35.logrt '{mesg=}' ")
        print(f"LOGRT: {mesg}")
        self._log_control.log_one_line(mesg)
        raise RuntimeError(mesg)
    def logi(self, mesg):
        #print(f"ELOG@40.logi '{mesg=}' ")
        print(mesg)
        self._log_control.log_one_line(mesg)


    def __str__(self):
        s = []
        s.append("cls=%s" % str(self.class_name))
        s.append("logEnabled=%s" % str(self._log_enabled))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))




###
