# list_log_filenames.py 
 
#
# See 
#   ~/git/microcontrollers/pi_pico/projects/maranr_watering_system/mws_logs_FAKED
# It contains fake log files and a script to push them to the Pico.

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
        #print(f" {item}")
        # micropython seems to always provide the 'size' element
        #name, itype, inode, size = item
        #if inode != 0:
        #    m = f"@@29 **ERROR** list-dir-item has non-zero inode value: {item}"
        #    print(m)
        #    continue
        #    #raise RuntimeError(m)
        ###type_stg = f"unknown {hex(itype)}"
        name = item[0]
        itype = item[1]
        # inode = item[2]
        size = item[3]
        if itype == 0x4000:
            # a dir - skip
            continue
        if itype == 0x8000:
            # a file
            #print(f"  {"'"+name+"'":<14}   {inode=}   {size=}  ")
            print(f"  {"'"+name+"'":<14}     {size=}  ")
            continue
        m = f"@@43 Unknown file-item-type: 0x{itype:04X}"
        print(m)

def main():
    dir_path = "/"
    ilist_dir_contents(dir_path)
    
    
if __name__ == "__main__":
    main()