# ElemLoggerABC.py

import sys

from .ElemLogControl import ElemLogControl

PRT=False
def prt(s):
    if PRT: print (s)

class ElemLoggerABC:

    def __init__(self):
        try:
            prt(f"ELABC@15.init  self is {self}")
        except Exception as ex:
            prt(f"ELABC@17.init  'str(self)' failed. Ctor not completed(?)  ex={repr(ex)}  {str(ex)}")

        elc = ElemLogControl.get_instance()
        prt(f"ELABC@20.init ElemLogControl obj is {elc}")
        logger = elc.register_user_class(self)
        prt(f"ELABC@22.init  logger is: {logger}")
        # Tell the subclass what to use for its logging functions
        self._set_logger(logger)

    def _get_control_instance(self):
        return ElemLogControl.get_instance()


    @classmethod
    def _enable_prt(self, enabled=True):
        # unit test
        global PRT 
        PRT = not not enabled

###
