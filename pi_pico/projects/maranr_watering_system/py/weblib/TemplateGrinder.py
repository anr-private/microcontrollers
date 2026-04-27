# TemplateGrinder.py


from logger_elem.ElemLoggerABC import ElemLoggerABC

from utils import get_memory_status_string
from utils import get_fs_space_string
from lib2.TimeMgr import TimeMgr

#PRT=True
#def prt(s):
#    if PRT: print (s)


log = None
logrt = None
logi = None

START_MARKER = "[["
END_MARKER = "]]"


BODY_SUBS = {
    # NOTE keys are always all lower case!
    "filesystem-status-splitline": (get_fs_space_string, (), {"sep":"<br>"} ),
    "memory-status": (get_memory_status_string, ()),
    "date-time": (TimeMgr.get_formatted_date_time_string, ()),
    }

VALIDATE = 7020405

class TemplateGrinder(ElemLoggerABC):
    
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = TemplateGrinder(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        ElemLogControl._instance = None
        # Remove any messages - unit test only
        #ElemLogControl._clear_latest_messages()


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"TG@52 CALLED CTOR use get_instance()"
            raise RuntimeError(m)

        #self.num = num
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def _fetch_value_for_symbol(self, symbol_stg):
        funct_info = BODY_SUBS.get(symbol_stg)
        if funct_info is None:
            return f"UNKOWN:{symbol_stg}"
            
        funct = funct_info[0]
        args = ()
        kw = {}
        if len(funct_info) > 1:
            args = funct_info[1]
        if len(funct_info) > 2:
            kw = funct_info[2]

        r = funct(*args, **kw)
        return r


    def _split_the_file_contents(self, file_contents):
        lines = file_contents.split("\n")
        return lines

    def substitute_into_line(self, lno, processed_line):
        start_pos = processed_line.find(START_MARKER, 0)
        if start_pos < 0:
            return None

        end_pos = processed_line.find(END_MARKER, start_pos + len(START_MARKER))
        if end_pos <= start_pos:
            return None

        symbol = processed_line[start_pos + len(START_MARKER):end_pos]
        headb = processed_line[:start_pos]
        tailb = processed_line[end_pos + len(END_MARKER):]

        if len(symbol) <= 0:
            processed_line = "".join([headb, tailb])
            return processed_line

        value = self._fetch_value_for_symbol(symbol)

        processed_line = "".join([headb, value, tailb])
        return processed_line


    def _grind_one_line(self, lno, raw_line):

        processed_line = raw_line
        # repeat substitution - handles nested substitution items like [[my [[date]] bday]]
        while 1:
            updated = self.substitute_into_line(lno, processed_line)
            if updated is None:
                break
            processed_line = updated
        return processed_line


    def _grind_lines(self, lines):

        processed_lines = list()

        for lno, line in enumerate(lines):

            processed_line = self._grind_one_line(lno, line)

            processed_lines.append(processed_line)

        return processed_lines


    def grind_file_contents(self, raw_file_contents):
        # raw_file_contents is a str containing an entire file or
        # a chunk of file. This method breaks it into a list of lines
        # and then grinds the lines.

        if isinstance(raw_file_contents, str):
            file_contents = raw_file_contents
        elif isinstance(raw_file_contents, bytes):
            file_contents = raw_file_contents.decode("utf-8")
        else:
            logi(f"TG@144 @@@@@@@@@@@@@@@@@@ UNEXPECTED FILE CONTENTS TYPE: {type(raw_file_contents)}")
            return None

        raw_lines = self._split_the_file_contents(file_contents)

        processed_lines = self._grind_lines(raw_lines)

        ###new_contents_by tes = b"\n".join(processed_lines)
        new_contents_stg = "\n".join(processed_lines)

        #new_contents_stg = new_contents_by tes.decode("utf-8")
        return new_contents_stg


    def __str__(self):
        s = []
        #s.append("num=%s" % str(self.num))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
