# cpython_glue.py
#
# Platform glue for shared tests, CPython side (found by pytest through the
# `pythonpath` setting in pytest.ini). The Pico side is tests/pico/pico_glue.py.
import os
import tempfile

_ROOT = tempfile.mkdtemp(prefix="tests_")


def get_scratch_path(name):
    # A path inside a fresh temp directory.
    return os.path.join(_ROOT, name)

###
