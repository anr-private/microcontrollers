# test_lem_log_file_table.py
#
# Test for logger_embed_module.LemLogFileTable.py
#
# #@pytest.mark.skip(reason="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#
# LINEMARKER=ZLLFT
#
# *** NOTE  ***
# The log files differ on Pico vs local Cpython3 tests:
# the logged info includes the path of the log file,
# which is longer for local logs: /tmp/MWS_tmp_abcdefgg/
# vs /_scratch_dir on PICO. 
# So tests on the number of bytes and number of lines in a log file
# differ.
# The tests currently accommodate this by allowing a 'fuzz' diff
# in the expected numbers.
# The fuzz variables in the tests are called 'allowed_xxx_diff'.
# NOTE the fuzz is currently applied to BOTH platforms
# as there is no 'standard' way for a test to know which
# platform it is running on.


import os

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass

from lib1.file_utils import remove_subdir

from ztest_common.file_helpers_for_tests import create_subdir_with_files
from ztest_common.file_helpers_for_tests import list_dir_names
from ztest_common.file_helpers_for_tests import read_a_file_as_string
from ztest_common.file_helpers_for_tests import read_a_file_as_lines

from logger_embed_module.LemLogFileTable import LemLogFileTable

from logger_embed_module.LemLogFileTable import _determine_starting_fname_extension_value
from logger_embed_module.LemLogFileTable import _determine_biggest_existing_log_fname_extension_value
from logger_embed_module.LemLogFileTable import _determine_new_starting_extension_value
from logger_embed_module.LemLogFileTable import MESG_CANNOT_CREATE_LOGS_SUBDIRECTORY
from logger_embed_module.LemLogFileTable import LOGFILE_WAS_REMOVED, LOGFILE_IS_EXTANT
from logger_embed_module.LemLogFileTable import EMPTY_LOG_FPATH_MARKER_STG

try: from typing import Any, Literal
except ImportError: pass

Z_TESTS_PARAMETER_SELECTOR = "Z_tests"

# Context Manager for running tests
class LemTestContext():
    def __init__(self, log_parameters_selector:str=Z_TESTS_PARAMETER_SELECTOR) -> None:
        self._llft: LemLogFileTable | None = None
        self._log_parameters_selector = log_parameters_selector

    def __enter__(self) -> LemLogFileTable:
        print(f"ENTER lem test context...")
        logs_dir = get_scratch_path("logs")
        remove_scratch_path(logs_dir)
        self._llft = LemLogFileTable(logs_dir, self._log_parameters_selector)
        print(f"ZLLFT$61: ENTER  {self._llft=!r}")
        # This is what the 'as' variable receives
        return self._llft

    def __exit__(self, 
        exc_type: "type[BaseException] | None",
        exc_val: "BaseException | None",
        exc_tb: "object",  # Or "TracebackType | None" if imported under TYPE_CHECKING
        ) -> "Literal[False]":    ###bool | None:

        print(f"ZLLFT$71: EXIT lem test context.  {self._llft=!r}")
        logs_dir: str|None = None
        if self._llft is not None:
            logs_dir = self._llft.get_logs_directory()
            # Leave no (log) files dangling open - esp on Pico
            self._llft.close_logging()
        print(f"EXIT  {logs_dir=!r}")
        # Remove logs directory (if any)
        if logs_dir:
            remove_scratch_path(logs_dir)
        # Returning True here suppresses exceptions; returning False/None lets them propagate
        return False # raise any exception(s)


def test_log_parameters_selector() -> None:
    # NOTE this test will cause LemLogFileTable to print an error
    # because we never 
    with LemTestContext() as llft:
        print(f"ZLLFT$89 context: {llft=!r}")
        print(f"ZLLFT$90 context: str='{str(llft)}'")


def test_SKELETON_for_tests() -> None:
    # This is the old way - use the LemTestContext instead!
    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    log_parameters_selector="Z_tests"
    llft = LemLogFileTable(logs_dir, log_parameters_selector)
    try:
        pass # PUT TEST CODE HERE
    finally:
        # Leave no (log) files dangling open - esp on Pico
        llft.close_logging()
        remove_scratch_path(logs_dir)


