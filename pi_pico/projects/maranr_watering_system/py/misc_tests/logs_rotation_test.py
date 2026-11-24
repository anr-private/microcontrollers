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

from logger_embed_module.LemLogControl import LemLogControl, Z_replace_log_file_table

HELP_INFO="""NO HELP YET
"""


#=== OPTIONS PARSER  ============================================

class _Options:
    """ """
    def __init__(self):
        """ """

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
            print(f"ZLOGSROT$1 DEBUG-OPTIONS ENABLED  {args=}")
            break

    argidx = 0
    while argidx < len(args):

        arg = args[argidx]; argidx += 1

        print(f"ZLOGSROT$1  {arg=!r}")

        if arg.startswith("--"):
            opt = arg[2:]
        elif arg.startswith("-"):
            opt = arg[1:]
        else:
            print(f"ZLOGSROT$1 NOT AN OPT {arg=!r} - add to 'other_items")
            opts.other_items.append(arg)
            continue

        optLc = opt.lower()
        del arg
        print(f"ZLOGSROT$1  {optLc=!r}")

        if optLc in ("help","h"):
            print(HELP)
            sys.exit(1)

        elif opt in ("v", "verbose"):
            opts.verbose = True

        elif opt in ("V", "veryverbose"):
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
            s = f"ZLOGSROT$1 *ERROR* Unknown option '{opt}'"
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
    print(f"ZLOGSROT$28 MAIN: {args=}")

if __name__ == "__main__":
    #main(sys.argv[1:])

    run_options_tests()


###
