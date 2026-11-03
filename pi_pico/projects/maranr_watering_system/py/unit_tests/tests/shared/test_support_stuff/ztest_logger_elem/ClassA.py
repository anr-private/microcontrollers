# ClassA.py

from logger_elem.ElemLoggerABC import ElemLoggerABC

try: from typing import Any
except ImportError: pass

PRT=True
def prt(s):
    if PRT: print (s)


# Logging functions; our parent class sets using _set_logger()
log:   Any = None
logrt: Any = None
logi:  Any = None


class ClassA(ElemLoggerABC):
    
    def __init__(self, num):
        self.num = num
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        prt(f"ClassA@24 _set_logger  logger is {logger}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def to_log(self, m):
        print(f"@@@@@ ClassA@29  log is {log}")
        log(m)

    def to_logrt(self, m):
        logrt(m)

    def to_logi(self, m):
        logi(m)


    def try_all_loggers(self):
        log(f"LOG-MESG-ClassA-{self.num}-test@15")
        logrt(f"LOGRT-MESG-ClassA-{self.num}-test@16")
        logi(f"LOGI-MESG-ClassA-{self.num}-test@17")


    def __str__(self):
        s = []
        s.append("num=%s" % str(self.num))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
