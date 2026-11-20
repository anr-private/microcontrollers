# LemLogABC.py
#
# LINEMARKER=LEMABC

import sys

try: from typing import Any
except ImportError: pass

from .LemLogControl import LemLogControl
#from .LemLogger import LemLogger

PRT=False
def prt(s:str) -> None:
    if PRT: print (s)

# **IMPORTANT NOTE**
# A subclass should define any attributes BEFORE it invokes this class's
# __init__() method.
# Because this class's __init__() calls lemc.register_user_class()
# which in turn may use the str() or the repr() of the subclass.
# If it does, and if the subclass has not yet defined anything
# that is used in its str() or repr(), an 'AttributeError' occurs.
# So the correct form of a subclass is:
#    class ClassA(LemLogABC):
#        
#        def __init__(self, n:int) -> None:
#            self.n = n
#            # DO NOT CALL ANY LOGGING UNTIL super().__init__() finishes
#            #   NAMELY log(), logrt(), logi()
#            super().__init__()
#             # DO NOT DEFINE ATTRIBUTES USED BY str() or repr() HERE 
#             # I.E., AFTER CALLING super().__init__()

class LemLogABC:

    def __init__(self) -> None:
        try:
            prt(f"LEMABC$39.init  self is {self}")
        except Exception as ex:
            prt(f"LEMABC$41.init  'str(self)' failed. Ctor not completed(?)  ex={repr(ex)}  {str(ex)}")

        lemc = LemLogControl.get_instance()
        prt(f"LEMABC$44.init LemLogControl obj is {lemc}")
        logger = lemc.register_user_class(self)
        prt(f"LEMABC$46.init  logger is: {logger}")

    @classmethod
    def _enable_prt(cls, enabled:bool=True) -> None:
        # unit test
        global PRT 
        PRT = not not enabled

###
