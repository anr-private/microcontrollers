# test_read_last_n_lines.py
#
# Shared test for lib1/read_last_n_lines.py. It runs
#   - on the PC under pytest (CPython), and
#   - on the Pico: run_pico_tests.py appends tests/pico/pico_glue.py to a copy of
#     this file and sends it with `mpremote run`.
# Plain test_ functions with plain asserts: no pytest import. Every assert has a
# message with the values, because MicroPython shows no more than the message.
#
# Behavior being checked (the function's docstring, plus the existing behavior):
#   - relative_line_number = position of the first wanted line, counted from the
#     end of the file (1 = last line); number_of_lines = how many to return.
#   - result is in file order (oldest first)
#   - show_blank_lines=False (default): empty lines are ignored and not counted
#   - show_blank_lines=True: empty lines count like any other line; the final
#     newline of the file does not start another line
#   - a line holding only a CR (from CRLF) is NOT empty, in either mode
#   - if relative_line_number is larger than the number of lines in the file,
#     the oldest number_of_lines lines of the file are returned
#   - bytes that are not valid UTF-8 are replaced, never an exception
#   - unreadable file -> [] and ONE message through the print hook (errno=2 here)
#   - Z__set_chunk_size() returns the old size and rejects sizes below 1
# The tests change the chunk size via Z__set_chunk_size() (tests only), which
# exercises chunk boundaries and UTF-8 characters split across chunks.
import os
import random
import sys

from lib1.read_last_n_lines import read_last_n_lines, Z__set_chunk_size, Z__set_print

# CPython: the real module tests/cpython/cpython_glue.py.
# Pico: there is no such module; run_pico_tests.py appends get_scratch_path().
try: from cpython_glue import get_scratch_path
except ImportError: pass

# Only the NUMBERS differ by platform: every case writes a file, and the Pico's flash
# should not be worn out. Behavior being tested is the same.
_ON_MICROPYTHON = sys.implementation.name == "micropython"
CHUNK_SIZES = (1, 3, 7, 100, 128) if _ON_MICROPYTHON else (1, 2, 3, 7, 16, 100, 128)
RANDOM_CASES_PER_CHUNK = 60 if _ON_MICROPYTHON else 1500
RANDOM_SEED = 12345
SCRATCH_NAME = "rlnl.txt"

# (file bytes, rel, n, expected with show_blank_lines=False, expected with True)
# Expected values are written by hand.
FIXED = [
    (b"a\nb\nc\n", 1, 1, ["c"], ["c"]),
    (b"a\nb\nc\n", 2, 2, ["b", "c"], ["b", "c"]),
    (b"a\nb\nc\n", 3, 1, ["a"], ["a"]),             # reaches the FIRST line
    (b"a\nb\nc\n", 3, 2, ["a", "b"], ["a", "b"]),
    (b"a\nb\nc", 1, 1, ["c"], ["c"]),               # no trailing newline
    (b"a\nb\nc", 3, 3, ["a", "b", "c"], ["a", "b", "c"]),
    (b"only", 1, 1, ["only"], ["only"]),            # single line, no newline
    (b"only\n", 1, 1, ["only"], ["only"]),
    (b"a", 1, 1, ["a"], ["a"]),
    (b"first\nsecond", 2, 1, ["first"], ["first"]),  # first line, no newline in tail
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
    (b"a\nb\nc\n", 10, 2, ["a", "b"], ["a", "b"]),  # rel beyond the file: oldest lines
    (b"a\nb\nc\n", 0, 1, [], []),
    (b"a\nb\nc\n", 1, 0, [], []),
    (b"\xc3\xa9\n\xe6\x97\xa5\xe6\x9c\xac\n", 2, 2, ["é", "日本"], ["é", "日本"]),
]

WORDS = ["a", "bb", "ccc", "line", "x" * 40, "é", "日本語", ""]
#if not _ON_MICROPYTHON:
WORDS.append("\U0001F600")      # a 4-byte character

class CapturesPrint:
    """ Capture printed output from the function being tested """
    def __init__(self) -> None:
        self.captured: list[str] = []

    def print(self, s: str) -> None:
        self.captured.append(s)


def create_reference_data(data: bytes, rel: int, n: int, show_blank_lines: bool) -> list[str]:
    """ Does the same thing as the read_last_n_lines() function.
    It's a simpler, obviously-correct version: read everything, split, slice.
    """
    if rel <= 0 or n <= 0:
        return []
    pieces = data.split(b"\n")
    if data == b"" or data.endswith(b"\n"):
        pieces = pieces[:-1]            # what follows the final newline is not a line
    if not show_blank_lines:
        pieces = [p for p in pieces if p]
    wanted = pieces[-rel:]              # last `rel` lines (all of them if fewer)
    return [p.decode("utf-8") for p in wanted[:n]]


