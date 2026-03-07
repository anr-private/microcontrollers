# ElemLogControl.py
# 
# Control and registrar for ElemLogger

import os
import sys

from utils import MWS_CONFIG

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
        ElemLogControl._clear_latest_messages()


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"ElemLogControl@34 CALLED CTOR use get_instance()"
            raise RuntimeError(m)
        self._log_file_path = "mws_log.txt"
        config_fpath = MWS_CONFIG.get("log_file_path")
        if config_fpath:
            self._log_file_path = config_fpath
        print(f"ElemLogControl@47  log_file_path='{self._log_file_path}' ")


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses ElemLogControlABC
        # Returns a tuple of the log functions the caller should use

        prt(f"ElemLogControl@42   obj is {repr(obj_instance)} ")

        # get the Class of the obj_instance
        #cls_obj = type(obj_instance)
        #prt(f"ElemLogControl@46  register obj={repr(cls_obj)}  type={type(cls_obj)}")        
        #cls_stg = str(cls_obj)
        #prt(f"ElemLogControl@33 @@@@@@@@@@@@@@@@ register {cls_stg=}")        

        simplified_class_name = extract_simplified_classname(obj_instance)
        prt(f"ElemLogControl@51 {simplified_class_name=}")

        # does this class have a logger assigned?
        logger = self.registry.get(simplified_class_name)
        prt(f"ElemLogControl@55  logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = ElemLogger(self, simplified_class_name)
            self.registry[simplified_class_name] = logger
        return logger


    def remove_old_log_file(self):
        # remove old log if any
        fpath = self._log_file_path
        try:
            os.remove(fpath)
            print(f"Old log file '{fpath}' deleted.")
        except OSError as ex:
            print(f"ElemLogControl@81 FAILED to delete log '{fpath}': {repr(ex)}")
            print(f"ElemLogControl@82 ex='{str(ex)}' ")

    def log_one_line(self, line):
        # write to file
        if line is None: line = ""
        fname = self._log_file_path
        try:
            with open(fname, "a") as f:
                f.write(line)
                f.write("\n")
        except Exception as ex:
            print(f"ElemLogControl@95: Error writing to file '{fname}': {repr(ex)}")
            print(f"ElemLogControl@56: Error writing to file '{fname}': {str(ex)}")



def extract_simplified_classname(obj_instance):
    # given a full class name string like "abc.def.MyClass"; return "MyClass"
    # Obtain the string using  str(obj.__class__)
    obj_repr = repr(obj_instance)
    prt(f"ElemLogControl@70 extract_simplified_classname   {obj_repr=}")
    parts = obj_repr.rsplit(".", 1)
    prt(f"ElemLogControl@73  {parts=}")
    name_and_addr = parts[-1]
    parts = name_and_addr.split(None, 1)
    prt(f"ElemLogControl@76  {parts=}")

    simplified_class_name = parts[0]
    return simplified_class_name

###
