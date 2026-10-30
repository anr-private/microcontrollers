# test_read_last_n_lines.py
#
# Tests for the read_last_n_lines() function.
# Intended to be run using CPython 3 under Linux.
# There is a separate test (pico_test_read_last_n_lines.py) for running on the Pico.
#
# This test currently is run like this:
#     python3 test_read_last_n_lines.py
# It assumes the read_last_n_lines.py is in the same dir as this test.
#
# The tests change the chunk size via Z__set_chunk_size() (tests only), which
# exercises chunk boundaries and UTF-8 characters split across chunks.
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
#   - unreadable file -> []
#   - Z__set_chunk_size() returns the old size and rejects sizes below 1
import os
import random
import sys
import tempfile

from lib1.read_last_n_lines import read_last_n_lines, Z__set_chunk_size, Z__set_print
print("Imported successfully the function(s) from lib1/read_last_n_lines.py")

CHUNK_SIZES = (1, 2, 3, 7, 16, 100, 128)
RANDOM_CASES_PER_CHUNK = 1500

class CapturesPrint:
    """ Capture printed output from the function being tested """
    def __init__(self):
        self.captured: list[str] = []

    def print(self, s:str) -> None:
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


def create_random_data(rng: random.Random) -> bytes:
    words = ["a", "bb", "ccc", "line", "x" * 40, "é", "日本語", "\U0001F600", ""]
    out = []
    for _ in range(rng.randint(0, 40)):
        line = " ".join(rng.choice(words) for _ in range(rng.randint(0, 6)))
        if rng.random() < 0.2:
            line = ""                              # make sure there are blank lines
        out.append(line + rng.choice(["\n", "\n", "\n", "\r\n"]))
    data = "".join(out).encode("utf-8")
    if data and rng.random() < 0.4:
        data = data.rstrip(b"\r\n")        # no trailing newline
    return data


"""
old_chunk = Z__set_chunk_size(CHUNK_SIZES[0])   # sets it and returns the old one
try: ...
finally:
    Z__set_chunk_size(old_chunk)
"""


def perform_test() -> int:
    """ """
    
    # save the original chunk size - restore below, so multiple uses
    # of the package in different tests can be done
    # (We don't use the size we are setting - it's arbitrary but
    #  must not be a 'bad' value like 0 or -1 etc.)
    original_chunk_size = Z__set_chunk_size(CHUNK_SIZES[0])

    # capture 'print' from the function
    capturesPrint = CapturesPrint()
    old_print = Z__set_print(capturesPrint.print)

    try:
        result = do_perform_test(capturesPrint)
    finally:
        Z__set_print(old_print)
        Z__set_chunk_size(original_chunk_size)
    return result


def do_perform_test(capturesPrint: CapturesPrint) -> int:
    """ """
    
    failures = []
    total = 0
    rng = random.Random(12345)

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "t.txt")

        def run_test_case(label, data, rel, n, show, expected, chunk):
            nonlocal total
            total += 1
            with open(path, "wb") as f:
                f.write(data)
            try:
                got = read_last_n_lines(path, rel, n, show_blank_lines=show)
            except Exception as ex:             # noqa
                got = f"RAISED {type(ex).__name__}: {ex}"
            if got != expected:
                failures.append((label, chunk, show, data, rel, n, expected, got))

        # Verify the test data:
        # the hand-written expected values must agree with the reference data
        for data, rel, n, exp_ignore, exp_show in FIXED:
            assert create_reference_data(data, rel, n, False) == exp_ignore, ("reference disagrees", data, rel, n, False)
            assert create_reference_data(data, rel, n, True) == exp_show, ("reference disagrees", data, rel, n, True)

        for chunk in CHUNK_SIZES:
            Z__set_chunk_size(chunk)
            for data, rel, n, exp_ignore, exp_show in FIXED:
                run_test_case("fixed", data, rel, n, False, exp_ignore, chunk)
                run_test_case("fixed", data, rel, n, True, exp_show, chunk)
            for _ in range(RANDOM_CASES_PER_CHUNK):
                data = create_random_data(rng)
                nlines = len(data.split(b"\n"))
                rel = rng.randint(0, nlines + 3)
                n = rng.randint(0, 6)
                for show in (False, True):
                    run_test_case("random", data, rel, n, show, 
                                  create_reference_data(data, rel, n, show), chunk)
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
                             f"{again=} {rejected=} {after=}"))

        # missing file -> []
        print("TRLNL@195: Try to read a file that does not exist.")
        print("TRLNL@196: It should print ONE error line (FileNotFoundError) and return [].")
        total += 1
        assert len(capturesPrint.captured) == 0
        got = read_last_n_lines(os.path.join(tmp, "does_not_exist.txt"), 1, 1)
        assert len(capturesPrint.captured) == 1
        print(f"TRLNL@201: Captured print: {capturesPrint.captured=}")
        assert "FileNotFoundError" in capturesPrint.captured[0]
        if got != []:
            failures.append(("missing file", None, None, b"", 1, 1, [], got))

    print(f"TRLNL@206: {total} cases, {len(failures)} failures")
    for label, chunk, show, data, rel, n, expected, got in failures[:5]:
        print(f"TRLNL@208:    e.g. [{label}, chunk={chunk}, show_blank_lines={show}] data={data[:60]!r} rel={rel} n={n}")
        print(f"TRLNL@209:         expected={expected!r}")
        print(f"TRLNL@210:         got     ={got!r}")
    print("TRLNL@211: RESULT: " + ("FAILED" if failures else "PASSED - all cases correct"))
    return 1 if failures else 0


def main() -> int:
    """ """
    return perform_test()


if __name__ == "__main__":
    sys.exit(main())

###
