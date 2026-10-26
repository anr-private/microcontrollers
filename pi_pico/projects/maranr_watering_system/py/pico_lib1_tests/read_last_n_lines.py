# os module on MicroPython does not define these (unlike Py3)
SEEK_SET = 0  # relative to start of file
SEEK_CURR = 1  # relative to current file position
SEEK_END = 2  # relative to end of file

_CHUNK_SIZE = 128  # bytes read per step, small to save memory on the Pico


def read_last_n_lines(fpath: str, relative_line_number: int, number_of_lines: int) -> list[str]:
    """ Reads lines from the end of a text file efficiently in MicroPython.
    Arg relative_line_number is the line number of the first line
    being requested, relative to the end of the file.
    number_of_lines is the number of lines.
    So (1,1) gets the last line in the file,
    (10,2) gets the 10th and 9th lines from the end of file.
    Lines are returned in file order (oldest first).
    Empty lines are ignored and not counted.
    Returns [] if the file cannot be read.
    """
    if relative_line_number <= 0 or number_of_lines <= 0:
        return []
    try:
        with open(fpath, 'rb') as f:  # binary mode for reliable seeking
            f.seek(0, SEEK_END)
            position = f.tell()
            found = 0  # non-empty lines seen so far, counting from the end
            lines: list[str] = []  # the oldest number_of_lines of those, oldest first
            buf = b""

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
                    if line:
                        lines.insert(0, line.decode('utf-8'))
                        found += 1
                        if len(lines) > number_of_lines:
                            lines.pop()  # drop the newest, we want the older ones
            return lines
    except OSError as ex:
        print(f"FU read_last_n_lines  EX={repr(ex)}  errno={ex.errno}")
        return []
