# test_lem_log_ABC.py
#
# Use 'pytest -s' to see stdout
# Use 'pytest -v' to see more details
# Use pytest TestHdrAccum.py::TestHdrAccum::test_xxx   to run just that test
#  @pytest.mark.skip(reason="XXXXXXXXXXXXXXXXXXXXXXXX")
#
# LINEMARKER=ZLLABC

import os
import sys
import pytest

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass

from ztest_logger_embed_module.ClassA import ClassA
#from ztest_logger_embed_module.ClassB import ClassB
from ztest_logger_embed_module.ZLemLogFileTable import ZLemLogFileTable

from logger_embed_module.LemLogControl import LemLogControl, Z_replace_log_file_table
from logger_embed_module.LemLogABC import LemLogABC
from logger_embed_module.LemLogger import LemLogger

try: from typing import Callable, Any, Literal
except ImportError: pass

Z_TESTS_PARAMETER_SELECTOR = "Z_tests"


class LemTestContext:
    def __init__(self, log_parameters_selector:str=Z_TESTS_PARAMETER_SELECTOR) -> None:
        self._llc: LemLogControl | None = None
        self._log_parameters_selector = log_parameters_selector

    def __enter__(self) -> LemLogControl:
        print(f"ZLLABC$37 ENTER lem test context...")
        ###logs_dir = get_scratch_path("logs")
        ###remove_scratch_path(logs_dir)
        ###self._llc = LemLogControl.configure_logger(logs_dir)

        # Using None for logs_dir
        self._llc = LemLogControl.configure_logger(None, self._log_parameters_selector)
        assert self._llc is not None

        zllft = ZLemLogFileTable()
        Z_replace_log_file_table(zllft)
        print(f"ZLLABC$48: ENTER  USING LogCtl: {self._llc=!r}")
        print(f"ZLLABC$49: ENTER  USING FAKE:   {zllft!r}")

        # This is what the 'as' variable receives
        return self._llc

    def __exit__(self, 
          exc_type: "type[BaseException] | None",
          exc_val: "BaseException | None",
          exc_tb: "object",  # Or "TracebackType | None" if imported under TYPE_CHECKING
          ) -> "Literal[False]":    ###bool | None:

        if self._llc is not None:
            self._llc.close_all_logging()
        # Returning True here suppresses exceptions; returning False/None lets them propagate
        return False # raise any exception(s)


def test_class_gets_registered() -> None:
    print(f"ZLLABC$67  === test_1  =================")

    with LemTestContext() as llc:
        LemLogABC._enable_prt(True)
    
        #print(f"ZLLABC$72 logged lines: {zllft.z_get_lines()}")
    
        aa = ClassA(111)
    
        ###@@@@@llc = LemLogControl.get_instance()
        print(f"ZLLABC$77  llc is {llc}")
    
        if 1:
            clses = llc.get_registered_classes()
            print(f"ZLLABC$81 registered classes: {clses}")
            print(f"ZLLABC$82 registered classes type: {type(clses)}")
    
        exp_class_name = aa.__class__.__name__
        print(f"ZLLABC$85  {exp_class_name=!r}")
        assert exp_class_name in clses
    
        the_logger = llc.get_logger_for_class(exp_class_name)
        print(f"ZLLABC$89 {the_logger!r}")
        assert isinstance(the_logger, LemLogger)
    
        # just try getting the value
        # its value depends on default logging-enabled state in LemLogControl
        f = the_logger.is_enabled()



# SAVED STUFF - but this really belongs in the test for LemLogControl
#
#
#    # turn logger on, if it's not on
#    if not the_logger.is_enabled():
#        llc.enable_logging(
#
#    exp_line = "from ZLLABC$105"
#    aa.to_log(exp_line)
#    got_line = zllft.z_get_latest_line()
#    assert exp_line == got_line, got_line
#def test_class_gets_registered() -> None:
#    print(f"ZLLABC$110  === test_1  =================")
#
#    LemLogControl._nullify_instance()
#    llc = LemLogControl.get_instance()
#    zllft = ZLemLogFileTable()
#    Z_replace_log_file_table(zllft)
#
#    ###LemLogABC._enable_prt(True)
#
#    #print(f"ZLLABC$119 logged lines: {zllft.z_get_lines()}")
#
#    aa = ClassA(111)
#
#    llc = LemLogControl.get_instance()
#    print(f"ZLLABC$124  llc is {llc}")
#
#    if 1:
#        clses = llc.get_registered_classes()
#        print(f"ZLLABC$128 registered classes: {clses}")
#        print(f"ZLLABC$129 registered classes type: {type(clses)}")
#
#    exp_class_name = aa.__class__.__name__
#    print(f"ZLLABC$132  {exp_class_name=!r}")
#    assert exp_class_name in clses
#
#    the_logger = llc.get_logger_for_class(exp_class_name)
#    print(f"ZLLABC$136 {the_logger!r}")
#    #assert the_logger.is_enabled() is True
#    
#    # turn logger on, if it's not on
#    if not the_logger.is_enabled():
#        llc.enable_logging(
#
#    exp_line = "from ZLLABC$143"
#    aa.to_log(exp_line)
#    got_line = zllft.z_get_latest_line()
#    assert exp_line == got_line, got_line
#
#
#def SAVE():
#
#
#    llc.enable_logging(aa.__class__.__name__, True)
#
#    logmesg_1 = "from ZLLABC$154"
#    aa.to_log(logmesg_1)
#
#    got = _read_log_file(llc)
#    print(f"ZLLABC$158 log file contents len={len(got)}")
#    ###assert len(got) == 100
#    assert logmesg_1 in got
#
#
# def _read_log_file(llc):
    # elft = llc._log_file_table
    # try:
        # with open(elft._current_log_fpath, "r") as inf:
            # return inf.read()
    # except Exception as ex:
        # print(f"ZLLABC$169 Reading log file got ex={ex}")
# 
# def _remove_old_log_file(log_fpath):
    # print(f"ZLLABC$172 Remove old log file, if any: path='{log_fpath}'")
    # # remove old log if any
    # try:
        # os.remove(log_fpath)
        # print(f"ZLLABC$176 Removed old log file '{log_fpath}'")
    # except OSError as ex:
        # if 0:
            # print(f"ZLLABC$179 FAILED to delete log '{log_fpath}': {repr(ex)}")
            # print(f"ZLLABC$180 ex='{str(ex)}' ")
# 



###
                                            
