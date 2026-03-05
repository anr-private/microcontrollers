# DataBoard.py
#
# Global data board

from trivlog.TrivlogABC import TrivlogABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class DataBoard(TrivlogABC):
    def __init__(self):
        super().__init__()


    def _get_log_functions(self): 
        return (log, logrt, logi)
    def _set_log_functions(self, log_arg, logrt_arg, logi_arg):
        global log, logrt, logi
        #print(f"TrivlogExample@30.set_log_functions  {log_arg=}  {log_arg=}  {log_arg=}")
        log = log_arg
        logrt = logrt_arg
        logi = logi_arg



###