def test_get_current_log_fpath_no_files_open() -> None:
    """ Trivial case: no files open yet """

    with LemTestContext() as llft:
        print(f"ZLLFT$112  start test  {llft=!r}")

        got_path = llft.get_current_log_fpath()
        assert got_path == EMPTY_LOG_FPATH_MARKER_STG, got_path
    
        got_fsize = llft.get_current_log_fsize()
        assert got_fsize == 0, got_fsize


def test_get_log_table_info_when_empty() -> None:
    """ trivial table content: no items """

    with LemTestContext() as llft:

        # Table is empty initially
        item = llft.get_log_table_item(0)
        assert item is None
    
        num_removed = llft.get_number_of_removed_logfiles()
        assert num_removed == 0, num_removed

        num_extant = llft.get_number_of_extant_logfiles()
        assert num_extant == 0, num_extant

        removed_fsize = llft.get_fsize_of_removed_logfiles()
        assert removed_fsize == 0, removed_fsize

        extant_fsize = llft.get_fsize_of_extant_logfiles()
        assert extant_fsize == 0, extant_fsize


def test_log_one_line() -> None:
    # basic test for log_one_line() 
    # Also a simple test for close_logging()
    with LemTestContext() as llft:
        curr_log_path = llft.get_current_log_fpath()
        print(f"ZLLFT$148 {curr_log_path=}")

        llft.log_one_line("ZLLFT$150 test_log_one_line Writing just one line to log")
    
        curr_log_path = llft.get_current_log_fpath()
        print(f"ZLLFT$153 {curr_log_path=}")
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None
        assert curr_log_path.startswith(logs_dir + "/"), (curr_log_path, logs_dir)

        file_stg = read_a_file_as_string(curr_log_path)
        print(f"ZLLFT$159  {file_stg=}")
        assert file_stg is not None, file_stg
        assert "OPENED NEW LOG" in file_stg, file_stg

        # verify there is only 1 log file and has an expected name (prefix)
        names = os.listdir(logs_dir)
        assert len(names) == 1, names
        assert names[0].startswith("mws_log."), names


def test_logging_after_closing() -> None:
    # Once close_logging() has been called, no further logging
    # is allowed/possible
    saved_llft = None
    with LemTestContext() as llft:
        saved_llft = llft

        curr_log_path = llft.get_current_log_fpath()
        print(f"ZLLFT$177 {curr_log_path=}")

        llft.log_one_line("ZLLFT$179 test_log_one_line Writing just one line to log")
        
        curr_log_path = llft.get_current_log_fpath()
        print(f"ZLLFT$182 {curr_log_path=}")
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None
        assert curr_log_path.startswith(logs_dir + "/"), (curr_log_path, logs_dir)

        file_stg = read_a_file_as_string(curr_log_path)
        print(f"ZLLFT$188  {file_stg=}")
        assert file_stg is not None, file_stg
        assert "OPENED NEW LOG" in file_stg, file_stg

        # verify there is only 1 log file and has an expected name (prefix)
        names = os.listdir(logs_dir)
        assert len(names) == 1, names
        assert names[0].startswith("mws_log."), names

    try:
        saved_llft.log_one_line(f"ZLLFT$198 SHOULD NOT BE ABLE TO LOG THIS LINE")
        assert False, "Expected an exception"
    except RuntimeError as ex:
        assert MESG_CANNOT_CREATE_LOGS_SUBDIRECTORY in str(ex), str(ex)


def test_log_one_line_call_many_times() -> None:
    # log many lines
    with LemTestContext() as llft:
        num_lines_written = 100
        line_len = 0
        for i in range(num_lines_written):
            lno = i+1
            line = f"ZLLFT$211 This is line {lno:3d}"
            llft.log_one_line(line)
            if line_len <= 0:
                line_len = len(line) 
            assert line_len == len(line)
        # expect fpath is "logs/mws_log.010"
        fpath = llft._current_log_fpath

        got_data = read_a_file_as_string(fpath)
        assert got_data is not None
        print(f"ZLLFT$221 len of log file data is {len(got_data)}")

        got_lines = got_data.split("\n")
        assert len(got_lines) == num_lines_written + 4




def test_get_lines_from_log_file() -> None:
    print(f"ZLLFT$230  === test_get_lines_from_log_file  ======")
    with LemTestContext() as llft:
        # fill the log with recognizable pattern of lines
        for i in range(10):
            llft.log_one_line(f"THIS is line {i+1}")
        relative_line_number = 4
        number_of_lines = 2
        got_lines = llft.get_lines_from_log_file(relative_line_number, number_of_lines)
        print(f"ZLLFT$238 lines:...")
        print(got_lines)
        exp_lines = ("THIS is line 7", "THIS is line 8")
        assert len(got_lines) == len(exp_lines)
        for j in range(len(got_lines)):
            got = got_lines[j]
            exp = exp_lines[j]
            assert got == exp


