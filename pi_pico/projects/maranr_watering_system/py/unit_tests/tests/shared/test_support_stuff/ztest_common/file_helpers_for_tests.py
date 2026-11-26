# file_helpers_for_tests.py
#
# Utilities and helpers for running (shared) tests.
# These operate identically on both platforms.
# For items that require platform-specific stuff,
# see cpython_glue.py and pico_glue.py.
# Because they can be used on both platforms, they are imported like this:
#   ztest_common.file_helpers_for_tests import read_a_file_as_string

import os

from lib1.file_utils import remove_subdir

def list_dir_names(dir_path: str) -> list[str] | None:
    """ Sorted names in the directory, or None if it cannot be listed. 
    Used for comparing the logs directory before and after a test
    (for example).
    """
    try:
        return sorted(os.listdir(dir_path))
    except OSError:
        return None

def read_a_file_as_string(fpath: str) -> str|None:
    """ Reads the file at fpath and returns
    entire content as is - one big string.
    Returns None if fails.
    """
    try:
        with open(fpath, "r", encoding="utf-8") as inf:
            data = inf.read()
            return data
    except Exception as ex:
        print(f"FHFT$34 read_a_file_as_string FAILED: '{fpath}' ex={ex}")
    return None


def read_a_file_as_lines(fpath: str) -> list[str] | None:
    """ Reads the file at fpath and returns
    entire content as is - one big string.
    Returns None if fails.
    """
    try:
        with open(fpath, "r", encoding="utf-8") as inf:
            # Handles both '\n' and '\r\n' line endings.
            data = inf.read().splitlines()
            return data
    except Exception as ex:
        print(f"FHFT$49 read_a_file_as_string FAILED: '{fpath}' ex={ex}")
    return None


def write_these_lines_to_file(lines: list[str], fpath: str) -> None:
    """ Write lines into a test file.
    Use remove_scratch_path() to remove the file when done.
    """
    try:
        with open(fpath, "w", encoding="utf-8") as outf:
            for line in lines:
                outf.write(line)
                outf.write("\n")
    except Exception as ex:
        print(f"FHFT$63 write_these_lines_to_file FAILED: '{fpath}' ex={ex}")
    return None


def create_subdir_with_files(subdir, fnames: list[str], min_file_size=0) \
                            -> tuple[ tuple[str, int],...  ]:
    # Create subdir with files in it such as log files
    # given a list of filenames plus a subdir into which they are created.
    # If min_file_size > 0, each file has fluff written to it until
    # its sizes reaches/exceeds this min.
    #
    # Returns a table of info about the files:
    # Each item in the table is:
    #   ("full/path/of/file", size-of-file-in-bytes)
    # The dir part of the  path is the 'subdir' arg.
    # The filenames are based on the 'fnames' arg.
    remove_subdir(subdir)
    os.mkdir(subdir)

    # Put a line in each file - each is unique.
    added_tail = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    j = 1
    file_items = []
    for log_fname in fnames:
        fpath: str = subdir + "/" + log_fname
        fsize: int = 0
        with open(fpath, "w") as outf:
            line = f"This is file {fpath:>45} {added_tail[:j]}\n"
            outf.write(line)
            fsize += len(line)
            j += 1

            ctr = 1
            while fsize < min_file_size:
                padline = f"{line} THIS IS A PADDING LINE {ctr=}\n"
                outf.write(padline)
                fsize += len(padline)
                ctr += 1

        finfo = (fpath, fsize)
        file_items.append(finfo)
    return tuple(file_items)





if __name__ == "__main__":
    """ quick tests """

    # expects this to be a file with 3 lines
    fpath = "./junk.txt"
    src_lines = ["Line 1", "Line 2", "Line 3"]
    src_stg = "\n".join(src_lines) + "\n"  # add the extra EOL
    write_these_lines_to_file(src_lines, fpath)

    got_stg = read_a_file_as_string(fpath)
    assert got_stg is not None
    print(f"As string: len={len(got_stg)}")
    print(f"  Content: '{got_stg}'")
    print(f"      src: '{src_stg}'")
    assert len(got_stg) == len(src_stg), f"'{len(got_stg)}' '{len(src_stg)}'"
    assert got_stg == src_stg

    got_lines = read_a_file_as_lines(fpath)
    assert got_lines is not None
    print(f"As lines: len={len(got_lines)}")
    print(f"Lines:...")
    for line in got_lines:
        print(f">>'{line}'<<")
    assert len(got_lines) == len(src_lines)
    assert got_lines == src_lines

    print(f"*** >>>  REMOVE THIS TEST FILE: '{fpath}'  <<< ***")

###
