# file_system_utils.py
#
# Utils for accessing info about the file system.
# LINEMARKER=FSUT

import os

from lib1.utils import format_number_with_commas


def _calculate_filesystem_space(statvfs_values: tuple[int,...]) -> tuple[int, int]:
    # WAS calculate_flash_space
    # Given the 10-tuple returned by os.statvfs().
    # Returns two values: total_space and free_space (in bytes)
    # On Linux, both block_size and fragment_size are almost always 4096.
    # On a Raspberry Pi Pico (MicroPython), both are almost always either
    # 512 or 4096 (depending on how the LittleFS/FAT partition was formatted).
    # On Pico 2 W 2026-11-01:
    #     import os
    #     print(os.statvfs("/"))
    #     (4096, 4096, 640, 603, 603, 0, 0, 0, 0, 255)
    # So this PICO reports 640 x 4096 = 2,621,440 bytes total and
    # 603 x 4096 = 2,469,888 bytes free.

    # Block size
    ###block_size = statvfs_values[0]
    # Fragment size
    fragment_size = statvfs_values[1]
    # Total number of blocks
    total_blocks = statvfs_values[2]
    # Number of free blocks available to unprivileged user
    #free_blocks = statvfs_values[3]
    avail_blocks = statvfs_values[4]

    # Calculate total and free space in bytes
    total_space = fragment_size * total_blocks
    free_space = fragment_size * avail_blocks

    return total_space, free_space


def get_filesystem_space() -> tuple[int,int]:
    # Get filesystem statistics for the root directory ("/")
    # This works on both Pico and CPython/linux, mac.
    # (Does not work on Windoze but so what).
    # Returns tuple (number of bytes):
    #   (total space on device, currently-available free space)
    #print(f"FSUT$48 Using 'real' filespace info")
    # os.statvfs(...) returns a tuple:
    #  [0] f_bsize: File system block size Linux: 4096  Pico: 4096 (or 512)
    #  [1] f_frsize: Fragment size  Usu same as f_bsize
    #  [2] f_blocks: Size of the filesystem in f_frsize units
    #  [3] f_bfree: Number of free blocks
    #  [4] f_bavail: Number of free blocks for unprivileged users
    #  [5] f_files: Number of inodes (often returns 0 on embedded flash filesystems)
    #  [6] f_ffree: Number of free inodes (often returns 0)
    #  [7] f_favail: Number of free inodes for unprivileged users (often returns 0)
    #  [8] f_flag: Mount flags
    #  [9] f_namemax: Maximum filename length
    # See test_file_system_utils.py for more details.

    statvfs_values = os.statvfs("/")

    total_space, free_space = _calculate_filesystem_space(statvfs_values)

    return total_space, free_space


def convert_fs_space_to_string(fs_space: int) -> str:
    # Convert to KB and MB for easier reading
    KB = 1024
    MB = 1024 * KB

    # Total space ex:  868,352 bytes, 848.00 KB, 0.83 MB
    # Free space ex:   507,904 bytes, 496.00 KB, 0.48 MB
    bytes_stg = f"{fs_space:,}"
    kb_stg = format_number_with_commas(fs_space/KB, 2)
    mb_stg = format_number_with_commas(fs_space/MB, 2)
    #return f"{fs_space:,} bytes, {(fs_space/KB):,.2f} KB, {(fs_space/MB):.2f} MB"
    return f"{bytes_stg} bytes, {kb_stg} KB, {mb_stg} MB"

def get_fs_space_string(sep:str="") -> str:
    total_space, free_space = get_filesystem_space()
    total_space_stg = convert_fs_space_to_string(total_space)
    free_space_stg = convert_fs_space_to_string(free_space)
    return f"TOTAL SPACE {total_space_stg}   {sep}FREE SPACE {free_space_stg}"


###
