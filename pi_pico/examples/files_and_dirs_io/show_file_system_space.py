# show_file_size.py

import os
import machine

def get_flash_space():
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

    # Convert to KB and MB for easier reading
    KB = 1024
    MB = 1024 * KB

    print(f"Total space: {total_space:,} bytes, {total_space / KB:,.2f} KB, {total_space / MB:.2f} MB")
    print(f"Free space: {free_space:,} bytes, {free_space / KB:,.2f} KB, {free_space / MB:.2f} MB")

# Run the function
get_flash_space()

###
