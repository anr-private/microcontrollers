# timing_flush_test.py

import os
import time

LINE_COUNT = 200
ONE_LINE = "x" * 80

FILL_DIR = "junk_fill"
FILL_FILE_BYTES = 16384
RESERVE_BLOCKS = 40


def count_free_blocks() -> int:
    return os.statvfs("/")[3]


def fill_the_filesystem() -> int:
    try:
        os.mkdir(FILL_DIR)
    except OSError:
        pass
    one_kb = b"y" * 1024
    file_count = 0
    while count_free_blocks() > RESERVE_BLOCKS:
        with open(f"{FILL_DIR}/fill_{file_count:04d}.bin", "wb") as fillf:
            for _ in range(FILL_FILE_BYTES // 1024):
                fillf.write(one_kb)
        file_count += 1
    return file_count


def remove_the_fill() -> None:
    for name in os.listdir(FILL_DIR):
        os.remove(f"{FILL_DIR}/{name}")
    os.rmdir(FILL_DIR)

def time_with_full_filesystem():
    try:
        print("fill files created:", fill_the_filesystem(), " free blocks:", count_free_blocks())
        print("flush each line:", time_the_writes(True, 0), "ms for", LINE_COUNT, "lines")
        print("flush every 10: ", time_the_writes(False, 10), "ms for", LINE_COUNT, "lines")
        print("flush every 50: ", time_the_writes(False, 50), "ms for", LINE_COUNT, "lines")
    finally:
        remove_the_fill()

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

if 0:
    print("flush each line:", time_the_writes(True, 0), "ms for", LINE_COUNT, "lines")
    print("no flush:       ", time_the_writes(False, 0), "ms for", LINE_COUNT, "lines")
    print("flush every  10: ", time_the_writes(False, 10), "ms for", LINE_COUNT, "lines")
    print("flush every  50: ", time_the_writes(False, 50), "ms for", LINE_COUNT, "lines")
    print("flush every 100: ", time_the_writes(False, 100), "ms for", LINE_COUNT, "lines")

if 1:
    time_with_full_filesystem()

###

