# ZLemLogFileTable.py
#
# LINEMARKER=ZZ_LLFT

V = False

class ZLemLogFileTable:
    # Fake for LemLogFileTable

    def __init__(self, verbose=False):
        """ """
        self._lines: list[str] = list()
        self._closed = False
        global V
        V = verbose

    def log_one_line(self, line):
        if self._closed:
            raise RuntimeError(f"ZZ_LLFT$19 LOGGING IS CLOSED but log_one_line was called {line=!r}")
        if V:print(f"ZZ_LLFT$20 LOG-ONE-LINE: {line!r}")
        self._lines.append(line)

    def close_logging(self) -> None:
        if V:print(f"ZZ_LLFT$24 CLOSE LOGGING")
        self._closed = True

    def get_lines_from_log_file(self, relative_line_number: int, 
                                      number_of_lines: int) -> list[str]:
        # get lines from the log file
        # relative_line_number is the line number of the first line
        # being requested, relative to the end of the file.
        # number_of_lines is the number of lines
        # So (1,1) gets the last line in the file,
        # (10,2) gets the 10th and 9th lines from the end of file.
        # lines = read_last_n_lines(self._current_log_fpath,
                                  # relative_line_number,
                                  # number_of_lines)

        if V:print(f"ZZ_LLFT$39 {relative_line_number=} {number_of_lines=}")
        start_idx = len(self._lines) - relative_line_number
        end_idx = start_idx + number_of_lines
        if V:print(f"ZZ_LLFT$42  {start_idx=}  {end_idx=}  len(lines)={len(self._lines)}")
        lines = self._lines[start_idx:end_idx]
        return lines

    #=== UNIT TEST SUPPORT  ===================================

    def z_num_lines(self):
        return len(self._lines)

    def z_get_lines(self) -> list[str]:
        return list(self._lines)

    def z_get_latest_line(self) -> str:
        # get the most recently logged line else marker
        if not self._lines: 
            return  "-- ZLemLogFileTable NO RECENTLY LOGGED LINE --"
        return self._lines[-1]

###
