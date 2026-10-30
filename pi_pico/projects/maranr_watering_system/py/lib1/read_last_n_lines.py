# read_last_n_lines.py
#
# Micropython function to read lines from the tail of a file (e.g., a log)

try: from typing import Callable
except ImportError: pass

# os module on MicroPython does not define these (unlike Py3)
SEEK_SET = 0  # relative to start of file
SEEK_CURR = 1  # relative to current file position
SEEK_END = 2  # relative to end of file

# Bytes read per step, small to save memory on the Pico.
# Tests change this ONLY via Z__set_chunk_size(); production code must never change it.
_CHUNK_SIZE = 128

# Allows redirecting the output of this module - mainly for testing. See Z__set_print().
def _PRINT(s:str) -> None:
    print(s)
_print: Callable[[str],None] = _PRINT


def read_last_n_lines(fpath: str, relative_line_number: int, number_of_lines: int,
                      show_blank_lines: bool = False) -> list[str]:
    """ Reads lines from the end of a text file efficiently in MicroPython.
    Arg relative_line_number is the line number of the first line
    being requested, relative to the end of the file.
    number_of_lines is the number of lines.
    So (1,1) gets the last line in the file,
    (10,2) gets the 10th and 9th lines from the end of file.
    Lines are returned in file order (oldest first).
    show_blank_lines: if False (the default), empty lines are ignored and not
    counted. If True, empty lines count like any other line and can be
    returned (as ""). The final newline of the file ends the last line, it
    does not start another one. A line holding only a CR (from a CRLF file)
    is not empty.
    Bytes that are not valid UTF-8 are replaced with U+FFFD which 
    precludes a UnicodeError.
    Returns [] if the file cannot be read.
    """
    if relative_line_number <= 0 or number_of_lines <= 0:
        return []
    try:
        with open(fpath, 'rb') as f:  # binary mode for reliable seeking
            f.seek(0, SEEK_END)
            position = f.tell()
            found = 0  # lines seen so far, counting from the end
            lines: list[str] = []  # the oldest number_of_lines of those, oldest first
            buf = b""
            at_end = True  # the next piece taken is the one at the very end of the file

            while position > 0 and found < relative_line_number:
                start = max(0, position - _CHUNK_SIZE)
                f.seek(start)
                buf = f.read(position - start) + buf
                position = start
                if position == 0:
                    buf = b"\n" + buf  # treat the start of the file as a newline

                while found < relative_line_number:
                    idx = buf.rfind(b"\n")
                    if idx < 0:
                        break  # the line continues in the previous chunk
                    line = buf[idx + 1:]
                    buf = buf[:idx]
                    # An empty piece at the very end of the file is only what follows
                    # the final newline, not a line. Any other empty piece is a blank line.
                    counts = bool(line) or (show_blank_lines and not at_end)
                    at_end = False
                    if counts:
                        lines.insert(0, line.decode('utf-8', 'replace'))
                        found += 1
                        if len(lines) > number_of_lines:
                            lines.pop()  # drop the newest, we want the older ones
            return lines
    except OSError as ex:
        _print(f"read_last_n_lines  EX={repr(ex)}  errno={ex.errno}")
        return []


def Z__set_chunk_size(new_chunk_size: int) -> int:
    # FOR TESTS ONLY - production code must never call this.
    # (Z__ prefix: grep for "Z_" in production code should find nothing.)
    # Sets the chunk size used by read_last_n_lines() and returns the OLD size,
    # so a test can put it back when it is finished.
    global _CHUNK_SIZE
    if new_chunk_size < 1:
        raise ValueError("chunk size must be 1 or more")
    old_chunk_size = _CHUNK_SIZE
    _CHUNK_SIZE = new_chunk_size
    return old_chunk_size

def Z__set_print(new_print: Callable[[str], None]) -> Callable[[str], None]:
    """ Replace the print output function with one the caller
    wants to use. Used mainly for testing.
    """
    global _print
    old_print = _print
    _print = new_print
    return old_print


# ----------------------------------------------------------------------
# COMMENTARY (not code): why the "if position == 0" block prepends a newline to buf
#
#     if position == 0:
#         buf = b"\n" + buf  # treat the start of the file as a newline
#
# This has nothing to do with numbering. Lines are counted from the end of
# the file, and `found` goes up by one for each line extracted.
# The prepended newline is there so the first line of the file can be
# extracted by the same code as every other line.
#
# The inner loop pulls out a line by finding the last \n in the buffer and
# taking everything after it. Every line except the first has a \n in front
# of it. The first line has nothing in front of it, so without help it would
# be left sitting in `buf` when the loop ended. The original code handled
# this with a separate block after the loop, and that block was the one
# with the `line`/`fbytes` bug.
#
# The prepended \n gives the first line a delimiter, so there is no special
# case. Example, with the file  a\nb\n :
#
#   1. After reading the whole file, buf is  \na\nb\n  once the newline is
#      added.
#   2. The last \n has nothing after it, so that empty "line" is skipped.
#   3. Next comes  b , which counts as 1 from the end.
#   4. Then  a , which counts as 2 from the end. The leading \n it was
#      waiting for is the one we added.
#
# It is added only when position == 0, meaning the read has reached the
# start of the file. At any other chunk boundary the buffer starts in the
# middle of a line, and adding a newline there would split that line in two.
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# COMMENTARY (not code): show_blank_lines, and the at_end flag
#
# The file  a\nb\n\n\nc\nd\n  asked for (4, 3), meaning start at the 4th
# line from the end and take 3 lines:
#
#   show_blank_lines=False (default): blank lines are dropped before
#       counting. From the end: d=1, c=2, b=3, a=4. Result: a, b, c.
#   show_blank_lines=True: the two blank lines are real lines.
#       From the end: d=1, c=2, ""=3, ""=4, b=5, a=6.
#       Result: "", "", c.
#
# The final \n of a file ends its last line, it does not start a new,
# empty one. So the first piece taken from the end of the file is empty
# when the file ends with a newline, and must never count as a blank
# line. `at_end` is True only for that first piece. After that, an empty
# piece is a real blank line (counted only when show_blank_lines is True).
# ----------------------------------------------------------------------

###
