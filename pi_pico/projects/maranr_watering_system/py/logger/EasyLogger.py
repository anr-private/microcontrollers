# logger
#
# See LoggerABC for details

class EasyLogger:

    _logger = None

    @classmethod
    def get_instance(cls):
        ###print(f"@@@ EasyLogger.get_instance CALLED")
        if EasyLogger._logger is None:
            EasyLogger._logger = EasyLogger()
            #print(f"          @@@ EasyLogger.get_instance CREATED NEW INSTANCE {EasyLogger._logger}")
        #print(f"          @@@ EasyLogger.get_instance returns {EasyLogger._logger}")
        return EasyLogger._logger


    def __init__(self):
        self.classes = {}

        # primarily for testing
        self._latest_mesg_ = None
        self._latest_logged_mesg_ = None
        self._latest_muted_mesg_ = None


    # === LOGGING METHODS ==================

    def log_log_(self, s):
        print(f"EasyLogger.log_log_ MESG IS {s}")
        self._latest_logged_mesg_ = s
        self._latest_mesg_ = s

    def log_mute_(self, s):
        print(f"EasyLogger.log_mute_     -----   MUTED ------ MESG IS {s}")
        self._latest_muted_mesg_ = s
        self._latest_mesg_ = s
    
    def log_rt_(self, s):
        print(f"EasyLogger.log_rt_ *ERROR* {s}")
        raise RuntimeError(s)

    # === SUPPORT  =================================

    def register_class(self, cls):
        print(f"@@@ EasyLogger@47.register_class  {cls=}")
        self.classes[str(cls)] = cls
        self.dump_the_registered_classes()

    def dump_the_registered_classes(self):
        print(f"@@@ EasyLogger@52  DUMP Registered classes: ")
        for k,v in self.classes.items():
            print(f"  {k=}  v={v}")

###
