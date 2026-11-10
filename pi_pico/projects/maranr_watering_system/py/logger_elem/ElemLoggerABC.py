# ElemLoggerABC.py
#
# LINEMARKER=ELABC

import sys

try: from typing import Any
except ImportError: pass

from .ElemLogControl import ElemLogControl
from .ElemLogger import ElemLogger

PRT=False
def prt(s:str) -> None:
    if PRT: print (s)

class ElemLoggerABC:

    def __init__(self) -> None:
        try:
            prt(f"ELABC$21.init  self is {self}")
        except Exception as ex:
            prt(f"ELABC$23.init  'str(self)' failed. Ctor not completed(?)  ex={repr(ex)}  {str(ex)}")

        self.elc = ElemLogControl.get_instance()
        prt(f"ELABC$26.init ElemLogControl obj is {self.elc}")
        logger = self.elc.register_user_class(self)
        prt(f"ELABC$28.init  logger is: {logger}")
        # Tell the subclass what to use for its logging functions
        self._set_logger(logger)

    #### REMOVE?
    def _get_control_instance_NOTUSED(self) -> "ElemLogControl":
        return ElemLogControl.get_instance()

    def _get_log_control_instance(self) -> "ElemLogControl":
        return self.elc


    ### @abstractmethod   NOT AVAILABLE IN micropython 1.29.0
    def _set_logger(self, logger: "ElemLogger") -> None:
        """ Tell the subclass what to use as its logger 
        This is an abstract method: the subclass must implement.
        """
        raise NotImplementedError(f"Obj={self} _set_logger() is not implemented in the ElemLogControlABC subclass")


    @classmethod
    def _enable_prt(cls, enabled:bool=True) -> None:
        # unit test
        global PRT 
        PRT = not not enabled

###
