# mkdir_and_chdir.py

import os

def show_curr_dir():
    curr = os.getcwd()
    print(f"Current: {curr=}")
    return curr

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

def change_current_dir(new_dir):
    try:
        print(f"\nChange to dir {new_dir=}")
        os.chdir(new_dir)
    except OSError as e:
        print(f"*** mkdir ***** got exc={e}")
        #print(f"DIR(e) {dir(e)}")
        print(f" {e.errno=}")
        if e.errno == 2:
            print(f"Error 17: ENOENT  dir '{new_dir}' is not found")
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

def write_a_file(fpath):
    # Using the 'with' statement for automatic file closing
    # use 'a' to append, 'w' to overwrite
    print(f"\nWriting file {fpath=}")
    try:
        with open(fpath, "w") as file:
            file.write("Data logging started.")
            file.write("\\nMore sensor data could go here.")
    except Exception as ex:
        print(f"*** wrote-file  GOT ERROR writing file {fpath} ex={ex}")
        
def remove_a_file(fpath):
    print(f"\nRemoving file {fpath=}")
    try:
        os.remove(fpath)
    except Exception as ex:
        print(f"*** os.remove  GOT ERROR removing file {fpath} ex={ex}")

def test_mkdir_and_rmdir():
    dir_path = "/junkdir"
    fpath = dir_path + "/junk.tx"
    
    show_curr_dir()
    
    make_a_dir(dir_path)
    
    write_a_file(fpath)
    
    remove_a_file(fpath)
    
    remove_a_dir(dir_path)

def test_chdir():
    # this also changes the chdir seen in the file mgr in Thonny
    dir_path = "lib"
    change_current_dir(dir_path)
    
    # this gets a errno 2 NOENT because there is no lib/ subdir in lib/ (which is our current dir)
    change_current_dir(dir_path)

    dir_path = "/lib"
    change_current_dir(dir_path)
    

def main():
    #test_mkdir_and_rmdir()
    test_chdir()

if __name__ == "__main__":
    main()
    
###
