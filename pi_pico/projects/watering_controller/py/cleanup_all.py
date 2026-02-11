# cleanup_all.py
#
# Run it on the pi pico to clean up all the old files.
#
# src: https://github.com/orgs/micropython/discussions/9802

import os

# values used with os.ilistdir
# it returns tuples:
#  (name, type, inode[, size])
FILE_MARKER = 0x8000  # 32768
DIRECTORY_MARKER      = 0x4000  # 16384


def prt(*args: str) -> None:
    print(*args)  # noqa: T201


def join(path_a: str, path_b: str) -> str:
    return f"{path_a}/{path_b}"


def list_files(base: str) -> list:
    # micropython: -> ignore attr-defined
    return [d[0] for d in os.ilistdir(base) if d[1] == FILE_MARKER]  # type: ignore[attr-defined]


def list_directories(base: str) -> list:
    # micropython: -> ignore attr-defined
    return [d[0] for d in os.ilistdir(base) if d[1] == DIRECTORY_MARKER]  # type: ignore[attr-defined]


def cleanup(base: str = ".") -> None:
    prt(f"CLEANUP: {base}")

    for f in list_directories(base):
        file_to_remove = join(base, f)
        prt(f"removing file: {file_to_remove}")
        ###os.remove(file_to_remove)  # noqa:  PTH107 (micropython)
        print(f"os.remove(file_to_remove)")  # noqa:  PTH107 (micropython)

    for d in list_files(base):
        dir_to_remove = join(base, d)
        prt(f"removing dir: {dir_to_remove}")
        cleanup(dir_to_remove)
        ###os.rmdir(dir_to_remove)  # noqa:  PTH106 (micropython)
        print(f"os.rmdir(dir_to_remove) ")  # noqa:  PTH106 (micropython)
        
def xxx_show_dirs():
    print(f"dirs /")
    print(list_directories("/"))
    print()

    print(f"dirs ./")
    print(list_directories("./"))
    print()

    print(f"dirs .")
    print(list_directories("."))
    print()
def xxx_show_files_and_dirs():
    print("FILES and DIRS in '/'  (slash, top-level dir):")
    for d in os.ilistdir("/"):
        print(f"  {d=}")
    print("FILES -----")
    dd = "/"
    files = [f for f in os.ilistdir(dd) if f[1] == FILE_MARKER]
    for f in files:
        print(f"  {f}")
    print("DIRs -----")
    dd = "/"
    dirs = [x for x in os.ilistdir(dd) if x[1] == DIRECTORY_MARKER]
    for x in dirs:
        print(f"  {x}")


if __name__ == "__main__":
    ###cleanup(".")
    xxx_show_files_and_dirs()


### end ###
