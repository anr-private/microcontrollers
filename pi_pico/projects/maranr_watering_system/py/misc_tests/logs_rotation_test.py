# logs_rotation_test.py
#
# LINEMARKER=ZLOGSROT
#
# Test for creating log files repeatedly, verifying that as logs get
# created eventually the old ones get removed in order to keep
# the system filespace from being filled up / overwhelmed.
# This is a stand-alone test meant to be run like this:
#    - ensure that the Pico has the latest install for 
#      lib*/ and logger_embed_module/*
#    - copy this program to the Pico
#        - stop Thonny
#        - mpremote cp logs_rotation_test.py :
#    - use Thonny to run it
# NOTE the following does not work: the 'run' command of mpremote
# does not support any kind of keyboard input.
#    - mpremote run logs_removal_test.py


import os

s = input("Enter input")
print(f"{s=!r}")

from logger_embed_module.LemLogControl import LemLogControl, Z_replace_log_file_table

def main(args):
    print(f"ZLOGSROT$28 MAIN: {args=}")

if __name__ == "__main__":
    main(sys.argv[1:])


###
