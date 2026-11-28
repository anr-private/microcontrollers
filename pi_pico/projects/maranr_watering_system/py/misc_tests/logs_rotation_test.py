# logs_rotation_test.py
#
# LINEMARKER=ZLOGSROT
#
# Test for creating log files repeatedly, verifying that as logs get
# created eventually the old ones get removed in order to keep
# the system filespace from being filled up / overwhelmed.
# This is a stand-alone test meant to be run like this:
#    - ensure that the Pico has the latest install for 
#      lib*/ and logger_embed_module/*
#    - copy this program to the Pico
#        - stop Thonny
#        - mpremote cp logs_rotation_test.py :
#    - use Thonny to run it
# NOTE the following does not work: the 'run' command of mpremote
# does not support any kind of keyboard input.
#    - mpremote run logs_removal_test.py


import os
import sys

# add py/ to our path - for both Pico and linux
sys.path.append('..')
# for p in sys.path:
    # print(p)


from lib1.file_utils import remove_subdir
from lib1.file_system_utils import get_filesystem_space, get_actual_current_freespace
from lib1.platform_info import USING_PICO_HARDWARE, USING_LINUX_HARDWARE

from logger_embed_module.LemLogControl import LemLogControl, Z_replace_log_file_table

V = False
VV = False

HELP_INFO="""NO HELP YET
"""

class _Options:
    """ """
    def __init__(self):
        """ """
        # Items that are not options (do not start with '-' or '--')
        self.other_items = []
        self.verbose = False
        self.veryverbose = False
        self.debug = False
        self.debugOptions = False

    @property
    def optionNames(self):
        """ Returns a collection of str: the property names
        of the option values.
        """
        names = []
        for n in self.__dict__.keys():
            if n.startswith("_"): continue
            names.append(n)
        return names

    def __str__(self):
        """ """
        s = []
        for name in self.optionNames:
            val = getattr(self, name)
            s.append(f"{name}={val}")
        return f"{self.__class__.__name__}[{','.join(s)}]"
    __repr__ = __str__



def perform_test(opts: _Options) -> None:
    print(f"ZLOGSROT$75 PERFORM TEST   {opts=}")

    logs_dir = "LOGS_ROTATION_TEST"
    remove_subdir(logs_dir)

    log_parameters_selector = "Z_tests"

    llc = LemLogControl.configure_logger(logs_dir, log_parameters_selector)

    print(f"ZLOGSROT$84 LemLogControl: {llc}")

    llft = llc.ZgetLemLogFileTable()

    r = llc.get_logs_totals(include_currently_open_file=True)
    print(f"ZLOGSROT$89 Initial values: {r=}")
    num_extant_files, extant_logfile_fsize, log_file_table_size = r
    print(f"ZLOGSROT$91 Initial values: {num_extant_files=}  {extant_logfile_fsize=}  {log_file_table_size=}")
    prev_num_extant_files = num_extant_files
    n = 0
    num_files_created = 0
    prev_biased_freespace = 0
    while 1:

        biased_freespace = llft._get_biased_filesystem_freespace()

        r = llc.get_logs_totals(include_currently_open_file=True)
        ###print(f"ZLOGSROT$101 {r=}")
        num_extant_files, extant_logfile_fsize, log_file_table_size = r

        if biased_freespace != prev_biased_freespace:
            print(f"ZLOGSROT$105 {num_extant_files=:3d} prev={prev_num_extant_files:3d} "+\
                  f"extantLogFsize={extant_logfile_fsize:6d}         "+\
                  f"{log_file_table_size=:7d}  {llft._get_biased_filesystem_freespace()=:6d}")
            prev_biased_freespace = biased_freespace

        #print(f"ZLOGSROT$110 {num_extant_files=} prev={prev_num_extant_files} "+\
        #      f"extantLogFsize={extant_logfile_fsize}         {log_file_table_size=}")

        #print(f"ZLOGSROT$113 {num_extant_files=} prev={prev_num_extant_files}  "+
        #    f"      biased_freesp={llft._get_biased_filesystem_freespace()}")

        if prev_num_extant_files < num_extant_files:
            num_files_created += 1
            prev_num_extant_files = num_extant_files
            print(f"ZLOGSROT$119 {num_files_created=}")
            if num_files_created >= 10:
                break

        llc.log_one_line(f"ZLOGSROT$123 Line 1")

        n += 1
        if n >= 3000000:
            break


#=== OPTIONS PARSER  ============================================


def parse_options(args):
    """ """

    opts = _Options()

    # Items that are not options (do not start with '-' or '--')
    opts.other_items = []

    opts.verbose = False
    opts.veryverbose = False
    opts.debug = False
    opts.debugOptions = False

    argidx = 0
    while argidx < len(args):
        arg = args[argidx]; argidx += 1
        if arg in ("--Zoptions", "--zoptions", "--debugOptions"):
            opts.debugOptions = True
            print(f"ZLOGSROT$151 DEBUG-OPTIONS ENABLED  {args=}")
            break

    argidx = 0
    while argidx < len(args):

        arg = args[argidx]; argidx += 1

        print(f"ZLOGSROT$159  {arg=!r}")

        if arg.startswith("--"):
            opt = arg[2:]
        elif arg.startswith("-"):
            opt = arg[1:]
        else:
            print(f"ZLOGSROT$166 NOT AN OPT {arg=!r} - add to 'other_items")
            opts.other_items.append(arg)
            continue

        optLc = opt.lower()
        del arg
        print(f"ZLOGSROT$172  {optLc=!r}")

        if optLc in ("help","h"):
            print(HELP_INFO)
            sys.exit(1)

        elif opt in ("v", "verbose"):
            opts.verbose = True

        elif opt in ("V", "vv", "veryverbose"):
            opts.verbose = True
            opts.veryverbose = True
            print("VERY VERBOSE MODE")

        elif opt in ("Z", "debug"):
            opts.debug = True

        elif opt in ("Zoptions", "zoptions", "debugOptions"):
            # This is redundant - see the pre-screen loop above
            opts.debugOptions = True

        # elif optLc in ("raw",):
            # opts.showRaw = True
        # elif _isInt(opt):
            # ival = int(opt)
            # opts.dataSets.append(ival)

        else:
            s = f"ZLOGSROT$200 *ERROR* Unknown option '{opt}'"
            raise RuntimeError(s)

    return opts


################################################################

def _isInt(self, stg):
    try:
        _ = int(stg)
        return True
    except (ValueError, TypeError):
        pass
    return False

################################################################

def run_options_tests():
    if 1:
        opts = parse_options(["-Zoptions", "-v"])
        print(f"+++ opts={opts}")
        assert opts.verbose is True
        assert opts.veryverbose is False
        assert opts.other_items == []
    if 1:
        opts = parse_options(["-Zoptions", "a", "b"])
        print(f"+++ opts={opts}")
        assert opts.other_items == ["a", "b"]


###  MAIN  ####################################################

def main(args):
    print(f"ZLOGSROT$234 MAIN: {args=}")
    opts = parse_options(args)

    global V, VV, DEBUG
    V = opts.verbose or opts.veryverbose
    VV = opts.veryverbose
    DEBUG = opts.debug
    if V: print(f"ZLOGSROT$241  {V=} VeryV={VV}  {DEBUG=}")

    perform_test(opts)


if __name__ == "__main__":
    if 0:
        run_options_tests()
        sys.exit(1)

    main(sys.argv[1:])

###