def create_random_data() -> bytes:
    """ A random file: up to 40 lines, some blank, LF or CRLF, maybe no final newline. """
    out = []
    for _ in range(random.randint(0, 40)):
        line = " ".join([random.choice(WORDS) for _ in range(random.randint(0, 6))])
        if random.random() < 0.2:
            line = ""                              # make sure there are blank lines
        out.append(line + random.choice(["\n", "\n", "\n", "\r\n"]))
    data = "".join(out).encode("utf-8")
    if data and random.random() < 0.4:
        data = data.rstrip(b"\r\n")                # no trailing newline
    return data


def read_lines_of_data(data: bytes, rel: int, n: int, show_blank_lines: bool) -> object:
    """ Write `data` to the scratch file and read it back with read_last_n_lines().
    Returns the list of lines, or a string saying what exception was raised. """
    path = get_scratch_path(SCRATCH_NAME)
    with open(path, "wb") as f:
        f.write(data)
    try:
        return read_last_n_lines(path, rel, n, show_blank_lines=show_blank_lines)
    except Exception as ex:
        return "RAISED " + repr(ex)


def remove_scratch_file() -> None:
    try:
        os.remove(get_scratch_path(SCRATCH_NAME))
    except OSError:
        pass


def test_reference_agrees_with_fixed_cases() -> None:
    # The hand-written expected values and create_reference_data() must agree,
    # otherwise it is the test that is wrong.
    for data, rel, n, exp_ignore, exp_show in FIXED:
        assert create_reference_data(data, rel, n, False) == exp_ignore, ("TEST BUG", data, rel, n, False)
        assert create_reference_data(data, rel, n, True) == exp_show, ("TEST BUG", data, rel, n, True)


def test_fixed_cases() -> None:
    failures = []
    old_chunk = Z__set_chunk_size(CHUNK_SIZES[0])
    try:
        for chunk in CHUNK_SIZES:
            Z__set_chunk_size(chunk)
            for data, rel, n, exp_ignore, exp_show in FIXED:
                for show, expected in ((False, exp_ignore), (True, exp_show)):
                    got = read_lines_of_data(data, rel, n, show)
                    if got != expected:
                        failures.append((chunk, show, data, rel, n, expected, got))
    finally:
        Z__set_chunk_size(old_chunk)
        remove_scratch_file()
    # each failure: (chunk, show_blank_lines, data, rel, n, expected, got)
    assert not failures, (len(failures), failures[:5])


def test_random_cases() -> None:
    random.seed(RANDOM_SEED)
    failures = []
    old_chunk = Z__set_chunk_size(CHUNK_SIZES[0])
    try:
        for chunk in CHUNK_SIZES:
            Z__set_chunk_size(chunk)
            for _ in range(RANDOM_CASES_PER_CHUNK):
                data = create_random_data()
                rel = random.randint(0, len(data.split(b"\n")) + 3)
                n = random.randint(0, 6)
                show = random.choice([False, True])
                expected = create_reference_data(data, rel, n, show)
                got = read_lines_of_data(data, rel, n, show)
                if got != expected:
                    failures.append((chunk, show, data[:60], rel, n, expected, got))
    finally:
        Z__set_chunk_size(old_chunk)
        remove_scratch_file()
    assert not failures, (len(failures), failures[:5])


def test_invalid_utf8_is_replaced() -> None:
    old_chunk = Z__set_chunk_size(CHUNK_SIZES[0])
    try:
        for chunk in (1, 3, 128):
            Z__set_chunk_size(chunk)
            # one bad byte in the middle of the file
            got = read_lines_of_data(b"a\n\xff\nb\n", 3, 3, False)
            assert got == ["a", "�", "b"], (chunk, got)
            # a character cut short (power loss) at the end of the file. How many
            # replacement characters it becomes may differ by platform: not checked.
            got = read_lines_of_data(b"ok\n\xe6\x97", 2, 2, False)
            assert isinstance(got, list) and len(got) == 2 and got[0] == "ok", (chunk, got)
            assert len(got[1]) >= 1 and set(got[1]) == {"�"}, (chunk, got)
    finally:
        Z__set_chunk_size(old_chunk)
        remove_scratch_file()


def test_set_chunk_size() -> None:
    # returns the old size, rejects sizes below 1 and leaves the size unchanged then
    before = Z__set_chunk_size(9)
    try:
        again = Z__set_chunk_size(11)
        rejected = []
        for bad in (0, -5):
            try:
                Z__set_chunk_size(bad)
                rejected.append(False)
            except ValueError:
                rejected.append(True)
        after = Z__set_chunk_size(before)       # puts the original back, returns 11
    finally:
        Z__set_chunk_size(before)
    assert again == 9, again
    assert rejected == [True, True], rejected
    assert after == 11, after


def test_missing_file_prints_one_message_and_returns_empty() -> None:
    capture = CapturesPrint()
    old_print = Z__set_print(capture.print)
    try:
        before = list(capture.captured)
        got = read_last_n_lines(get_scratch_path("does_not_exist.txt"), 1, 1)
    finally:
        Z__set_print(old_print)
    assert before == [], before
    assert got == [], got
    assert len(capture.captured) == 1, capture.captured
    assert "errno=2" in capture.captured[0], capture.captured

###
