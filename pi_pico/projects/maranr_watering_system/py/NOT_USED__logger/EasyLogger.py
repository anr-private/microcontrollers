# logger
#
# See LoggerABC for details

class EasyLogger:

    _logger = None

    @classmethod
    def get_instance(cls):
        ###print(f"@@@ EasyLogger.get_instance CALLED")
        if EasyLogger._logger is None:
            EasyLogger._logger = EasyLogger(123456)
            #print(f"          @@@ EasyLogger.get_instance CREATED NEW INSTANCE {EasyLogger._logger}")
        #print(f"          @@@ EasyLogger.get_instance returns {EasyLogger._logger}")
        return EasyLogger._logger


    def __init__(self, do_not_call_directly):
        if do_not_call_directly != 123456:
            raise RuntimeError("EasyLogger.init DO NOT CALL")

        self.log_file_path = "mws_log.txt"

        # key:   str   "<class 'test_classes.ClassA.ClassA'>"  NOTE embedded quotes
        # value: class  <class 'test_classes.ClassA.ClassA'>
        self.classes = {}

        # primarily for testing
        self._latest_mesg_ = None
        self._latest_logged_mesg_ = None
        self._latest_muted_mesg_ = None

        try:
            os.remove(self.log_file_path)
        except Exception as ex:
            print(f"EasyLogger.init No log file exists: '{self.log_file_path}' ")



    # === METHODS for Querying and Controlling the logging in registered classes
    #             IE for use by GUI/webpage/etc

    def get_registered_classes(self):
        # returns a copy of the dict of registered classes
        print(f"@@@@ get_registered_classes  {self.classes=}")
        return {item[0]:item[1] for item in self.classes.items()}


    def get_class_obj(self, full_class_name):
        # returns Class obj 
        return self.classes.get(full_class_name)

    def set_logging_enabled_in_all_classes(self, enable):
        # set/reset logging in all registered classes
        ...


    # === LOGGING METHODS for 'user' classes ==================

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

    def log_i_(self, s): # important log info - never muted
        print(f"EasyLogger.log_i_ {s}")

    def _write_to_file(stg):
        if stg is None: stg = ""
        fname = LOG_FNAME
        try:
            with open(fname, "a") as f:
                f.write(stg)
                f.write("\n")
        except Exception as ex:
            print(f"log(): Error writing to file '{fname}': {ex}")


    # === SUPPORT for logger base class  LoggerABC  ===================

    def register_class(self, cls):
        print(f"@@@ EasyLogger@47.register_class  {cls=}")
        self.classes[str(cls)] = cls
        self.dump_the_registered_classes()


    # === MISC  ============================================

    def dump_the_registered_classes(self):
        print(f"@@@ EasyLogger@52  DUMP Registered classes: ")
        for k,v in self.classes.items():
            print(f"  {k=}  v={v}")

###
