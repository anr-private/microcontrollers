# LemLogFileTable.py
#
# LINEMARKER=LEMLFT

import os
#import sys

from lib1.read_last_n_lines import read_last_n_lines
from lib1.file_utils import remove_file
from lib1.file_utils import filter_dir_contents

try: from typing import IO, Any
except ImportError: pass

# log files are this base name plus '.' plus '000', '001', etc
BASE_LOG_FNAME = "mws_log"

# Starting point for creating the extensions for log files
DEFAULT_FNAME_STARTING_EXTENSION_VALUE = 10

LOG_PARAMETERS_PROFILES = {
    "pico":    (25_000, 1_000_000, 750_000),
    "cpython": (25_000, 1_000_000, 750_000),
    "Z_tests": (25_000, 1_000_000, 750_000),
}

# # nominal max size of a log file  in bytes
# # it may be slightly larger due to 'hint keep-lines'
# MAX_ LOG_ FILE_ SIZE = 25_000
# 
# # Max amount of filespace that log files are allowed to occupy.
# # Whenever a new log is created, the total logfile space is checked.
# # If it exceeds this max, the oldest log files are removed until
# # the total space is less than the low water mark.
# self._log_usage_high_watermark = 1_000_000
# self._log_usage_low_watermark =    750_000

# One of the values in the info tuple; tuples found in _log_file_table
LOGFILE_IS_EXTANT = 1
LOGFILE_WAS_REMOVED = 0

EMPTY_LOG_FPATH_MARKER_STG = "NULL_LOG_FPATH"

# Error message contents - make available for unit tests
MESG_CANNOT_CREATE_LOGS_SUBDIRECTORY = "CANNOT CREATE LOGS SUBDIRECTORY (LOGGING HAS BEEN CLOSED)"

