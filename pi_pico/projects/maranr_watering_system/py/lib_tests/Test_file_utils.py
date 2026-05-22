# Test_file_utils.py
#
# Runs under both python3 and micropython
#
# Detects presence of pytest to determine which platform is present
#
# Use 'pytest -s' to see stdout
# Use 'pytest -v' to see more details
# Use pytest TestExamples.py::TestExamples::test_one   to run just that test

try:
    import pytest  # py3
except ImportError:
    pytest = None   # micropython

import os
import sys


# mimics the micropython inclusion of ':/lib' on its path
sys.path.append("./lib")
from lib.file_utils import read_last_n_lines, remove_subdir
from lib.file_utils import filter_dir_contents, list_dir_contents



class Test_file_utils:

    def setup_method(self):
        print("setup method call")

 
    def test_read_last_n_lines_1(self):
        fpath = "test_files/fifty_lines.txt"

        relative_line_number = 10
        nlines = 10
        lines = read_last_n_lines(fpath, relative_line_number, nlines)

        print(f"Result is {type(lines)}")
        assert len(lines) == nlines, f"len(lines)={len(lines)}  {nlines=}"
        exp_first_line = f"This is line {50-relative_line_number+1}"
        exp_last_line = f"This is line {50-relative_line_number+nlines}"
        assert exp_first_line == "This is line 41"
        assert exp_last_line == "This is line 50"
        got_first_line = lines[0]
        got_last_line = lines[-1]
        print(f"@@T@48 exp-first: {exp_first_line}")
        print(f"@@T@49 got-first: {got_first_line}")
        print(f"@@T@50 exp-last:  {exp_last_line}")
        print(f"@@T@51 exp-last:  {got_last_line}")
        assert got_first_line == exp_first_line
        assert got_last_line == exp_last_line


    def test_read_last_n_lines_2(self):
        fpath = "test_files/fifty_lines.txt"

        relative_line_number = 10
        nlines = 5
        lines = read_last_n_lines(fpath, relative_line_number, nlines)

        print(f"Result is {len(lines)=}")
        print(f"@@T@64  {lines[0]=}")
        print(f"@@T@65  {lines[-1]=}")

        assert len(lines) == nlines
        exp_first_line = f"This is line {50-relative_line_number+1}"
        exp_last_line = f"This is line {50-relative_line_number+nlines}"
        got_first_line = lines[0]
        got_last_line = lines[-1]
        print(f"@@T@72 exp-first: {exp_first_line}")
        print(f"@@T@73 got-first: {got_first_line}")
        print(f"@@T@74 exp-last:  {exp_last_line}")
        print(f"@@T@75 got-last:  {got_last_line}")
        assert got_first_line == exp_first_line
        assert got_last_line == exp_last_line
 

    def test_read_last_n_lines_3(self):
        fpath = "test_files/fifty_lines.txt"

        relative_line_number = 10
        nlines = 1
        lines = read_last_n_lines(fpath, relative_line_number, nlines)

        print(f"Result is {len(lines)=}")
        print(f"@@T@88  {lines[0]=}")
        print(f"@@T@89  {lines[-1]=}")

        assert len(lines) == nlines
        exp_first_line = f"This is line {50-relative_line_number+1}"
        exp_last_line = f"This is line {50-relative_line_number+nlines}"
        got_first_line = lines[0]
        got_last_line = lines[-1]
        print(f"@@T@96 exp-first: {exp_first_line}")
        print(f"@@T@97 got-first: {got_first_line}")
        print(f"@@T@98 exp-last:  {exp_last_line}")
        print(f"@@T@99 got-last:  {got_last_line}")
        assert got_first_line == exp_first_line
        assert got_last_line == exp_last_line


    def test_remove_subdir(self):
        ...
        subdir = "test__remove_subdir"

        exp_items = {
            "mws_log.010": ("mws_log.010", "f", 51),
            "mws_log.011": ("mws_log.011", "f", 52),
            "mws_log.012": ("mws_log.012", "f", 53),
        }
        fnames = tuple(exp_items.keys())
        print(f"@@T@114  fnames: {fnames}")

        _create_test_subdir(subdir, fnames)

        
        items = list_dir_contents(subdir)
        assert len(items) == len(exp_items)
        del items

        remove_subdir(subdir)

        items = list_dir_contents(subdir)
        assert len(items) == 0, f"got={len(items)} exp=ZERO"
        del items



    def test_list_dir_contents(self):
        ...
        subdir = "test__list_dir_contents"

        exp_items = {
            "mws_log.010": ("mws_log.010", "f", 51),
            "mws_log.011": ("mws_log.011", "f", 52),
            "mws_log.012": ("mws_log.012", "f", 53),
        }
        fnames = tuple(exp_items.keys())
        print(f"@@T@141  fnames: {fnames}")

        _create_test_subdir(subdir, fnames)

        items = list_dir_contents(subdir)

        assert len(items) == len(exp_items), f"@@@"

        for j, item in enumerate(items):
            print(f"@@T@150 file-item {j=} is {item}")
            fname = item[0]
            exp_item = exp_items.get(fname)
            assert item == exp_item, f"{j=}"


    def test_filter_dir_contents(self):

        subdir = "test__filter_dir_contents"

        upy_fix = 1
        exp_items = {
            "mws_log.001": ("mws_log.001", "f", 53,   1),
            "mws_log.010": ("mws_log.010", "f", 54,  10),
            "mws_log.011": ("mws_log.011", "f", 55,  11),
            "mws_log.012": ("mws_log.012", "f", 56,  12),
            "mws_log.250": ("mws_log.250", "f", 57, 250),
        }
        # Keep the fnames in order - else _create_test_subdir()
        # writes different lines into each file under py vs upy.
        fnames = list(sorted(exp_items.keys()))
        # add some junk
        fnames.extend([ "mws_log.txt", "mws_log.0250", "mws_log.26", 
                        "mws_log.000", ###"mws_log.999",
                        "mws_log.1000", "mws_log.0100",
                        "other.txt", "another.txt", "no-extention",
                        "has.extra.dots.txt"])
        print(f"@@T@177  fnames: {fnames}")

        _create_test_subdir(subdir, fnames)

        def is_3_digit_int(s):
            if not  s: return None
            if len(s) != 3: return None
            try:
                ival = int(s)
            except (TypeError, ValueError):
                return None
            if ival <= 0 or ival > 999: return None
            return ival


        def _file_filt(fname, ftype, fsize):
            # returns None to exclude the file
            print(f"@@T@194  _file_filt  {fname=}  {ftype=}  {fsize=} " )
            if ftype != "f": return None
            #
            parts = fname.rsplit('.',1)
            print(f"@@@@ parts {parts}")
            if len(parts) != 2: return None
            #
            fpart    = parts[0]
            ext_part = parts[1]
            #
            if fpart != "mws_log": return None
            ext_val = is_3_digit_int(ext_part)
            print(f"@@T@206   extension is_3_digit_int('{ext_part}') is {ext_val}")
            if ext_val is None: return None
            return ext_val

        got_items = filter_dir_contents(subdir, _file_filt)

        print(f"@@T@212 filtered-got_items = {got_items}")

        assert len(got_items) == len(exp_items)

        for got_item in got_items:
            got_fname = got_item[0]
            got_ftype = got_item[1]
            got_fsize = got_item[2]
            got_ext_val = got_item[3]

            exp_item = exp_items[got_fname]
            assert got_fname == exp_item[0], got_item
            assert got_ftype == exp_item[1], got_item
            assert got_fsize == exp_item[2], f"{exp_item=} {got_item=}"
            assert got_ext_val == exp_item[3], got_item


