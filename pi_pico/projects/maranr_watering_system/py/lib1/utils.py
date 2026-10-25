# utils.py

import micropython
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
try:
    import gc
    _ = gc.mem_free
except Exception as ex:
    print(f"UTILS@15 utils.py  CANNOT IMPORT MICROPYTHON VERSION of 'gc' !!!!!")
    del gc   
    #                       # 'type ignore' is for mypy                         
    import gc_FAKE as gc    # type: ignore
    print(f"UTILS@18 utils.py  USING FAKE VERSION OF 'gc'  !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#@@@@@@@@@@ TODO fake the GC using CpythonTestSupport  see TestElemLogControl.py

# if "micropython" in platform.platform().lower():
    # PLATFORM : str = "micropython"
# else:
    # PLATFORM : str = "cpython"
#@@@@ TODO REMOVE THE ABOVE

# "micropython" or "cpython"
PLATFORM = sys.implementation.name
if PLATFORM == "cpython":   # Py3
    from cpython_test_support import CpythonTestSupport   # type:ignore
    cpyt = CpythonTestSupport.get_instance()              # type:ignore 
    GET_FLASH_SPACE = cpyt.fake_get_flash_space           # type:ignore
else:
    # use the 'real' filespace info
    GET_FLASH_SPACE = None

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

# def show_cc(line: str|None) -> str:
    # # convert line to a new line, replacing all control chars with visible rep 
    # if line is None: line = ""
    # chars = []
    # for ch in line:
        # if ch == "\r":
            # chars.append("\\r")
        # elif ch == "\n":
            # chars.append("\\n")
        # elif ch == "\t":
            # chars.append("\\t")
        # else:
            # chars.append(ch)
    # return "".join(chars)
#
# def show_cc(line: str | None) -> str:
    # # Show control characters as visible text (\r, \n, \t, or \xNN)
    # if line is None: return ""
    # names = {"\r": "\\r", "\n": "\\n", "\t": "\\t"}
    # return "".join(names.get(ch) or (f"\\x{ord(ch):02x}" if ord(ch) < 32 or ord(ch) >= 127 else ch)
                   # for ch in line)


#@@@@ TODO REMOVE
# def show_len(item):
    # # return as str the length of an object like a string or list 
    # try:
        # return str(len(item))
    # except Exception as ex:
        # return f"ITEM-HAS-NO-LEN {item=} {ex=}"


def len_to_str(item: Any) -> str:
    # return as str the length of an object like a string or list 
    try:
        return str(len(item))
    except Exception as ex:
        return f"len(ITEM)-FAILED {item=} {ex=}"
len_to_string=len_to_str

def gc_collect():
    # per https://docs.micropython.org/en/latest/reference/constrained.html#the-heap
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())


def get_memory_status_string(do_garbage_collect:bool=False) -> str:
    ### # prints memory map of block usage
    ###micropython.mem_info(1)
    if do_garbage_collect: gc.collect()
    return f" {gc.mem_alloc()=}   {gc.mem_free()=}"


def get_flash_space() -> tuple[int,int]:

    if  GET_FLASH_SPACE is not None:
        print(f"UTILS@109 Using FAKE for get_flash_space(): {GET_FLASH_SPACE} ")
        return GET_FLASH_SPACE()

    # Get filesystem statistics for the root directory ("/")
    # On uPy it is os.statvfs("/"); on CPy it uses faker CpythonTestSupport
    print(f"UTILS@114 Using 'real' filespace info")
    stat = os.statvfs("/")

    # Block size
    block_size = stat[0]
    # Total number of blocks
    total_blocks = stat[2]
    # Number of free blocks available to unprivileged user
    free_blocks = stat[3]

    # Calculate total and free space in bytes
    total_space = block_size * total_blocks
    free_space = block_size * free_blocks

    return total_space, free_space


def convert_fs_space_to_string(fs_space: int) -> str:
    # Convert to KB and MB for easier reading
    KB = 1024
    MB = 1024 * KB

    # Total space ex:  868,352 bytes, 848.00 KB, 0.83 MB
    # Free space ex:   507,904 bytes, 496.00 KB, 0.48 MB
    return f"{fs_space:,} bytes, {(fs_space/KB):,.2f} KB, {(fs_space/MB):.2f} MB"

def get_fs_space_string(sep:str="") -> str:
    ts, fs = get_flash_space()
    tss = convert_fs_space_to_string(ts)
    fss = convert_fs_space_to_string(fs)
    return f"TOTAL SPACE {tss}   {sep}FREE SPACE {fss}"


def determine_py_platform() -> str:
    # returns "micropython" or "cpython"  (some systems: "pypy", or something else)
    return sys.implementation.name
#@@@@ TODO REMOVE BELOW:
# def determine_py_platform() -> str:
    # # returns "micropython", "cpython" 
    # if "micropython" in platform.platform().lower():
        # return "micropython"
    # return "cpython"


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
    print(f"UTILS@173 FS SPACE: {get_fs_space_string()}")
    print(f"UTILS@174 MEMORY: {get_memory_status_string()} ")

if __name__ == "__main__":
    main()

### end ###
