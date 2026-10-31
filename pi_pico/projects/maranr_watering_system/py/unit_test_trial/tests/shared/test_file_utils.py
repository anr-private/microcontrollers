# test_file_utils.py
#
# Shared test for lib1/file_utils.py. It runs
#   - on the PC under pytest (CPython), and
#   - on the Pico: run_pico_tests.py appends tests/pico/pico_glue.py to a copy of
#     this file and sends it with `mpremote run`.
# Plain test_ functions with plain asserts: no pytest import. Every assert has a
# message with the values, because MicroPython shows no more than the message.
#
# Covers what the application uses: list_dir_contents(), filter_dir_contents(),
# remove_subdir() and remove_file().
#
# Each test makes its own scratch directory (get_scratch_path(), from the platform
# glue) and removes it in a finally: the tests do not depend on each other or on
# their order. About a dozen tiny files per test, one of BIG_SIZE bytes, so the
# Pico's flash wear is negligible.
#
# Three tests make file_utils print error lines on purpose (a missing directory,
# a missing file, a missing path). Each is announced by a "Next:" line and closed
# by an "(end of the expected ...)" line. Lines that start with TFUT@NNN: come from
# this test; the code under test prints lines that start with FU@. run_pico_tests.py
# shows the output only for a file that did not pass.
#
# Not tested on purpose: symlinks, FIFOs and the like (they cannot exist on the
# Pico), and the size reported for a directory (the application does not use it).
import os

from lib1.file_utils import list_dir_contents, filter_dir_contents, remove_subdir, remove_file

# CPython: the real module tests/cpython/cpython_glue.py.
# Pico: there is no such module; run_pico_tests.py appends get_scratch_path().
try: from cpython_glue import get_scratch_path
except ImportError: pass

BIG_SIZE = 1000

# What create_scratch_dir() makes, as list_dir_contents() should report it:
# (name, type, size). The size of a directory is None: it is not checked.
EXPECTED_LISTING = sorted([
    (".hidden", "f", 3),
    ("a.txt", "f", 5),
    ("data.bin", "f", BIG_SIZE),
    ("empty.txt", "f", 0),
    ("name with spaces.txt", "f", 2),
    ("emptydir", "d", None),
    ("sub", "d", None),
])

# What filter_dir_contents() should return for filter_big_files(): the files only
# (the filter drops directories), each with the filter's True/False as 4th item.
EXPECTED_FILTERED = sorted([
    (".hidden", "f", 3, False),
    ("a.txt", "f", 5, True),
    ("data.bin", "f", BIG_SIZE, True),
    ("empty.txt", "f", 0, False),
    ("name with spaces.txt", "f", 2, False),
])

filter_calls: list[tuple[str, str, int]] = []


def does_path_exist(path: str) -> bool:
    """ True if the file or directory exists. """
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def create_file(path: str, size: int) -> None:
    """ Create a file of `size` bytes. """
    with open(path, "wb") as f:
        f.write(b"x" * size)


def remove_dir_if_present(path: str) -> None:
    """ Clear away leftovers of an earlier run that crashed. """
    if does_path_exist(path):
        remove_subdir(path)


def create_scratch_dir(path: str) -> None:
    """ Make the directory `path` with the contents described by EXPECTED_LISTING. """
    remove_dir_if_present(path)
    os.mkdir(path)
    create_file(path + "/a.txt", 5)
    create_file(path + "/empty.txt", 0)
    create_file(path + "/data.bin", BIG_SIZE)
    create_file(path + "/name with spaces.txt", 2)
    create_file(path + "/.hidden", 3)
    os.mkdir(path + "/emptydir")
    os.mkdir(path + "/sub")
    create_file(path + "/sub/inner.txt", 7)


def normalize_listing(items: list) -> list:
    """ Sort by name and set the size of directories to None (it differs
    between platforms and the application does not use it). """
    out = []
    for item in items:
        name, ftype, fsize = item[0], item[1], item[2]
        if ftype == "d":
            fsize = None
        out.append((name, ftype, fsize))
    return sorted(out)


def filter_big_files(fname: str, ftype: str, fsize: int) -> bool | None:
    """ A file_filter for filter_dir_contents(): drops directories (None),
    and gives True for a file of more than 4 bytes, False for a smaller one. """
    filter_calls.append((fname, ftype, fsize))
    if ftype == "d":
        return None
    return fsize > 4