def test_rotating_the_files() -> None:
    print(f"ZLLFT$249  === test_rotating_the_files  ======")
    with LemTestContext() as llft:
        
        # save the logs_dir b/c we close logging 'manually' below
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None
        print(f"ZLLFT$255  {logs_dir=!r}")

        new_max_logfile_size = 1200
        print(f"ZLLFT$258 SET MAX LOG FILE SIZE to {new_max_logfile_size}")
        llft.Z_set_max_log_file_size(new_max_logfile_size)
        
        num_lines_written = 127
        for i in range(num_lines_written):
            lno = i+1
            line = f"ZLLFT$264 This is line {lno:3d}"         
            llft.log_one_line(line)

        llft.flush_current_log()
            
        last_fpath = llft._current_log_fpath
        assert last_fpath.endswith("logs/mws_log.014")

        # update the final / lastmost log file 
        llft.close_logging()
        
        exp_info = (
            ("mws_log.010",  1336,  40),                        
            ("mws_log.011",  1349,  37),
            ("mws_log.012",  1335,  35),
            ("mws_log.013",  1348,  34),
            ("mws_log.014",  1478,  27),
            )
        for fpath, exp_fsize, exp_num_lines in exp_info:
            full_fpath = logs_dir + "/" + fpath
            print(f"ZLLFT$284 {full_fpath=!r}")
            got_data = read_a_file_as_string(full_fpath)
            assert got_data is not None

            # The log files differ on Pico vs local Cpython3 tests:
            # the logged info includes the path of the log file,
            # which is longer for local logs: /tmp/MWS_tmp_abcdefgg/
            # vs /_scratch_dir on PICO. 
            # file size must be (approximately) as expected
            # These are the allowed differences between the table above
            # and the actual. The table has info for local tests;
            # the allowances are for PICO variation.
            # NOTE they current get applied to BOTH platforms.
            # See the notes at the top of this file.
            allowed_fsize_diff = 200
            allowed_num_lines_diff = 4

            print(f"ZLLFT$301 len of log file '{fpath}' is {len(got_data)}")
            got_len = len(got_data)
            fsize_diff = abs(got_len - exp_fsize)
            assert fsize_diff <= allowed_fsize_diff, \
                f"fpath={fpath} {got_len=} {exp_fsize=}  {fsize_diff=} {allowed_fsize_diff=}"
            ###print(f"ZLLFT$306  Log file contains: '{got_data}'")
            # MICROPYTHON DOES NOT SUPPORT: got_lines = got_data.split("\n", keepends=True)
            got_lines = read_a_file_as_lines(full_fpath)
            assert got_lines is not None
            print(f"ZLLFT$310 number of lines is {len(got_lines)}")
            got_num_lines = len(got_lines)
            num_lines_diff = abs(got_num_lines - exp_num_lines)
            assert num_lines_diff <= allowed_num_lines_diff, \
                f"fpath={fpath} {got_num_lines=} {exp_num_lines=}  {num_lines_diff=} {allowed_num_lines_diff=}"


def test_determine_new_starting_extension_value() -> None:
    print(f"ZLLFT$318  === test_determine_new_starting_extension_value  ======")

    tests = (
        ( 9, 10),
        (110, 120),
        (211, 220),
        (322, 330),
        (433, 440),
        (544, 550),
        (675, 680),
        (796, 800),
        (817, 830),
        (928, 940),
        (739, 750),
        (610, 620),
        )

    for biggest_existing, exp_new_value in tests:
        got_new_value = _determine_new_starting_extension_value(biggest_existing)

        print(f"ZLLFT$338  {biggest_existing=}  {got_new_value=}  {exp_new_value=}")

        assert got_new_value == exp_new_value


