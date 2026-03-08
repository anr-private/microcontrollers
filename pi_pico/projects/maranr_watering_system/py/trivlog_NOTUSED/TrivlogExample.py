# TrivlogExample.py

import sys

PRT=True
def prt(s):
    if PRT: print (s)

try:
    from trivlog.TrivlogABC import TrivlogABC
except Exception as ex:
    ###prt(f"TrivlogExample@8 failed to import: {ex=}")
    from TrivlogABC import TrivlogABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class TrivlogExample(TrivlogABC):
    def __init__(self):
        super().__init__()


    def _get_log_functions(self): 
        return (log, logrt, logi)
    def _set_log_functions(self, log_arg, logrt_arg, logi_arg):
        global log, logrt, logi
        prt(f"TrivlogExample@30.set_log_functions  {log_arg=}  {log_arg=}  {log_arg=}")
        log = log_arg
        logrt = logrt_arg
        logi = logi_arg


    def do_logging(self, mesg):
        s = "TrivlogExample"
        prt(f"{s}@38.do_logging:  log is currently {log}")

        m = f"{s}.do_logging this is 'log' mesg: '{mesg}'"
        prt(f"{s}@41 {m}")
        log(m)

        m = f"{s}.do_logging: RUNTIME_ERROR 'logrt' mesg: '{mesg}'"
        prt(f"{s}@45 {m}")
        logrt(m)

        m = f"{s}.do_logging: IMPORTANT 'logi' mesg: '{mesg}'"
        prt(f"{s}@49 {m}")
        logi(m)

    def do_sample_logging(self, mesg):
        mlog = f"SAMPLE-LOG-MESG {mesg=}"
        mrt  = f"SAMPLE-LOGRT-MESG {mesg=}"
        mi   = f"SAMPLE-LOGI-MESG {mesg=}"
        log(mlog)
        logrt(mrt)
        logi(mi)

    @classmethod
    def _enable_prt(self, enabled=True):
        # unit test
        global PRT 
        PRT = not not enabled


if __name__ == "__main__":
    te = TrivlogExample()
    te.do_logging("@@MAIN@56 SAMPLE LOG MESSAGE")
###
