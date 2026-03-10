# test_file_utils.py
#
# You can run this either locally on the linux system by
# opening this file in Thonny and then running it.
# (That is the easiest way)
#
# Or you can copy the file to the Pico, go to the Pico's remote files/dirs
# window, double-click it (downloads it back into Thonny), and then run
# it in Thonny.

import sys

from lib.FileUtils import FileUtils


def create_a_text_file(fpath):
    with open(fpath, "w") as f:
        for i in range(1, 21):
            f.write(f"This is line {i}.\n")


def test1():
    fpath = "file_20_lines.txt"
    create_a_text_file(fpath)

    fu = FileUtils()

    
    print(f"\nTest 1: Read the last 5 lines")
    print("  Expect lines 16..20")
    last_lines = fu.read_last_n_lines(fpath, 5, 999)
    print("Last 5 lines:")
    for line in last_lines:
        print(line.strip())

    print(f"\nTest 2: Read 5 lines, start 10 lines from the end of file")
    print(f"  Expect lines 10-14")    
    # Read the last 5 lines starting at 10 lines from the end
    last_lines = fu.read_last_n_lines(fpath, 10, 5)
    print("Last 5 lines:")
    for line in last_lines:
        print(line.strip())


    print(f"\nTest 3: Read 1 line, start 12 lines from the end of file")
    print(f"  Expect line 8")    
    # Read the last 5 lines starting at 10 lines from the end
    last_lines = fu.read_last_n_lines(fpath, 12, 1)
    print("Last 5 lines:")
    for line in last_lines:
        print(line.strip())


def main(*args):
    test1()


if __name__ == "__main__":
    main(sys.argv[1:])




###