class LemLogFileTable:
    # Manages the list of logfiles, both extant and now-deleted.
    # A log file gets deleted (removed) if/when system file space
    # runs low.

    def __init__(self, log_dir: str|None, log_parameters_selector:str) -> None:

        # Determine the limits to be used during this execution.
        # Max amount of filespace that log files are allowed to occupy.
        #   _max_log_file_size:
        # Whenever a new log is created, the total logfile space is checked.
        # If it exceeds this max 'watermark', the oldest log file(s) are 
        # removed until the total space is not greater than the low water mark.
        #  _log_usage_high_watermark
        #  _log_usage_low_watermark
        limit_vals = LOG_PARAMETERS_PROFILES.get(log_parameters_selector, None)
        if limit_vals is None:
            m = f"LEMLFT$64 UNKNOWN/BAD log parameters selector: {log_parameters_selector!r}"
            print(m)
            raise RuntimeError(m)
        self._max_log_file_size: int = limit_vals[0]
        self._log_usage_high_watermark: int = limit_vals[1]
        self._log_usage_low_watermark: int  = limit_vals[2]
        # Some consistency checks
        if self._log_usage_high_watermark < self._log_usage_low_watermark:
            m = f"LEMLFT$72 Inconsistent watermark values (high < low): {self._log_usage_high_watermark} < {self._log_usage_low_watermark}"
            print(m)
            raise RuntimeError(m)


        # Table of all logfiles (except currently-open logfile)
        # Contains tuples of form:
        #   (log-filename:str, fsize: int, extant-flag)
        # where 
        #  log-filename is the full path of the log file
        #                      ex: /logs/mws_log.10
        #  fsize is the file size in bytes
        #  extant-flag is 1 if file is extant, 0 if file has been
        #    removed to reclaim file space.
        # A logfile is added to the table when it is closed and
        # so replaced with a new 'currently-open logfile'.
        # Arg log_dir is the full path of a directory in whic
        # this class writes log files.
        # It can be specified as None, which makes the instance
        # a placeholder - typically that will be replaced 
        # by a unit test using Z_replace_log_file_table()
        # before any logging is attempted.
        # If logging is attempted and the log dir is None,
        # an exception is raised.
        self._log_file_table: list[ tuple[str, int, int] ] = []
        
        # Directory in which log files are created
        # None if this class is in its 'closed' state.
        # OR caller can provide None - which prevents this class
        # from doing any logging. Unit test can do this to 
        # prevent logging before it can install a 'fake' log table
        # by using Z_replace_log_file_table()
        self._logs_directory: str | None = log_dir

        # path of currently-open log file
        self._current_log_fpath: str = EMPTY_LOG_FPATH_MARKER_STG
        # file descriptor for currently-open logfile
        self._logf: IO[str] | None = None
        # file size (bytes) of the currently-open file
        self._current_log_fsize: int = 0

        # An int value: the value to be used for the file extension 
        # of the next log file that will be created. 
        # The value is converted into 3 decimal digits
        # and used as the file extension on BASE_LOG_FNAME.
        # If negative (ex: -1), no logs have been opened yet so we'll need  to
        # determine the file extension of the first file.
        # And if None, the _log_file_table will be empty.
        self._fname_next_ctr: int = -1

    def _nullify_logging(self):
        # Nullify this object so it cannot be used/reused
        self._max_log_file_size = 0
        self._log_usage_high_watermark = 0
        self._log_usage_low_watermark = 0
        self._log_file_table.clear()
        self._logs_directory = None
        self._current_log_fpath = EMPTY_LOG_FPATH_MARKER_STG
        self._logf = None
        self._current_log_fsize = 0
        self._fname_next_ctr = -1

    def Z_set_max_log_file_size(self, new_max: int):
        self._max_log_file_size = new_max

    def Z_set_watermarks(self, new_low_watermark: int, new_high_watermark: int) -> None:
        # UNIT TEST ONLY
        # the tests are just to catch any bad requests
        if new_high_watermark > 100: self._log_usage_high_watermark = new_high_watermark
        if new_low_watermark > 100: self._log_usage_low_watermark = new_low_watermark

    def get_logs_directory(self) -> str | None:
        return self._logs_directory

    def get_current_log_fpath(self) -> str:
        return self._current_log_fpath

    def get_current_log_fsize(self) -> int:
        return self._current_log_fsize


    def get_logs_totals(self, include_currently_open_file: bool) -> tuple[int, int, int]:
        # get the total values / stats 
        # Returns a tuple of these values:
        # 1. The number of extant log files (ie ones that have not
        #    been removed to reclaim file space)
        # 2. The total size (bytes) of all extant log files
        #    (obviously excluding logfiles that have been removed)
        # #. The size of the log file table (ie the total number
        #    of files that have been created during this session so far)
        # NOTE if include_currently_open_file is True, 
        #  items 1 and 2 include the currently-open file.
        #  I.e, item 1 will be 1 larger and item 2 will have the
        #  size of the currently-open logfile added to it.

        num_extant_files = self.get_number_of_extant_logfiles()
        extant_logfile_fsize = self.get_fsize_of_extant_logfiles()
        table_size = len(self._log_file_table)

        if include_currently_open_file:
            num_extant_files += 1
            extant_logfile_fsize += self._current_log_fsize
        return (num_extant_files, extant_logfile_fsize, table_size)

    # def get_total_logs_fspace(self):
        # # Get the total size (bytes) of all logfiles, whether
        # currently extant or already-been-deleted
        # if len(self._log_file_table) == 0:
            # return 0
        # total_size = sum(fitem[1] for fitem in self._log_file_table)


    def get_number_of_removed_logfiles(self) -> int:
        # Get the number of all extant (non-deleted) logfiles
        # IE ignores files whose 'extant-flag' is False-y.
        if len(self._log_file_table) == 0: return 0
        num_files = sum(1 for fitem in self._log_file_table
                            if not fitem[2])
        return num_files

    def get_number_of_extant_logfiles(self) -> int:
        # Get the number of all extant (non-deleted) logfiles
        # IE ignores files whose 'extant-flag' is False-y.
        if len(self._log_file_table) == 0: return 0
        num_files = sum(1 for fitem in self._log_file_table
                            if fitem[2])
        return num_files

    def get_fsize_of_removed_logfiles(self) -> int:
        # Get the total size of all removed (non-extant) logfiles
        # IE ignores files whose 'extant-flag' is True-y.
        if len(self._log_file_table) == 0: return 0
        total_size = sum(fitem[1] for fitem in self._log_file_table
                                   if not fitem[2])
        return total_size

    def get_fsize_of_extant_logfiles(self) -> int:
        # Get the total size of all extant (non-deleted) logfiles
        # IE ignores files whose 'extant-flag' is False-y.
        if len(self._log_file_table) == 0: return 0
        total_size = sum(fitem[1] for fitem in self._log_file_table
                                   if fitem[2])
        return total_size


    def get_log_table_item(self, item_index: int) -> tuple[str, int, int] | None:
        try:
            return self._log_file_table[item_index]
        except IndexError:
            return None

    def get_status_lines(self) -> tuple[str,...]:
        # Returns a collection of str values that describe
        # the state of the log files and table.
        # Suitable for display on a webpage
        lines = []
        lines.append(f"Current log: {self._current_log_fpath} &nbsp; {self._current_log_fsize} bytes")
        lines.append(f"Logs Extant: {self.get_number_of_extant_logfiles()} files. &nbsp; {self.get_fsize_of_extant_logfiles()} bytes")
        lines.append(f"Logs Removed: {self.get_number_of_removed_logfiles()} files. &nbsp;  {self.get_fsize_of_removed_logfiles()}")
        lines.append(f"Log Watermarks: &nbsp; high={self._log_usage_high_watermark} &nbsp; low={self._log_usage_low_watermark} &nbsp; MAX-filesize={self._max_log_file_size}")
        return tuple(lines)


    def get_lines_from_log_file(self, relative_line_number: int, 
                                      number_of_lines: int) -> list[str]:
        # get lines from the log file
        # relative_line_number is the line number of the first line
        # being requested, relative to the end of the file.
        # number_of_lines is the number of lines
        # So (1,1) gets the last line in the file,
        # (10,2) gets the 10th and 9th lines from the end of file.
        lines = read_last_n_lines(self._current_log_fpath,
                                  relative_line_number,
                                  number_of_lines)
        return lines


    def _append_to_log_file_table(self, fname: str, fsize: int) -> None:
        # Append a new item
        # This represents a new log file having been created.
        # So the item is always marked LOGFILE_IS_EXTANT
        log_file_info = (fname, fsize, LOGFILE_IS_EXTANT)
        self._log_file_table.append(log_file_info)
        print(f"LEMLFT$255 _append_to_log_file_table  Append: {log_file_info} TableSize now={len(self._log_file_table)}")

    def _mark_file_was_removed(self, fitem_index: int) -> bool:
        # mark the specified item as 'LOGFILE_WAS_REMOVED'
        # It should currently be 'LOGFILE_IS_EXTANT"
        # Returns True if ok, else False
        fitem = self.get_log_table_item(fitem_index)
        if fitem is None:
            m = f"LEMLFT$263 *ERROR* No such {fitem_index=} in _log_file_table. Table size is {len(self._log_file_table)}"
            print(m)
            self._log_a_line(m)
            return False

        if not fitem[2]:
            m = f"LEMLFT$269 *ERROR* Already marked 'removed': {fitem_index=} {fitem=}."
            print(m)
            self._log_a_line(m)
            return False

        # Mark it 'REMOVED'
        self._log_file_table[fitem_index] = (fitem[0], fitem[1], LOGFILE_WAS_REMOVED)

        return True

    def flush_current_log(self) -> None:
        if self._logf:
            self._logf.flush()
            print(f"LEMLFT$282 CURRENT LOG HAS BEEN FLUSHED")

    def log_one_line(self, line:str) -> None:

        if self._logf is None:
            self._start_a_new_logfile()

        self._log_a_line(line)

        if self._current_log_fsize > self._max_log_file_size:
            print(f"LEMLFT$292  curr log size > MAX curr={self._current_log_fsize} max={self._max_log_file_size}")
            self._close_current_log_file("log_one_line")

    def _log_a_line(self, line: str) -> None:
        # low-level write to log file
        if line is None: line = ""

        if self._logf is None:
            m = f"LEMLFT$300 !!! _log_a_line NO LOGFILE OPEN!!!!  {line=}"
            print(m)
            return

        try:
            self._logf.write(line)
            self._logf.write("\n")
            self._logf.flush()
            self._current_log_fsize += len(line)+1
    
        except OSError as ex:
            # see examples/file_and_dirs_io/errno_show_all.py to see all errno values
            print(f"LEMLFT$312  Error writing '{self._current_log_fpath}' EX={repr(ex)}  EX='{str(ex)}' ")
            # 28 is 'out of space'
            print(f"LEMLFT$314 {ex.errno=}")
            print(f"LEMLFT$315 {line=}")
            
        except Exception as ex:
            print(f"LEMLFT$318: Error writing to file '{self._current_log_fpath}': ex={ex}")
            print(f"LEMLFT$319: Error writing to file '{self._current_log_fpath}': repr(ex)={repr(ex)}")
            print(f"LEMLFT$320: Error writing to file '{self._current_log_fpath}': str(ex)={str(ex)}")
            print(f"LEMLFT$321 {line=}")


    def _start_a_new_logfile(self) -> None:
        # If there has no log file ever been written in this session,
        # we look to see if there are any previously-extant logfiles.
        # If so, we want to choose a file extension NNN that is
        # somewhat bigger than the biggest extant one.
        # Ex: if we have just started this session, and we find the
        # biggest logfile in logs/ is mws_log.105, then we want
        # our first filename to be something bigger than that one --
        # say mws_log.110. So someone can tell where the logs from one
        # session ended and the next session (ours) started.
        # If we have already done that, then we'll have an existing
        # self._fname_next_ctr which tells us that we have already
        # opened (at least one) logfile.

        # This should never happen!
        if self._logf is not None:
            m = f"LEMLFT$340 _start_a_new_logfile OLD LOG FILE IS NOT CLOSED!"
            print(m)
            raise RuntimeError(m)

        self._create_the_logs_subdir()

        new_log_fpath = self._make_new_log_fpath()

        try:
            logf = open(new_log_fpath, "w")
        except Exception as ex:
            print(f"LEMLFT$351 CANNOT OPEN LOGFILE '{new_log_fpath}'  ex={ex}  {str(ex)}")
            return
        self._logf = logf
        self._current_log_fpath = new_log_fpath
        self._current_log_fsize = 0
        m = f"LEMLFT$356  OPENED NEW LOG {self._current_log_fpath}"
        print(m)
        self._log_a_line(m)

        self.dump_file_table("from-LEMLFT$360")
        
        self._remove_logs_if_fspace_needed()


    def _make_new_log_fpath(self) -> str:
        # create the full path for a new log file
        dir_is_ok = ( isinstance(self._logs_directory, str) and 
                      len(self._logs_directory) > 0)
        if not dir_is_ok:
            m = f"LEMLFT$370 CANNOT MAKE NEW LOG FPATH: _logs_directory is BAD {self._logs_directory}"
            print(m)
            raise RuntimeError(m)
        assert self._logs_directory is not None # for mypy typechecking
        if self._fname_next_ctr < 0:
            # Determine the file extension of the first logfile that
            # we are going to write in this session.
            new_extension_value = \
                _determine_starting_fname_extension_value(self._logs_directory)
            # The next file's extension
            self._fname_next_ctr = new_extension_value + 1
        else:
            # We have already created at least one logfile,
            # so subsequent logfiles' extensions are just sequential int
            # values.
            new_extension_value = self._fname_next_ctr
            self._fname_next_ctr += 1


        fpath = f"{self._logs_directory}/{BASE_LOG_FNAME}.{new_extension_value:03d}"
        #@@@@@@@@@ TODO what if > 999?
        print(f"LEMLFT$391 new log-fpath='{fpath}'")
        return fpath


    def _remove_logs_if_fspace_needed(self) -> None:
        # See if filespace is running low. If so, remove some old logs.
        total_fsize = self.get_fsize_of_extant_logfiles()
        if total_fsize < self._log_usage_high_watermark:
            m = f"LEMLFT$399 NO NEED TO REMOVE LOGFILES yet.  total_log_size={total_fsize}  {self._log_usage_high_watermark=}"
            print(m)
            self._log_a_line(m)
            return
        self._reduce_file_usage_to_below_low_watermark()


    def _reduce_file_usage_to_below_low_watermark(self) -> None:
        m = f"LEMLFT$407 _reduce_file_usage_to_below_low_watermark extant-fsize={self.get_fsize_of_extant_logfiles()}"
        print(m)
        self._log_a_line(m)
        num_files_removed = 0
        while 1:
            extant_fsize = self.get_fsize_of_extant_logfiles()
            if extant_fsize < self._log_usage_low_watermark:
                #print("LEMLFT$414 *********************_____________________________________________________________________")
                break
            ok = self._remove_the_oldest_extant_logfile()
            if not ok:
                m = f"LEMLFT$418 FAILED to remove oldest extant logfile. {extant_fsize=}  {self._log_usage_low_watermark=} num_files_removed{num_files_removed=}"
                print(m)
                self._log_a_line(m)
                break
            num_files_removed += 1
        m = f"LEMLFT$423 Removed old logs. Extant-filespace now below low mark. {extant_fsize=}  {self._log_usage_low_watermark=} num_files_removed{num_files_removed=}"
        print(m)
        self._log_a_line(m)


    def _remove_the_oldest_extant_logfile(self) -> bool:
        m = f"LEMLFT$429 _remove_the_oldest_extant_logfile extant-fsize={self.get_fsize_of_extant_logfiles()}"
        print(m)
        self._log_a_line(m)

        # Remove the oldest file in the file table that is still extant.
        # Update the table to show it has been removed.
        # Returns True if succeeded, False if failed.
        # If failed, probably shouldn't try again.
        oldest_extant_idx = self._find_the_oldest_extant_logfile()
        if oldest_extant_idx is None:
            m = f"LEMLFT$439 Cannot find the oldest-extant-logfile. table-size={len(self._log_file_table)}"
            print(m)
            self._log_a_line(m)
            return False
        fitem = self.get_log_table_item(oldest_extant_idx)
        if  fitem is None:
            m = f"LEMLFT$445 _remove_the_oldest_extant_logfile Bad {oldest_extant_idx} table-size={len(self._log_file_table)}"
            print(m)
            self._log_a_line(m)
            return False

        fpath = fitem[0]
        ok = remove_file(fpath)

        if not ok:
            m = f"LEMLFT$454 _remove_the_oldest_extant_logfile FAILED to remove logfile '{fpath}'"
            print(m)
            self._log_a_line(m)
            return False

        self._mark_file_was_removed(oldest_extant_idx)
 
        m = f"LEMLFT$461 _remove_the_oldest_extant_logfile REMOVED OLD LOGFILE '{fpath}'"
        print(m)
        self._log_a_line(m)

        return True


    def _find_the_oldest_extant_logfile(self) -> int | None:
        # Find the oldest file in the file table that is still extant.
        # Update the table to show it has been removed.

        oldest_extant_idx = None
        for j, fitem in enumerate(self._log_file_table):
            print(f"LEMLFT$474 LOOP: {j=}  {fitem=}")
            if fitem[2]:
                oldest_extant_idx = j
                print(f"LEMLFT$477 Found oldest extant logfile item: {oldest_extant_idx=} {fitem=}")
                break
        return oldest_extant_idx


    def close_logging(self) -> None:
        # close the logger
        # NOTE this tries to write to logfile, so gets an error if
        # no logfile has every been opened. That's ok.
        m = f"LEMLFT$486 CLOSE LOGGING ^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(m)
        self._log_a_line(m)
        # Save the file status info
        self.dump_file_table("from-LEMLFT$490")
        # Then close the log
        self._close_current_log_file("close_logging")
        # clear everything so that we cannot be used for additional logging
        self._nullify_logging()


    def _create_the_logs_subdir(self) -> None:
        # create the subdir into which we write log files

        # Cannot proceed if we have been 'closed'!
        dir_is_ok = ( isinstance(self._logs_directory, str) and 
                      len(self._logs_directory) > 0)
        if not dir_is_ok:
            m = f"LEMLFT$504 {MESG_CANNOT_CREATE_LOGS_SUBDIRECTORY}: _logs_directory is BAD {self._logs_directory}"
            print(m)
            raise RuntimeError(m)
        assert self._logs_directory is not None  # for mypy type checking

        try:
            os.mkdir(self._logs_directory)
        except OSError as ex:
            if ex.errno == 17: # already exists
                pass
                #print(f"LEMLFT$514  Subdir '{self._logs_directory}' already exists")
            else:
                print(f"LEMLFT$516 *ERROR* {self._logs_directory} errno={ex.errno} dir  cannot be created")


    def _close_current_log_file(self, who:str) -> None:
        if self._logf is not None:
            m = f"LEMLFT$521 CLOSING_close_current_log_file {who=}: close file '{self._current_log_fpath}' size={self._current_log_fsize}"
            print(m)
            self._log_a_line(m)

            try:
                self._logf.close()
            except Exception as ex:
                m = f"LEMLFT$528 ERROR CLOSING log file '{self._current_log_fpath}'  ex={ex} {str(ex)}"
                print(m)

            # Keep track of every log file as it is closed.
            fname = self._current_log_fpath
            # Underestimates: (b/c filetable gets dumped to log): fsize = self._current_log_fsize
            fsize = _get_true_file_size(self._current_log_fpath)
            self._append_to_log_file_table(fname, fsize)
            print(f"LEMLFT$536 Closed current log. LOG TABLE: {self._log_file_table}")
        # We have no open logfile.
        self._logf = None
        self._current_log_fpath = EMPTY_LOG_FPATH_MARKER_STG
        self._current_log_fsize = 0


    def dump_file_table(self, comment:str, to_log:bool=True) -> None:
        # write the file table into the log
        if len(self._log_file_table) <= 0:
            m = f"LEMLFT$546 DUMP LOG-FILE-TABLE:  the table is empty  {comment}"
            print(m)
            if to_log: self._log_a_line(m)
            return

        m = f"+++  LOG FILE TABLE  Dump  +++++++++++  {comment}  ++++++++++++++++++++++++++  LEMLFT$551"
        print(m)
        if to_log: self._log_a_line(m)
        for finfo in self._log_file_table:
            try:
                fname = finfo[0]
                fsize  = finfo[1]
                extant_val = finfo[2]
                if extant_val:
                    extant_flag = "EXTANT"
                else:
                    extant_flag = "REMOVED"

                m = f"LEMLFT$564   {fname:<16}  {fsize} {extant_flag}"
                print(m)
                if to_log: self._log_a_line(m)

            except Exception as ex:
                m = f"LEMLFT$569 Error dumping log file table: ex={ex} str={str(ex)}"
                print(m)
                if to_log: self._log_a_line(m)

        m = "+++  end of LOG FILE TABLE  +++++++++++++++++++++++++++++++++++++ LEMLFT$573"
        print(m)
        if to_log: self._log_a_line(m)
        m = ""
        print(m)
        if to_log: self._log_a_line(m)

    def __str__(self):
        s = []
        s.append("max_file_size=%s" % str(self._max_log_file_size))
        s.append("high_watermark=%s" % str(self._log_usage_high_watermark))
        s.append("low_watermark=%s" % str(self._log_usage_low_watermark))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


