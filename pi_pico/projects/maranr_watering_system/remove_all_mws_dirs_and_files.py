# remove_all_mws_dirs_and_files.py

import os

# if False, dry run
DO_REMOVALS = True

file_paths_to_remove = [
    "main.py",    # original file is: watering_project_main.py
    "mws_log.txt",
    "maranr_watering_system_main.py",
    "wsp_log.txt",
    ]

dirs_to_empty_out = [
    "displays",
    "http",
    "lib",
    "pages",
    "primitives",
    "sensors",
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
    prt(f"  REMOVE FILE: {fpath}")
    if DO_REMOVALS:
        try:
            os.remove(fpath)
        except Exception as ex:
            print(f"*** FAILED TO REMOVE FILE {fpath}")
            print(f"    ex: {ex}")
    else:
        print(f"        dry run - file {fpath} not removed")

def remove_dir_by_path(dir_path: str):
    prt(f"  REMOVE DIR: {dir_path}")
    if DO_REMOVALS:
        try:
            os.rmdir(dir_path)
        except Exception as ex:
            print(f"*** FAILED TO REMOVE DIR {dir_path}")
            print(f"    ex: {ex}")
    else:
        print(f"        dry run - dir {dir_path} not removed")

def get_files_in_directory(dir_path: str) -> list:
    try:
        files_in_dir = [ff[0] for ff in os.ilistdir(dir_path) if ff[1] == FILE_MARKER]  # type: ignore[attr-defined]
    except Exception as ex:
        print(f"*** Error get_files_in_directory({dir_path}). ex={repr(ex)} ex.str={str(ex)}")
        files_in_dir = list()
    return files_in_dir

def remove_the_listed_files():
    """ remove the files in the explicit file_paths_to_remove list """
    print("REMOVE THE FILES in the explicit remove list")
    for fpath in file_paths_to_remove:
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
        remove_dir_by_path(dir_path)

def main():
    print("=== REMOVE THE OLD FILES of the WATERING PROJECT ==================")
    remove_the_listed_files()
    remove_the_files_from_listed_dirs()
    print("=== end of REMOVE THE OLD FILES of the WATERING PROJECT ==================")

if __name__ == "__main__":
    main()

### end ###
