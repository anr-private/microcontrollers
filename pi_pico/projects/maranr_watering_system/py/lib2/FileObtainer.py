# FileObtainer.py
#
# LINEMARKER=FOBT

import os

from logger_elem.ElemLoggerABC import ElemLoggerABC

try: from typing import Callable, Any
except ImportError: pass

# Logging functions; provided by our parent class using set_log_functions()
log:   Any = None
logrt: Any = None
logi:  Any = None

# os module does not define these (unlike Py3)
SEEK_SET = 0  # relative to the start of file
SEEK_CURR = 1  # relative to current file position
SEEK_END = 2	# relative to end of file


class FileObtainer(ElemLoggerABC):

    _SIM_USING_PY3: bool = False

    @classmethod
    def _SET_SIM_USING_PY3(cls) -> None:
        # unit testing only
        cls._SIM_USING_PY3 = True
        print(f"************ USING PY3 compatible FILE NAMING: strip the leading slash ************")



    def __init__(self) -> None:
        super().__init__()


    def _set_logger(self, logger: Any) -> None:
        global log, logrt, logi
        #print(f"FOBT$41 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def _GET_THE_SIM_USING_PY3_FLAG(self) -> bool:
        return self._SIM_USING_PY3


    def obtain_entire_binary_file_contents(self,
                                           fpath: str, 
                                           prefix_dir:str="",
                                           w:str="?WHO?") -> str | None:
        contents = self._obtain_entire_file_contents(fpath, prefix_dir,
                                                     True, w)
        return contents


    def obtain_entire_text_file_contents(self,
                                         fpath: str, 
                                         prefix_dir:str="",
                                         w:str="?WHO?") -> str | None:
        contents = self._obtain_entire_file_contents(fpath, prefix_dir,
                                                     False, w)
        return contents


    def _obtain_entire_file_contents(self,
            fpath: str, 
            prefix_dir:str="",
            binary_mode:bool=False,
            #####read_contents:bool=False, 
            w:str="?WHO?") -> str | None:
        """ Read the contents of the specified file. 
        Returns the entire contents of the file if read goes ok.
        Returns None if cannot read the file (either with or without prefix).

        fpath - the path. 
          On pico you typically see "/pages/some.html", starts with '/'.

        prefix_dir - if not "", use this as a prefix to the fpath if trying
         to open 'fpath' fails. Ex: fpath="some.html" and prefix_dir="/pages";
         if open(some.html) fails, create path "/pages/some.html"
         NOTE that if prefix_dir does not start with "/", it is added.
           So prefix_dir="pages" and prefix_dir="/pages" are equivalent.

        w is the caller ex "RH $ 91" ie a LINE MARKER
        """
        log(f"FOBT$92 obtain_entire_text_file_contents {fpath=!r}  {prefix_dir=!r} {binary_mode=!r} {w=!r}")

        tried_paths: list[str] = []

        actual_path = fpath
        tried_paths.append(actual_path)
        if self._SIM_USING_PY3:
            actual_path = self._adjust_actual_path(actual_path)
            log(f"FOBT$100:{w} USE SIMULATED FILE PATHS  {fpath=} {actual_path=}  ***********************")
    
        contents = self._try_reading_entire_file(actual_path, binary_mode, w)

        if contents is not None:
            log(f"FOBT$105:{w} SUCCESS  accessed {fpath=}  {actual_path=}  {prefix_dir=} LEN={len(contents)}")
            return contents

        # Failed with simple fpath - try adding prefix_dir
        if prefix_dir:
            log(f"FOBT$110:{w}  Add {prefix_dir=} to {actual_path=} and try again")
            actual_path = self._add_prefix_dir(fpath, prefix_dir, w)
            tried_paths.append(actual_path)
            if self._SIM_USING_PY3:
                old_actual = actual_path
                actual_path = self._adjust_actual_path(actual_path)
                log(f"FOBT$116:{w} USE SIMULATED FILE PATHS  {old_actual=} {actual_path=}  ***********************")

            contents = self._try_reading_entire_file(actual_path, binary_mode, w)
        
            if contents is not None:
                log(f"FOBT$121:{w} SUCCESS  accessed {fpath=}  {actual_path=}  {prefix_dir=} LEN={len(contents)}")
                return contents
    
        # FAILED!
        log(f"FOBT$125:{w}  _obtain_entire_file_contents **FAILED** Return None!   {fpath=!r} {prefix_dir=!r}  {binary_mode=!r}")
        log(f"FOBT$126:{w}    ... {tried_paths=}  who='{w!r}' ")
        return None


    def _try_reading_entire_file(self, actual_path: str, 
                                    binary_mode: bool, w:str) -> str | None:
        """ Try reading the specified file.
        If successful, returns the entire file content as str.
        If not returns None.
        """
        log(f"FOBT$136:{w} Try _try_reading_entire_file {actual_path=!r} {binary_mode=!r} {w=!r} ")
        try:
            mode_stg = "rb" if binary_mode else "r"
            with open(actual_path, mode_stg) as inf:
                log(f"FOBT$140:{w} {mode_stg!r} try to read {actual_path=!r} contents.")
                contents = inf.read()
                log(f"FOBT$142:{w!r} {mode_stg!r} from {actual_path=!r}: len(contents)={len(contents)}")
                return contents
        except OSError as ex:
            log(f"FOBT$145:{w}  Reading {actual_path=!r} got OSError EX={repr(ex)}  EX='{str(ex)}' ")
        except UnicodeDecodeError as ex:
            log(f"FOBT$147:{w}  Reading {actual_path=!r} got EX=UnicodeDecodeError EX={repr(ex)}  EX='{str(ex)}' ")
        except Exception as ex:
            log(f"FOBT$149:{w}  Reading {actual_path=!r} got EXC={repr(ex)}  EX='{str(ex)}' ")
        return None


    def _adjust_actual_path(self, actual_path: str) -> str:
        if len(actual_path) <= 0:  # should never happen!
            return actual_path 
            
        if actual_path[0] != "/": return actual_path
        # strip the leading '/' 
        return actual_path[1:]


    def _add_prefix_dir(self, fpath: str, prefix_dir: str, w: str) -> str:
        log(f"FOBT$163:{w} Add {prefix_dir=} to {fpath=}")
        if not fpath or not prefix_dir: return fpath

        sep1 = ""
        if prefix_dir[0] != '/':
            sep1 = '/'
        sep2 = ""
        if fpath[0] != '/':
            sep2 = '/'
        new_fpath = sep1 + prefix_dir + sep2 + fpath
        log(f"FOBT$173:{w} {new_fpath=} -- Added {prefix_dir=} to {fpath=}")
        return new_fpath


###