### SUPPORT  FUNCTIONS  #################################################

def is_3_digit_int(s:str) -> int | None:
    # Returns int(s) if s is a 3-digit number; else None.
    if not  s: return None
    if len(s) != 3: return None
    try:
        ival = int(s)
    except (TypeError, ValueError):
        return None
    if ival <= 0 or ival > 999: return None
    return ival


def _log_file_filter(fname:str, ftype: str, fsize: int) -> int | None:
    # Returns None if the file is not chosen.
    # Returns the filename extension value (an int) if chosen
    print(f"LEMLFT$606 _log_file_filter  fname='{fname}'  {fsize=}")

    if ftype != "f": return None
    #
    parts = fname.rsplit('.',1)
    if len(parts) != 2: return None
    #
    fpart    = parts[0]
    ext_part = parts[1]
    #
    if fpart != "mws_log": return None
    ext_val = is_3_digit_int(ext_part)
    print(f"LEMLFT$618   extension is_3_digit_int('{ext_part}') is {ext_val}")
    if ext_val is None: return None
    return ext_val


def _get_true_file_size(fpath: str) -> int:
    """ Size in bytes. os.stat() returns a bare tuple on MicroPython,
    so the size is taken by index, which works on CPython too.
    """
    return os.stat(fpath)[6]


