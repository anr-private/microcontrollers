# utils.py

###@@@@ REMOVE import micropython
import os
import platform
import sys
import time

try: from typing import Any
except ImportError: pass

# try:
    # import time
# except ModuleNotFoundError:
    # import utime as time
#### @@@ TODO remove the above

# if "micropython" in platform.platform().lower():
    # PLATFORM : str = "micropython"
# else:
    # PLATFORM : str = "cpython"
#@@@@ TODO REMOVE THE ABOVE

MWS_CONFIG = {
    "btn_left_gpio":     15,
    "btn_right_gpio":    21,
    "btn_up_gpio":       14,
    "btn_down_gpio":     22,
    "btn_center_gpio":   20,
    "btn_upper_left_gpio":  19,
    "btn_lower_left_gpio":  17,
    "btn_upper_right_gpio": 18,
    "btn_lower_right_gpio": 16,

    "lcd1602_sda_pin": 2,
    "lcd1602_scl_pin": 3,

    "log_file_path":  "mws_log.txt",
    }
#TODO ADD table for daylight savings time changes

#@@@ TODO REMOVE THIS
def junk(s:str, i:int, f:float):
    if s is None: return [s,i,f]
    if i > 100: return [i,s,f]
    if f < -10.0: return [f,i,s]
    return [f,i,None]


def seconds_to_hhmmss_string(total_secs: int) -> str:
    hhmmss = seconds_to_hhmmss(total_secs)
    hours = hhmmss[0]
    mins = hhmmss[1]
    secs = hhmmss[2]
    stg = f"{hours:02d}:{mins:02d}:{secs:02d}"
    return stg

def seconds_to_hhmmss(total_secs: int) -> tuple[int, int, int]:
    # converts secs to hours,mins,seconds
    # For use with counters that count seconds,
    # NOT FOR USE with date-time expressed as seconds
    ###minutes = total_secs // 60
    ###s = total_secs - minutes*60
    ###hours = minutes // 60
    ###m = minutes - hours * 60 
    ###return (hours, m, s)
    minutes, secs = divmod(total_secs, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, secs


def format_number_with_commas(float_value: float, decimal_places: int) -> str:
    """ Format float_value with comma thousands separators and
    `decimal_places` decimal places,
    like '{:,.2f}' in CPython. 
    Rounds once; works the same on MicroPython.
    Why this is needed: MicroPython cannot handle ',' in a float format;
    it just ignores it (it's a bug).
    """
    factor = 10 ** decimal_places
    scaled = int(round(abs(float_value) * factor))     # whole number of 1/factor units
    whole, fraction = divmod(scaled, factor)

    digits = str(whole)
    groups: list[str] = []
    while len(digits) > 3:
        groups.insert(0, digits[-3:])
        digits = digits[:-3]
    groups.insert(0, digits)
    text = ",".join(groups)

    if decimal_places > 0:
        fraction_stg = str(fraction)
        text += "." + "0" * (decimal_places - len(fraction_stg)) + fraction_stg
    if float_value < 0 and scaled != 0:   # do not produce '-0.00'
        text = "-" + text
    return text


def string_to_int(s: str) -> int|None:
    try:
        return int(s)
    except (ValueError,TypeError) as ex:
        print(f"UTILS@65 string_to_int  NOT AN INT: '{s}'  ex={ex}")
        return None
    #@@@ TODO remove the below
    #except Exception  as ex:
    #    print(f"UTILS@68 string_to_int  UNKNOWN EXCEPTION: '{s}'  ex={ex}")
    #    return None

def _show_char(ch: str) -> str:
    # for one character: return its printable form
    if ch == "\r": return "\\r"
    if ch == "\n": return "\\n"
    if ch == "\t": return "\\t"
    if ord(ch) < 32 or ord(ch) == 127:
        return f"\\x{ord(ch):02x}"
    return ch

def show_cc(line: str | None) -> str:
    # Show control characters as visible text (\r, \n, \t, or \xNN)
    if line is None: return ""
    parts = [_show_char(ch) for ch in line]
    return "".join(parts)


def len_to_str(item: Any) -> str:
    # return as str the length of an object like a string or list 
    try:
        return str(len(item))
    except Exception as ex:
        return f"len(ITEM)-FAILED {item=} {ex=}"
len_to_string=len_to_str


def determine_py_platform() -> str:
    # returns "micropython" or "cpython"  (some systems: "pypy", or something else)
    return sys.implementation.name


def determine_machine_type() -> str:
    # Returns::
    # "pi pico w" for Pi PICO-W
    # "pi pico 2 w" for Pi PICO2-W
    # Else "unknown"

    os_uname = os.uname()

    #@@@@ TODO REMOVE   raw_machine_name_lc = os_uname[4].lower()
    raw_machine_name_lc = os_uname.machine.lower()
    if "pi pico w" in raw_machine_name_lc:
        return "pi pico w"
    if "pi pico 2 w" in raw_machine_name_lc:
        return "pi pico 2 w"
    return "unknown"


def main() -> None:
    print(f"UTILS@199 NOT YET")

if __name__ == "__main__":
    main()

### end ###
