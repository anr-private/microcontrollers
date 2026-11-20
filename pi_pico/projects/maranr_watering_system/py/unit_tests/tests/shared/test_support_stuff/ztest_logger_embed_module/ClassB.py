# ClassB.py
#
# LINEMARKER=CLSB

from logger_embed_module.LemLogABC import LemLogABC

try: from typing import Callable, Any
except ImportError: pass

log:   Any = None
logrt: Any = None
logi:  Any = None

class ClassB(LemLogABC):
    
    def __init__(self, n:int) -> None:
        self.n = n
        super().__init__()

    def to_log(self, m):
        #print(f"CLSB$21  log is {log}")
        log(m)

    def to_logrt(self, m):
        logrt(m)

    def to_logi(self, m):
        logi(m)


    def try_all_loggers(self):
        log(f"LOG-MESG-ClassB CLSB$32")
        logrt(f"LOGRT-MESG-ClassB CLSB$33")
        logi(f"LOGI-MESG-ClassB CLSB$$34")


    def __str__(self) -> str:
        s: list[str] = []
        s.append("num=%s" % str(self.n))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))



### end ###
