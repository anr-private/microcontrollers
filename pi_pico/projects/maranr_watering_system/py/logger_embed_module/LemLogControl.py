# LemLogControl.py
#
# LINEMARKER=LEMLC

import os
import sys

from .LemLogger import LemLogger
from .LemLogFileTable import LemLogFileTable, EMPTY_LOG_FPATH_MARKER_STG

try: from typing import Callable, Any
except ImportError: pass


VALIDATE = 30894687

class LemLogControl:

    _instance: "LemLogControl | None" = None

    @classmethod
    def configure_logger(cls, logs_dir: str|None, log_parameters_selector:str) -> "LemLogControl":
        # logs_dir is None for unit testing: no LemLogFileTable gets created(??)
        if cls._instance is not None:
            m = "LEMLC$25 LOGGER IS ALREADY CONFIGURED!"
            print(m)
            raise RuntimeError(m)
        cls._instance = LemLogControl(logs_dir, log_parameters_selector, VALIDATE)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "LemLogControl":
        if cls._instance is None:
            m = "LEMLC$34 LOGGER IS NOT CONFIGURED!"
            print(m)
            raise RuntimeError(m)
        return cls._instance


    def __init__(self, logs_dir: str|None, log_parameters_selector:str, validate:int) -> None:
        if validate != VALIDATE:
            m = f"LEMLC$42 CALLED CTOR use get_instance()"
            raise RuntimeError(m)


        # The default logging mode that all loggers start with
        self._default_logging_enabled: bool = True

        # Keep track of classes that have had explicit request(s)
        # to set the logging-enabled state.
        # This allows the state to be specified before an instance
        # of the class is created.
        # E.g., main() can request that class "Abc" have a specified
        # logging state before an Abc instance ever gets created.
        # If there is no entry for a class name, the presumed value
        # is _default_logging_enabled.
        # KEY: simplified class name
        # VALUE: the logging-enabled state it will be given
        # when the class is created 
        self._logging_enabled_overrides: dict[str, bool] = {}

        # Registry of loggers - must exist before anything registers
        # (including our own registration below)
        # key: simplified class name   value: LemLogger for that class
        self._registry: dict[str, "LemLogger"] = {}

        # Table of log files that have been created and are now closed
        # List contains tuples:
        #   (log-filename:str, fsize: int, extant-flag)
        # The extant-flag is 1 if file is extant, 0 if file has been
        # removed to reclaim file space.
        self._log_file_table = LemLogFileTable(logs_dir, log_parameters_selector)

        # Register ourself and give ourself an LemLogger, just like
        # every other class.
        # NOTE we must do this AFTER creating the LemLogFileTable
        # b/c LemLogger.__init__ might try to do logging -- 
        # we give it a reference to ourself, so it could call
        # our LOG() or log_one_line() methods.
        print(f"LEMLC$80 ****** REGISTER OURSELF  ************")
        our_simplified_class_name = extract_simplified_classname(self)
        print(f"LEMLC$82 {our_simplified_class_name=}")
        our_logging_enabled_initially = \
                self._logging_enabled_overrides.get(our_simplified_class_name,
                                                     self._default_logging_enabled)
        self._our_own_logger: LemLogger = \
                LemLogger(self, our_simplified_class_name,
                                 our_logging_enabled_initially)
        self._registry[our_simplified_class_name] = self._our_own_logger


    def close_all_logging(self) -> None:
        # close logging - program is terminating
        print(f"LEMLC$94 CLOSE ALL LOGGING")
        self._log_file_table.close_logging()
        print(f"LEMLC$96 CLOSED LOGGING: DESTROY LemLogControl INSTANCE")
        print(f"LEMLC$97 CLOSED LOGGING: DESTROY LemLogControl INSTANCE _____________=========================__________________________=====================")
        self.__class__._instance = None

    def get_current_log_fpath(self) -> str:
        return self._log_file_table.get_current_log_fpath()

    def get_current_log_fsize(self) -> int:
        return self._log_file_table.get_current_log_fsize()

    def get_logs_totals(self, include_currently_open_file: bool) -> tuple[int, int, int]:
        return self._log_file_table.get_logs_totals(include_currently_open_file)

    def get_log_table_item(self, item_index: int) -> tuple[str, int, int] | None:
        return self._log_file_table.get_log_table_item(item_index)

    def get_log_table_status_lines(self) -> tuple[str,...]:
        return self._log_file_table.get_status_lines()

    def get_registry_size(self) -> int:
        """ Return the size of the registry: the number of classes
        that have registered.
        """
        return len(self._registry)


    def register_user_class(self, obj_instance: Any) -> "LemLogger":
        # obj is a user obj that subclasses LemLogABC
        # Returns a logger obj the caller should use

        ###self.LOG = print

        simplified_class_name = extract_simplified_classname(obj_instance)
        
        # NOTE this method runs from within the __init__() method of
        # the subclass object, and the subclass is still in progress
        # with its construction. So we just use its simplified_class_name
        # instead.
        ####self.LOG(f"LEMLC$134 register_user_class  obj is {obj_instance!r} ")
        self.LOG(f"LEMLC$135 register_user_class  obj is {simplified_class_name!r} ")

        obj_module = self._get_module_for_object(obj_instance)

        if not obj_module:
            m = f"LEMLC$140 No module found for the obj_instance. {simplified_class_name=!r}"
            self.LOG(m)
            raise RuntimeError(m)

        self.LOG(f"LEMLC$144 register_user_class {simplified_class_name=}")

        # does this class have a logger assigned (yet)?
        logger = self._registry.get(simplified_class_name)
        self.LOG(f"LEMLC$148 register_user_class logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = self._create_and_connect_a_logger(simplified_class_name)

            ### DON'T DO THESE: the obj is still being constructed in __init__, 
            ###    so str() and repr() may fail.
            ### self.LOG(f"LEMLC$154 Registered new class for logging: obj_instance={str(obj_instance)}")
            ### self.LOG(f"LEMLC$155 Registered new class for logging: {obj_instance=!r}")
            self.LOG(f"LEMLC$156 Registered new class for logging: {simplified_class_name=!r}")
            #self.LOG(f"LEMLC$157 Registered new class for logging: {logger=!r}")

            # connect the object's class to its logger
            obj_module.log = logger.log
            obj_module.logi = logger.logi
            obj_module.logrt = logger.logrt

        if 0: self.dump_registered_loggers()
        return logger


    def _create_and_connect_a_logger(self, simplified_class_name: str) -> LemLogger:
        LOGLOG = print

        logging_enabled_initially = \
            self._logging_enabled_overrides.get(simplified_class_name,
                                                self._default_logging_enabled)
        logger = LemLogger(self, simplified_class_name,
                                  logging_enabled_initially)
        self._registry[simplified_class_name] = logger
        LOGLOG(f"LEMLC$177 Registered new class for logging: {simplified_class_name=!r}")
        LOGLOG(f"LEMLC$178 Registered new class for logging: {logger=!r}")
        return logger


    def _get_module_for_object(self, obj_instance: Any) -> Any:

        LOGLOG = print

        obj_class = type(obj_instance)
        LOGLOG(f"LEMLC$187 register_user_class  {obj_class=!r} ")

        obj_module_name = getattr(obj_class, "__module__")

        #LOGLOG(f"LEMLC$191  {obj_module_name=!r}")

        obj_module = sys.modules.get(obj_module_name)

        #LOGLOG(f"LEMLC$195  MODULE={obj_module!r}")
        #LOGLOG(f"LEMLC$196  DIR={dir(obj_module)}")
        return obj_module


    def get_registered_classes(self) -> tuple[str,...]:
        return tuple(self._registry.keys())

    def get_logger_for_class(self, class_name: str) -> LemLogger | None:
        """ Get the logger associated with the specified class_name
        (which must be a simplified class name).
        Returns the LemLogger or None if none found.
        """
        return self._registry.get(class_name, None)

    def get_unmatched_override_classnames(self) -> tuple[str,...]:
        """ Get a tuple containing each classname that was specified
        to have a logging-enabled override but that classname
        has never been registered. It's probably a typo
        in the classname. This method is obviously useful
        mainly after initial startup is completed and all
        classes have registered.
        """
        found: list[str] = list()
        for classname in self._logging_enabled_overrides.keys():
            if classname not in self._registry:
                found.append(classname)
        return tuple(found)


    def LOG(self, m:str) -> None:
        # simulates the log() method of a 'regular' class
        self._our_own_logger.log(m)


    def enable_logging(self, class_name: str, enabled: bool) -> bool:
        """ Enable/disable logging for the specified class
        (class_name must be the simple class name).
        Set its logging state to enabled/disabled per arg 'enabled'.
        Returns True if successful, False if any problem.
        """

        logger = self._registry.get(class_name)
        m = f"LEMLC$240 enable_logging: logger is {logger}  {enabled=} {class_name=}"
        print(m)
        self.log_one_line(m)
        if logger is None:
            m = f"LEMLC$244 logger is NONE for {class_name=}  {enabled=}"
            print(m)
            self.log_one_line(m)
            return False
        logger.enable_log(enabled)
        return True

    def log_and_print_one_line(self, line: str) -> None:
        self.log_one_line(line)
        print(line)

    def log_one_line(self, line:str) -> None:
        self._log_file_table.log_one_line(line)

    def get_lines_from_log_file(self, relative_line_number: int,
                                number_of_lines: int) -> list[str]:
        lines = self._log_file_table.get_lines_from_log_file(relative_line_number,
                                                             number_of_lines)
        return lines


    def dump_registered_loggers(self) -> None:
        m = "LEMLC$266  Classes registered in ElemLogControl:"
        print(m)
        self.log_one_line(m)
        for k,v in self._registry.items():
            m = f"  {k}  {v}"
            print(m)
            self.log_one_line(m)

    def __str__(self):
        s = []
        s.append(f"default_logging={self._default_logging_enabled}")
        s.append(f"registry.len={len(self._registry)}")
        s.append(f"logging_overrides.len={len(self._logging_enabled_overrides)}")
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))



