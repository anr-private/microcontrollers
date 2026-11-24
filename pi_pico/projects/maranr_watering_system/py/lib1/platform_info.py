# platform_info.py
#
# LINEMARKER=PLTFRMINFO

import os
import sys

USING_MICROPYTHON = (sys.implementation.name == "micropython")
USING_CPYTHON     = (sys.implementation.name == "cpython")

USING_PICO_HARDWARE = (sys.platform == "rp2")
USING_PICO2_HARDWARE = (USING_PICO_HARDWARE and ("RP2350" in os.uname().machine))
USING_LINUX_HARDWARE = (sys.platform == "linux")

# ** NOTE **
# USING_PICO_HARDWARE is true on Pico, Pico W, Pico 2, Pico 2 W
# USING_PICO2_HARDWARE is specific to the Pico 2, Pico 2 W

# ** NOTE **
# Do not use sys.version or sys.version_info to decide capabilities.
# On PICO 2 W, sys.version is '3.4.0; MicroPython v1.29.0 on 2026-08-24'
# regardless of what syntax MicroPython actually accepts - it has some
# capabilities from later versions of Python. Instead use a try/except
# on an import or on a call, or use the symbols above.

if __name__ == "__main__":
    print(f"USING_MICROPYTHON = {USING_MICROPYTHON}")
    print(f"USING_CPYTHON = {USING_CPYTHON}")
    print(f"USING_PICO_HARDWARE = {USING_PICO_HARDWARE}")
    print(f"USING_PICO2_HARDWARE = {USING_PICO2_HARDWARE}")
    print(f"USING_LINUX_HARDWARE = {USING_LINUX_HARDWARE}")

# OUTPUT:
#   PICO 2 W:
#     USING_MICROPYTHON = True
#     USING_CPYTHON = False
#     USING_PICO_HARDWARE = True
#     USING_PICO2_HARDWARE = True
#     USING_LINUX_HARDWARE = False
#  Linux / Ubuntu 24.04  Cpython version 3.12.3
#     USING_MICROPYTHON = False
#     USING_CPYTHON = True
#     USING_PICO_HARDWARE = False
#     USING_PICO2_HARDWARE = False
#     USING_LINUX_HARDWARE = True
#     

###

