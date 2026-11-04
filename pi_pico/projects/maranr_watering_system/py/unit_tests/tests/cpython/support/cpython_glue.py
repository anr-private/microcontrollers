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

# One temp directory for the whole pytest run; removed when the run ends.
_ROOT = tempfile.mkdtemp(prefix="tests_")
atexit.register(shutil.rmtree, _ROOT, True)    # True = ignore errors


def get_scratch_path(name: str) -> str:
    """ A path inside the temp directory for this run. Nothing is created. """
    return os.path.join(_ROOT, name)


def remove_scratch_path(path: str) -> None:
    """ Remove a file or a directory tree with specified path.
    The path is typically a path returned from get_scratch_path().
    Does nothing if the path is not there. 
    Primary use is in finally blocks in unit tests.
    """
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
