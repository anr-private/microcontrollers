# Basic multi thread example - runs 2 threads, each printing digits
#
# 

from time import sleep # should use utime
import _thread


def core0_thread():
    counter = 0
    while True:
        print(counter)
        counter += 2
        sleep(1)


def core1_thread():
    counter = 1
    while True:
        print(counter)
        counter += 2
        sleep(2)


second_thread = _thread.start_new_thread(core1_thread, ())

core0_thread()

###
