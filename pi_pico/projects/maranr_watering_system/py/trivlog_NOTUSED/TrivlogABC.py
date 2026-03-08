# TrivlogABC.py

try:
    from .Trivlog import Trivlog
except Exception as ex:
    m=f"Trivlog@6.import failed  ex={ex} {str(ex)}"
    ###print(m)
    from Trivlog import Trivlog


PRT=True
def prt(s):
    if PRT: print (s)

class TrivlogABC:

    def __init__(self):
        try:
            prt(f"TrivlogABC@19.init  self is {self}")
        except Exception as ex:
            pass
            # Exception probably caused by ctor not finished so obj is lacking propertie(s)
            #prt(f"TrivlogABC@21.init  'str(self)' failed. Ctor not completed(?)  ex={repr(ex)}  {str(ex)}")

        self._trivlog = Trivlog.get_instance()
        prt(f"TrivlogABC@21.init trivlog obj is {self._trivlog}")
        logs = self._trivlog.register_user_class(self)
        prt(f"TrivlogABC@23.init  log-functs: {logs}")
        # Tell the subclass what to use for its logging functions
        self._set_log_functions(*logs)



    @classmethod
    def _enable_prt(self, enabled=True):
        # unit test
        global PRT 
        PRT = not not enabled

###
