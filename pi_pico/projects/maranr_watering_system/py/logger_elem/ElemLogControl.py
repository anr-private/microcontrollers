# ElemLogControl.py
# 
# Control and registrar for ElemLogger

import os
import sys

from file_utils import read_last_n_lines, filter_dir_contents

from .ElemLogger import ElemLogger
from .ElemLogFileTable import ElemLogFileTable


VALIDATE = 13524687


class ElemLogControl:
    # central control for logging
    # Handles the log file(s) - the only class that does so

    _instance = None

    #@@@@@@@@@@@@@@@@@@@@ move this into the instance?  why is it at the class level?
    # key: simplified class name   value: ElemLogger for that class
    registry = {}


    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = ElemLogControl(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        #print(f"ELC@36  NULLIFY INSTANCE  =======================================")
        # UNIT TEST ONLY
        ElemLogControl._instance = None
        ElemLogControl.registry = {}


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"ELC@44 CALLED CTOR use get_instance()"
            raise RuntimeError(m)

        # FAKE having an ElemLogger - to allow controlling logging from log-control webpage
        self._log_enabled = False

        print(f"ELC@50 ******************************$@$@$@$*$*$")
        print(f"ELC@51 ****** REGISTER OURSELF")
        simplified_class_name = extract_simplified_classname(self)
        print(f"ELC@53 {simplified_class_name=}")
        self.registry[simplified_class_name] = self
        
        # Table of log files that have been created and are now closed
        # List contains tuples:
        #   (log-filename:str, fsize: int, extant-flag)
        # The extant-flag is 1 if file is extant, 0 if file has been
        # removed to reclaim file space.
        self._log_file_table = ElemLogFileTable()
    #
    # FAKE having a logger
    def enable_log(self, enabled):
        # Fake the ElemLogger method - so we can be registered as if
        # we were using that class as our logger
        self._log_enabled = not not enabled
    def is_enabled(self):
        return self._log_enabled

    def close_all_logging(self):
        # close logging - program is terminating
        print(f"ELC@73 CLOSE ALL LOGGING")
        self._log_file_table.close_logging()

    def get_current_log_fpath(self):
        return self._log_file_table.get_current_log_fpath()

    def get_current_log_fsize(self):
        return self._log_file_table.get_current_log_fsize()

    def get_logs_totals(self, include_currently_open_file):
        return self._log_file_table.get_logs_totals(include_currently_open_file)

    def get_log_table_item(self, item_index):
        return self._log_file_table.get_log_table_item(item_index)

    def get_log_table_status_lines(self):
        return self._log_file_table.get_status_lines()


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses ElemLogControlABC
        # Returns a logger obj the caller should use

        self.LOG(f"ELC@96 register_user_class  obj is {repr(obj_instance)} ")

        simplified_class_name = extract_simplified_classname(obj_instance)
        self.LOG(f"ELC@99 register_user_class {simplified_class_name=}")

        # does this class have a logger assigned?
        logger = self.registry.get(simplified_class_name)
        self.LOG(f"ELC@103 register_user_class logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = ElemLogger(self, simplified_class_name)
            self.registry[simplified_class_name] = logger
        if 0: self.dump_registered_loggers()
        return logger


    def get_registered_classes(self):
        return self.registry.keys()


    def LOG(self, m):
        # simulates the log() method of a 'regular' class
        # IE a class not part of logging
        # Part of FAKE-ing the ElemLogger - this class has no associated ElemLogger
        if self._log_enabled:
            self.log_and_print_one_line(m)


    def enable_logging(self, class_name, enabled):
        # enable/disable logging for the specified class
        logger = self.registry.get(class_name)
        m = f"ELC@126 logger is {logger}  {enabled=}"
        print(m)
        self.log_one_line(m)
        # may enable ourself(!) if class_name is this class
        logger.enable_log(enabled)


    def log_and_print_one_line(self, line):
        self.log_one_line(line)
        print(line)

    def log_one_line(self, line):
        self._log_file_table.log_one_line(line)



    def get_lines_from_log_file(self, relative_line_number, number_of_lines):
        lines = self._log_file_table.get_lines_from_log_file(relative_line_number, number_of_lines)
        return lines


    def dump_registered_loggers(self):
        m = "ELC@148  Classes registered in ElemLogControl:"
        print(m)
        self.log_one_line(m)
        for k,v in self.registry.items():
            m = f"  {k}  {v}"
            print(m)
            self.log_one_line(m)


### FUNCTIONS  ###########################################################

def is_3_digit_int(s):
    # Returns int(s) if s is a 3-digit number; else None.
    if not  s: return None
    if len(s) != 3: return None
    try:
        ival = int(s)
    except (TypeError, ValueError):
        return None
    if ival <= 0 or ival > 999: return None
    return ival


def _log_file_filter(fname, ftype, fsize):
    # Returns None if the file is not chosen.
    # Returns the filename extention value (an int) if chosen
    print(f"ELC@174 _log_file_filter  fname='{fname}'  {fsize=}")

    if ftype != "f": return None
    #
    parts = fname.rsplit('.',1)
    if len(parts) != 2: return None
    #
    fpart    = parts[0]
    ext_part = parts[1]
    #
    if fpart != "mws_log": return None
    ext_val = is_3_digit_int(ext_part)
    ###print(f"ELC@186   extension is_3_digit_int('{ext_part}') is {ext_val}")
    if ext_val is None: return None
    return ext_val


def extract_simplified_classname(obj_instance):
    # given a full class name string like "abc.def.MyClass"; return "MyClass"
    # Obtain the string using  str(obj.__class__)
    obj_repr = repr(obj_instance)
    #print(f"ELC@195 extract_simplified_classname   {obj_repr=}")
    parts = obj_repr.rsplit(".", 1)
    #print(f"ELC@197  {parts=}")
    name_and_addr = parts[-1]
    parts = name_and_addr.split(None, 1)
    #print(f"ELC@200  {parts=}")

    simplified_class_name = parts[0]
    simplified_class_name = simplified_class_name.replace("<", "")
    simplified_class_name = simplified_class_name.replace(">", "")
    return simplified_class_name

###
