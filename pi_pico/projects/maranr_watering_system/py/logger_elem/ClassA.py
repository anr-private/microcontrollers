# ClassA.py


from log_elem.ElemLoggerABC import ElemLoggerABC

PRT=True
def prt(s):
    if PRT: print (s)


log = None
logrt = None
logi = None


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


    def try_all_loggers(self):
        log(  "LOG-MESG-ClassA-{self.num}-test@15")
        logrt("LOGRT-MESG-ClassA-{self.num}-test@16")
        log(  "LOGI-MESG-ClassA-{self.num}-test@17")


    def __str__(self):
        s = []
        s.append("num=%s" % str(self.num))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
