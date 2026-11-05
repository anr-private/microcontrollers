# test_elem_log_file_table.py
#
# Test for logger_elem.ElemLogFileTable.py

import os

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass
from ztest_common.file_helpers_for_tests import list_dir_names
from ztest_common.file_helpers_for_tests import read_a_file_as_string

from logger_elem.ElemLogFileTable import ElemLogFileTable
from logger_elem.ElemLogFileTable import Z__set_log_file_dir
from logger_elem.ElemLogFileTable import Z__set_max_log_file_size
from logger_elem.ElemLogFileTable import Z__set_log_fspace_high_watermark
from logger_elem.ElemLogFileTable import Z__set_log_fspace_low_watermark
from logger_elem.ElemLogFileTable import EMPTY_LOG_FPATH_MARKER_STG

try: from typing import Any
except ImportError: pass

#def EXAMPLE_test_SKELETON_for_tests() -> None:
def test_SKELETON_for_tests() -> None:
    """ """
    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    # Clear out any leftover 'global' stuff in ElemLogControl
    #@@@@@@@@@ TODO anything here?
    ###ElemLogControl._nullify_instance()
    ###elc = ElemLogControl.get_instance()
    elft = ElemLogFileTable()
    try:
        pass # PUT TEST CODE HERE
    finally:
        # Leave no (log) files dangling open - esp on Pico
        elft.close_logging()
        #@@@@@@@ElemLogControl._nullify_instance()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)


def test_get_current_log_fpath_no_files_open() -> None:
    """ Trivial case: no files open yet """
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    elft = ElemLogFileTable()
    try:
        got_path = elft.get_current_log_fpath()
        assert got_path == EMPTY_LOG_FPATH_MARKER_STG, got_path
    
        got_fsize = elft.get_current_log_fsize()
        assert got_fsize == 0, got_fsize
    finally:
        elft.close_logging()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)


def test_get_log_table_info_when_empty() -> None:
    """ trivial table content: no items """

    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    elft = ElemLogFileTable()
    try:

        # Table is empty initially
        item = elft.get_log_table_item(0)
        assert item is None
    
        num_removed = elft.get_number_of_removed_logfiles()
        assert num_removed == 0, num_removed

        num_extant = elft.get_number_of_extant_logfiles()
        assert num_extant == 0, num_extant

        removed_fsize = elft.get_fsize_of_removed_logfiles()
        assert removed_fsize == 0, removed_fsize

        extant_fsize = elft.get_fsize_of_extant_logfiles()
        assert extant_fsize == 0, extant_fsize

    finally:
        elft.close_logging()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)



def test_log_one_line() -> None:
    """ basic test for log_one_line() """
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    old_logs_dir = Z__set_log_file_dir(logs_dir)
    old_logs_dir_items_before = list_dir_names(old_logs_dir)

    elft = ElemLogFileTable()
    try:
        curr_log_path = elft.get_current_log_fpath()
        print(f"TELF@104 {curr_log_path=}")

        elft.log_one_line("TELF@106 test_log_one_line Writing just one line to log")
    
        curr_log_path = elft.get_current_log_fpath()
        print(f"TELF@109 {curr_log_path=}")
        assert curr_log_path.startswith(logs_dir + "/"), (curr_log_path, logs_dir)

        file_stg = read_a_file_as_string(curr_log_path)
        print(f"TELF@113  {file_stg=}")
        assert file_stg is not None, file_stg
        assert "OPENED NEW LOG" in file_stg, file_stg

        # verify there is only 1 log file and has an expected name (prefix)
        names = os.listdir(logs_dir)
        assert len(names) == 1, names
        assert names[0].startswith("mws_log."), names


    finally:
        elft.close_logging()
        Z__set_log_file_dir(old_logs_dir)
        remove_scratch_path(logs_dir)
        # there should be no change to the production logs/ dir
        assert check_production_log_dir_unchanged(old_logs_dir, old_logs_dir_items_before), old_logs_dir

def check_production_log_dir_unchanged(old_logs_dir: str, old_logs_dir_items_before: list[str] | None) -> bool:
    """ True if the production log directory is as it was: same file names 
    or the directory is still missing if it was missing before the test.
    This checks to make sure the test(s) do not disturb the production
    logs/ dir.
    """
    after = list_dir_names(old_logs_dir)
    if after == old_logs_dir_items_before:
        return True
    print(f"TELF@139: production log dir CHANGED: {old_logs_dir}, before: {old_logs_dir_items_before}, after: {after}")
    return False




###