def test_list_dir_contents() -> None:
    """ list_dir_contents() on a directory with several kinds of entries. """
    d = get_scratch_path("list")
    create_scratch_dir(d)
    try:
        got = list_dir_contents(d)
        assert isinstance(got, list), got
        assert all(isinstance(item, tuple) and len(item) == 3 for item in got), got
        assert normalize_listing(got) == EXPECTED_LISTING, (normalize_listing(got), EXPECTED_LISTING)
        assert "inner.txt" not in [item[0] for item in got], ("went into sub/", got)
        empty = list_dir_contents(d + "/emptydir")
        assert empty == [], empty
    finally:
        remove_subdir(d)


def test_list_missing_dir_raises() -> None:
    """ list_dir_contents() on a directory that does not exist raises. """
    print("TFUT@136: Next: listing a directory that does not exist, on purpose.")
    print("TFUT@137: file_utils should print ONE error line and raise. That is expected.")
    raised: Exception | None = None
    try:
        list_dir_contents(get_scratch_path("does_not_exist"))
    except Exception as ex:
        raised = ex
    print("TFUT@143: (end of the expected error output)")
    assert raised is not None, "no exception was raised"


def test_filter_dir_contents() -> None:
    """ filter_dir_contents(): the filter is called once per entry with
    (name, type, size); None drops an entry; False keeps it. """
    d = get_scratch_path("filter")
    create_scratch_dir(d)
    try:
        del filter_calls[:]
        got = filter_dir_contents(d, filter_big_files)
        assert len(filter_calls) == len(EXPECTED_LISTING), filter_calls
        assert normalize_listing(filter_calls) == EXPECTED_LISTING, filter_calls
        assert sorted(got) == EXPECTED_FILTERED, (sorted(got), EXPECTED_FILTERED)
    finally:
        remove_subdir(d)


def test_remove_file() -> None:
    """ remove_file(): True when removed, False (with 2 error lines) when missing. """
    d = get_scratch_path("rmfile")
    create_scratch_dir(d)
    try:
        path = d + "/a.txt"
        removed = remove_file(path)
        assert removed is True, removed
        assert not does_path_exist(path), "file is still there"
        print("TFUT@171: Next: removing a file that does not exist, on purpose.")
        print("TFUT@172: file_utils should print TWO error lines and return False. That is expected.")
        removed_again = remove_file(path)
        print("TFUT@174: (end of the expected error output)")
        assert removed_again is False, removed_again
    finally:
        remove_subdir(d)


def test_remove_subdir_removes_tree() -> None:
    """ remove_subdir() removes a tree 3 levels deep. (Setup and cleanup in the
    other tests use remove_subdir() too: if it is broken, this test says so.) """
    t = get_scratch_path("tree")
    remove_dir_if_present(t)
    os.mkdir(t)
    create_file(t + "/top.txt", 1)
    os.mkdir(t + "/a")
    create_file(t + "/a/mid.txt", 2)
    os.mkdir(t + "/a/b")
    create_file(t + "/a/b/deep.txt", 3)
    os.mkdir(t + "/a/b/c")
    remove_subdir(t)
    assert not does_path_exist(t), "tree is still there"


def test_remove_subdir_missing_path_does_not_raise() -> None:
    """ remove_subdir() of a path that is not there does not raise
    (on the Pico it prints ONE error line then). """
    print("TFUT@199: Next: removing a directory that does not exist, on purpose.")
    print("TFUT@200: On the Pico file_utils prints ONE error line (none on CPython). That is expected.")
    raised: Exception | None = None
    try:
        remove_subdir(get_scratch_path("does_not_exist"))
    except Exception as ex:
        raised = ex
    print("TFUT@206: (end of the expected error output)")
    assert raised is None, raised

""" Claude's comments: what this tests:
The filter’s if ok is not None: check was changed to if ok:.
Reported file sizes were off by one.
Hidden files were skipped.
remove_file returned True for a missing file.
shutil.rmtree was replaced by os.rmdir.
The raise for a missing directory was removed.
FileNotFoundError was re-raised in remove_subdir.
"""
###
