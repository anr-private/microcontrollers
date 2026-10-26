# On-device test for read_last_n_lines (MicroPython on the Pico; also runs on CPython).
#
# Setup: 1) edit the import line below so `mod` is the module that contains
#           read_last_n_lines (for example: import file_utils as mod)
#        2) copy this file to the Pico, or run it from the PC with:
#              mpremote run pico_test_read_last_n_lines.py
#        3) the output ends with RESULT: PASSED or RESULT: FAILED
#
# It writes a scratch file (TEST_PATH) to the Pico's flash and removes it at
# the end. It is kept to a few hundred writes to limit flash wear.
import os
import random

try:
    import lib1_FAKE.read_last_n_lines as mod   # <-- EDIT: the module that has read_last_n_lines
    TEST_PATH = "_rlnl_test.txt"
except ImportError:
    print("Failed to import the module that contains the read_last_n_lines function")

###TEST_PATH = "._rlnl_test.txt"

RANDOM_CASES_PER_CHUNK = 60       # raise for a longer run
CHUNK_SIZES = (1, 3, 7, 100, 128)  # used only if the module has _CHUNK_SIZE

fn = mod.read_last_n_lines


def reference(data, rel, n):
    # Simple, obviously-correct version: read everything, split, slice.
    if rel <= 0 or n <= 0:
        return []
    lines = [ln for ln in data.split(b"\n") if ln]
    wanted = lines[-rel:]
    return [ln.decode("utf-8") for ln in wanted[:n]]


# (file bytes, rel, n, expected) - expected values written by hand
FIXED = [
    (b"a\nb\nc\n", 1, 1, ["c"]),
    (b"a\nb\nc\n", 2, 2, ["b", "c"]),
    (b"a\nb\nc\n", 3, 1, ["a"]),               # reaches the FIRST line
    (b"a\nb\nc\n", 3, 2, ["a", "b"]),
    (b"a\nb\nc", 1, 1, ["c"]),                 # no trailing newline
    (b"a\nb\nc", 3, 3, ["a", "b", "c"]),
    (b"only", 1, 1, ["only"]),
    (b"only\n", 1, 1, ["only"]),
    (b"first\nsecond", 2, 1, ["first"]),
    (b"", 1, 1, []),                           # empty file
    (b"\n\n\n", 1, 1, []),                     # only blank lines
    (b"a\n\n\nb\n", 2, 2, ["a", "b"]),         # blank lines not counted
    (b"a\r\nb\r\n", 1, 1, ["b\r"]),            # CRLF keeps the \r
    (b"a\nb\nc\n", 10, 2, ["a", "b"]),         # rel beyond file: oldest lines
    (b"a\nb\nc\n", 0, 1, []),
    (b"a\nb\nc\n", 1, 0, []),
    (b"\xc3\xa9\n\xe6\x97\xa5\xe6\x9c\xac\n", 2, 2, ["é", "日本"]),
]

WORDS = ["a", "bb", "ccc", "line", "x" * 40, "é", "日本語", ""]


def random_file():
    out = []
    for _ in range(random.randint(0, 25)):
        words = [random.choice(WORDS) for _ in range(random.randint(0, 5))]
        out.append(" ".join(words) + random.choice(["\n", "\n", "\n", "\r\n"]))
    data = "".join(out).encode("utf-8")
    if data and random.random() < 0.4:
        data = data.rstrip(b"\r\n")            # no trailing newline
    return data


failures = []
total = 0


def check(label, data, rel, n, expected, chunk):
    global total
    total += 1
    with open(TEST_PATH, "wb") as f:
        f.write(data)
    try:
        got = fn(TEST_PATH, rel, n)
    except Exception as ex:
        got = "RAISED " + repr(ex)
    if got != expected:
        failures.append((label, chunk, data, rel, n, expected, got))


random.seed(12345)
chunks = CHUNK_SIZES if hasattr(mod, "_CHUNK_SIZE") else (None,)
for chunk in chunks:
    if chunk is not None:
        mod._CHUNK_SIZE = chunk
    print("chunk size:", chunk)
    for data, rel, n, expected in FIXED:
        check("fixed", data, rel, n, expected, chunk)
    for _ in range(RANDOM_CASES_PER_CHUNK):
        data = random_file()
        nlines = len([x for x in data.split(b"\n") if x])
        rel = random.randint(0, nlines + 3)
        n = random.randint(0, 5)
        check("random", data, rel, n, reference(data, rel, n), chunk)

os.remove(TEST_PATH)

print("Next: reading a file that does not exist, on purpose. The function should")
print("print ONE error line and return []. That is expected.")
total += 1
got = fn("/_does_not_exist_.txt", 1, 1)
print("(end of the expected error output)")
if got != []:
    failures.append(("missing file", None, b"", 1, 1, [], got))

print(total, "cases,", len(failures), "failures")
for item in failures[:5]:
    label, chunk, data, rel, n, expected, got = item
    print(" e.g.", label, "chunk=", chunk, "data=", data[:60], "rel=", rel, "n=", n)
    print("     expected:", expected)
    print("     got:     ", got)
print("RESULT: " + ("FAILED" if failures else "PASSED - all cases correct"))
