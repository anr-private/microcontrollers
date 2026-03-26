# RHUtils.py

from logger_elem.ElemLoggerABC import ElemLoggerABC
from logger_elem.ElemLogControl import ElemLogControl

# Logging functions; our parent ses set_log_functions()
log = None
logrt = None
logi = None


class RHUtils(ElemLoggerABC):
    def __init__(self):
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    @staticmethod
    def guess_file_content_type(file_path):
        # parts is ".../filename", "html" etc
        parts = file_path.rsplit(".", 1)
        #log(f"RH@389 _guess_file_content_type {parts=} {file_path=} ")
        if len(parts) < 2:
            # no extension found
            return None
        ext = parts[1].lower()
        #log(f"RH@394 _guess_file_content_type {ext=} {file_path=} ")
        if ext in ["html", "htm", "htmlp"]:
            #@@@@ maybe use "text/html; charset=UTF-8"?
            t = "text/html"
        elif ext in ["js",]:
            t = "text/javascript"
        elif ext in ["css",]:
            t = "text/css"
        elif ext in ["ico",]:
            t = "image/x-icon"
        elif ext in ["png",]:
            t = "image/png"
        elif ext in ["jpeg", "jpg"]:
            t = "image/jpeg"
        elif ext in ["gif",]:
            t = "image/gif"
        elif ext in ["json",]:
            t = "application/json"
        else:
            log(r"RHUtils@52 **ERROR** Unknow Content-Type for file '{file_path}'")
            t = None
        log(f"RHUtils@54 _guess_file_content_type {ext=} {file_path=} guessed-type='{t}'")
        return t


###
