# pico_test_read_last_n_lines.py
#
# On-device test for read_last_n_lines (MicroPython on the Pico; also runs on CPython).
#
# Setup: 1) edit the import line below if the function lives somewhere else
#           (for example: from file_utils import read_last_n_lines, Z__set_chunk_size)
#        2) copy this file to the Pico, or run it from the PC with:
#              mpremote run pico_test_read_last_n_lines.py
#        3) the output ends with RESULT: PASSED or RESULT: FAILED
#
# It writes a scratch file (TEST_PATH) to the Pico's flash and removes it at
# the end. It is kept to a few hundred writes to limit flash wear.
import os
import random

ok_flag = False
try:
    # This import is used on the PICO where lib1_FAKE simulates the
    # lib1/ package.
    from lib1_FAKE.read_last_n_lines import read_last_n_lines, Z__set_chunk_size   # <-- EDIT if needed
    TEST_PATH = "_rlnl_test.txt"
    ok_flag = True
except ImportError:
    print("Using lib1_FAKE: Failed to import the module that contains the read_last_n_lines, Z__set_chunk_size functions.")
try:
    # This imports the function from ./read_last_n_lines.py
    # It is used to run this test directly in the PICO repo dir:
    #   .../git/microcontrollers/pi_pico/projects/maranr_watering_system/py/pico_lib1_tests
    from read_last_n_lines import read_last_n_lines, Z__set_chunk_size   # <-- EDIT if needed
    TEST_PATH = "_rlnl_test.txt"
    ok_flag = True
except ImportError:
    print("From ./read_last_n_lines.py: Failed to import the module that contains the read_last_n_lines, Z__set_chunk_size functions.")
if not ok_flag:
    raise RuntimeError("Cannot find/import the module that contains the read_last_n_lines function")

###TEST_PATH = "._rlnl_test.txt"

RANDOM_CASES_PER_CHUNK = 60       # raise for a longer run
CHUNK_SIZES = (1, 3, 7, 100, 128)


def reference(data, rel, n, show_blank_lines):
    # Simple, obviously-correct version: read everything, split, slice.
    if rel <= 0 or n <= 0:
        return []
    pieces = data.split(b"\n")
    if data == b"" or data.endswith(b"\n"):
        pieces = pieces[:-1]            # what follows the final newline is not a line
    if not show_blank_lines:
        pieces = [p for p in pieces if p]
    wanted = pieces[-rel:]
    return [p.decode("utf-8") for p in wanted[:n]]


# (file bytes, rel, n, expected with show_blank_lines=False, expected with True)
# Expected values are written by hand.
FIXED = [
    (b"a\nb\nc\n", 1, 1, ["c"], ["c"]),
    (b"a\nb\nc\n", 2, 2, ["b", "c"], ["b", "c"]),
    (b"a\nb\nc\n", 3, 1, ["a"], ["a"]),             # reaches the FIRST line
    (b"a\nb\nc\n", 3, 2, ["a", "b"], ["a", "b"]),
    (b"a\nb\nc", 1, 1, ["c"], ["c"]),               # no trailing newline
    (b"a\nb\nc", 3, 3, ["a", "b", "c"], ["a", "b", "c"]),
    (b"only", 1, 1, ["only"], ["only"]),
    (b"only\n", 1, 1, ["only"], ["only"]),
    (b"a", 1, 1, ["a"], ["a"]),
    (b"first\nsecond", 2, 1, ["first"], ["first"]),
    (b"", 1, 1, [], []),                            # empty file
    (b"\n", 1, 1, [], [""]),                        # one blank line
    (b"\n\n\n", 1, 1, [], [""]),                    # only blank lines
    (b"\n\n\n", 3, 3, [], ["", "", ""]),
    (b"a\n\n", 1, 1, ["a"], [""]),                  # blank line is the last line
    (b"\na\n", 2, 2, ["a"], ["", "a"]),             # blank line is the first line
    (b"a\n\n\nb\n", 2, 2, ["a", "b"], ["", "b"]),   # blank lines in the middle
    (b"a\n\n\nb", 1, 1, ["b"], ["b"]),
    (b"a\n\n\nb", 4, 4, ["a", "b"], ["a", "", "", "b"]),
    (b"a\nb\n\n\nc\nd\n", 4, 3, ["a", "b", "c"], ["", "", "c"]),
    (b"a\r\nb\r\n", 1, 1, ["b\r"], ["b\r"]),        # CRLF keeps the \r
    (b"a\r\n\r\nb\r\n", 2, 1, ["\r"], ["\r"]),      # a CR-only line is not empty
    (b"a\nb\nc\n", 10, 2, ["a", "b"], ["a", "b"]),  # rel beyond file: oldest lines
    (b"a\nb\nc\n", 0, 1, [], []),
    (b"a\nb\nc\n", 1, 0, [], []),
    (b"\xc3\xa9\n\xe6\x97\xa5\xe6\x9c\xac\n", 2, 2, ["é", "日本"], ["é", "日本"]),
]

