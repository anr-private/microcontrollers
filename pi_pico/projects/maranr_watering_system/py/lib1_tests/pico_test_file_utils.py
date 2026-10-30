# pico_test_file_utils.py
#
# On-device test for file_utils (MicroPython on the Pico).
# Covers what the application uses: list_dir_contents(), filter_dir_contents(),
# remove_subdir() and remove_file().
#
# Run it from the PC with:
#     mpremote run pico_test_file_utils.py
# It needs lib1/file_utils.py on the Pico. The output ends with a line that
# contains RESULT: PASSED or RESULT: FAILED.
#
# It also runs on CPython3.
#
# It creates two scratch directories (SCRATCH_DIR, TREE_DIR) in the Pico's flash
# and removes them at the end. About a dozen tiny files, one of BIG_SIZE bytes,
# so the flash wear is negligible.
#
# Lines that start with TFUT@NNN: come from this test. Any other line comes from
# the code under test (its error messages start with FU@).
# Three of the checks make file_utils print error lines on purpose. Each is
# announced by a "Next:" line and closed by an "(end of the expected ...)" line.
#
# Not tested on purpose: symlinks, FIFOs and the like (they cannot exist on the
# Pico), and the size reported for a directory (the application does not use it).
#
# No __main__ guard: this file is only ever run, never imported.

import os

from lib1.file_utils import list_dir_contents, filter_dir_contents, remove_subdir, remove_file

# Relative paths: relative to the current directory (the root, '/', on the Pico).
SCRATCH_DIR = "_tfu_scratch"
TREE_DIR = "_tfu_tree"
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

failures: list[tuple[str, object, object]] = []
total = 0
filter_calls: list[tuple[str, str, int]] = []


def expect_equal(label: str, got: object, expected: object) -> None:
    """ Count one check; remember it if the result is not the expected one. """
    global total
    total += 1
    if got != expected:
        failures.append((label, got, expected))


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


def create_scratch_dir() -> None:
    """ Make SCRATCH_DIR with the contents described by EXPECTED_LISTING. """
    os.mkdir(SCRATCH_DIR)
    create_file(SCRATCH_DIR + "/a.txt", 5)
    create_file(SCRATCH_DIR + "/empty.txt", 0)
    create_file(SCRATCH_DIR + "/data.bin", BIG_SIZE)
    create_file(SCRATCH_DIR + "/name with spaces.txt", 2)
    create_file(SCRATCH_DIR + "/.hidden", 3)
    os.mkdir(SCRATCH_DIR + "/emptydir")
    os.mkdir(SCRATCH_DIR + "/sub")
    create_file(SCRATCH_DIR + "/sub/inner.txt", 7)


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


def filter_big_files(fname: str, ftype: str, fsize: int) -> "bool | None":
    """ A file_filter for filter_dir_contents(): drops directories (None),
    and gives True for a file of more than 4 bytes, False for a smaller one. """
    filter_calls.append((fname, ftype, fsize))
    if ftype == "d":
        return None
    return fsize > 4


def check_list_dir_contents() -> None:
    """ list_dir_contents() on a directory with several kinds of entries. """
    got = list_dir_contents(SCRATCH_DIR)
    expect_equal("list: result is a list", isinstance(got, list), True)
    expect_equal("list: every item is a 3-tuple",
                 all(isinstance(item, tuple) and len(item) == 3 for item in got), True)
    expect_equal("list: contents", normalize_listing(got), EXPECTED_LISTING)
    names = [item[0] for item in got]
    expect_equal("list: does not go into sub/", "inner.txt" in names, False)
    expect_equal("list: empty directory", list_dir_contents(SCRATCH_DIR + "/emptydir"), [])


def check_list_missing_dir() -> None:
    """ list_dir_contents() on a directory that does not exist raises. """
    print("TFUT@132: Next: listing a directory that does not exist, on purpose.")
    print("TFUT@133: file_utils should print ONE error line and raise. That is expected.")
    raised: "Exception | None" = None
    try:
        list_dir_contents(SCRATCH_DIR + "/does_not_exist")
    except Exception as ex:
        raised = ex
    print("TFUT@139: (end of the expected error output)")
    expect_equal("list missing dir: raises", raised is not None, True)


def check_filter_dir_contents() -> None:
    """ filter_dir_contents(): the filter is called once per entry with
    (name, type, size); None drops an entry; False keeps it. """
    del filter_calls[:]
    got = filter_dir_contents(SCRATCH_DIR, filter_big_files)
    expect_equal("filter: filter called once per entry", len(filter_calls), len(EXPECTED_LISTING))
    expect_equal("filter: filter called with name, type, size",
                 normalize_listing(filter_calls), EXPECTED_LISTING)
    expect_equal("filter: result", sorted(got), EXPECTED_FILTERED)


