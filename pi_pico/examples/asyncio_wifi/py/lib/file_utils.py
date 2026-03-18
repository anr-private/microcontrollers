# FileTailer.py

import os

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

# os module does not define these (unlike Py3)
SEEK_SET = 0  # relative to the start of file
SEEK_CURR = 1  # relative to current file position
SEEK_END = 2	# relative to end of file


def read_last_n_lines(fpath, relative_line_number, number_of_lines):
    """Reads the last N lines of a text file efficiently in MicroPython."""
    try:
        with open(fpath, 'rb') as f: # Open in binary mode for reliable seeking
            f.seek(0, SEEK_END)
            file_size = f.tell()
            position = file_size
            lines_found = 0
            lines = []
            fbytes = b""

            while True:
                #print(f"\n@@LOOP TOP -- pos={position}  {lines_found=}  {relative_line_number=}")
                if position <= 0:
                    break
                if lines_found >= relative_line_number:
                    break

                # Read a chunk from near the end
                chunk_size = 128 # Read in small chunks to save memory
                chunk_size = 100 #@@@@@@@@@@@@@@@@@@@@@@@

                position = max(0, position-chunk_size)
                #print(f"@@214  seek pos {position=}")
                f.seek(position)

                chunk = f.read(file_size-position if position == 0 else chunk_size)

                #print(f"FU@219  READ got {len(chunk)} bytes")

                file_size = position # Update file_size for next iteration if needed
                #print(f"@223  new file size {file_size}")
                fbytes = chunk + fbytes # Prepend the new chunk to the fbytes
                print(f"FU@219  combined bytes {len(fbytes)} bytes")
                
                # Count newlines in the fbytes
                while b'\n' in fbytes and lines_found < relative_line_number:
                    #print(f"@@ ---- INNERLOOP-------------")
                    # Find the last newline
                    last_newline_index = fbytes.rfind(b'\n')
                    #print(f"@@232  {last_newline_index=} ")
                    if last_newline_index < 0:
                        break
                    
                    line = fbytes[last_newline_index + 1:]
                    #print(f"@@237  len.line is {len(line)}")

                    if line: # Avoid empty lines if file ends with newline
                        line_stg = line.decode('utf-8')
                        #print(f"@@241  line is '{line_stg}' ")
                        # Insert at beginning
                        lines.insert(0, line_stg)
                        #print(f"@@244  num-in-list = {len(lines)}")
                        lines_found += 1
                        #print(f"@@246  {lines_found=}")
                        # Discard 'extra' lines at the end
                        if len(lines) > number_of_lines:
                            _ = lines.pop()
                            #print(f"@@250 popped {_}  new-num-in-list={len(lines)}")

                    # Keep the remaining fbytes for the next line
                    fbytes = fbytes[:last_newline_index]
                    #print(f"@@245  remain len is  {len(fbytes)=}")
                    #print(f"@@256  remain bytes are {fbytes.decode('utf-8')}")

            # If loop finishes and there's still content in fbytes, it's the first line(s)
            #print(f"@@257 ___ after loop:  {lines_found=}   {len(fbytes)=}")
            #print(f"@@@@  lines: len={len(lines)} {lines}")
            if fbytes and lines_found < relative_line_number:
                line_stg = line.decode('utf-8')
                #print(f"@@260 LAST  line is '{line_stg}' ")
                lines.insert(0, line_stg)
                #print(f"@@262  LAST: num-in-list = {len(lines)}")
                lines_found += 1
                #print(f"@@264 LAST  {lines_found=}")
                if len(lines) > number_of_lines:
                    _ = lines.pop()
                    #print(f"@@268 LAST: popped {_}  new-num-in-list={len(lines)}")

            # Return only the last N lines
            lines_returned = lines[-relative_line_number:]
            #print(f"@@268 len(lines_returned): {len(lines_returned)}  {relative_line_number=}")
            return lines_returned
    except OSError:
        print(f"FU@270 read_last_n_lines  EX={repr(ex)}")
        print(f"FU@271 read_last_n_lines  EX={str(ex)}")
        return []




###
