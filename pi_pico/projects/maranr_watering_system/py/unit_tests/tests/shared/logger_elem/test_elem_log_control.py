# test_elem_log_control.py
#
# Shared test for logger_elem.ElemLogControl

import os

if 1:
    #@@@@@@@@@@@@@@@@@@@@@@@@
    import sys
    for s in sys.path:
        print(f"PATH: {s}")

from ztest_logger_elem.ClassA import ClassA
from ztest_logger_elem.ClassB import ClassB

#from lib1.file_utils import xxx
#@@@@@@ NEEDED?
from lib1.utils import string_to_int

try: from cpython_glue import get_scratch_path
except ImportError: pass

from logger_elem.ElemLogControl import ElemLogControl

# NOTE: the setup_method() and teardown_method() used by the 
# 'old' CPython pytest classes are replaced by explicit calls
# in each test that nullify ElemLogControl and do get_instance().

def test_USE_THIS_SKELETON_as_basis_for_all_tests() -> None:
    """ """
    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    # Clear out any leftover 'global' stuff in ElemLogControl
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        pass # PUT TEST CODE HERE
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()


def test_registry_trivial_case() -> None:
    """ The registry contains one element, ElemLogControl itself.
    It is created when the instance is created.
    """
    logs_dir = get_scratch_path("logs")
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        classes = elc.get_registered_classes()
        assert len(classes) == 1, classes
        # classes is a view object, does not support [0]
        assert list(classes)[0] == "ElemLogControl"
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()


def test_get_lines_from_log_file() -> None:
    """ Try a simple fetch of lines from a log file """
    logs_dir = get_scratch_path("logs")
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()

    try:
         # fill the log with recognizable pattern of lines
        for i in range(10):
            elc.log_one_line(f"THIS is line {i+1}")
    
        relative_line_number = 4
        number_of_lines = 2
        lines = elc.get_lines_from_log_file(relative_line_number, number_of_lines)
        print(f"@@TELC@62 lines:...")
        print(lines)
    
        assert len(lines) == 2, len(lines)
        line1 = lines[0]
        line2 = lines[1]
        assert line1 == "THIS is line 7", line1
        assert line2 == "THIS is line 8", line2
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()



def test_registry_access() -> None:
    """ Test simplest access to the registery of 
    registered classes that are loggers - that is, classes
    that invoke log() functions to write to a log.
    """
    logs_dir = get_scratch_path("logs")
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()

    try:
        # By default the ElemLogControl class registers itself
        assert len(elc.registry) == 1
    
        aa = ClassA(1)
        bb = ClassB(2)
        aaa = ClassA(3)
        bbb = ClassB(4)
    
        for clsname, logger in elc.registry.items():
            print(f"@@TELC@67  {clsname=}  {logger} ")
            assert logger.is_enabled() is False
    
        a_logger = elc.registry.get("ClassA")
        print(f"@@TELC@85 class A logger is {a_logger}")
        b_logger = elc.registry.get("ClassB")
        print(f"@@TELC@87 class B logger is {b_logger}")
    
        assert a_logger is not None
        assert b_logger is not None
    
        a_logger.enable_log(True)
        print(f"@@TELC@90  a_logger is {a_logger}")
        for clsname, logger in elc.registry.items():
            print(f"@@TELC@92  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
                # skip  - it uses faked logger/logging
                continue
            if logger.class_name == "ClassA":
                assert logger.log_enabled is True
            elif logger.class_name == "ClassB":
                assert logger.log_enabled is False
            else:
                assert False, f"UNKNOWN LOGGER {logger}"
    
        b_logger.enable_log(True)
        print(f"@@TELC@101  b_logger is {b_logger}")
        for clsname, logger in elc.registry.items():
            print(f"@@TELC@103  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
                # skip  - it uses faked logger/logging
                continue
            if logger.class_name == "ClassA":
                assert logger.log_enabled is True
            elif logger.class_name == "ClassB":
                assert logger.log_enabled is True
            else:
                assert False, f"UNKNOWN LOGGER {logger}"
    
        a_logger.enable_log(False)
        b_logger.enable_log(False)
        for clsname, logger in elc.registry.items():
            print(f"@@TELC@114  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
                # skip  - it uses faked logger/logging
                continue
            assert logger.log_enabled is False

    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()



###
