# timing_flush_test.py

import os
import time

LINE_COUNT = 200
ONE_LINE = "x" * 80


def time_the_writes(flush_each_line: bool) -> int:
    logf = open("junk_flush_test.txt", "w")
    start_ms = time.ticks_ms()
    for _ in range(LINE_COUNT):
        logf.write(ONE_LINE + "\n")
        if flush_each_line:
            logf.flush()
    logf.close()
    return time.ticks_diff(time.ticks_ms(), start_ms)


print("flush each line:", time_the_writes(True), "ms for", LINE_COUNT, "lines")
print("no flush:       ", time_the_writes(False), "ms for", LINE_COUNT, "lines")
os.remove("junk_flush_test.txt")

###

