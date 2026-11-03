# test_file_system_utils.py

from lib1.file_system_utils import get_flash_space, calculate_flash_space, convert_fs_space_to_string

# CPython only
###try: from cpython_test_support import CpythonTestSupport
###except ImportError: pass

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

def test_calculate_flash_space() -> None:
    fragment_size = 4096
    # Total number of blocks
    total_blocks = 100
    # Number of free ('available') blocks available to unprivileged user
    avail_blocks = 25

    # fake the 10-tuple result of os.statvfs()
    # The 4 digit numbers should never be used - if they are
    # we'll pick it up as a bad result from calculate_flash_space()
    fake_statvfs_result = (
        9988,fragment_size,
        total_blocks, 9246, avail_blocks,
        8877, 7766, 9853, 9075, 8356
        )
    assert len(fake_statvfs_result) == 10

    exp_total_space = fragment_size * total_blocks 
    exp_free_space = fragment_size * avail_blocks
    got_total_space,got_free_space = calculate_flash_space(fake_statvfs_result)
    assert exp_total_space == got_total_space, got_total_space
    assert exp_free_space == got_free_space, got_free_space


def test_get_flash_space() -> None:
    # on shadow Ubunt 24.04, the actual is:
    #   exp_total_space = 1_966_736_678_912
    #print(f"@@T@ DIR cpython_test_support is {dir(cpython_test_support)}")
    #print(f"@@T@ DIR cpython_test_support.file is {cpython_test_support.__file__}")
    #from cpython_test_support import CpythonTestSupport
    # cts = CpythonTestSupport.get_instance()
    # faked_FS_total = 12345
    # faked_FS_free  =   987
    # cts.fake_total_FS_space = faked_FS_total
    # cts.fake_free_FS_space = faked_FS_free
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Linux numbers:  df shows:
    #      filesystem   1K-blocks   used      available    Use%
    #  /dev/nvme0n1p2  1920641288  156455772  1666548552    9% /
    # 1,920,641,288 KiB x 1024 = 1,966,736,678,912 bytes
    # f_bfree:   (note Linux reserves some space for root use
    #  1,806,526,021,632 bytes / 1024 = 1,764,185,568 KiB.
    # That is f_bfree, the free blocks including the reserved ones.
    # total minus used (1,920,641,288 − 156,455,772 = 1,764,185,516 KiB)
    #  (small difference due to file system being active/ in use)
    # gap: 1,764,185,568 − 1,666,548,552 = 97,637,016 KiB, about 100 GB.
    #   5.08% of the disk: ext4’s default 5% reserve for root.
    # Both numbers are correct. They answer different questions:
    # stat[3]  f_bfree  the free space including the root-only reserve.
    # stat[4]  f_bavail the space a program can actually use as a normal user
    #                   (the number shown by 'df')

    got_total_space, got_free_space = get_flash_space()

    print(f"@@T@38  {got_total_space=}  {got_free_space=}")
    
    # Linux: 1,966,736,678,912 bytes total (2Tb)
    #        1,806,526,021,632 bytes free
    #
    # Pico: 256Mb(?)
    exp_min_total_space = 2_500_000
    assert got_total_space >= exp_min_total_space, f"{got_total_space} not >= {exp_min_total_space}"
    # Linux: 1,806,526,676,992 approx 1441800192
    assert got_free_space >= 100_000, got_free_space
    # The free space should not exceed total space
    diff = got_total_space - got_free_space
    assert diff >= 0, diff


def test_convert_fs_space_to_string() -> None:
    total_space = 12345678
    total_stg = convert_fs_space_to_string(total_space)
    print(f"@@T@34  {total_stg=}")
    exp_total_stg = '12,345,678 bytes, 12,056.33 KB, 11.77 MB'
    assert total_stg == exp_total_stg, f"'{exp_total_stg}', '{total_stg}'"

    free_space = 987654
    free_stg = convert_fs_space_to_string(free_space)
    print(f"@@T@40  {free_stg=}")
    exp_free_stg = '987,654 bytes, 964.51 KB, 0.94 MB'
    assert free_stg == exp_free_stg, free_stg


###
