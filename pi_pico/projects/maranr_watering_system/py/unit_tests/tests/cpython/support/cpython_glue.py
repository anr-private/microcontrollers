# cpython_glue.py
#
# Platform glue for shared tests, CPython side (found by pytest through the
# `pythonpath` setting in pytest.ini). The Pico side is tests/pico/pico_glue.py.
# Both provide get_scratch_path() and remove_scratch_path().
# More details in pico_glue.py

import atexit
import os
import shutil
import tempfile

# If true, saves the scratch dir and its contents for viewing/debugging
# The scratch dir(s) will be removed when Ubuntu reboots but are
# preserved until then. If false, the dir and contents are removed
# when each test completes.
SAVE_THE_SCRATCH_FILES = True

# One temp directory for the whole pytest run; removed when the run ends.
_ROOT = tempfile.mkdtemp(prefix="MWS_tests_")

def do_cleanup_at_exit():
    if SAVE_THE_SCRATCH_FILES:
        print(f"CPYTHON_GLUE@21 SAVING the scratch path: '{_ROOT}'")
        return
    shutil.rmtree(_ROOT, ignore_errors=True)

###@@@@@@@atexit.register(shutil.rmtree, _ROOT, True)    # True = ignore errors
atexit.register(do_cleanup_at_exit)


def get_scratch_path(name: str) -> str:
    """ A path inside the temp directory for this run. Nothing is created. """
    scratch_path = os.path.join(_ROOT, name)
    if SAVE_THE_SCRATCH_FILES:
        print(f"CPYTHON_GLUE@28 scratch path: '{scratch_path}'")
    return scratch_path
    #@@@@@@@@@@@@return os.path.join(_ROOT, name)


def remove_scratch_path(path: str) -> None:
    """ Remove a file or a directory tree with specified path.
    The path is typically a path returned from get_scratch_path().
    Does nothing if the path is not there. 
    Primary use is in finally blocks in unit tests.
    """
    if SAVE_THE_SCRATCH_FILES:
        print(f"CPYTHON_GLUE@30 remove_scratch_path is DISABLED")
        return

    if not _does_path_exist(path):
        return
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except OSError as ex:
        print(f"cpython_glue.remove_scratch_path **Error** {path} : {ex.strerror}")


def _does_path_exist(path: str) -> bool:
    """ True if the file or directory exists. """
    try:
        os.stat(path)
        return True
    except OSError:
        return False


###
