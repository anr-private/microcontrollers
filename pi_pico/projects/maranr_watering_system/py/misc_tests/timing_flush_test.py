# timing_flush_test.py

import os
import time

LINE_COUNT = 200
ONE_LINE = "x" * 80


def time_the_writes(flush_each_line: bool, flush_every_N:int) -> int:
    logf = open("junk_flush_test.txt", "w")
    ctr = 0
    start_ms = time.ticks_ms()
    for _ in range(LINE_COUNT):
        logf.write(ONE_LINE + "\n")

        do_flush = False
        if flush_every_N:
            ctr += 1
            if ctr >= flush_every_N:
                ctr = 0
                do_flush = True

        if do_flush or flush_each_line:
            logf.flush()
    logf.close()
    return time.ticks_diff(time.ticks_ms(), start_ms)


print("flush each line:", time_the_writes(True, 0), "ms for", LINE_COUNT, "lines")
print("no flush:       ", time_the_writes(False, 0), "ms for", LINE_COUNT, "lines")
print("flush every 10: ", time_the_writes(False, 10), "ms for", LINE_COUNT, "lines")
os.remove("junk_flush_test.txt")

###

