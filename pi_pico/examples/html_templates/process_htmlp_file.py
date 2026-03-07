# process_htmlp_file.py
#
# Example of processing an HTML file that contains template markup
# where [[xxx]] means 'substitute the value of xxx here'.

import os
import sys

START_MARKER = b"[["
END_MARKER = b"]]"


class HtmlFixer:

    def __init__(self):
        pass

    def fetch_value_for_symbol(self, symbol_stg):
        return "ITS-VALUE"

    def read_the_file(self, fpath):
        with open(fpath, "rb") as inf:
            lines = inf.readlines()
        print(f"@22 READ  {len(lines)}  lines from {fpath} ")
        return lines

    def write_the_lines(self, out_fpath, processed_lines):
        ctr = 0
        with open(out_fpath, "wb") as outf:
            for line in processed_lines:
                outf.write(line)
                ctr += 1
        print(f"write_the_lines@31  Wrote {ctr} lines to {out_fpath}")


    def process_the_lines(self, fpath, lines):
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


    def process_a_file(self, fpath):
        lines = self.read_the_file(fpath)

        processed_lines = self.process_the_lines(fpath, lines)

        out_fpath = fpath + ".out"
        self.write_the_lines(out_fpath, processed_lines)


def main(args):
    if len(args) > 0:
        fpath = args[0]
    else:
        fpath = "index.htmlp"

    hf = HtmlFixer()
    hf.process_a_file(fpath)
   
if  __name__ == "__main__":
    main(sys.argv[1:])
    
###