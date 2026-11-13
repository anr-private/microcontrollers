# test_elem_log_control.py
#
# Test for logger_elem.ElemLogControl.py
# # LINEMARKER=TELC

import os


from ztest_logger_elem.ClassA import ClassA
from ztest_logger_elem.ClassB import ClassB

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass

from logger_elem.ElemLogControl import ElemLogControl
from logger_elem.ElemLogFileTable import Z__set_log_file_dir

# NOTE: the setup_method() and teardown_method() used by the 
# 'old' CPython pytest classes are replaced by explicit calls
# in each test that nullify ElemLogControl and do get_instance().

def EXAMPLE_test_SKELETON_for_tests() -> None:
    """ """
    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    # Clear out any leftover 'global' stuff in ElemLogControl
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        pass # PUT TEST CODE HERE
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)


def test_registry_trivial_case() -> None:
    """ The registry contains one element, ElemLogControl itself.
    It is created when the instance is created.
    """
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        classes = elc.get_registered_classes()
        assert len(classes) == 1, classes
        # classes is a view object, does not support [0]
        assert list(classes)[0] == "ElemLogControl"
    finally:
        elc.close_all_logging()
        ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)


def test_get_lines_from_log_file() -> None:
    """ Try a simple fetch of lines from a log file """
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
         # fill the log with recognizable pattern of lines
        for i in range(10):
            elc.log_one_line(f"ELFT: THIS is line {i+1}")
    
        relative_line_number = 4
        number_of_lines = 2
        lines = elc.get_lines_from_log_file(relative_line_number, number_of_lines)
        print(f"TELC$76 lines:...")
        print(lines)
    
        assert len(lines) == 2, len(lines)
        line1 = lines[0]
        line2 = lines[1]
        assert line1 == "ELFT: THIS is line 7", line1
        assert line2 == "ELFT: THIS is line 8", line2
    finally:
        elc.close_all_logging()
        ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)


def test_registry_access() -> None:
    """ Test simplest access to the registry of 
    registered classes that are loggers - that is, classes
    that invoke log() functions to write to a log.
    """
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        # By default the ElemLogControl class registers itself
        registry_size = elc.get_registry_size()
        assert registry_size == 1, registry_size
    
        aa = ClassA(1)
        bb = ClassB(2)
        aaa = ClassA(3)
        bbb = ClassB(4)
    
        for clsname in elc.get_registered_classes():
            logger = elc.get_logger_for_class(clsname)

            assert logger is not None
            print(f"TELC$111  {clsname=}  {logger} ")
            assert logger.is_enabled() is True
    
        a_logger = elc.get_logger_for_class("ClassA")
        print(f"TELC$115 class A logger is {a_logger}")
        b_logger = elc.get_logger_for_class("ClassB")
        print(f"TELC$117 class B logger is {b_logger}")
    
        assert a_logger is not None
        assert b_logger is not None
    
        a_logger.enable_log(True)
        print(f"TELC$123  a_logger is {a_logger}")
        for clsname in elc.get_registered_classes():
            logger = elc.get_logger_for_class(clsname)
            assert logger is not None, clsname
            print(f"TELC$125  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
                # skip  - it uses faked logger/logging
                continue
            if logger.class_name == "ClassA":
                assert logger.is_enabled() is True
            elif logger.class_name == "ClassB":
                #@@@@@@@@@@@@@@@@@@@@ by default logging is enabled in ElemLogger
                assert logger.is_enabled() is True
                #@@@@@@@assert logger.is_enabled() is False
            else:
                assert False, f"UNKNOWN LOGGER {logger}"
    
        b_logger.enable_log(True)
        print(f"TELC$137  b_logger is {b_logger}")
        for clsname in elc.get_registered_classes():
            logger = elc.get_logger_for_class(clsname)

            assert logger is not None, clsname

            print(f"TELC$139  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
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
        for clsname in elc.get_registered_classes():
            logger = elc.get_logger_for_class(clsname)

            assert logger is not None, clsname

            print(f"TELC$153  {clsname=}  {logger} ")
            if clsname == "ElemLogControl":
                # skip  - it uses faked logger/logging
                continue
            assert logger.is_enabled() is False

    finally:
        elc.close_all_logging()
        ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)

def test_get_unmatched_override_classnames() -> None:
    """ """
    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    # Clear out any leftover 'global' stuff in ElemLogControl
    ElemLogControl._nullify_instance()
    elc = ElemLogControl.get_instance()
    try:
        aa = ClassA(1)
        bb = ClassB(2)
        aaa = ClassA(3)
        bbb = ClassB(4)

        registered = elc.get_registered_classes()

        print(f"TELC$199 {registered=}")

        # ClassA, ClassB, ElemLogControl itself
        assert elc.get_registry_size() == 3
        
        unmatched = elc.get_unmatched_override_classnames()
        assert len(unmatched) == 0

        

        
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elc.close_all_logging()
        ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)




###
