# ClassA.py
#
# LINEMARKER=CLSA

from logger_embed_module.LemLogABC import LemLogABC

try: from typing import Callable, Any
except ImportError: pass

log:   Any = None
logrt: Any = None
logi:  Any = None

class ClassA(LemLogABC):
    
    def __init__(self, n:int) -> None:
        self.n = n
        super().__init__()

    def to_log(self, m):
        #print(f"CLSA$21  log is {log}")
        log(m)

    def to_logrt(self, m):
        logrt(m)

    def to_logi(self, m):
        logi(m)


    def try_all_loggers(self):
        log(f"LOG-MESG-ClassA CLSA$32")
        logi(f"LOGI-MESG-ClassA CLSA$$34")
        logrt(f"LOGRT-MESG-ClassA CLSA$34")


    def __str__(self) -> str:
        s: list[str] = []
        s.append("num=%s" % str(self.n))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))



### end ###