def test_determine_biggest_existing_log_fname_extension_value() -> None:
    print(f"ZLLFT$344  === test_determine_biggest_existing_log_fname_extension_value  ======")

    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    llft = LemLogFileTable(logs_dir, Z_TESTS_PARAMETER_SELECTOR)
    try:

        remove_subdir(logs_dir)
        print(f"ZLLFT$353   removed {logs_dir=!r}")

        fnames = [
            "mws_log.210", 
            "mws_log.211", 
            "mws_log.212", 
            "mws_log.213", 
            "mws_log.214", 
            "mws_log.215", 
            "mws_log.216", 
        ]
        
        create_subdir_with_files(logs_dir, fnames)

        biggest = _determine_biggest_existing_log_fname_extension_value(logs_dir)

        print(f"ZLLFT$369 {biggest=}")

        assert biggest == 216

    finally:
        # Leave no (log) files dangling open - esp on Pico
        llft.close_logging()
        remove_scratch_path(logs_dir)


def test_determine_starting_fname_extension_value() -> None:
    print(f"ZLLFT$380  === test_determine_starting_fname_extension_value  ======")

    # Replace the production logs/ dir with a test dir
    logs_dir = get_scratch_path("logs")
    remove_scratch_path(logs_dir)
    try:

        remove_subdir(logs_dir)
        print(f"ZLLFT$388   removed {logs_dir=!r}")

        fnames = [
            "mws_log.310", 
            "mws_log.311", 
            "mws_log.312", 
            "mws_log.313", 
            "mws_log.314", 
            "mws_log.315", 
            "mws_log.316", 
            "mws_log.326", 
            "mws_log.346", 
        ]
        create_subdir_with_files(logs_dir, fnames)

        sfn = _determine_starting_fname_extension_value(logs_dir)

        print(f"ZLLFT$405  {sfn}")

        assert sfn == 350

    finally:
        remove_scratch_path(logs_dir)


def test_find_the_oldest_extant_logfile() -> None:
    print(f"ZLLFT$414  === test_find_the_oldest_extant_logfile  ======")
    with LemTestContext() as llft:
        # Test 'table is empty'
        oldest_idx = llft._find_the_oldest_extant_logfile()
        assert oldest_idx is None
        del oldest_idx

        # Test: found item zero: it's the only item in table, 
        # and it is an 'extant' entry (not a 'removed' file)
        # Make the table like this:
        #   0    file.1     EXTANT  <- new item
        fname1 = "file.1"
        fsize1 = 111
        llft._append_to_log_file_table(fname1, fsize1)

        # Test error: bad index
        fitem_idx = 1  # the only 1 in the table
        ok = llft._mark_file_was_removed(fitem_idx)
        assert not ok
        del fitem_idx

        # Test: find the 'EXTANT' item - it's the only one in the table
        oldest_idx = llft._find_the_oldest_extant_logfile()
        assert oldest_idx == 0
        del oldest_idx

        # Make the (only) fitem in the table as "REMOVED".
        fitem_idx = 0  # the only 1 in the table
        ok = llft._mark_file_was_removed(fitem_idx)
        assert ok
        del fitem_idx

        # Verify the item was updated to "REMOVED"
        # File table should look like this:
        #   0    file.1     REMOVED  <- was EXTANT
        fitem_idx = 0  # the only 1 in the table
        got_fitem = llft.get_log_table_item(fitem_idx)
        assert got_fitem is not None
        assert got_fitem[2] != LOGFILE_IS_EXTANT
        assert got_fitem[2] == LOGFILE_WAS_REMOVED
        del got_fitem
        del fitem_idx

        # Test error: cannot mark an item removed if it is already marked 'REMOVED'
        # File table is:
        #   0    file.1     REMOVED
        fitem_idx = 0  # the only 1 in the table
        ok = llft._mark_file_was_removed(fitem_idx)
        assert not ok
        del fitem_idx

        # Test: there is no oldest extant - only 1 fitem, and it is 'REMOVED'
        # File table is:
        #   0    file.1     REMOVED
        fitem_idx_no_oldest = llft._find_the_oldest_extant_logfile()
        assert fitem_idx_no_oldest is None
        del fitem_idx_no_oldest

        # Add a new extant item. 
        # Make the table like this:
        #   0    file.1     REMOVED
        #   1    file.2     EXTANT  <- new item
        fname2 = "file.2"
        fsize2 = 222
        llft._append_to_log_file_table(fname2, fsize2)
        # Verify the 2 items are what we expect
        fitem = llft.get_log_table_item(0)
        assert fitem is not None
        assert fitem[0] == fname1
        assert not fitem[2] # REMOVED
        fitem = llft.get_log_table_item(1)
        assert fitem is not None
        assert fitem[0] == fname2
        assert fitem[2] # EXTANT
        # Try to find the oldest extant
        oldest_extant = llft._find_the_oldest_extant_logfile()
        assert oldest_extant == 1

        # Make the table like this:
        #   0    file.1     REMOVED
        #   1    file.2     EXTANT
        #   2    file.3     EXTANT  <- new item
        # Add new item[2]
        fname3 = "file.3"
        fsize3 = 333
        llft._append_to_log_file_table(fname3, fsize3)
        # Try to find the oldest extant
        oldest_extant = llft._find_the_oldest_extant_logfile()
        assert oldest_extant == 1

        # Make the table like this:
        #   0    file.1     REMOVED
        #   1    file.2     REMOVED  <- was EXTANT
        #   2    file.3     EXTANT
        # Mark [1] as REMOVED
        ok = llft._mark_file_was_removed(1)
        assert ok
        # Try to find the oldest extant
        oldest_extant = llft._find_the_oldest_extant_logfile()
        assert oldest_extant == 2

        # Make the table like this:
        #   0    file.1     REMOVED
        #   1    file.2     REMOVED
        #   2    file.3     EXTANT
        #   3    file.4     EXTANT    <- new item
        # Add new item[3]
        fname4 = "file.4"
        fsize4 = 444
        llft._append_to_log_file_table(fname4, fsize4)
        # Try to find the oldest extant
        oldest_extant = llft._find_the_oldest_extant_logfile()
        assert oldest_extant == 2

        # Make the table like this:
        #   0    file.1     REMOVED
        #   1    file.2     REMOVED  
        #   2    file.3     REMOVED   <- was EXTANT
        #   3    file.4     EXTANT
        #   4    file.5     EXTANT    <- new item
        #   5    file.6     EXTANT    <- new item
        # Mark [2] as REMOVED
        ok = llft._mark_file_was_removed(2)
        # Add new item[4]
        fname5 = "file.5"
        fsize5 = 555
        llft._append_to_log_file_table(fname5, fsize5)
        # Add new item[5]
        fname6 = "file.6"
        fsize6 = 666
        llft._append_to_log_file_table(fname6, fsize6)
        assert ok
        # Try to find the oldest extant
        oldest_extant = llft._find_the_oldest_extant_logfile()
        assert oldest_extant == 3


