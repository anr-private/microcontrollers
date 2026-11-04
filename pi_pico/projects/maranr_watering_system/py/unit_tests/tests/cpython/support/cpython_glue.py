# cpython_glue.py
#
# Platform glue for shared tests, CPython side (found by pytest through the
# `pythonpath` setting in pytest.ini). The Pico side is tests/pico/pico_glue.py.
import os
import tempfile
import shutil

_ROOT = tempfile.mkdtemp(prefix="tests_")


def get_scratch_path(name:str) -> str:
    # A path inside a fresh temp directory.
    return os.path.join(_ROOT, name)

def remove_scratch_path(name: str) -> None:
    _remove_dir_if_present(name)

def _remove_dir_if_present(path: str) -> None:
    """ Clear away leftovers of an earlier run that crashed. """
    if _does_path_exist(path):
        _remove_the_subdir(path)

def _does_path_exist(path: str) -> bool:
    """ True if the file or directory exists. """
    try:
        os.stat(path)
        return True
    except OSError:
        return False

def _remove_the_subdir(dir_path: str) -> None:
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"cpython_glue._remove_the_subdir **Error** {dir_path} : {e.strerror}")


###
