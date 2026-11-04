# pico_glue.py
#
# Platform glue for shared tests, Pico side. NEVER imported: run_pico_tests.py
# appends this text AFTER the test file's source, then sends the result with
# mpremote run. Because it comes after, line numbers in a traceback are the
# test file's own line numbers.
import sys

from lib1.file_utils import remove_subdir


def get_scratch_path(name:str) -> str:
    # Relative path: the Pico's current directory is the root, '/'.
    return "_t_" + name

def remove_scratch_path(name: str) -> None:
    _remove_dir_if_present(name)

def _remove_dir_if_present(path: str) -> None:
    """ Clear away leftovers of an earlier run that crashed. """
    if _does_path_exist(path):
        remove_subdir(path)

def _does_path_exist(path: str) -> bool:
    """ True if the file or directory exists. """
    try:
        os.stat(path)
        return True
    except OSError:
        return False

def run_all_tests() -> None:
    names = sorted([n for n in globals() if n.startswith("test_")])
    failed = []
    for name in names:
        try:
            globals()[name]()
        except Exception as ex:  # AssertionError too
            failed.append(name)
            print("FAILED:", name)
            sys.print_exception(ex)
    print(len(names), "tests,", len(failed), "failed")
    print("RESULT: " + ("FAILED" if failed else "PASSED"))


run_all_tests()

###
