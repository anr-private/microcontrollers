# LoggerABC.py
#
# See README_EasyLogger.txt for how-to

import sys

from .EasyLogger import EasyLogger

class LoggerABC:
    def __init__(self):
        pass

    @classmethod
    def init_logger(cls, enable=True):
        # This is called every time a new user class object is created.
        # So it cannot be allowed to alter the current state of logging
        # EXCEPT for the first instance of the user class; when that
        # first instance is create, ONLY THEN and ONLY ONCE we do
        # the logging setup.
        print(f"EasyLogger@84.initlogger  arg 'enable' has value {enable}")

        # See if logger is set up yet.
        curr_log = cls._get_logger()
        if curr_log is None:
            print(f"@@@@ LoggerABC@23.initlogger CLASS {cls} is not set up yet!!!!!!!!!!!!!!!")
            cls._set_up_logging()
        print(f"@@@@@ initlogger has FINISHED.........")


    @classmethod
    def _set_up_logging(cls):
        # this is done just once, during program startup
        print("LoggerABC@33 _set_up_logging - one-time initialization!")
        return

        cls._enable_the_logger(True)

        # register the class
        easyLogger = EasyLogger.get_instance()
        easyLogger.register_class(cls)
        

    @classmethod
    def get_logger_status(cls):
        # First, checks to see if the logger for this class has been set up.
        # If not, sets up the logger in 'enabled' state.
        # If already set up, returns the current status of the logger:
        #   True if logging is enable, False if not.
        # FIRST: is this class set up for logging?
        got_log = cls._get_logger()
        print(f"LoggerABC@39 (cls={cls}) get_logger_status.  got_log = {got_log}")
        if got_log is None:
            print(f"LoggerABC@41 (cls={cls}) LOGGER HAS NOT YET BEEN SET UP! DO IT NOW!")
            raise RuntimeError("@@@@@@@@@@@@ LoggerABC@54.get_logger_status SHOULD NEVER BE CALLED BEFORE LOGGING IS INITIALIZED!")
            #### WAS...
            ####  cls._enable_the_logger(True)
        return cls._get_the_status()

    @classmethod
    def _get_the_status(cls):
        # Returns True if the logger is enabled, False if not.
        # NOTE that this uses the log_name_ from the user class,
        # not the bound method value in the user class's module variable 'log'.
        print(f"LoggerABC._get_the_status  CALLED ")
        ###@@@easyLogger = EasyLogger.get_instance()
        got_log = cls._get_logger()
        #@@@@@@@@@@@ ensure the log var is not None!
        # NOTE tried using str(got_log), which gives the name of the 
        # bound method in Python3 but not in Micropython (which just
        # says 'bound method', nothing more).
        # So we are forced to use the log_name_ variable from the user class.
        ######got_log_stg = str(got_log)
        ######print(f"   _get_the_status {got_log_stg=}")
        ######print(f"   _get_the_status {cls._is_bound_method_loglog(got_log_stg)}")
        #########DOES NOT WORK: each bound method gets a different 'binder' obj(?)
        #########status = got_log is easyLogger.log_log_
        ######status = cls._is_bound_method_loglog(got_log_stg)
        got_log_name = cls._get_logger_name()
        status = got_log_name == "log" # else "mute"
        print(f"LoggerABC._get_the_status  RETURNS {status=} ")
        return status


    @classmethod
    def enable_logger(cls, enable):
        # Arg enable must be True/False
        print(f"ABC.enable_logger Requested: {enable=}")
        #print(f"ABC.enable_logger    cls is {type(cls)}")
        #print(f"ABC.enable_logger    cls is {cls}")

        ###easyLogger = EasyLogger.get_instance()

        if not (enable is True or enable is False):
            m = f"LoggerAbc[cls{cls}].enable_logger  'enable' arg is not True/False:  {enable}"
            print(m)
            raise RuntimeError(m)

        cls._enable_the_logger(enable)

        #@@@@ HEY it no longer returns a status
        #xxx = cls._enable_the_logger(enable)
        #zzz =  cls._get_the_status()
        #print(f"@@@@>>>>>>>>>>>>>>>> enable_logger  {xxx=}  {zzz=}")

        print(f"LoggerABC.enable_logger status: {cls._get_the_status()}")

        return cls._get_the_status()


    @classmethod
    def _enable_the_logger(cls, enable):
        print(f"ABC._enable_the_logger  ___ Requested: {enable=}")
        #print(f"ABC._enable_the_logger    cls is {type(cls)}")
        #print(f"ABC._enable_the_logger    cls is {cls}")
        easyLogger = EasyLogger.get_instance()
        if enable:
            new_logger = easyLogger.log_log_
            new_logger_name = "log"
            if 0:
                print(f"@@@.......... ABC _enable_the_logger  set newLogger to LOGGGG{new_logger}")
                print(f"@@@................  {new_logger is easyLogger.log_log_}")
                print(f"@@@................  {new_logger is easyLogger.log_mute_}")
                print(f"@@@................. new_logger is {new_logger}")
                print(f"@@@ ...............  call new_logger()")
                new_logger("AAAAA")
                easyLogger.log_log_("BBBBB")
        else:
            new_logger = easyLogger.log_mute_
            new_logger_name = "mute"
            if 0:
                print(f"@@@.......... ABC _enable_the_logger  set newLogger to MUTE {new_logger}")
                print(f"@@@................  {new_logger is easyLogger.log_log_}")
                print(f"@@@................  {new_logger is easyLogger.log_mute_}")
                print(f"@@@................. new_logger is {new_logger}")
        print(f"LoggerABC._enable_the_logger newlogger: {str(new_logger)}  {new_logger_name=} ")
        cls._set_logger(new_logger, new_logger_name)

        if 0:
            xxx = cls._get_logger()
            print(f"@@@@ 147 _enable_the_logger  xxx is {xxx}")
            xxx("ZZZXCXX")
        if 0:
            # @@@ NO CALLER needs this - they do it explicitly
            #@@@@@result = new_logger is easyLogger.log_log_
            result = cls._get_the_status()
            print(f"LoggerABC._enable_the_logger@164  .............. _enable_the_logger returns {result}")
            return result

    @classmethod
    def _is_bound_method_loglog(cls, bound_method):
        #print(f"@@@ _is_bound_method_loglog  bound_method is {str(bound_method)}")
        bound_method_stg = str(bound_method)
        #print(f"@@@ ___ bound method str is '{bound_method_stg}'")  
        is_loglog = "log_log_" in bound_method_stg
        #print(f"@@@ ___ _is_bound_method_loglog returns {is_loglog}")
        return is_loglog

###
