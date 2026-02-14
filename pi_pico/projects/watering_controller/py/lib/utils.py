# utils.py

import os
import platform
import sys

DEBUG = True

def dbg(stg=None):
    """ output a string to the debug output """
    if not DEBUG: return
    if stg is None: stg = ""
    print(f"DBG:{stg}")

def string_to_int(s):
    try:
        return int(s)
    except (ValueError,TypeError) as ex:
        dbg(f"string_to_int  NOT AN INT: '{s}'  ex={ex}")
        return None
    except Exception  as ex:
        dbg(f"string_to_int  UNKNOWN EXCEPTION: '{s}'  ex={ex}")
        return None

#@@@@@@@@@@@@@ NEED TO FIX. SHOULD NOT ADD EOLs
def FIXTHIS___make_mesg_stg_from_template(template_mesg_lines, values={}):
    """ Create a string that contains an HTTP mesg using 
    a list of lines (ie strings) as the input.
    The values arg is a dict of substition values.
    Each line of the template is processed like this:
        actual_line = template_line % values
    So the template lines can contain '%(value_name)s' items.
    """
    ###print(f"make_mesg_stg_from_template templet is {type(template_mesg_lines)}   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$444")
    ###for line in template_mesg_lines:
    ###    print(f"MAKE MESG STG $$$$$$$$$$$$$ LINE is {line}")
    actual_lines = []
    for line in template_mesg_lines:
        line = line % values
        actual_lines.append(line) 
    # add the HTTP separator
    stg = "\r\n".join(actual_lines)
    # add the terminator marker
    stg = stg + "\r\n\r\n"
    dbg(f"create_mesg_stg  mesg stg len={len(stg)}")
    return stg



def dump_received_mesg(mesg_stg, who=""):
    """ """
    if mesg_stg is None:
        print(f"--- RECEIVED MESG is NULL !!!  {who}  ---------------------")
        return

    print(f"--- RECVD  len={len(mesg_stg)} ---  {who}  --------------------------------------------")
    s = []
    lno = 0
    for ch in mesg_stg:
        if ch == "\n":
            s.append("\\n")
            lno += 1
            line = "".join(s)
            print(f" {lno}.  {line}")
            s = []
        elif ch == "\r":
            s.append("\\r")
        else:
            s.append(ch)
    if len(s) > 0:
        line = "".join(s)
        print(" Partial line: '{line}'")

    print("------------------------------------------------------------")


def dump_bytes(byte_vals, who=""):
    """ """
    if byte_vals is None:
        print(f"___ dump bytes __ len is ZERO!!!   ___ {who} ______________________")
        return

    print(f"----- dump bytes  len={len(byte_vals)}    {who}   --------------------")
    s = []
    for bv in byte_vals:
        v = int(bv)
        if v == ord("\n"):
            s.append("\\n")
            line = "".join(s)
            print(line)
            s = []
        elif v == ord("\r"):
            s.append("\\r")
        elif v < ord(" ") or v >=127:
            s.append(f"[{v}]")
        else:
            s.append(chr(v))
    if len(s) > 0:
        line = "".join(s)
        print(f" PARTIAL LINE: {line}")
    print(f"----------------------------------  {who} -------------")


def determine_py_platform():
    """ returns "micropython", "cpython" """
    if "micropython" in platform.platform().lower():
        return "micropython"
    return "cpython"


def determine_machine_type():
    """ Returns one of these:
    "pi pico w"   Pi PICO-W
     "unknown"
    """
    
    os_uname = os.uname()

    raw_machine_name_lc = os_uname[4].lower()
    if "pi pico w" in raw_machine_name_lc:
        return = "pi pico w"
    return "unknown"

### end ###
