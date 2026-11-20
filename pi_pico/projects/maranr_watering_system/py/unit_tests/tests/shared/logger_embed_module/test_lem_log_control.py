# test_lem_log_control.py
#
# Test for logger_embed_module.LemLogControl
# LINEMARKER=ZLLC

import os

from ztest_logger_embed_module.ClassA import ClassA
from ztest_logger_embed_module.ClassB import ClassB
from ztest_logger_embed_module.ZLemLogFileTable import ZLemLogFileTable

from logger_embed_module.LemLogControl import LemLogControl, Z_replace_log_file_table

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass

try: from typing import Callable, Any, Literal
except ImportError: pass

Z_TESTS_PARAMETER_SELECTOR = "Z_tests"

class LemTestContext():
    def __init__(self, log_parameters_selector:str=Z_TESTS_PARAMETER_SELECTOR) -> None:
        self._llc: LemLogControl | None = None
        self._log_parameters_selector = log_parameters_selector

    def __enter__(self) -> LemLogControl:
        print(f"ZLLC$28 ENTER lem test context...")
        ###logs_dir = get_scratch_path("logs")
        ###remove_scratch_path(logs_dir)
        ###self._llc = LemLogControl.configure_logger(logs_dir)

        # Using None for logs_dir
        #@@@@@@@@@self._llc = LemLogControl.configure_logger(None)
        self._llc = LemLogControl.configure_logger(None, self._log_parameters_selector)
        assert self._llc is not None

        zllft = ZLemLogFileTable()
        Z_replace_log_file_table(zllft)
        print(f"ZLLC$40: ENTER  USING LogCtl: {self._llc=!r}")
        print(f"ZLLC$41: ENTER  USING FAKE:   {zllft!r}")

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


def test_registry_trivial_case() -> None:
    """ The registry contains one element, LemLogControl itself.
    It is created when the instance is created.
    """

    with LemTestContext() as llc:
        zllft = ZLemLogFileTable()
        Z_replace_log_file_table(zllft)

        classes = llc.get_registered_classes()
    
        print(f"ZLLC$69  registered_classes: {classes}")
        assert len(classes) == 1, classes
        # classes is a view object, does not support [0]
        assert list(classes)[0] == "LemLogControl"


def test_get_unmatched_override_classnames() -> None:
    """ """
    with LemTestContext() as llc:
        aa = ClassA(1)
        bb = ClassB(2)
        aaa = ClassA(3)
        bbb = ClassB(4)
    
        registered = llc.get_registered_classes()
    
        print(f"ZLLC$85 {registered=}")
    
        # ClassA, ClassB, LemLogControl itself
        assert llc.get_registry_size() == 3
        
        unmatched = llc.get_unmatched_override_classnames()
        assert len(unmatched) == 0


def test_get_lines_from_log_file() -> None:
    """ Try a simple fetch of lines from a log file """
    with LemTestContext() as llc:
         # fill the log with recognizable pattern of lines
        fmt =  "--ZLLC--: THIS is line %s"
        for i in range(10):
            llc.log_one_line(fmt % (i+1))
    
        relative_line_number = 4
        number_of_lines = 2
        lines = llc.get_lines_from_log_file(relative_line_number, number_of_lines)
        print(f"ZLLC$105 lines: {lines}")
    
        assert len(lines) == 2, len(lines)
        line1 = lines[0]
        line2 = lines[1]
        exp1 = fmt % 7
        exp2 = fmt % 8
        assert line1 == exp1, (exp1, line1)
        assert line2 == exp2, (exp2, line2)


def test_registry_access() -> None:
    """ Test simplest access to the registry of 
    registered classes that are loggers - that is, classes
    that invoke log() functions to write to a log.
    """
    with LemTestContext() as llc:
        # By default the LemLogControl class registers itself
        registry_size = llc.get_registry_size()
        assert registry_size == 1, registry_size
    
        aa = ClassA(1)
        bb = ClassB(2)
        aaa = ClassA(3)
        bbb = ClassB(4)
    
        for clsname in llc.get_registered_classes():
            logger = llc.get_logger_for_class(clsname)
    
            assert logger is not None
            print(f"ZLLC$135  {clsname=}  {logger} ")
            assert logger.is_enabled() is True
    
        a_logger = llc.get_logger_for_class("ClassA")
        print(f"ZLLC$139 class A logger is {a_logger}")
        b_logger = llc.get_logger_for_class("ClassB")
        print(f"ZLLC$141 class B logger is {b_logger}")
    
        assert a_logger is not None
        assert b_logger is not None

        a_logger.enable_log(True)
        print(f"ZLLC$147  a_logger is {a_logger}")
        for clsname in llc.get_registered_classes():
            logger = llc.get_logger_for_class(clsname)
            assert logger is not None, clsname
            print(f"ZLLC$151  {clsname=}  {logger} ")
            if clsname == "LemLogControl":
                # skip  - it uses faked logger/logging
                continue
            if logger.class_name == "ClassA":
                assert logger.is_enabled() is True
            elif logger.class_name == "ClassB":
                # ASSUMES by default logging is enabled in LemLogger
                assert logger.is_enabled() is True
                # ELSE assert logger.is_enabled() is False
            else:
                assert False, f"UNKNOWN LOGGER {logger}"
    
        b_logger.enable_log(True)
        print(f"ZLLC$165  b_logger is {b_logger}")
        for clsname in llc.get_registered_classes():
            logger = llc.get_logger_for_class(clsname)
    
            assert logger is not None, clsname
    
            print(f"ZLLC$171  {clsname=}  {logger} ")
            if clsname == "LemLogControl":
                # skip  - it uses faked logger/logging
                continue
            if logger.class_name == "ClassA":
                assert logger.is_enabled() is True
            elif logger.class_name == "ClassB":
                assert logger.is_enabled() is True
            else:
                assert False, f"UNKNOWN LOGGER {logger}"
    
        a_logger.enable_log(False)
        b_logger.enable_log(False)
        for clsname in llc.get_registered_classes():
            logger = llc.get_logger_for_class(clsname)
    
            assert logger is not None, clsname
    
            print(f"ZLLC$189  {clsname=}  {logger} ")
            if clsname == "LemLogControl":
                # skip  - it uses faked logger/logging
                continue
            assert logger.is_enabled() is False


###
