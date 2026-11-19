# ClassB.py
#
# LINEMARKER=ClassB

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


class ClassB(ElemLoggerABC):
    
    def __init__(self, num):
        self.num = num
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        prt(f"ClassB$29 _set_logger  logger is {logger}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def to_log(self, m):
        print(f"@@@@@ ClassB$36  log is {log}")
        log(m)

    def to_logrt(self, m):
        logrt(m)

    def to_logi(self, m):
        logi(m)


    def try_all_loggers(self):
        log(f"LOG-MESG-ClassB-{self.num}-test-47")
        logrt(f"LOGRT-MESG-ClassB-{self.num}-test-48")
        logi(f"LOGI-MESG-ClassB-{self.num}-test-49")


    def __str__(self):
        s = []
        s.append("num=%s" % str(self.num))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