def test_remove_the_oldest_extant_logfile() -> None:
    print(f"ZLLFT$552  === test_remove_the_oldest_extant_logfile  ======")
    with LemTestContext() as llft:
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None

        fnames = [
            "mws_log.420",
            "mws_log.421",
            "mws_log.422",
            "mws_log.423",
            "mws_log.424",
            "mws_log.425",
            "mws_log.426",
        ]
        file_items = create_subdir_with_files(logs_dir, fnames)

        if 1:
            print(f"ZLLFT$569 FILE ITEMS for the files created:")
            for fitem in file_items:
                print(f"   {fitem}")
            print()

        if 1:
            dir_contents = list_dir_names(logs_dir)
            assert dir_contents is not None
            assert len(dir_contents) == len(fnames)
            del dir_contents

        # Fill the log file table with the files we just created
        for fitem in file_items:
            llft._append_to_log_file_table(fitem[0], fitem[1])

        if 1:
            llft.dump_file_table(comment="ZLLFT$585", to_log=False)

        # Verify file table has no 'removed' files yet
        assert llft.get_number_of_removed_logfiles() == 0
        assert llft.get_number_of_extant_logfiles() == len(file_items)


        # Remove the log files one at a time, starting with
        # the oldest extant (which is the first file, mws_log.420)
        item_idx = 0
        num_files_removed = 0
        while 1:
            ok = llft._remove_the_oldest_extant_logfile()
            if not ok:
                break
            num_files_removed += 1

        assert num_files_removed == len(file_items)

        # All files should have been deleted
        dir_contents = list_dir_names(logs_dir)
        assert dir_contents is not None
        assert len(dir_contents) == 0
        del dir_contents


