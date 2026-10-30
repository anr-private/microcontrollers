# pico_glue.py
#
# Platform glue for shared tests, Pico side. NEVER imported: run_pico_tests.py
# appends this text AFTER the test file's source, then sends the result with
# mpremote run. Because it comes after, line numbers in a traceback are the
# test file's own line numbers.
import sys


def get_scratch_path(name):
    # Relative path: the Pico's current directory is the root, '/'.
    return "_t_" + name


def run_all_tests():
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