#=== UNIT TEST SUPPORT FUNCTIONS  ===================================


def Z_replace_log_file_table(new_log_file_table: Any) -> None:
    # UNIT TEST ONLY: replace the LemLogFileTable with a fake
    # Raises if we already have an active LemLogFileTable obj
    if LemLogControl._instance is None:
        raise RuntimeError(f"LEMLC$278 Z_replace_log_file_table LemLogControl._instance is None")
    lemc = LemLogControl.get_instance()
    lft = lemc._log_file_table
    # Not allowed if 'real' logging has been done
    if isinstance(lft, LemLogFileTable):
        if lft.get_current_log_fpath() != EMPTY_LOG_FPATH_MARKER_STG:
            raise RuntimeError(f"LEMLC$284 Z_replace_log_file_table LemLogControl already active: fpath={lft.get_current_log_fpath()}") 
        if lft.get_current_log_fsize() != 0:
            raise RuntimeError(f"LEMLC$286 Z_replace_log_file_table LemLogControl already active: log-size={lft.get_current_log_fsize()}") 
    lemc._log_file_table = new_log_file_table



def extract_simplified_classname(obj_instance: Any) -> str:
    # Return the plain class name of obj_instance, e.g. "MyClass".
    # Uses the class's __name__, so it never calls the object's
    # __repr__ or __str__ (which may not work yet during __init__).
    return type(obj_instance).__name__


###
