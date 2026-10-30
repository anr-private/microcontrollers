# test_file_utils_sketch.py
#
# SKETCH of a shared test: runs under pytest on the PC, and on the Pico when
# run_pico_tests.py assembles it with pico_glue.py and sends it with mpremote run.
# Plain functions named test_..., plain assert, no pytest import.
import os

from lib1.file_utils import list_dir_contents, remove_subdir

# CPython: the real module tests/cpython/cpython_glue.py.
# Pico: there is no such module; run_pico_tests.py appends get_scratch_path().
try: from cpython_glue import get_scratch_path
except ImportError: pass


def create_file(path, text):
    with open(path, "w") as f:
        f.write(text)


def test_list_empty_dir():
    d = get_scratch_path("empty")
    os.mkdir(d)
    try:
        assert list_dir_contents(d) == [], list_dir_contents(d)
    finally:
        remove_subdir(d)


def test_list_file_and_dir():
    d = get_scratch_path("mixed")
    os.mkdir(d)
    try:
        create_file(d + "/a.txt", "hello")
        os.mkdir(d + "/sub")
        got = sorted((name, ftype) for name, ftype, _size in list_dir_contents(d))
        assert got == [("a.txt", "f"), ("sub", "d")], got
    finally:
        remove_subdir(d)


def test_remove_deep_tree():
    d = get_scratch_path("tree")
    os.mkdir(d)
    os.mkdir(d + "/a")
    os.mkdir(d + "/a/b")
    create_file(d + "/a/b/deep.txt", "x")
    remove_subdir(d)
    try:
        os.stat(d)
        assert False, "tree still exists"
    except OSError:
        pass

###
