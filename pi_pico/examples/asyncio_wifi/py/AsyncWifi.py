# maranr_watering_system_main.py



class MaranrWateringSystem(ElemLoggerABC):

    def __init__(self):
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        print(f"MAIN@52 _set_logger: {repr(logger)}")
        print(f"MAIN@53 _set_logger: {str(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def main_task(self, host, port):
    
