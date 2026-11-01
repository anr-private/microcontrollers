# test_utils.py
#
# Shared test for lib1/utils.py

import os

from lib1.utils import seconds_to_hhmmss_string, seconds_to_hhmmss
from lib1.utils import string_to_int, show_cc
from lib1.utils import get_flash_space, convert_fs_space_to_string

from support.cpython_test_support import CpythonTestSupport


def test_seconds_to_hhmmss_string() -> None:
    total_secs = 1793501920
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "498194:58:40", s

    total_secs = 17935
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "04:58:55", s

    total_secs = 1978935
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "549:42:15", s

    total_secs = 0
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "00:00:00", s

    total_secs = 63
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "00:01:03", s

    total_secs = 5 + 60*3 + 60*60*4
    s = seconds_to_hhmmss_string(total_secs)
    assert s == "04:03:05", s


def test_seconds_to_hhmmss() -> None:
    total_secs = 1793501920
    v = seconds_to_hhmmss(total_secs)
    assert v == (498194,58,40), s

    total_secs = 17935
    v = seconds_to_hhmmss(total_secs)
    assert v == (4,58,55), v

    total_secs = 1978935
    v = seconds_to_hhmmss(total_secs)
    assert v == (549,42,15), v

    total_secs = 0
    v = seconds_to_hhmmss(total_secs)
    assert v == (0,0,0), v

    total_secs = 63
    v = seconds_to_hhmmss(total_secs)
    assert v == (0,1,3), v

    total_secs = 5 + 60*3 + 60*60*4
    v = seconds_to_hhmmss(total_secs)
    assert v == (4,3,5), v


def test_string_to_int() -> None:
    tests = (
        ("0", 0),
        ("-0", 0),
        ("+0", 0),
        ("@0", None),
        ("4839274", 4839274),
        )
    for stg, exp in tests:
        got = string_to_int(stg)
        assert exp == got, got


def test_show_cc() -> None:
    tests = (
        ("line 1", "line 1", 6),
        ("line2"+chr(10), "line2\\n", 7),
        ("line3"+chr(9), "line3\\t", 7),
        ("line4"+chr(7), "line4\\x07", 9),
        )

    for stg, exp_stg, exp_len in tests:
        got = show_cc(stg)
        assert len(got) == exp_len
        assert exp_stg == got, got
        if 0:
            print("")
            for x in got:
                print(f"{x} {ord(x)}")

def test_get_flash_space():
    # on shadow Ubunt 24.04, the actual is:
    #   exp_total_space = 1_966_736_678_912
    #print(f"@@T@ DIR cpython_test_support is {dir(cpython_test_support)}")
    #print(f"@@T@ DIR cpython_test_support.file is {cpython_test_support.__file__}")
    #from cpython_test_support import CpythonTestSupport
    cts = CpythonTestSupport.get_instance()
    faked_FS_total = 12345
    faked_FS_free  =   987
    cts.fake_total_FS_space = faked_FS_total
    cts.fake_free_FS_space = faked_FS_free

    got_total_space, got_free_space = get_flash_space()

    print(f"@@T@38  {got_total_space=}  {got_free_space=}")

    assert got_total_space == faked_FS_total
    assert got_free_space == faked_FS_free

def test_convert_fs_space_to_string():
    total_space = 12345678
    total_stg = convert_fs_space_to_string(total_space)
    print(f"@@T@34  {total_stg=}")
    exp_total_stg = '12,345,678 bytes, 12,056.33 KB, 11.77 MB'
    assert total_stg == exp_total_stg

    free_space = 987654
    free_stg = convert_fs_space_to_string(free_space)
    print(f"@@T@40  {free_stg=}")
    exp_free_stg = '987,654 bytes, 964.51 KB, 0.94 MB'
    assert free_stg == exp_free_stg


###
