# test_elem_logger_abc.py
#
# Use 'pytest -s' to see stdout
# Use 'pytest -v' to see more details
# Use pytest TestHdrAccum.py::TestHdrAccum::test_xxx   to run just that test

import os
import sys
import pytest

# mimics the micropython inclusion of ':/lib' on its path
sys.path.append("./lib")

PLATFORM="cpython"
print(f"ZTELABC$15  platform is {PLATFORM}")

from cpython_test_support import CpythonTestSupport, FileHelper


from logger_elem.ElemLogControl import ElemLogControl
from logger_elem.ElemLoggerABC import ElemLoggerABC
from logger_elem.ElemLogFileTable import LOG_FILES_SUBDIR

from ztest_logger_elem.ClassA import ClassA

try: from typing import Any
except ImportError: pass


class TestElemLoggerABC:

    def setup_method(self, method:Any) -> None:
        print("ZTELABC$33 setup method call")
        # Remove any previous instance
        ElemLogControl._nullify_instance()

    def teardown_method(self, method:Any) -> None:
        ###ElemLogControl.get_instance().remove_old_log_file()
        ElemLogControl._nullify_instance()
        

    #@pytest.mark.skip(reason="@$@$@$@$@$@$@$@$@$@$@$@@")
    def test_1(self) -> None:
        print(f"ZTELABC$44  === test_1  =================")

        fhelper = FileHelper.get_instance()

        fhelper.remove_subdir(LOG_FILES_SUBDIR)

        ElemLoggerABC._enable_prt(True)

        aa = ClassA(111)

        elc = ElemLogControl.get_instance()
        print(f"ZTELABC$55  elc is {elc}")

        if 1:
            clses = elc.get_registered_classes()
            print(f"ZTELABC$59 registered classes: {clses}")
            print(f"ZTELABC$60 registered classes type: {type(clses)}")

        mm = "This log line is from ZTELABC$62"
        aa.to_log(mm)


        #@@@@@@@@ LOGGING IS ENABLED by default in ElemLogger at the moment
        # by default logging is disabled
        elc.flush_current_log_file()
        got = _read_log_file(elc)
        #@@@@@@@@@@@@@@@assert got is None
        assert isinstance(got, str)

        exp_name = aa.__class__.__name__
        print(f"ZTELABC$74  {exp_name=}")
        assert aa.__class__.__name__ in clses

        elc.enable_logging(aa.__class__.__name__, True)

        logmesg_1 = "This log line is from ZTELABC$79"
        aa.to_log(logmesg_1)

        elc.flush_current_log_file()
        got = _read_log_file(elc)
        assert got is not None
        print(f"ZTELABC$85 log file contents len={len(got)}")
        print(f"ZTELABC$86 log file contents {got!r}")
        ###assert len(got) == 100
        assert logmesg_1 in got


def _read_log_file(elc: ElemLogControl) -> str | None:
    elft = elc._log_file_table
    try:
        with open(elft._current_log_fpath, "r") as inf:
            return inf.read()
    except Exception as ex:
        print(f"ZTELABC$97 Reading log file got ex={ex}")
    return None

def _remove_old_log_file(log_fpath: str) -> None:
    print(f"ZTELABC$101 Remove old log file, if any: path='{log_fpath}'")
    # remove old log if any
    try:
        os.remove(log_fpath)
        print(f"ZTELABC$105 Removed old log file '{log_fpath}'")
    except OSError as ex:
        if 0:
            print(f"ZTELABC$108 FAILED to delete log '{log_fpath}': {repr(ex)}")
            print(f"ZTELABC$109 ex='{str(ex)}' ")




###
                                            
