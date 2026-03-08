# DataBoard.py
#
# Global data board

from logger_elem.ElemLoggerABC import ElemLoggerABC


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

VALIDATE = 192756


class DataBoard(ElemLoggerABC):

    _instance = None

    def __init__(self):
        super().__init__()

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = DataBoard(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        DataBoard._instance = None
        DataBoard._clear_latest_messages()

    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"DataBoard@37 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi



###
