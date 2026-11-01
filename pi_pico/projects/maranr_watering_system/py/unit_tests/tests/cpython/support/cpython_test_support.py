# cpython_test_support.py
#
# Support for running tests under C-python ('real' python, py3)
# using pytest

import os

# how to support remove_subdir()
try:
    import shutil
except ImportError:
    shutil = None

# Mock the _X = const(123) capability of micropython
def const(x):
    return x


CTS_VALIDATE = 19385747
FHPR_VALIDATE = 974021

class CpythonTestSupport:
    # UNIT TEST ONLY
    
    _instance = None

    @classmethod
    def get_instance(cls):
        # UNIT TEST ONLY
        if cls._instance is not None: return cls._instance
        cls._instance = CpythonTestSupport(CTS_VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        #print(f"CPYS@34  NULLIFY INSTANCE  =======================================")
        # UNIT TEST ONLY
        CpythonTestSupport._instance = None
        CpythonTestSupport.registry = {}
        # Remove any messages - unit test only
        #CpythonTestSupport._clear_latest_messages()


    def __init__(self, validate):
        if validate != CTS_VALIDATE:
            raise RuntimeError("CpythonTestSupport ctor not allowed")

        self.fake_total_FS_space = 1000
        self.fake_free_FS_space = 1000

    def fake_get_flash_space(self):
        # Fake version of get_flash_space() function in lib/utils.py.
        # Get the total filespace in use and available/free
        # fake the filespace (FS) info
        #@@@@ TODO be able to fake FS space stats based on the 'dir_path' arg
        return (self.fake_total_FS_space, self.fake_free_FS_space)


    def fake_ntp_set_time(self):
        # fake version of ntp.settime()
        pass


    def fake_network_wlan(self, wifi_mode):
        # fake version of network.WLAN(mode)  mode=nework.STA_IF
        pass


class FileHelper:
    # UNIT TEST ONLY
    
    _instance = None

    @classmethod
    def get_instance(cls):
        # UNIT TEST ONLY
        if cls._instance is not None: return cls._instance
        cls._instance = FileHelper(FHPR_VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        #print(f"CPYS@81  NULLIFY INSTANCE  =======================================")
        # UNIT TEST ONLY
        FileHelper._instance = None
        FileHelper.registry = {}


    def __init__(self, validate):
        if validate != FHPR_VALIDATE:
            raise RuntimeError("FileHelper ctor not allowed")


    def read_file(self, the_fpath):
        print(f"CPYS@93 Read log file '{the_fpath}'")
        try:
            with open(the_fpath, "r") as inf:
                data = inf.read()
                #print(f"CPYS@97 Got input from file '{the_fpath}':  len={len(data)}")
                #print(f"CPYS@98 Got input from file '{the_fpath}':  data='{data}'")
                return data
        except Exception as ex:
            print(f"CPYS@101 Reading file '{the_fpath}'  got ex={ex}")
    

    def create_subdir_with_files(self, subdir, fnames, min_file_size=0):
        # Create subdir with files in it such as log files
        # given a list of filenames plus a subdir into which they are created.
        # If min_file_size > 0, each file has fluff written to it until
        # its sizes reaches/exceeds this min.
        #
        # Returns a table of info about the files:
        # Each item in the table is:
        #   ("full/path/of/file", size-of-file-in-bytes)
        # The dir part of the  path is the 'subdir' arg.
        # The filenames are based on the 'fnames' arg.
        self.remove_subdir(subdir)
        os.mkdir(subdir)
    
        # Put a line in each file - each is unique.
        added_tail = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        j = 1
        file_items = []
        for log_fname in fnames:
            fpath = subdir + "/" + log_fname
            fsize = 0
            with open(fpath, "w") as outf:
                line = f"This is file {fpath} {added_tail[:j]}\n"
                outf.write(line)
                fsize += len(line)
                j += 1

                ctr = 1
                while fsize < min_file_size:
                    padline = f"{line} THIS IS A PADDING LINE {ctr=}\n"
                    outf.write(padline)
                    fsize += len(padline)
                    ctr += 1

            finfo = (fpath, fsize)
            file_items.append(finfo)
        return file_items


    def remove_subdir(self, path):
        # copied from lib/file_utils.py

        if shutil is None:
            self.remove_subdir_micropython(path)
        else:
            self.remove_subdir_py3(path)
    
    def remove_subdir_py3(self, path):
        # Python3 version
        try:
            shutil.rmtree(path)
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            print(f"CPYS@158 CANNOT REMOVE LOG SUBDIR '{path}'  ex={ex}  {str(ex)}")
    
    def remove_subdir_micropython(self, path):
        # Micropython version
        # Check if path is a file or directory
        try:
            # Get list of items in the directory
            for entry in os.ilistdir(path):
                name, type = entry[0], entry[1]
                full_path = f"{path}/{name}"
                
                if type == 0x8000: # It's a file
                    os.remove(full_path)
                elif type == 0x4000: # It's a directory
                    self.remove_subdir_micropython(full_path) # Recurse into subdirectory
            
            # Finally, remove the now-empty directory
            os.rmdir(path)
        except OSError:
            # Handle cases where the path doesn't exist or permissions fail
            print("CPYS@178 Failed to remove:", path)
    
###
