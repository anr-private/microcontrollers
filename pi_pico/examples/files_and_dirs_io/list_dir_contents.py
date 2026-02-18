# list_dir_contents.py 
 
import os


def list_dir_contents(dir_path):
    # returns a list of names
    dir_contents = os.listdir(dir_path)
    print(f" {type(dir_contents)}")
    #print(f" {}")
    print(f" {dir_contents}")

def ilist_dir_contents(dir_path):
    # iterator that returns tuple (name, type, inode, [size])
    # type is 0x4000 (16384) for dir, 0x8000 (32768) for a file
    # size is #bytes for a file (zero for a dir)
    # inode is always zero
    for item in os.ilistdir(dir_path):
        #print(f" {type(item)}  {len(item)}")
        print(f" {item}")
        # micropython seems to always provide the 'size' element
        name, itype, inode, size = item
        if inode != 0:
            raise RuntimeError("**ERROR** ITEM has non-zero inode value: {item}")
        type_stg = f"unknown {hex(itype)}"
        if itype == 0x4000: type_stg = "dir "
        if itype == 0x8000: type_stg = "file"
        print(f"  {"'"+name+"'":<14}   {type_stg}  {inode=}   {size=}  ")
        print()
        
def main():
    dir_path = "/"
    ilist_dir_contents(dir_path)
    
    
if __name__ == "__main__":
    main()