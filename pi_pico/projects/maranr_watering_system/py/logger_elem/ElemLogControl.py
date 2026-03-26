# ElemLogControl.py
# 
# Control and registrar for ElemLogger

import os
import sys

from utils import MWS_CONFIG
from file_utils import read_last_n_lines

from .ElemLogger import ElemLogger

VALIDATE = 13524690

PRT=False
def prt(s):
    if PRT: print (s)


class ElemLogControl:
    # central control for logging
    # Handles the log file(s) - the only class that does so

    _instance = None

    # key: simplified class name   value: ElemLogger for that class
    registry = {}

    
    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = ElemLogControl(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        ElemLogControl._instance = None
        # Remove any messages - unit test only
        #ElemLogControl._clear_latest_messages()


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"ELC@44 CALLED CTOR use get_instance()"
            raise RuntimeError(m)
        self._log_file_path = "mws_log.txt"
        config_fpath = MWS_CONFIG.get("log_file_path")
        if config_fpath:
            self._log_file_path = config_fpath
        print(f"ELC@50  log_file_path='{self._log_file_path}' ")


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses ElemLogControlABC
        # Returns a logger obj the caller should use

        prt(f"ELC@57   obj is {repr(obj_instance)} ")

        simplified_class_name = extract_simplified_classname(obj_instance)
        prt(f"ELC@60 {simplified_class_name=}")

        # does this class have a logger assigned?
        logger = self.registry.get(simplified_class_name)
        prt(f"ELC@64  logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = ElemLogger(self, simplified_class_name)
            self.registry[simplified_class_name] = logger
        if 0: self.dump_registered_loggers(self.registry)
        return logger


    def get_registered_classes(self):
        return self.registry.keys()

    def enable_logging(self, class_name, enabled):
        logger = self.registry.get(class_name)
        print(f"@@@@ ELC@79 logger is {logger}  {enabled=}")
        logger.enable_log(enabled)


    def remove_old_log_file(self):
        # remove old log if any
        fpath = self._log_file_path
        try:
            os.remove(fpath)
            print(f"ELC@77 Old log file '{fpath}' deleted.")
        except OSError as ex:
            print(f"ELC@79 FAILED to delete log '{fpath}': {repr(ex)}")
            print(f"ELC@80 ex='{str(ex)}' ")


    def log_one_line(self, line):
        need_to_remove = self._log_this_line(line)
        if need_to_remove:
            print(f"ELC@85 REMOVING the current log file: error occurred, maybe out of space?")
            self.remove_old_log_file()
            self._log_this_line("ELC@87 REMOVED THE PREVIOUS LOGFILE - logger got an error")

    def _log_this_line(self, line):
        # write to file
        if line is None: line = ""
        fname = self._log_file_path
        remove_the_logfile = False
        try:
            with open(fname, "a") as f:
                f.write(line)
                f.write("\n")
        except OSError as ex:
            # see examples/file_and_dirs_io/errno_show_all.py to see all errno values
            print(f"ELC@99  Error writingReading '{fname}' EX={repr(ex)}  EX='{str(ex)}' ")
            #print(f"ELC@100  ex.dir: {dir(ex)} ")
            # 28 is 'out of space'
            print(f"ELC@102 {ex.errno=}")
            print(f"ELC@103  TEMP FIX: REMOVE THE logfile ")
            remove_the_logfile = True
        except Exception as ex:
            print(f"ELC@106: Error writing to file '{fname}': {repr(ex)}")
            print(f"ELC@107: Error writing to file '{fname}': {str(ex)}")
            remove_the_logfile = True

        return remove_the_logfile


    def get_lines_from_log_file(self, relative_line_number, number_of_lines):
        # get lines from the log file
        # relative_line_number is the line number of the first line
        # being requested, relative to the end of the file.
        # number_of_lines is the number of lines
        # So (1,1) gets the last line in the file,
        # (10,2) gets the 10th and 9th lines from the end of file.
        lines = read_last_n_lines(self._log_file_path, 
                                  relative_line_number,
                                  number_of_lines)
        return lines


    def dump_registered_loggers(self, registry):
        m = "ELC@114  Classes registered in ElemLogControl:"
        prt(m)
        self.log_one_line(m)
        for k,v in self.registry.items():
            m = f"  {k}  {v}"
            prt(m)
            self.log_one_line(m)


def extract_simplified_classname(obj_instance):
    # given a full class name string like "abc.def.MyClass"; return "MyClass"
    # Obtain the string using  str(obj.__class__)
    obj_repr = repr(obj_instance)
    prt(f"ELC@127 extract_simplified_classname   {obj_repr=}")
    parts = obj_repr.rsplit(".", 1)
    prt(f"ELC@129  {parts=}")
    name_and_addr = parts[-1]
    parts = name_and_addr.split(None, 1)
    prt(f"ELC@132  {parts=}")

    simplified_class_name = parts[0]
    simplified_class_name = simplified_class_name.replace("<", "")
    simplified_class_name = simplified_class_name.replace(">", "")
    return simplified_class_name

###
