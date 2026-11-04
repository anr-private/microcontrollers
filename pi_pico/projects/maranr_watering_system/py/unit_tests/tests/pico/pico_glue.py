# pico_glue.py
#
# Platform glue for shared tests, Pico side. NEVER imported: run_pico_tests.py
# appends this text AFTER the test file's source, then sends the result with
# mpremote run. Because it comes after, line numbers in a traceback are the
# test file's own line numbers. The 'assembled' test files are run using
# 'mpremote run'; they are found in the build/ subdir.
#
# Provides get_scratch_path() and remove_scratch_path() to create a 
# scratch subdir for files created by tests (example: log files in the
# logger_elem tests).
#  Note cpython_glue.py provides the same functions for tests run on the PC.
# Every scratch path is inside one directory, _SCRATCH_ROOT. 
# The runner creates it before the first test and removes it after the last
# so the PICO final state is as it was before testing,
# even if a test forgets to clean up. 
# If the subdir remains after a crashed run or badly-formed test,
# it is removed at the start of the next run.

import os
import sys

from lib1.file_utils import remove_subdir

# Relative path: the Pico's current directory is the root, '/',
# so the scratch dir is "/" + _SCRATCH_ROOT.
_SCRATCH_ROOT = "_test_scratch"


def get_scratch_path(name: str) -> str:
    """ Returns a path inside _SCRATCH_ROOT. Nothing is created. """
    return _SCRATCH_ROOT + "/" + name


def remove_scratch_path(path: str) -> None:
    """ Remove a file or a directory tree with specified path.
    The path is typically a path returned from get_scratch_path().
    Does nothing if the path is not there. 
    Primary use is in finally blocks in unit tests.
    """
    if not _does_path_exist(path):
        return
    if _is_directory(path):
        remove_subdir(path)
    else:
        os.remove(path)


def _does_path_exist(path: str) -> bool:
    """ True if the file or directory exists. """
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def _is_directory(path: str) -> bool:
    """ True if path is a directory (0x4000 is the directory bit of st_mode). """
    return bool(os.stat(path)[0] & 0x4000)


def run_all_tests() -> None:
    """ Find and run the unit tests - runs on the PICO """
    # find the tests
    names = sorted([n for n in globals() if n.startswith("test_")])
    failed = []
    # Remove any old / leftover scratch subdir and its contents.
    # Create a new one for the tests we are going to run.
    remove_scratch_path(_SCRATCH_ROOT)
    os.mkdir(_SCRATCH_ROOT)
    # Run the tests
    try:
        for name in names:
            try:
                globals()[name]()
            except Exception as ex:  # AssertionError too
                failed.append(name)
                print("FAILED:", name)
                sys.print_exception(ex)
    finally:
        remove_scratch_path(_SCRATCH_ROOT)
    print(len(names), "tests,", len(failed), "failed")
    print("RESULT: " + ("FAILED" if failed else "PASSED"))


run_all_tests()

###
