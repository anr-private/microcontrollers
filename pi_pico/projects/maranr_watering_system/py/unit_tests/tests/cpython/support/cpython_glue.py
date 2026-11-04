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

# Set MWS_SAVE_SCRATCH=1 in the environment to keep scratch files for
# viewing/debugging. When saving, remove_scratch_path() moves a path aside
# (name.saved_1, name.saved_2, ...) instead of deleting it, so later tests
# still see a clean slate. The saved files stay under /tmp until Ubuntu
# clears it (reboot or the periodic age-based cleanup).
SAVE_THE_SCRATCH_FILES = os.environ.get("MWS_SAVE_SCRATCH") is not None

# One temp directory for the whole pytest run. Removed when the run ends,
# unless SAVE_THE_SCRATCH_FILES is true.
_ROOT = tempfile.mkdtemp(prefix="MWS_tests_")

_saved_count = 0


def _remove_scratch_root() -> None:
    if SAVE_THE_SCRATCH_FILES:
        print(f"cpython_glue@29: ++++   SAVED scratch files in '{_ROOT}' ++++++++++++++++++++++++++++++++")
        return
    shutil.rmtree(_ROOT, ignore_errors=True)


atexit.register(_remove_scratch_root)


def get_scratch_path(name: str) -> str:
    """ A path inside the temp directory for this run. Nothing is created. """
    return os.path.join(_ROOT, name)


def remove_scratch_path(path: str) -> None:
    """ Remove a file or a directory tree with specified path.
    The path is typically a path returned from get_scratch_path().
    Does nothing if the path is not there.
    When SAVE_THE_SCRATCH_FILES is true the path is moved aside, not deleted.
    Primary use is in finally blocks in unit tests.
    """
    global _saved_count
    if not _does_path_exist(path):
        return
    try:
        if SAVE_THE_SCRATCH_FILES:
            _saved_count += 1
            os.rename(path, f"{path}.saved_{_saved_count}")
        elif os.path.isdir(path):
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