def test_reduce_file_usage_to_below_low_watermark() -> None:
    print(f"ZLLFT$612  === test_reduce_file_usage_to_below_low_watermark  ======")

    with LemTestContext() as llft:
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None

        fnames = [
            "mws_log.420",
            "mws_log.421",
            "mws_log.422",
            "mws_log.423",
            "mws_log.424",
            "mws_log.425",
            "mws_log.426",
            "mws_log.427",
            "mws_log.428",
            "mws_log.429",
        ]
        file_items = create_subdir_with_files(logs_dir, fnames, 20_000)

        if 1:
            print(f"ZLLFT$633 FILE ITEMS for the files created:")
            for fitem in file_items:
                print(f"   {fitem}")
            print()

        if 1:
            dir_contents = list_dir_names(logs_dir)
            assert dir_contents is not None
            assert len(dir_contents) == len(fnames)
            del dir_contents

        # create the logs file table based on the logfiles we created
        # Fill the log file table with the files we just created
        for fitem in file_items:
            llft._append_to_log_file_table(fitem[0], fitem[1])

        if 1:
            llft.dump_file_table(comment="ZLLFT$650", to_log=False)

        # Verify file table has no 'removed' files yet
        print(f"ZLLFT$653 BEFORE REMOVING OLD LOG FILES:")
        assert llft.get_number_of_removed_logfiles() == 0
        assert llft.get_number_of_extant_logfiles() == len(file_items)
        print(f"ZLLFT$656 Total size of removed files: {llft.get_fsize_of_removed_logfiles()}")
        print(f"ZLLFT$657 Total size of extant  files: {llft.get_fsize_of_extant_logfiles()}")
        assert llft.get_fsize_of_removed_logfiles() == 0

        # The sizes vary on platforms PICO vs local CPython3
        # due to length of the log file paths, which are logged
        # in the log files.
        # See the notes at the top of this file.
        got_extant_fsize = llft.get_fsize_of_extant_logfiles()
        exp_extant_fsize = 200_332  # Cpython3 value
        extant_fsize_diff = abs(got_extant_fsize - exp_extant_fsize)
        allowed_extant_fsize_diff = 25
        assert extant_fsize_diff <= allowed_extant_fsize_diff,\
            f"{got_extant_fsize=} {exp_extant_fsize=}  {extant_fsize_diff=} {allowed_extant_fsize_diff=} "
        #assert llft.get_fsize_of_extant_logfiles() == 200_332

        # Set the low watermark
        llft.Z_set_watermarks(101_000, -1)

        llft._reduce_file_usage_to_below_low_watermark()

        # After removing:
        print()
        print(f"ZLLFT$679 AFTER REMOVING OLD LOG FILES:")
        assert llft.get_number_of_removed_logfiles() == 5
        assert llft.get_number_of_extant_logfiles() == len(file_items)-5
        print(f"ZLLFT$682 Total size of removed files: {llft.get_fsize_of_removed_logfiles()}")
        print(f"ZLLFT$683 Total size of extant  files: {llft.get_fsize_of_extant_logfiles()}")
        # check size of removed files
        got_removed_fsize = llft.get_fsize_of_removed_logfiles()
        exp_removed_fsize = 100_165
        removed_fsize_diff = abs(got_removed_fsize - exp_removed_fsize)
        allowed_fsize_diff = 25
        assert removed_fsize_diff <= allowed_fsize_diff,\
            f"{got_removed_fsize=} {exp_removed_fsize=}  {removed_fsize_diff=} {allowed_fsize_diff=} "
        ###assert llft.get_fsize_of_removed_logfiles() == 100_165
        
        # check size of extant (remaining) files
        got_remains_fsize = llft.get_fsize_of_extant_logfiles() 
        exp_remains_fsize =100_167
        remains_fsize_diff = abs(got_remains_fsize - exp_remains_fsize)
        allowed_remains_fsize_diff = 3 
        assert remains_fsize_diff <= allowed_remains_fsize_diff,\
            f"{got_remains_fsize=} {exp_remains_fsize=}  {remains_fsize_diff=} {allowed_remains_fsize_diff=} "
        ###assert llft.get_fsize_of_extant_logfiles() == 100_167