def _create_test_subdir(subdir, fnames):
    remove_subdir(subdir)
    os.mkdir(subdir)

    added_tail = "ABCDEFGHIJKL"
    j = 1
    for log_fname in fnames:
        fpath = subdir + "/" + log_fname
        with open(fpath, "w") as outf:
            line = f"This is file {fpath} {added_tail[:j]}\n"
            outf.write(line)
            j += 1


#def test_standalone_func():
#    assert "pytest".upper() == "PYTEST"
if pytest is None:
    # running under micropython

    def test_1():
        print("===  TEST 1   ================================================")
        t = Test_file_utils()
        t.test_remove_subdir()
        print("===  end of TEST 1   ================================================\n")
    
    
    def test_2():
        print("===  TEST 2   ================================================")
        t = Test_file_utils()
        t.test_list_dir_contents()
        print("===  end of TEST 2   ================================================\n")
    
    
    def test_3():
        print("===  TEST 3   ================================================")
        t = Test_file_utils()
        t.test_filter_dir_contents()
        print("===  end of TEST 3   ================================================\n")
    
    
    def test_4():
        print("===  TEST 4   ================================================")
        t = Test_file_utils()
        t.test_read_last_n_lines_1()
        print("===  end of TEST 4   ================================================\n")
    
    
    def test_5():
        print("===  TEST 5   ================================================")
        t = Test_file_utils()
        t.test_read_last_n_lines_2()
        print("===  end of TEST 5   ================================================\n")
    
    
    def test_6():
        print("===  TEST 6   ================================================")
        t = Test_file_utils()
        t.test_read_last_n_lines_3()
        print("===  end of TEST 6   ================================================\n")
    
    
    def main():
        print("MAIN @@T@291 starting -- RUNNING UNDER MICROPYTHON ---")
        test_1()
        test_2()
        test_3()
        test_4()
        test_5()
        test_6()
        
        print("MAIN @@T@299 finished")
        
    main()


### end ###