WORDS = ["a", "bb", "ccc", "line", "x" * 40, "é", "日本語", ""]


def random_file():
    out = []
    for _ in range(random.randint(0, 25)):
        words = [random.choice(WORDS) for _ in range(random.randint(0, 5))]
        line = " ".join(words)
        if random.random() < 0.2:
            line = ""                              # make sure there are blank lines
        out.append(line + random.choice(["\n", "\n", "\n", "\r\n"]))
    data = "".join(out).encode("utf-8")
    if data and random.random() < 0.4:
        data = data.rstrip(b"\r\n")            # no trailing newline
    return data


failures = []
total = 0


def check(label, data, rel, n, show, expected, chunk):
    global total
    total += 1
    with open(TEST_PATH, "wb") as f:
        f.write(data)
    try:
        got = read_last_n_lines(TEST_PATH, rel, n, show_blank_lines=show)
    except Exception as ex:
        got = "RAISED " + repr(ex)
    if got != expected:
        failures.append((label, chunk, show, data, rel, n, expected, got))


# the hand-written expected values must agree with the reference
for data, rel, n, exp_ignore, exp_show in FIXED:
    if reference(data, rel, n, False) != exp_ignore or reference(data, rel, n, True) != exp_show:
        print("TEST BUG: reference disagrees with the hand-written value for", data, rel, n)

random.seed(12345)
original_chunk = Z__set_chunk_size(CHUNK_SIZES[0])
for chunk in CHUNK_SIZES:
    Z__set_chunk_size(chunk)
    print("chunk size:", chunk)
    for data, rel, n, exp_ignore, exp_show in FIXED:
        check("fixed", data, rel, n, False, exp_ignore, chunk)
        check("fixed", data, rel, n, True, exp_show, chunk)
    for _ in range(RANDOM_CASES_PER_CHUNK):
        data = random_file()
        nlines = len(data.split(b"\n"))
        rel = random.randint(0, nlines + 3)
        n = random.randint(0, 5)
        show = random.choice([False, True])
        check("random", data, rel, n, show, reference(data, rel, n, show), chunk)
Z__set_chunk_size(original_chunk)

os.remove(TEST_PATH)

# Z__set_chunk_size: returns the old size, rejects sizes below 1
total += 1
before = Z__set_chunk_size(9)
again = Z__set_chunk_size(11)
rejected = []
for bad in (0, -5):
    try:
        Z__set_chunk_size(bad)
        rejected.append(False)
    except ValueError:
        rejected.append(True)
after = Z__set_chunk_size(before)       # puts the original back
if not (again == 9 and all(rejected) and after == 11):
    failures.append(("Z__set_chunk_size", None, None, b"", 0, 0,
                     "returns old size, rejects 0 and -5, unchanged by a rejected call",
                     "again=" + repr(again) + " rejected=" + repr(rejected) + " after=" + repr(after)))

print("Next: reading a file that does not exist, on purpose. The function should")
print("print ONE error line and return []. That is expected.")
total += 1
got = read_last_n_lines("/_does_not_exist_.txt", 1, 1)
print("(end of the expected error output)")
if got != []:
    failures.append(("missing file", None, None, b"", 1, 1, [], got))

print(total, "cases,", len(failures), "failures")
for item in failures[:5]:
    label, chunk, show, data, rel, n, expected, got = item
    print(" e.g.", label, "chunk=", chunk, "show_blank_lines=", show, "data=", data[:60], "rel=", rel, "n=", n)
    print("     expected:", expected)
    print("     got:     ", got)
print("RESULT: " + ("FAILED" if failures else "PASSED - all cases correct"))

###
