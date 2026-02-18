# write_a_file.py
#
# write a file into a subdir /junk/, which we create
# then remove it and remove the subdir

import os

def make_a_dir(dir_path):
    try:
        print(f"\nCreate dir {dir_path=}")
        os.mkdir(dir_path)

    except OSError as e:
        print(f"*** mkdir ***** got exc={e}")
        #print(f"DIR(e) {dir(e)}")
        print(f" {e.errno=}")
        if e.errno == 17:
            print(f"Error 17: EEXISTS  the dir already exists")
        else:
            print(f"Error {e.errno} unknown meaning")

def remove_a_dir(dir_path):
    try:
        print(f"\nRemove the diretory {dir_path}.  ** IT MUST BE EMPTY **  Use os.remove(fname) to remove any files first.")
        os.rmdir(dir_path)
    except OSError as e:
        print(f"*** os.rmdir ***** got exc={e}")
        #print(f"DIR(e) {dir(e)}")
        print(f"  {e.errno=}")
        if e.errno == 39:
            print(f"Error 39: ENOTEMPTY  the dir is not empty")
        else:
            print(f"Error {e.errno} unknown meaning")

def read_a_file(fpath):
    try:
        # Open the file in read mode ('r' is the default)
        with open(fpath, 'r') as inf:
            # Read the entire content of the file
            content = inf.read()
            if 1:
                print("File content:")
                print(content)
            return content

    except OSError as ex:
        print(f"*** ERROR* Reading file '{fpath}': {ex}")
        print("     {ex.errno=}")
    

def write_a_file(fpath, file_lines, append=False):
    # Using the 'with' statement for automatic file closing
    # use 'a' to append, 'w' to overwrite
    if append:
        write_mode = "a"
    else:
        write_mode = "w"

    print(f"\nWriting file {fpath=}  {write_mode=} ")
    
    try:
        num_lines = 0
        with open(fpath, "w") as outf:
            for line in file_lines:
                outf.write(line+"\n")                
                num_lines += 1

        print(f"Wrote {num_lines} line(s) into file {fpath}")

    except Exception as ex:
        print(f"*** wrote-file  GOT ERROR writing file {fpath} ex={ex}")
        
def remove_a_file(fpath):
    print(f"\nRemoving file {fpath=}")
    try:
        os.remove(fpath)
    except Exception as ex:
        print(f"*** os.remove  GOT ERROR removing file {fpath} ex={ex}")

def test_write_a_file_in_a_subdir():
    """ Create a subdir, write a file into it, read back the file,
    then remove the file and the subdir.
    """
    dir_path = "/junk"
    fpath = "/junk/junk.txt"

    make_a_dir(dir_path)

    file_lines = ["line 1", "line 2"]
    write_a_file(fpath, file_lines)

    # Read back what we wrote - is it what we expect?
    content = read_a_file(fpath)
    print(f"CONTENT '{content}'")
    ###lines_w_eol = add_eol_to_lines(file_lines)
    expected_content = "\n".join(file_lines)
    expected_content += "\n"
    print(f"CONTENT  '{show_cc(content)}'")
    print(f"EXPECTED '{show_cc(expected_content)}'")
    assert expected_content == content
    print(f"  Content matches what we expected.")

    print(f"\nRemove the file {fpath}")
    remove_a_file(fpath)

    print(f"Remove the subdir {dir_path}")
    remove_a_dir(dir_path)


def show_cc(line):
    """ convert line to a new line, replacing all control chars with visible rep """
    if line is None: line = ""
    chars = []
    for ch in line:
        if ch == "\r":
            chars.append("\\r")
        elif ch == "\n":
            chars.append("\\n")
        elif ch == "\t":
            chars.append("\\t")
        else:
            chars.append(ch)
    return "".join(chars)


def add_eol_to_lines(lines):
    results = []
    for line in lines:
        results.append(line+"\r\n")
    return results



def main():
    test_write_a_file_in_a_subdir()

if __name__ == "__main__":
    main()
    
###