def test_remove_logs_if_fspace_needed() -> None:
    print(f"ZLLFT$704  === test_remove_logs_if_fspace_needed  ======")
    with LemTestContext() as llft:
        logs_dir = llft.get_logs_directory()
        assert logs_dir is not None

        fnames = [
            "mws_log.420",
            "mws_log.421",
            "mws_log.422",
            "mws_log.423",
            "mws_log.424",
            "mws_log.425",
            "mws_log.426",
            "mws_log.427",
            "mws_log.428",
            "mws_log.429",
        ]
        file_items = create_subdir_with_files(logs_dir, fnames, 20000)

        if 1:
            print(f"ZLLFT$724 FILE ITEMS for the files created:")
            for fitem in file_items:
                print(f"   {fitem}")
            print()

        if 1:
            dir_contents = list_dir_names(logs_dir)
            assert dir_contents is not None
            assert len(dir_contents) == len(fnames)
            del dir_contents


        # create the logs file table based on the logfiles we created
        # Fill the log file table with the files we just created
        for fitem in file_items:
            llft._append_to_log_file_table(fitem[0], fitem[1])

        if 1:
            llft.dump_file_table(comment="ZLLFT$742", to_log=False)

        # Verify file table has no 'removed' files yet
        print(f"ZLLFT$745 BEFORE REMOVING OLD LOG FILES:")
        assert llft.get_number_of_removed_logfiles() == 0
        assert llft.get_number_of_extant_logfiles() == len(file_items)
        print(f"ZLLFT$748 Total size of removed files: {llft.get_fsize_of_removed_logfiles()}")
        print(f"ZLLFT$749 Total size of extant  files: {llft.get_fsize_of_extant_logfiles()}")

        # check 'before' sizes
        assert llft.get_fsize_of_removed_logfiles() == 0
        # The sizes vary on platforms PICO vs local CPython3
        # due to length of the log file paths, which are logged
        # in the log files.
        # See the notes at the top of this file.
        got_extant_fsize = llft.get_fsize_of_extant_logfiles()
        exp_extant_fsize = 200_332  # Cpython3 value
        extant_fsize_diff = abs(got_extant_fsize - exp_extant_fsize)
        allowed_extant_fsize_diff = 25
        assert extant_fsize_diff <= allowed_extant_fsize_diff,\
            f"{got_extant_fsize=} {exp_extant_fsize=}  {extant_fsize_diff=} {allowed_extant_fsize_diff=} "
        ###assert llft.get_fsize_of_extant_logfiles() == 200_332

        # Set new watermarks to force action
        llft.Z_set_watermarks(101_000, 195_000)

        llft._remove_logs_if_fspace_needed()

        # Check 'after' removing:
        print()
        print(f"ZLLFT$772 AFTER REMOVING OLD LOG FILES:")
        assert llft.get_number_of_removed_logfiles() == 5
        assert llft.get_number_of_extant_logfiles() == len(file_items)-5
        print(f"ZLLFT$775 Total size of removed files: {llft.get_fsize_of_removed_logfiles()}")
        print(f"ZLLFT$776 Total size of extant  files: {llft.get_fsize_of_extant_logfiles()}")
        # check size of removed files
        got_removed_fsize = llft.get_fsize_of_removed_logfiles()
        exp_removed_fsize = 100_165
        removed_fsize_diff = abs(got_removed_fsize - exp_removed_fsize)
        allowed_fsize_diff = 25
        assert removed_fsize_diff <= allowed_fsize_diff,\
            f"{got_removed_fsize=} {exp_removed_fsize=}  {removed_fsize_diff=} {allowed_fsize_diff=} "
        ###assert llft.get_fsize_of_removed_logfiles() == 100_165
        # check size of extant (remaining) files
        got_remains_fsize = llft.get_fsize_of_extant_logfiles() 
        exp_remains_fsize =100_167
        remains_fsize_diff = abs(got_remains_fsize - exp_remains_fsize)
        allowed_remains_fsize_diff = 3 
        assert remains_fsize_diff <= allowed_remains_fsize_diff,\
            f"{got_remains_fsize=} {exp_remains_fsize=}  {remains_fsize_diff=} {allowed_remains_fsize_diff=} "



### HELPERS #####################################

def check_production_log_dir_unchanged(old_logs_dir: str, old_logs_dir_items_before: list[str] | None) -> bool:
    """ True if the production log directory is as it was: same file names 
    or the directory is still missing if it was missing before the test.
    This checks to make sure the test(s) do not disturb the production
    logs/ dir.
    """
    after = list_dir_names(old_logs_dir)
    if after == old_logs_dir_items_before:
        return True
    print(f"ZLLFT$806: production log dir CHANGED: {old_logs_dir}, before: {old_logs_dir_items_before}, after: {after}")
    return False




###
