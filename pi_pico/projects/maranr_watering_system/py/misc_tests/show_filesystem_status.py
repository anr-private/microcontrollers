# show_filesystem_status.py
#
# LINEMARKER=SHOW_FS_STATUS

import os

# OUTPUT when file system is full:
#   SHOW_FS_STATUS$8 Total space: 2,621,440 bytes (2560.00 KB)
#   SHOW_FS_STATUS$9 Used space:  2,752,512 bytes (2688.00 KB)
#   SHOW_FS_STATUS$10 Free space:  -131,072 bytes (-128.00 KB)



# Get filesystem stats for the root directory
stats = os.statvfs("/")

block_size = stats[0]     # f_bsize: File system block size (in bytes)
total_blocks = stats[2]   # f_blocks: Total number of blocks
free_blocks = stats[3]    # f_bfree: Number of free blocks

# Calculate sizes in bytes
total_bytes = block_size * total_blocks
free_bytes = block_size * free_blocks
used_bytes = total_bytes - free_bytes

print(f"SHOW_FS_STATUS$26 Total space: {total_bytes:,} bytes ({total_bytes / 1024:.2f} KB)")
print(f"SHOW_FS_STATUS$27 Used space:  {used_bytes:,} bytes ({used_bytes / 1024:.2f} KB)")
print(f"SHOW_FS_STATUS$28 Free space:  {free_bytes:,} bytes ({free_bytes / 1024:.2f} KB)")

###

