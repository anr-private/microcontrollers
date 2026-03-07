# DataBoard.py
#
# Global data board

from logger_elem.ElemLoggerABC import ElemLoggerABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class DataBoard(ElemLoggerABC):
    def __init__(self):
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"DataBoard@20 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi



###
