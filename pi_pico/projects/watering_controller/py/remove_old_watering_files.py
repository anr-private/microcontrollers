# remove_old_watering_files.py

import os

# if False, dry run
DO_REMOVALS = True

files_to_remove = [
    "main.py",    # original file is: watering_project_main.py
    ]

dirs_to_empty_out = [
    "wsp_http",
    ]


# values used with os.ilistdir
# it returns tuples:
#  (name, type, inode[, size])
FILE_MARKER = 0x8000  # 32768
DIRECTORY_MARKER      = 0x4000  # 16384


def prt(*args: str) -> None:
    print(*args)  # noqa: T201


def join(path_a: str, path_b: str) -> str:
    return f"{path_a}/{path_b}"

def remove_file_by_path(fpath: str):
    prt(f"  REMOVE: {fpath}")
    if DO_REMOVALS:
        try:
            os.remove(fpath)
        except Exception as ex:
            print(f"*** FAILED TO REMOVE {fpath}")
            print(f"    ex: {ex}")
    else:
        print(f"        dry run - file not removed")

def get_files_in_directory(dir_path: str) -> list:
    return [ff[0] for ff in os.ilistdir(dir_path) if ff[1] == FILE_MARKER]  # type: ignore[attr-defined]


def remove_the_listed_files():
    """ remove the files in the explicit files_to_remove list """
    print("REMOVE THE FILES in the explicit remove list")
    for fpath in files_to_remove:
        #prt(f" Remove: {fpath}")
        remove_file_by_path(fpath)

def remove_the_files_from_listed_dirs():
    """ Remove the files in the explicit dirs_to_empty_out list. """

    print("REMOVE THE FILES in the explicitly-listed dirs")
    for dir_path in dirs_to_empty_out:
        file_names = get_files_in_directory(dir_path)
        prt(f"  dir={dir_path}  files={file_names}")
        for file_name in file_names:
            fpath = join(dir_path, file_name)
            #prt(f"  REMOVE: {fpath}")
            remove_file_by_path(fpath)

def main():
    print("=== REMOVE THE OLD FILES of the WATERING PROJECT ==================")
    remove_the_listed_files()
    remove_the_files_from_listed_dirs()
    print("=== end of REMOVE THE OLD FILES of the WATERING PROJECT ==================")

if __name__ == "__main__":
    main()

### end ###
