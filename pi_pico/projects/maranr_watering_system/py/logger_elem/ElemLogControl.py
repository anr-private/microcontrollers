# ElemLogControl.py
# 
# Control and registrar for ElemLogger

import os
import sys

from file_utils import read_last_n_lines, filter_dir_contents

from .ElemLogger import ElemLogger

# subdir in which log files are found
LOG_FILES_SUBDIR = "logs"

# log files are this base name plus '.' plus '000', '001', etc
BASE_LOG_FNAME = "mws_log"

# Starting point for creating the extensions for log files
DEFAULT_FNAME_STARTING_EXTENSION_VALUE = 10

# nominal max size of a log file  in bytes
# it may be slightly larger due to 'hint keep-lines'
MAX_LOG_FILE_SIZE = 20_000

# If keep-lines hint has been requested, we'll allow a log file to get 
# bigger than MAX_LOG_FILE_SIZE by this amount:
KEEP_LINES_HINT_ADDED_SIZE = 1000



VALIDATE = 13524687

def prt(s):
    print(s)


class ElemLogControl:
    # central control for logging
    # Handles the log file(s) - the only class that does so

    _instance = None

    #@@@@@@@@@@@@@@@@@@@@ move this into the instance?  why is it at the class level?
    # key: simplified class name   value: ElemLogger for that class
    registry = {}


    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = ElemLogControl(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        #print(f"ELC@56  NULLIFY INSTANCE  =======================================")
        # UNIT TEST ONLY
        ElemLogControl._instance = None
        ElemLogControl.registry = {}

    @classmethod
    def _set_max_log_file_size(cls, new_max_size):
        # unit test ONLY
        print(f"ELC@64  _set_max_log_file_size to {new_max_size} =======================================")
        global MAX_LOG_FILE_SIZE
        MAX_LOG_FILE_SIZE = new_max_size


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"ELC@71 CALLED CTOR use get_instance()"
            raise RuntimeError(m)

        # An int value: the value to be used for the file extension 
        # of the next log file that will be created. 
        # The value is converted into 3 decimal digits
        # and used as the file extension on BASE_LOG_FNAME.
        # If None, no logs have been opened yet so we'll need  to
        # determine the file extension of the first file.
        # And if None, the _log_file_table will be empty.
        self._fname_next_ctr = None

        # log files that have been created and are now closed
        # List contains tuples: (log-filename:str, fsize: int)
        self._log_file_table = []

        # path of currently-open log file
        self._current_log_fpath = None
        # file descriptor for currently-open logfile
        self._logf = None
        # current log file size (bytes)
        self._current_log_fsize = 0


    def get_logs_totals(self, include_currently_open_file=True):
        # get the total values / stats 
        num_logs = len(self._log_file_table)
        total_size = sum(fitem[1] for fitem in self._log_file_table)
        if include_currently_open_file:
            num_logs += 1
            total_size += self._current_log_fsize
        return (num_logs, total_size)

    def get_log_table_item(self, item_index):
        try:
            return self._log_file_table[item_index]
        except IndexError:
            return None


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses ElemLogControlABC
        # Returns a logger obj the caller should use

        prt(f"ELC@115   obj is {repr(obj_instance)} ")

        simplified_class_name = extract_simplified_classname(obj_instance)
        prt(f"ELC@118 {simplified_class_name=}")

        # does this class have a logger assigned?
        logger = self.registry.get(simplified_class_name)
        prt(f"ELC@122  logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = ElemLogger(self, simplified_class_name)
            self.registry[simplified_class_name] = logger
        if 0: self.dump_registered_loggers(self.registry)
        return logger


    def get_registered_classes(self):
        return self.registry.keys()


    def enable_logging(self, class_name, enabled):
        logger = self.registry.get(class_name)
        print(f"ELC@136 logger is {logger}  {enabled=}")
        logger.enable_log(enabled)


    def log_and_print_one_line(self, line):
        self.log_one_line(line)
        print(line)

    def log_one_line(self, line):
        if line is None: line = ""

        if self._logf is None:
            self._start_a_new_logfile()

        try:
            self._logf.write(line)
            self._logf.write("\n")
            self._logf.flush()
            self._current_log_fsize += len(line)+1
            print(f"ELC@155  @@@@@ curr log size {self._current_log_fsize}  {line=}")

        except OSError as ex:
            # see examples/file_and_dirs_io/errno_show_all.py to see all errno values
            print(f"ELC@159  Error writing '{self._current_log_fpath}' EX={repr(ex)}  EX='{str(ex)}' ")
            # 28 is 'out of space'
            print(f"ELC@161 {ex.errno=}")
        except Exception as ex:
            print(f"ELC@163: Error writing to file '{self._current_log_fpath}': {repr(ex)}")
            print(f"ELC@164: Error writing to file '{self._current_log_fpath}': {str(ex)}")

        if self._current_log_fsize > MAX_LOG_FILE_SIZE:
            print(f"ELC@167  @@@@@ curr log size > MAX curr={self._current_log_fsize} max={MAX_LOG_FILE_SIZE}")
            self._close_current_log_file("log_one_line")

    def _start_a_new_logfile(self):
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
            m = f"ECL@144 _start_a_new_logfile OLD LOG FILE IS NOT CLOSED!"
            print(m)
            raise RuntimeError(m)

        self._create_the_logs_subdir()

        new_log_fpath = self._make_new_log_fpath()

        try:
            logf = open(new_log_fpath, "w")
        except Exception as ex:
            print(f"@@@@@@@@@@@@@ CANNOT OPEN LOGFILE '{new_log_fpath}'  ex={ex}  {str(ex)}")
        self._logf = logf
        self._current_log_fpath = new_log_fpath
        self._current_log_fsize = 0
        print(f"ELC@201  OPENED NEW LOG {self._current_log_fpath}")


    def _make_new_log_fpath(self):
        if self._fname_next_ctr is None:
            # Determine the file extension of the first logfile that
            # we are going to write in this session.
            new_extension_value = self._determine_starting_fname_extension_value()
            # The next file's extension
            self._fname_next_ctr = new_extension_value + 1
        else:
            # We have already created at least one logfile,
            # so subsequent logfiles' extensions are just sequential int
            # values.
            new_extension_value = self._fname_next_ctr
            self._fname_next_ctr += 1

        fpath = f"{LOG_FILES_SUBDIR}/{BASE_LOG_FNAME}.{new_extension_value:03d}"
        #@@@@@@@@@ TODO what if > 999?
        print(f"ELC@220 @@@@@@@@@@@@@@@ new fpath='{fpath}'")
        return fpath


    # def _make_new_log_fpath__OLD(self):#@@@@@@@@@@@@@@@@
        # # Init if we have no value yet
        # if self._fname_next_ctr is None:
            # self._fname_next_ctr = DEFAULT_FNAME_STARTING_EXTENSION_VALUE
# 
        # self._fname_next_ctr = self._determine_starting_fname_extension_value()
# 
        # fpath = f"{LOG_FILES_SUBDIR}/{BASE_LOG_FNAME}.{self._fname_next_ctr:03d}"
        # self._fname_next_ctr += 1
        # #@@@@@@@@@ TODO what if > 999?
        # print(f"ELC@234 @@@@@@@@@@@@@@@ new fpath='{fpath}'")
        # return fpath


    def _determine_starting_fname_extension_value(self):
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
            self._determine_biggest_existing_log_fname_extension_value()

        if not biggest_existing_extension_value:
            return DEFAULT_FNAME_STARTING_EXTENSION_VALUE

        print(f"ELC@257 {biggest_existing_extension_value=}")

        if biggest_existing_extension_value is None:
            # Use a fake biggest if there are no extant logfiles
            biggest_existing_extension_value = DEFAULT_FNAME_STARTING_EXTENSION_VALUE
            print(f"ELC@262 USED DEFAULT TO FAKE THIS: {biggest_existing_extension_value=}")

        new_extension_value = \
          self._determine_new_starting_extension_value(biggest_existing_extension_value)

        print(f"ELC@267 {new_extension_value=}")

        return new_extension_value


    def _determine_biggest_existing_log_fname_extension_value(self):
        # Look for old log files. 
        # Pick the one with the highest value 000-900 as its extension.
        # Return the int value of that file extension.
        # Returns 
        # gets (fname, ftype, fsize, file-extension-int-value) 
        existing_logs_info = filter_dir_contents(LOG_FILES_SUBDIR, _log_file_filter)

        print(f"ELC@280 _determine_starting_fname_extension_value fname_ext_values={existing_logs_info}")

        if len(existing_logs_info) == 0: 
            return None

        biggest = max([fitem[3] for fitem in existing_logs_info])

        print(f"ELC@287 max _determine_starting_fname_extension_value is {biggest=}")

        return biggest


    def _determine_new_starting_extension_value(self, biggest_existing_extension_value):
        # find a new extension value that is bigger than the
        # biggest_prior_value. 
        # Returns int value
        
        # This should never happen:
        if biggest_existing_extension_value < DEFAULT_FNAME_STARTING_EXTENSION_VALUE:
            return DEFAULT_FNAME_STARTING_EXTENSION_VALUE

        ###units = biggest_existing_extension_value - ((biggest_existing_extension_value // 10) * 10)
        units = biggest_existing_extension_value % 10
        print(f"ELC@303  {biggest_existing_extension_value=}  {units=}")

        # Pick an increment based on the lowest-order digit of the 
        # biggest previous file extension.
        # This creates a gap in the number of logfiles from one session
        # to the next.
        inc = [10, 9, 8, 7, 6, 5, 4, 13, 12, 11][units]
        new_value = inc + biggest_existing_extension_value
        return new_value


    def close_logging(self):
        # close the logger

        self._close_current_log_file("close_logging")


    def _create_the_logs_subdir(self):
        # create the subdir into which we write log files
        try:
            os.mkdir(LOG_FILES_SUBDIR)
        except OSError as ex:
            if ex.errno == 17: # already exists
                pass
                #print(f"ELC@327  Subdir '{LOG_FILES_SUBDIR}' already exists")
            else:
                print(f"ELC@329 *ERROR* {LOG_FILES_SUBDIR} errno={ex.errno} dir  cannot be created")


    def _close_current_log_file(self, who):
        if self._logf is not None:
            print(f"ELC@334 CLOSING_close_current_log_file {who=}: close file '{self._current_log_fpath}'")
            try:
                self._logf.close()
            except Exception as ex:
                m = f"ELC@338 ERROR CLOSING log file '{self._current_log_fpath}'  ex={ex} {str(ex)}"
            # Keep track of every log file as it is closed.
            fname = self._current_log_fpath
            fsize = self._current_log_fsize
            log_file_info = (fname, fsize)
            print(f"ELC@343 Closed current log. Saving log info: {log_file_info}")
            self._log_file_table.append(log_file_info)
            print(f"ELC@345 Closed current log. LOG TABLE: {self._log_file_table}")
        # We have no open logfile.
        self._logf = None
        self._current_log_fpath = None
        self._current_log_fsize = 0


    def get_lines_from_log_file(self, relative_line_number, number_of_lines):
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


    def dump_registered_loggers(self, registry):
        m = "ELC@366  Classes registered in ElemLogControl:"
        prt(m)
        self.log_one_line(m)
        for k,v in self.registry.items():
            m = f"  {k}  {v}"
            prt(m)
            self.log_one_line(m)


### FUNCTIONS  ###########################################################

def is_3_digit_int(s):
    # Returns int(s) if s is a 3-digit number; else None.
    if not  s: return None
    if len(s) != 3: return None
    try:
        ival = int(s)
    except (TypeError, ValueError):
        return None
    if ival <= 0 or ival > 999: return None
    return ival


def _log_file_filter(fname, ftype, fsize):
    # Returns None if the file is not chosen.
    # Returns the filename extention value (an int) if chosen
    print(f"ELC@392 _log_file_filter  fname='{fname}'  {fsize=}")

    if ftype != "f": return None
    #
    parts = fname.rsplit('.',1)
    print(f"@@@@ parts {parts}")
    if len(parts) != 2: return None
    #
    fpart    = parts[0]
    ext_part = parts[1]
    #
    if fpart != "mws_log": return None
    ext_val = is_3_digit_int(ext_part)
    print(f"@@T@206   extension is_3_digit_int('{ext_part}') is {ext_val}")
    if ext_val is None: return None
    return ext_val


def extract_simplified_classname(obj_instance):
    # given a full class name string like "abc.def.MyClass"; return "MyClass"
    # Obtain the string using  str(obj.__class__)
    obj_repr = repr(obj_instance)
    prt(f"ELC@414 extract_simplified_classname   {obj_repr=}")
    parts = obj_repr.rsplit(".", 1)
    prt(f"ELC@416  {parts=}")
    name_and_addr = parts[-1]
    parts = name_and_addr.split(None, 1)
    prt(f"ELC@419  {parts=}")

    simplified_class_name = parts[0]
    simplified_class_name = simplified_class_name.replace("<", "")
    simplified_class_name = simplified_class_name.replace(">", "")
    return simplified_class_name

###