def _determine_starting_fname_extension_value(log_files_subdir: str) -> int:
    # Look for old log files. 
    # Pick the one with the highest value 000-900 as its extension.
    # Use that value as a basis for creating a new extension value
    # that is bigger than it.
    # We make it more than just 1 bigger - so that there is a gap
    # in file extension numbers between the last file created in
    # one session and the first file created in the next extension.
    # So you can see the gaps between sessions easily.
    # Return the file_extension_value as int value;
    # it gets used in the logfilename of the first logfile
    # created in this session.

    biggest_existing_extension_value = \
        _determine_biggest_existing_log_fname_extension_value(log_files_subdir)

    if not biggest_existing_extension_value:
        return DEFAULT_FNAME_STARTING_EXTENSION_VALUE

    print(f"LEMLFT$649 {biggest_existing_extension_value=}")

    if biggest_existing_extension_value is None:
        # Use a fake biggest if there are no extant logfiles
        biggest_existing_extension_value = DEFAULT_FNAME_STARTING_EXTENSION_VALUE
        print(f"LEMLFT$654 USED DEFAULT TO FAKE THIS: {biggest_existing_extension_value=}")

    new_extension_value = \
      _determine_new_starting_extension_value(biggest_existing_extension_value)

    print(f"LEMLFT$659 {new_extension_value=}")

    return new_extension_value


