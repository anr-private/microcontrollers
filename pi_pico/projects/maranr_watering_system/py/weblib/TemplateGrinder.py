# TemplateGrinder.py


from logger_elem.ElemLoggerABC import ElemLoggerABC

#PRT=True
#def prt(s):
#    if PRT: print (s)


log = None
logrt = None
logi = None

START_MARKER = "[["
END_MARKER = "]]"


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

            processed_line = self.process_one_line(lno, line)

            processed_lines.append(processed_line)

        return processed_lines


    def process_one_line(self, lno, raw_line):

        processed_line = raw_line
        while 1:
            updated = self.substitute_into_line(lno, processed_line)
            if updated is None:
                break
            processed_line = updated
        return processed_line


    def substitute_into_line(self, lno, processed_line):
        start_pos = processed_line.find(START_MARKER, 0)
        if start_pos < 0:
            return None

        print(f"@57  {start_pos=}")

        end_pos = processed_line.find(END_MARKER, start_pos + len(START_MARKER))
        print(f"@59  {end_pos=}")
        if end_pos <= start_pos:
            return None

        symbol = processed_line[start_pos + len(START_MARKER):end_pos]
        headb = processed_line[:start_pos]
        tailb = processed_line[end_pos + len(END_MARKER):]

        print(f"@@65  {len(symbol)=}  {symbol=} ")
        if len(symbol) <= 0:
            processed_line = "".join([headb, tailb])
            print(f"@@81 EMPTY SYMBOL:  {processed_line=}")
            return processed_line

        print(f"@@61 found line {lno}. {processed_line}")
        print(f"@@64 {len(headb)=}  {headb=}    {len(tailb)=} {tailb=}")
        #lhead = 

        value = self.fetch_value_for_symbol(symbol)

        processed_line = "".join([headb, value, tailb])
        print(f"@@84  {processed_line=}")
        return processed_line


    def grind_file_contents(self, raw_file_contents):
        ###@@@@@@@@@@@@@@@

        if isinstance(raw_file_contents, str):
            file_contents = raw_file_contents
        elif isinstance(raw_file_contents, bytes):
            file_contents = raw_file_contents.decode("utf-8")
        else:
            logi("RH@109 @@@@@@@@@@@@@@@@@@ UNEXPECTED FILE CONTENTS TYPE={type(raw_file_contents)}")

        raw_lines = self._split_the_file_contents(file_contents)

        processed_lines = self.process_the_lines(raw_lines)

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
