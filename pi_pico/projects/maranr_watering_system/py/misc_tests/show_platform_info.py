# show_platform_info.py
import sys

# LINUX / CPYTHON 
#  SPFI$5  implementation.name = 'cpython'
#  SPFI$6  implementation._machine = '<missing>'
#  SPFI$7  sys.platform = 'linux'
#  SPFI$8  sys.version = '3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]'
#  SPFI$9 os.uname() = posix.uname_result(sysname='Linux', nodename='shadow', release='7.2.15-76070215-generic', version='#202611011338~1793722468~24.04~d8e9a1a~dev SMP PREEMPT_DYNAMIC T', machine='x86_64')
#  SPFI$10 gc.mem_free unavailable: AttributeError("module 'gc' has no attribute 'mem_free'")
# 
# PICO 2 W / Micropython 1.29.0
#  SPFI$13  implementation.name = 'micropython'
#  SPFI$14  implementation._machine = 'Raspberry Pi Pico 2 W with RP2350'
#  SPFI$15  sys.platform = 'rp2'
#  SPFI$16  sys.version = '3.4.0; MicroPython v1.29.0 on 2026-08-24'
#  SPFI$17 os.uname() = (sysname='rp2', nodename='rp2', release='1.29.0', version='v1.29.0 on 2026-08-24 (GNU 16.1.0 MinSizeRel)', machine='Raspberry Pi Pico 2 W with RP2350')
#  SPFI$18 gc.mem_free = 440128


def show_platform_info() -> None:
    impl = getattr(sys, "implementation", None)
    print(f"SPFI$23  implementation.name = {getattr(impl, 'name', '<missing>')!r}")
    print(f"SPFI$24  implementation._machine = {getattr(impl, '_machine', '<missing>')!r}")
    print(f"SPFI$25  sys.platform = {sys.platform!r}")
    print(f"SPFI$26  sys.version = {sys.version!r}")

    try:
        import os
        print(f"SPFI$30 os.uname() = {os.uname()}")
    except (ImportError, AttributeError) as ex:
        print(f"SPFI$32 os.uname() unavailable: {ex!r}")

    try:
        import gc
        print(f"SPFI$36 gc.mem_free = {gc.mem_free()}")
    except (ImportError, AttributeError) as ex:
        print(f"SPFI$38 gc.mem_free unavailable: {ex!r}")

show_platform_info()

###

