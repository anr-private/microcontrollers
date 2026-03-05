# FileUtils.py

import os

import utils 
from trivlog.TrivlogABC import TrivlogABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


class FileUtils(TrivlogABC):

    _SIM_USING_PY3 = False

    @classmethod
    def _SET_SIM_USING_PY3(cls):
        # unit testing only
        cls._SIM_USING_PY3 = True
        print(f"************ USING PY3 compatible FILE NAMING: strip the leading slash ************")



    def __init__(self):
        # if True, this class is being tested using Py3 / Linux
        # so leading '/' are stripped:  '/pages/a.html' -> 'pages/a.html'
        #@@@@@@@@@@@@@@@@@@self._use_py3_sim = False
        super().__init__()

    def _get_log_functions(self): 
        return (log, logrt, logi)
    def _set_log_functions(self, log_arg, logrt_arg, logi_arg):
        global log, logrt, logi
        #print(f"TrivlogExample@30.set_log_functions  {log_arg=}  {log_arg=}  {log_arg=}")
        log = log_arg
        logrt = logrt_arg
        logi = logi_arg


    def _GET_THE_SIM_USING_PY3_FLAG(self):
        return self._SIM_USING_PY3


    def obtain_input_file(self,
            fpath, *, 
            binary=False, read_contents=False, prefix_dir=None,
            w="?WHO?"):
        log(f"FU@31 obtain_input_file {fpath=}  {binary=}  {read_contents=}  {prefix_dir=}")

        # path is the path. On pico you typically see "/pages/some.html", starts with ./.
        # binary - if True, read as binary else read as text
        # read_contents if True, read and return the file contents.
        #   if False, just open the file and return True if file exists else False.
        # prefix_dir - if not None, use this as a prefix to the fpath if trying
        #  to open 'fpath' fails. Ex: fpath="some.html" and prefix_dir="/pages";
        #  if open(some.html) fails, create path "/pages/some.html"
        #  NOTE that if prefix_dir does not start with "/", it is added.
        #    So prefix_dir="pages" and prefix_dir="/pages" are equivalent.
        # w is the caller ex "RH@34" where RH is shortened class name and
        #    digits are line number.
        # Returns False-y (ex None) if request fails. Returns the file
        # contents if read_contents is True; else returns just True
        # if the file was just opened and then closed.
    
        actual_path = fpath
        if self._SIM_USING_PY3:
            actual_path = self._adjust_actual_path(actual_path)
            log(f"FU@51:{w} USE SIMULATED FILE PATHS  {fpath=} {actual_path=}  ***********************")
    
        mode = "rb" if binary else "r"
    
        result = self._try_accessing_file(actual_path, mode, read_contents, w)

        if result is not None:
            log(f"FU@58:{w} SUCCESS  accessed {fpath=}  {actual_path=}  {binary=}  {mode=}  {read_contents=}  {prefix_dir=}")
            if result is True:
                log(f"FU@60:{w} ...  return TRUE - just checked for file exists, did not read contents.")
            else:
                log(f"FU@62:{w} ...  return file contents  LEN={len(result)}")
            return result

        # Failed with simple fpath - try adding prefix_dir
        if prefix_dir is not None:
            log(f"FU@67:{w}  Add {prefix_dir=} to {actual_path=} and try again")
            actual_path = self._add_prefix_dir(fpath, prefix_dir, w)
            if self._SIM_USING_PY3:
                old_actual = actual_path
                actual_path = self._adjust_actual_path(actual_path)
                log(f"FU@72:{w} USE SIMULATED FILE PATHS  {old_actual=} {actual_path=}  ***********************")

            result = self._try_accessing_file(actual_path, mode, read_contents, w)
    
            if result is not None:
                log(f"FU@77:{w} SUCCESS  accessed {fpath=}  {actual_path=}  {binary=}  {mode=}  {read_contents=}  {prefix_dir=}")
                if result is True:
                    log(f"FU@79:{w} ...  return TRUE - just checked for file exists, did not read contents.")
                else:
                    log(f"FU@81:{w} ...  return file contents  LEN={len(result)}")
                return result
    
        # FAILED!
        log(f"FU@85:{w}  obtain_input_file **FAILED** Return None!   {fpath=} {actual_path=}")
        log(f"FU@86:{w}    ... {binary=}  {read_contents=}  {prefix_dir=}  who='{w}' ")
        return None


    def _try_accessing_file(self, actual_path, mode, read_contents, w):
        log(f"FU@91:{w} Try accessing {actual_path=}  {mode=} ")
        try:
            with open(actual_path, mode) as inf:
                if read_contents:
                    log(f"FU@95:{w}  read {actual_path=} contents.")
                    contents = inf.read()
                    log(f"FU@97:{w} from {actual_path=} len(contents)={len(contents)}")
                    return contents
                log(f"FU@99:{w} opened/closed {actual_path=} ok; return True")
                return True
        except OSError as ex:
            log(f"FU@102:{w}  Reading {actual_path=} got EX={repr(ex)}  EX='{str(ex)}' ")
        except Exception as ex:
            log(f"FU@104:{w}  Reading {actual_path=} got EX={repr(ex)}  EX='{str(ex)}' ")
    

    def _add_prefix_dir(self, fpath, prefix_dir, w):
        log(f"FU@108:{w} Add {prefix_dir=} to {fpath=}")
        if not fpath or not prefix_dir: return fpath

        sep1 = ""
        if prefix_dir[0] != '/':
            sep1 = '/'
        sep2 = ""
        if fpath[0] != '/':
            sep2 = '/'
        new_fpath = sep1 + prefix_dir + sep2 + fpath
        log(f"FU@118:{w} {new_fpath=} -- Added {prefix_dir=} to {fpath=}")
        return new_fpath


    def _adjust_actual_path(self, actual_path):
        if len(actual_path) <= 0:  # should never happen!
            return actual_path 
            
        if actual_path[0] != "/": return actual_path
        # strip the leading '/' 
        return actual_path[1:]
    



###
