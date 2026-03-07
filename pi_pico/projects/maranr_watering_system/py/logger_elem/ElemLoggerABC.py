# ElemLoggerABC.py

import sys

from .ElemLogControl import ElemLogControl

PRT=False
def prt(s):
    if PRT: print (s)

class ElemLoggerABC:

    def __init__(self):
        try:
            prt(f"ElemLoggerABC@19.init  self is {self}")
        except Exception as ex:
            prt(f"ElemLoggerABC@21.init  'str(self)' failed. Ctor not completed(?)  ex={repr(ex)}  {str(ex)}")

        elc = ElemLogControl.get_instance()
        prt(f"ElemLoggerABC@24.init ElemLogControl obj is {elc}")
        logger = elc.register_user_class(self)
        prt(f"ElemLoggerABC@26.init  logger is: {logger}")
        # Tell the subclass what to use for its logging functions
        self._set_logger(logger)



    @classmethod
    def _enable_prt(self, enabled=True):
        # unit test
        global PRT 
        PRT = not not enabled

###
