# file_utils.py

import os

try: from typing import Callable, Any
except ImportError: pass

# Which 'list dir' method is available
try:
    # micropython
    _ = os.ilistdir   # type: ignore
    use_os_ilistdir = True
except AttributeError:
    # 'real' Python3
    use_os_ilistdir = False

# how to support remove_subdir()
try:
    import shutil
    SHUTIL_IS_AVAILABLE = True
except ImportError:
    SHUTIL_IS_AVAILABLE = False

# NOT USED YET
# Logging functions; our parent class sets using _set_logger()
#log:   Any = None
#logrt: Any = None
#logi:  Any = None


### TODO update the annotation
def filter_dir_contents(dir_path:Any, file_filter:Any) -> Any:
    # Filter the filenames in a directory.
    # Returns a collection of tuples:
    #   (fname, ftype, fsize, result-value)
    # Where 
    #  fname is the filename (incl extension, but no path info)
    #    (it is the dir name if ftype is 'd')
    #  ftype is 'd', 'f', '?'
    #  fsize is an int value, size in bytes
    #  result-value is the result of the file_filter() function
    #    called like this:
    #      file_filter(fname, ftype, fsize)
    # If the file_filter returns None, the fname (and its info)
    # is dropped and not included in the result collection.
    # The result-value allows the file_filter() function to 
    # add info to the tuples that are returned in the collection.
    #
    # **NOTE** If the filter returns False, the file info is
    # INCLUDED!!  This allows the extra info 'result-value'
    # to be provided as True or False.
    # The file_filter MUST RETURN None to exclude the item.
    #
    # Details: the file_filter is a function:
    #   file_filter: Callable[ [str, int], bool ]
    #   file_filter(fname:str, fsize:int) -> bool
    # Sample call made by this filter_dir_contents function:
    #    selected = file_filter("some-filename', 123) 
    # It is asking: do you want this file? Its name is 'some-filename'
    # and its size is 123 bytes. Return True if you want it,
    # False to exclude from the list returned by filter_dir_contents.

    dir_contents = list_dir_contents(dir_path)

    #print(f"FU@65 dir_contents={dir_contents}")

    selected_items = []

    for item in dir_contents:
        (fname, ftype, fsize) = item
        #print(f"FU@71  {fname=}  {ftype=}  {fsize=} ")

        ok = file_filter(fname, ftype, fsize)

        #print(f"FU@75 filter_dir_contents {ok=}  {fname=}  {ftype=}  {fsize=} ")

        if ok is not None:
            selected_items.append( (fname, ftype, fsize, ok) )

    #print(f"FU@80  {selected_items=}  {dir_path=} ")
    return  selected_items


def list_dir_contents(dir_path):
    # Returns dir contents as tuples (in no particular order):
    #   (fname, ftype, fsize)
    # fname is filename (no path info)
    # ftype is 'd' for a dir, 'f' for a file, '?' otherwise
    if use_os_ilistdir: return list_dir_micropython(dir_path)
    return list_dir_python(dir_path)

# def list_dir_python(dir_path): # 'real' python
    # results = []
    # try:
        # for fname in os.listdir(dir_path):
            # fpath = dir_path + "/" + fname
            # #print(f"FU@97 {fname=}  {fpath=}")
            # fsize = os.path.getsize(fpath)
            # results.append ( (fname, "f", fsize) )
    # except FileNotFoundError as ex:
        # print(f"FU@101 Cannot find dir='{dir_path}'")
    # return results

def list_dir_python(dir_path): # 'real' python
    results = []
    with os.scandir(dir_path) as entries:
        for entry in entries:
            #fpath = entry.path
            item_name = entry.name
            file_size = entry.stat().st_size
            if entry.is_dir():
                item_type = "d"
            elif entry.is_file():
                item_type = "f"
            elif entry.is_symlink():
                item_type = "L"
            elif stat.S_ISFIFO(mode):
                item_type = 'F'
            elif stat.S_ISSOCK(mode):
                item_type = 'S'
            elif stat.S_ISBLK(mode):
                item_type = 'B'
            elif stat.S_ISCHR(mode):
                item_type = 'C'
            else:
                item_type = "unknown"
            results.append( [item_name, item_type, file_size] )
    return results

def list_dir_micropython(dir_path):
    #print(f"FU@106  USING list_dir_micropython  {dir_path}")

    results = []

    try:
        for entry in os.ilistdir(dir_path):   # type: ignore[attr-defined]
            fname = entry[0] # may be the dir name
            entry_type = entry[1]
            # inode = entry[2]
    
            fsize = 0
            if len(entry) >= 4:
                fsize = entry[3]
    
            if entry_type == 0x8000:
                ftype = "f"
                ###print(f"FU@122 File: {fname}")
            elif entry_type == 0x4000:
                ftype = "d"
                ###print(f"FU@125 Directory: {fname}")
            else:
                ftype = "?"
    
            results.append ( (fname, ftype, fsize) )
    except Exception as ex:
        print(f"FU@131 FAILED TO LISTDIR '{dir_path}'  ex={ex} {str(ex)}")

    return results


def remove_subdir(path):
    if SHUTIL_IS_AVAILABLE:
        remove_subdir_py3(path)
    else:
        remove_subdir_micropython(path)

def remove_subdir_py3(path):
    # Python3 version
    try:
        shutil.rmtree(path)
    except FileNotFoundError as ex:
        pass
    except Exception as ex:
        print(f"FU@149 CANNOT REMOVE LOG SUBDIR '{path}'  ex={ex}  {str(ex)}")

def remove_subdir_micropython(path: str) -> None:
    # Micropython version
    # Check if path is a file or directory
    try:
        # Get list of items in the directory
        for entry in os.ilistdir(path):    # type: ignore[attr-defined]
            name, type = entry[0], entry[1]
            full_path = f"{path}/{name}"
            
            if type == 0x8000: # It's a file
                os.remove(full_path)
            elif type == 0x4000: # It's a directory
                remove_subdir_micropython(full_path) # Recurse into subdirectory
        
        # Finally, remove the now-empty directory
        os.rmdir(path)
    except OSError:
        # Handle cases where the path doesn't exist or permissions fail
        print("FU@169 Failed to remove:", path)

def remove_file(fpath):
    #print(f"FU@172 Remove file '{fpath}'")
    try:
        os.remove(fpath)
        return True
    except OSError as ex:
        m = f"FU@177 remove_file '{fpath}' FAILED. OSError={ex} {str(ex)}"
        print(m)
        m = f"FU@179 remove_file '{fpath}' FAILED. errno={ex.errno}"
        print(m)
    except Exception as ex:
        m = f"FU@182 remove_file '{fpath}' FAILED. EX={ex} {str(ex)}"
        print(m)
    return False


###
