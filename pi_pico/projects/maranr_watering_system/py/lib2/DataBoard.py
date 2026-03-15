# DataBoard.py
#
# Global data board
#
# Running average:   Average =+ (next_value - Average) / new-sample-count

from logger_elem.ElemLoggerABC import ElemLoggerABC


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

VALIDATE = 192756


class DataBoard(ElemLoggerABC):

    _instance = None

    def __init__(self, validate):
        if validate != VALIDATE:
            raise RuntimeError(f"DataBoard CTOR is private!")
        self.internal_temp_f = 0
        self.internal_temp_c = 0
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

    def set_internal_temps(self, degsF, degsC):
        self.internal_temp_f = degsF
        self.internal_temp_c = degsC


    def get_internal_temps_one_dec_place(self):
        degs_f = f"{self.internal_temp_f:.1f}"
        degs_c = f"{self.internal_temp_c:.1f}"
        return degs_f, degs_c




###
