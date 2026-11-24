# test_elem_log_file_table.py
#
# Test for logger_elem.ElemLogFileTable.py

import os

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass
from ztest_common.file_helpers_for_tests import list_dir_names
from ztest_common.file_helpers_for_tests import read_a_file_as_string

from lib1.platform_info import USING_PICO_HARDWARE, USING_LINUX_HARDWARE
from logger_elem.ElemLogFileTable import ElemLogFileTable
from logger_elem.ElemLogFileTable import _check_for_low_filespace
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
        print(f"TELF$105 {curr_log_path=}")

        elft.log_one_line("TELF$107 test_log_one_line Writing just one line to log")
    
        elft.flush_log_file()

        curr_log_path = elft.get_current_log_fpath()
        print(f"TELF$112 {curr_log_path=}")
        assert curr_log_path.startswith(logs_dir + "/"), (curr_log_path, logs_dir)

        file_stg = read_a_file_as_string(curr_log_path)
        print(f"TELF$116  {file_stg=}")
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


#== TESTS FOR SUPPORT FUNCTIONS  =================================================

# These tests do not need to read/write anything to/from filespace.

def test_check_for_low_filespace() -> None:
    print(f"TELF$138 test_check_for_low_filespace()")

    stats = os.statvfs("/")
    block_size = stats[0]     # f_bsize: File system block size (in bytes)
    total_blocks = stats[2]   # f_blocks: Total number of blocks
    free_blocks = stats[3]    # f_bfree: Number of free blocks
    # Calculate sizes in bytes
    total_bytes = block_size * total_blocks
    free_bytes = block_size * free_blocks
    used_bytes = total_bytes - free_bytes
    assert total_bytes

    # Sample values on Linux
    # free_bytes=         1805871259648
    # FREESPACE_MIN_BYTES=1500000000000.
    # Test the very edge of 'all is ok'
    print(f"TELF$154 Test the 'very edge' of 'all is ok'")
    log_fspace_high_watermark = 1234
    fsize_of_extant_logfiles = (log_fspace_high_watermark - 1)
    freespace_min_bytes = free_bytes - 1
    result = _check_for_low_filespace(
                    fsize_of_extant_logfiles,
                    log_fspace_high_watermark,
                    freespace_min_bytes)
    print(f"TELF$162  {fsize_of_extant_logfiles=}  {result=}")
    assert result[0] == ""
    assert isinstance(result[1], str)

    print(f"TELF$166 Test barely exceeding the high watermark")
    log_fspace_high_watermark = 1234
    fsize_of_extant_logfiles = (log_fspace_high_watermark)
    freespace_min_bytes = free_bytes - 1
    result = _check_for_low_filespace(
                    fsize_of_extant_logfiles,
                    log_fspace_high_watermark,
                    freespace_min_bytes)
    print(f"TELF$174  {fsize_of_extant_logfiles=}  {result=}")
    assert result[0] == "logfile_sizes_too_high"
    assert isinstance(result[1], str)

    print(f"TELF$178 Test the 'just 1 byte too little free space'")
    log_fspace_high_watermark = 1234
    fsize_of_extant_logfiles = (log_fspace_high_watermark - 1)
    freespace_min_bytes = free_bytes 
    result = _check_for_low_filespace(
                    fsize_of_extant_logfiles,
                    log_fspace_high_watermark,
                    freespace_min_bytes)
    print(f"TELF$186  {fsize_of_extant_logfiles=}  {result=}")
    assert result[0] == "freespace_low"
    assert isinstance(result[1], str)




#== HELPER FUNCTIONS  =================================================

def check_production_log_dir_unchanged(old_logs_dir: str, old_logs_dir_items_before: list[str] | None) -> bool:
    """ True if the production log directory is as it was: same file names 
    or the directory is still missing if it was missing before the test.
    This checks to make sure the test(s) do not disturb the production
    logs/ dir.
    """
    after = list_dir_names(old_logs_dir)
    if after == old_logs_dir_items_before:
        return True
    print(f"TELF$204: production log dir CHANGED: {old_logs_dir}, before: {old_logs_dir_items_before}, after: {after}")
    return False




###