def _determine_biggest_existing_log_fname_extension_value(log_files_subdir: str) \
                                                          -> int | None:
    # Look for old log files. 
    # Pick the one with the highest value 000-900 as its extension.
    # Return the int value of that file extension.
    # Returns 
    # gets (fname, ftype, fsize, file-extension-int-value)
    print(f"LEMLFT$671  {log_files_subdir=!r}")
    try:
        existing_logs_info = filter_dir_contents(log_files_subdir, _log_file_filter)
        print(f"LEMLFT$674 _determine_biggest_existing_log_fname_extension_value fname_ext_values={existing_logs_info}")
    except RuntimeError as ex:
        print(f"LEMLFT$676 _determine_biggest_existing_log_fname_extension_value FAILED: ex={ex} {str(ex)}")
        return None

    if len(existing_logs_info) == 0: 
        return None

    biggest: int = max([fitem[3] for fitem in existing_logs_info])

    print(f"LEMLFT$684 max _determine_biggest_existing_log_fname_extension_value is {biggest=}")

    return biggest


def _determine_new_starting_extension_value(
                        biggest_existing_extension_value: int) -> int:
    # find a new extension value that is bigger than the
    # biggest_prior_value. 
    # Returns int value

    # This should never happen:
    if biggest_existing_extension_value < DEFAULT_FNAME_STARTING_EXTENSION_VALUE:
        return DEFAULT_FNAME_STARTING_EXTENSION_VALUE
    
    ###units = biggest_existing_extension_value - ((biggest_existing_extension_value // 10) * 10)
    units = biggest_existing_extension_value % 10
    print(f"LEMLFT$701  {biggest_existing_extension_value=}  {units=}")
    
    # Pick an increment based on the lowest-order digit of the 
    # biggest previous file extension.
    # This creates a gap in the number of logfiles from one session
    # to the next.
    inc = [10, 9, 8, 7, 6, 5, 4, 13, 12, 11][units]
    new_value = inc + biggest_existing_extension_value
    return new_value


