# ClassA.py
#
# NOTE this class is not currently used

import sys

from logger.LoggerABC import LoggerABC

log = None
log_name_ = "None"

logrt = None

class ClassA(LoggerABC):
    def __init__(self):
        super().__init__()
        # NOTE this is a call to a class-method, so you only need
        # to provide the ClassB obj, not an instance of ClassB.
        # But this is convenient - accessing a class-method via
        # an instance works file.
        self.init_logger()

    @classmethod
    def _get_logger(cls): global log; return log
    @classmethod
    def _get_logger_name(cls): global log_name_; return log_name_
    @classmethod
    def _set_logger(cls, newlog, new_name):
        global log, log_name_; log = newlog; log_name_ = new_name
    @classmethod
    def _set_logger_rt(cls, newlog_rt):
        global logrt; logrt = newlog_rt


    def do_logging(self, mesg):
        print(f"classA.do_logging@30  log is currently {log}")
        log(f"classA.do_logging wants to log '{mesg}'")


###
