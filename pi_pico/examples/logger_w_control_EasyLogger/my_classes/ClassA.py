# ClassA.py

import sys

from logger.LoggerABC import LoggerABC

log = None
log_name_ = "None"
logrt = None

class ClassA(LoggerABC):
    def __init__(self):
        super().__init__()
        # NOTE this is a call to a class-method, so you only need
        # to provide the Class obj, not an instance of the Class.
        # But this is convenient - accessing a class-method via
        # an instance works file.
        self.init_logger()
        print(f"ClassA@19.init logrt is {str(logrt)}")
        assert log is not None
        assert len(log_name_) > 0
        assert logrt is not None

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
        s = "classA"
        print(f"{s}.do_logging  log is currently {log}")
        log(f"{s}.do_logging wants to log '{mesg}'")

    def log_runtime_error(self, mesg):
        #global logrt
        logrt(mesg)
###
