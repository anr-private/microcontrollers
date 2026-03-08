# TemplateGrinder.py


from logger_elem.ElemLoggerABC import ElemLoggerABC

#PRT=True
#def prt(s):
#    if PRT: print (s)


log = None
logrt = None
logi = None

START_MARKER = b"[["
END_MARKER = b"]]"


class TemplateGrinder(ElemLoggerABC):
    
    def __init__(self):
        #self.num = num
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"TemplateGrinder@24 _set_logger  logger is {logger}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi

    def fetch_value_for_symbol(self, symbol_stg):
        return "THE-VALUE-FOR-"+symbol_stg

    def _split_the_file_contents(self, file_contents):
        lines = file_contents.split("\n")
        print(f"TGND@36 @@@@@@@@@@ _split_the_file_contents  {len(lines)=}")
        print(f"TGND@38 @@@@@@@@@@ _split_the_file_contents  {type(lines)=}")
        print(f"TGND@38 @@@@@@@@@@ _split_the_file_contents  {type(lines[0])=}")
        return lines

    def process_the_lines(self, lines):

        processed_lines = list()

        for lno, line in enumerate(lines):

            if 0: print(f"@@@@ {lno} {line}")

            processed_line_bytes = self.process_one_line(lno, line)

            processed_lines.append(processed_line_bytes)

        return processed_lines


    def process_one_line(self, lno, line_bytes):

        processed_line = line_bytes

        while 1:
            updated = self.substitute_into_line(lno, processed_line)
            if updated is None:
                break
            processed_line = updated
        return processed_line


    def substitute_into_line(self, lno, line_bytes):
        start_pos = line_bytes.find(START_MARKER, 0)
        if start_pos < 0:
            return None

        print(f"@57  {start_pos=}")

        end_pos = line_bytes.find(END_MARKER, start_pos + len(START_MARKER))
        print(f"@59  {end_pos=}")
        if end_pos <= start_pos:
            return None

        symbol_bytes = line_bytes[start_pos + len(START_MARKER):end_pos]
        headb = line_bytes[:start_pos]
        tailb = line_bytes[end_pos + len(END_MARKER):]

        print(f"@@65  {len(symbol_bytes)=}  {symbol_bytes=} ")
        if len(symbol_bytes) <= 0:
            processed_line_bytes = b"".join([headb, tailb])
            print(f"@@81 EMPTY SYMBOL:  {processed_line_bytes=}")
            return processed_line_bytes

        print(f"@@61 found line {lno}. {line_bytes}")
        print(f"@@64 {len(headb)=}  {headb=}    {len(tailb)=} {tailb=}")
        #lhead = 

        symbol_stg = symbol_bytes.decode("utf-8")

        value_stg = self.fetch_value_for_symbol(symbol_stg)

        value_bytes = value_stg.encode("utf-8")

        processed_line_bytes = b"".join([headb, value_bytes, tailb])
        print(f"@@84  {processed_line_bytes=}")
        return processed_line_bytes


    def grind_file_contents(self, file_contents):
        ###@@@@@@@@@@@@@@@

        raw_lines = self._split_the_file_contents(file_contents)

        processed_lines = self.process_the_lines(raw_lines)

        new_contents_bytes = b"\n".join(processed_lines)

        new_contents_stg = new_contents_bytes.decode("utf-8")
        return new_contents_stg


    def __str__(self):
        s = []
        #s.append("num=%s" % str(self.num))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
