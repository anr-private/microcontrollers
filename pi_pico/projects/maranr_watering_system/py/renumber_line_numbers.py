# renumber_line_numbers.py


import os
import sys

HELP="""
Usage:  py  renumber_line_numbers.py  SOMEFILE.py  'marker'
The 'marker' is something like '"FU@' where this is the
string after which are found the source line numbers such as
   print(f"FU@37:{w} USE SIMULATED FILE PATHS  ")
Marker    ----
Any digits after the marker are deleted and replaced with the 
source code line number of the line 1..N.

"""


# count how many lines fixed
NUM_FIXED = 0

def dbg(stg=""):
    if 0:
        print(stg)

def renumber_line_numbers(fpath, out_fpath, bkup_fpath, marker):
    lines = read_file(fpath)
    print(f"Read {fpath=}  numlines={len(lines)}")

    lines = remove_eols(lines)

    write_file(bkup_fpath, lines)

    lines = fix_line_numbers(lines, marker)

    write_file(out_fpath, lines)


def read_file(fpath):
    with open(fpath, "r") as inf:
        lines = inf.readlines()
    return lines

def write_file(out_fpath, lines):
    numlines = 0
    with open(out_fpath, 'w') as outf:
        for line in lines:
            outf.write(line + '\n')
            numlines += 1
    print(f"Wrote {out_fpath=}  numlines={numlines}")


def fix_line_numbers(lines, marker):

    ###marker = "\"FU@"

    newlines = []
    lnum = 0
    for line in lines:
        lnum += 1
        #dbg(f" {lnum} {line}")

        ###dbg(f"@@@ fix this {lnum} {line}")
        new_line = fix_one_line(lnum, line, marker)
        if marker in new_line:
            dbg(f"@@@   fixed '{new_line}'")
        newlines.append(new_line)
    return newlines


def fix_one_line(lnum, line, marker):
    global NUM_FIXED

    if marker not in line: return line
    dbg()
    dbg(f"@@@ fix this {lnum} {line} marker='{marker}' ")

    pos = line.find(marker)
    head_end = pos + len(marker)
    head = line[0:head_end]
    dbg(f" HEAD '{head}'")

    raw_tail = line[head_end:]
    dbg(f"  RAWTAIL '{raw_tail}'")

    tail = strip_leading_digits(raw_tail)
    dbg(f"  TAIL '{tail}'")

    new_line = head + f"{lnum}" + tail

    NUM_FIXED += 1
    dbg(f"@@@@@@@@@@@@@@@@@@ num fixed {NUM_FIXED}")

    return new_line


def strip_leading_digits(stg):
    if len(stg) <= 0: return stg
    
    while len(stg) > 0:
        ch = stg[0]
        if ord(ch) < ord('0') or ord(ch) > ord('9'):
            dbg(f"@@@@@@@@@@ not a digit - stop! {ch=}  stg='{stg}' ")
            break
        stg = stg[1:]
        dbg(f"@@@@@@@@ stg is now '{stg}'")
    return stg


def remove_eols(lines):
    new_lines = []
    for line in lines:
        if len(line) > 0:
            if line[-1] == "\n":
                line = line[0:-1]
        new_lines.append(line)
    return new_lines

def main(args):
    dbg(f"MAIN {args=}")

    if "help" in args[0]:
        print(HELP)
        sys.exit(1)

    fpath = args[0]
    out_fpath = fpath + ".out"
    bkup_fpath = fpath + ".bak"

    marker = args[1]
    dbg(f"  MARKER: '{marker}'")

    renumber_line_numbers(fpath, out_fpath, bkup_fpath, marker)

if __name__ == "__main__":
    main(sys.argv[1:])

###
