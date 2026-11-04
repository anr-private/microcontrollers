# file_helpers_for_tests.py
#
# Utilities and helpers for running tests.
# These operate identically on both platforms.
# For items that require platform-specific stuff,
# see cpython_glue.py and pico_glue.py.

import os

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
        print(f"FHFT@21 read_a_file_as_string FAILED: '{fpath}' ex={ex}")
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
        print(f"FHFT@21 read_a_file_as_string FAILED: '{fpath}' ex={ex}")
    return None


def write_these_lines_to_file(lines: list[str], fpath: str) -> None:
    try:
        with open(fpath, "w", encoding="utf-8") as outf:
            for line in lines:
                outf.write(line)
                outf.write("\n")
    except Exception as ex:
        print(f"FHFT@44 write_these_lines_to_file FAILED: '{fpath}' ex={ex}")
    return None

        
def remove_this_test_file(fpath: str) -> None:
    if os.path.exists(fpath):
        os.remove(fpath)


if __name__ == "__main__":
    """ quick tests """

    # expects this to be a file with 3 lines
    fpath = "./junk.txt"
    src_lines = ["Line 1", "Line 2", "Line 3"]
    src_stg = "\n".join(src_lines) + "\n"  # add the extra EOL
    write_these_lines_to_file(src_lines, fpath)

    got_stg = read_a_file_as_string(fpath)
    print(f"As string: len={len(got_stg)}")
    print(f"  Content: '{got_stg}'")
    print(f"      src: '{src_stg}'")
    assert len(got_stg) == len(src_stg), f"'{len(got_stg)}' '{len(src_stg)}'"
    assert got_stg == src_stg

    got_lines = read_a_file_as_lines(fpath)
    print(f"As lines: len={len(got_lines)}")
    print(f"Lines:...")
    for line in got_lines:
        print(f">>'{line}'<<")
    assert len(got_lines) == len(src_lines)
    assert got_lines == src_lines

    remove_this_test_file(fpath)

###
