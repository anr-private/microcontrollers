# show_file_space.py
#
# LINEMARKER=SHOWFS

import sys
import os

# PICO OUTPUT:
# With filesystem 'empty':
#   $ mpremote run show_file_space.py 
#    TOTAL SPACE 2,621,440 bytes, 2560.00 KB, 2.50 MB   
#    FREE SPACE 2,605,056 bytes, 2544.00 KB, 2.48 MB
#
# With MWS py files loaded:
#  $ mpremote run show_file_space.py 
#   TOTAL SPACE 2,621,440 bytes, 2560.00 KB, 2.50 MB   
#   FREE SPACE 1,798,144 bytes, 1756.00 KB, 1.71 MB
#
# LINUX OUTPUT:
#  $ py show_file_space.py 
#   TOTAL SPACE 1,966,736,678,912 bytes, 1,920,641,288.00 KB, 1875626.26 MB   
#   FREE SPACE 1,805,665,325,056 bytes, 1,763,345,044.00 KB, 1722016.64 MB


def get_filesystem_space():
    # Get filesystem statistics for the root directory ("/")
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


def convert_fs_space_to_string(fs_space):
    # Convert to KB and MB for easier reading
    KB = 1024
    MB = 1024 * KB

    #print(f"Total space: {total_space:,} bytes, {total_space / KB:,.2f} KB, {total_space / MB:.2f} MB")
    #print(f"Free space:  {free_space:,} bytes, {free_space / KB:,.2f} KB, {free_space / MB:.2f} MB")
    space_stg = f"{fs_space:,} bytes, {fs_space / KB:,.2f} KB, {fs_space / MB:.2f} MB"
    return space_stg

def main():

    ts, fs = get_filesystem_space()

    tss = convert_fs_space_to_string(ts)
    fss = convert_fs_space_to_string(fs)

    print(f"TOTAL SPACE {tss}   FREE SPACE {fss}")

if __name__ == "__main__":
    main()
    
###
