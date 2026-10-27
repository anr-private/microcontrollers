# test_read_last_n_lines.py
#
# Test for the read_last_n_lines() function
# Intended to be run using CPython 3 under Linux.
# There is a separate test for performing testing on the PICO.

import importlib.util
import os
import random
import sys
import tempfile

DEFAULT_MODULE_PATH = "lib1_FAKE/read_last_n_lines.py"

HELP_INFO=f"""Tests for read_last_n_lines, run on CPython (Ubuntu python3).

Usage:
    python3 test_read_last_n_lines.py path/to/module_with_the_function.py
 OR
    python3 test_read_last_n_lines.py 
The no-parameter version uses a hard-coded path to the module:
   '{DEFAULT_MODULE_PATH}'

The module must define read_last_n_lines(fpath, relative_line_number, number_of_lines).
If it also has a module-level _CHUNK_SIZE, the tests repeat with several chunk
sizes (1, 2, 3, 7, ...), which exercises chunk boundaries and UTF-8 characters
split across chunks.

Behavior being checked (the function's docstring, plus the existing behavior):
  - relative_line_number = position of the first wanted line, counted from the
    end of the file (1 = last line); number_of_lines = how many to return.
  - result is in file order (oldest first)
  - empty lines are ignored and not counted
  - if relative_line_number is larger than the number of lines in the file,
    the oldest number_of_lines lines of the file are returned
  - unreadable file -> []
"""


def load(path):
    spec = importlib.util.spec_from_file_location("module_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reference(data: bytes, rel: int, n: int) -> list[str]:
    """Simple, obviously-correct version: read everything, split, slice."""
    if rel <= 0 or n <= 0:
        return []
    lines = [ln for ln in data.split(b"\n") if ln]
    wanted = lines[-rel:]          # last `rel` lines (all of them if fewer)
    return [ln.decode("utf-8") for ln in wanted[:n]]


# (file bytes, rel, n, expected) - expected values written by hand
FIXED = [
    (b"a\nb\nc\n", 1, 1, ["c"]),
    (b"a\nb\nc\n", 2, 2, ["b", "c"]),
    (b"a\nb\nc\n", 3, 1, ["a"]),                # reaches the FIRST line
    (b"a\nb\nc\n", 3, 2, ["a", "b"]),
    (b"a\nb\nc", 1, 1, ["c"]),                  # no trailing newline
    (b"a\nb\nc", 3, 3, ["a", "b", "c"]),
    (b"only", 1, 1, ["only"]),                  # single line, no newline
    (b"only\n", 1, 1, ["only"]),
    (b"first\nsecond", 2, 1, ["first"]),        # first line, no newline in tail
    (b"", 1, 1, []),                            # empty file
    (b"\n\n\n", 1, 1, []),                      # only blank lines
    (b"a\n\n\nb\n", 2, 2, ["a", "b"]),          # blank lines are not counted
    (b"a\r\nb\r\n", 1, 1, ["b\r"]),             # CRLF keeps the \r
    (b"a\nb\nc\n", 10, 2, ["a", "b"]),          # rel beyond the file: oldest lines
    (b"a\nb\nc\n", 0, 1, []),
    (b"a\nb\nc\n", 1, 0, []),
    (b"\xc3\xa9\n\xe6\x97\xa5\xe6\x9c\xac\n", 2, 2, ["é", "日本"]),
]


def random_file(rng: random.Random) -> bytes:
    words = ["a", "bb", "ccc", "line", "x" * 40, "é", "日本語", "\U0001F600", ""]
    out = []
    for _ in range(rng.randint(0, 40)):
        line = " ".join(rng.choice(words) for _ in range(rng.randint(0, 6)))
        out.append(line + rng.choice(["\n", "\n", "\n", "\r\n"]))
    data = "".join(out).encode("utf-8")
    if data and rng.random() < 0.4:
        data = data.rstrip(b"\r\n")        # no trailing newline
    return data


def main(module_path: str) -> int:
    mod = load(module_path)
    fn = mod.read_last_n_lines
    has_chunk = hasattr(mod, "_CHUNK_SIZE")
    chunk_sizes = [1, 2, 3, 7, 16, 100, 128] if has_chunk else [None]
    failures = []
    total = 0
    rng = random.Random(12345)

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "t.txt")

        def check(label, data, rel, n, expected, chunk):
            nonlocal total
            total += 1
            with open(path, "wb") as f:
                f.write(data)
            try:
                got = fn(path, rel, n)
            except Exception as ex:             # noqa
                got = f"RAISED {type(ex).__name__}: {ex}"
            if got != expected:
                failures.append((label, chunk, data, rel, n, expected, got))

        for chunk in chunk_sizes:
            if chunk is not None:
                mod._CHUNK_SIZE = chunk
            for data, rel, n, expected in FIXED:
                check("fixed", data, rel, n, expected, chunk)
                assert reference(data, rel, n) == expected, ("reference disagrees with hand value", data, rel, n)
            for _ in range(1500):
                data = random_file(rng)
                nlines = len([x for x in data.split(b"\n") if x])
                rel = rng.randint(0, nlines + 3)
                n = rng.randint(0, 6)
                check("random", data, rel, n, reference(data, rel, n), chunk)

        # missing file -> []
        print("Next: reading a file that does not exist on purpose. The function should")
        print("print ONE error line (FileNotFoundError) and return []. That is expected.")
        total += 1
        got = fn(os.path.join(tmp, "does_not_exist.txt"), 1, 1)
        print("(end of the expected error output)\n")
        if got != []:
            failures.append(("missing file", None, b"", 1, 1, [], got))

    print(f"{module_path}: {total} cases, {len(failures)} failures")
    kinds = {}
    for label, chunk, data, rel, n, expected, got in failures:
        key = "RAISED " + got.split(":")[0].split()[1] if isinstance(got, str) else "WRONG RESULT"
        kinds[key] = kinds.get(key, 0) + 1
    for k, v in sorted(kinds.items()):
        print(f"   {v:6d}  {k}")
    for label, chunk, data, rel, n, expected, got in failures[:5]:
        print(f"   e.g. [{label}, chunk={chunk}] data={data[:60]!r} rel={rel} n={n}")
        print(f"        expected={expected!r}")
        print(f"        got     ={got!r}")
    print("RESULT: " + ("FAILED" if failures else "PASSED - all cases correct"))
    return 1 if failures else 0


if __name__ == "__main__":
    print(f"MAIN: sys.argv is {sys.argv}")
    module_path = None
    if len(sys.argv) == 2:
        module_path = sys.argv[1]
    elif len(sys.argv) == 1:
        print(f"NO MODULE PATH PARAMETER SPECIFIED: ASSUMING {DEFAULT_MODULE_PATH=}")
        module_path = DEFAULT_MODULE_PATH
    else:
        print(HELP_INFO)
        sys.exit(2)
    sys.exit(main(module_path))

###