### UNIT TEST FUNCTIONS  #################################################

# def Z__set_max_log_file_size(new_max_size: int) -> int:
    # """ Set the global se lf._max_log_file_size.
    # Caller is normally a unit test and is expected to call this function
    # during its cleanup to restore the production value.
    # UNIT TEST ONLY
    # """
    # #print(f"LEMLFT$720  Z__set_max_log_file_size to {new_max_size} =======================================")
    # global se lf._max_log_file_size
    # old = s elf._max_log_file_size
    # se lf._max_log_file_size = new_max_size
    # return old
# 
# def Z__set_log_fspace_high_watermark(new_high_watermark: int) -> int:
    # """ Set the global LOG_FSPACE _HIGH_WATERMARK.
    # Caller is normally a unit test and is expected to call this function
    # during its cleanup to restore the production value.
    # UNIT TEST ONLY
    # """
    # #print(f"LEMLFT$732  Z__set_log_fspace_high_watermark to {new_high_watermark} =======================================")
    # global LOG_FSPACE_ HIGH_WATERMARK
    # old = LOG_FSPACE_ HIGH_WATERMARK
    # LOG_FSPACE_ HIGH_WATERMARK = new_high_watermark
    # return old
# 
# def Z__set_log_fspace_low_watermark(new_low_watermark: int) -> int:
    # """ Set the global LOG_FSPACE_ LOW_WATERMARK.
    # Caller is normally a unit test and is expected to call this function
    # during its cleanup to restore the production value.
    # UNIT TEST ONLY
    # """
    # #print(f"LEMLFT$744  Z__set_log_fspace_low_watermark to {new_low_watermark} =======================================")
    # global LOG_FSPACE_ LOW_WATERMARK
    # old = LOG_FSPACE_ LOW_WATERMARK
    # LOG_FSPACE_ LOW_WATERMARK = new_low_watermark
    # return old
#@@@@@@@@@@@@@@@ REMOVE THE ABOVE


###