def check_remove_file() -> None:
    """ remove_file(): True when removed, False (with 2 error lines) when missing.
    It changes SCRATCH_DIR, so run it after the checks that list SCRATCH_DIR. """
    path = SCRATCH_DIR + "/a.txt"
    expect_equal("remove_file: returns True", remove_file(path), True)
    expect_equal("remove_file: file is gone", does_path_exist(path), False)
    print("TFUT@160: Next: removing a file that does not exist, on purpose.")
    print("TFUT@161: file_utils should print TWO error lines and return False. That is expected.")
    got = remove_file(path)
    print("TFUT@163: (end of the expected error output)")
    expect_equal("remove_file: missing file returns False", got, False)


def check_remove_subdir() -> None:
    """ remove_subdir() removes a tree 3 levels deep, and does not raise
    for a path that is not there (on the Pico it prints ONE error line then). """
    os.mkdir(TREE_DIR)
    create_file(TREE_DIR + "/top.txt", 1)
    os.mkdir(TREE_DIR + "/a")
    create_file(TREE_DIR + "/a/mid.txt", 2)
    os.mkdir(TREE_DIR + "/a/b")
    create_file(TREE_DIR + "/a/b/deep.txt", 3)
    os.mkdir(TREE_DIR + "/a/b/c")
    remove_subdir(TREE_DIR)
    expect_equal("remove_subdir: tree is gone", does_path_exist(TREE_DIR), False)

    print("TFUT@180: Next: removing a directory that does not exist, on purpose.")
    print("TFUT@181: On the Pico file_utils prints ONE error line (none on CPython). That is expected.")
    raised: "Exception | None" = None
    try:
        remove_subdir(TREE_DIR)
    except Exception as ex:
        raised = ex
    print("TFUT@187: (end of the expected error output)")
    expect_equal("remove_subdir: missing path does not raise", raised, None)


def perform_test() -> int:
    """ Run all the checks; returns 0 if they all passed, else 1. """
    # leftovers from an earlier run that crashed
    for path in (SCRATCH_DIR, TREE_DIR):
        if does_path_exist(path):
            remove_subdir(path)
    create_scratch_dir()
    try:
        check_list_dir_contents()
        check_list_missing_dir()
        check_filter_dir_contents()
        check_remove_file()
        check_remove_subdir()
    finally:
        remove_subdir(SCRATCH_DIR)
    expect_equal("cleanup: scratch dir is gone", does_path_exist(SCRATCH_DIR), False)

    print("TFUT@208:", total, "checks,", len(failures), "failures")
    for label, got, expected in failures:
        print("TFUT@210: FAILED:", label)
        print("TFUT@211:     expected:", expected)
        print("TFUT@212:     got:     ", got)
    print("TFUT@213: RESULT: " + ("FAILED" if failures else "PASSED - all checks correct"))
    return 1 if failures else 0


perform_test()

"""
Claude built this test. Its notes:
It has 15 checks, in the same plain-script style as
 pico_test_read_last_n_lines.py. 
It builds a small scratch directory in flash and checks:

list_dir_contents: the names, types and sizes of files (including an empty file
 and a 1000-byte one), a hidden name, a name with spaces, a subdirectory and an
 empty directory. It also checks that the listing doesn’t descend into
 subdirectories, and that a missing directory raises.
filter_dir_contents: the filter is called once per entry with (name, type,
 size), None drops an entry, and False keeps it. That is the gotcha documented 
in the function’s comment.
remove_file: returns True when it removes a file and False for a missing one.
remove_subdir: removes a tree three levels deep and doesn’t raise for a missing
 path. On the board this is the first real test of the recursion fix.

Directory sizes, symlinks and FIFOs are skipped, as you decided. Test lines
 carry a TFUT@NNN: prefix, deliberately free of the substring FU@ so a search
 for FU@ finds only file_utils messages. The line numbers are already correct.

I ran it here on CPython: 15 checks passed. I also broke file_utils five
 different ways, and the test failed each time. I have no board, so none of
 this has run on the Pico. I also haven’t run mypy on it.

On the board you should see three groups of expected error lines: one from the
 missing directory, two from the missing file, and one from the missing path in 
remove_subdir. If the Pico reports different file sizes than the test expects, 
the “list: contents” check will say so, and that would be a real finding.


"""


###
