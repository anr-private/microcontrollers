# test_utils.py
#
# Shared test for lib1/utils.py

import os

from lib1.utils import seconds_to_hhmmss_string, seconds_to_hhmmss
from lib1.utils import format_number_with_commas, string_to_int, show_cc

# CPython only
try: from cpython_test_support import CpythonTestSupport
except ImportError: pass

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
    assert v == (498194,58,40), v

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


def test_format_number_with_commas() -> None:
    tests = (
        (1.0,        2,  "1.00"),
        (1.01,       2,  "1.01"),
        (1.99,       2,  "1.99"),
        (1.999,      2,  "2.00"),
        (12056.33,   2,  "12,056.33"),
        (0,          2,  "0.00"),
        (5,          2,  "5.00"),
        (999.999,    2,  "1,000.00"),
        (1000,       2,  "1,000.00"),
        (99999.99,   2,  "99,999.99"),
        (1234567,    2,  "1,234,567.00"),
        (-1234.5,    2,  "-1,234.50"),
        (-0.001,     2,  "0.00"),
        (-0.00,      2,  "0.00"),
        )
    
    for float_value, decimal_places, exp_stg in tests:
        got_stg = format_number_with_commas(float_value, decimal_places)
        assert exp_stg == got_stg, f"'{exp_stg}', '{got_stg}'"


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

###
