# list_log_filenames.py 
 
#
# See 
#   ~/git/microcontrollers/pi_pico/projects/maranr_watering_system/mws_logs_FAKED
# It contains fake log files and a script to push them to the Pico.

import os


# def list_dir_contents(dir_path):
    # # returns a list of names
    # dir_contents = os.listdir(dir_path)
    # print(f" {type(dir_contents)}")
    # #print(f" {}")
    # print(f" {dir_contents}")

def filter_directory_contents(dir_path, file_filter):
    # iterator that returns tuple (name, type, inode, [size])
    # type is 0x4000 (16384) for dir, 0x8000 (32768) for a file
    # size is #bytes for a file (zero for a dir)
    # inode is always zero
    selected_items = []
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
            if file_filter is None:
                keep_it = True
            else:
                keep_it = file_filter(name, size)
            if keep_it:
                selected_items.append( (name, size) )
            continue
        m = f"@@43 Unknown file-item-type: 0x{itype:04X}"
        print(m)
    return selected_items

def _logfile_file_filter(fname, size):
    if not fname:
        return False
    if fname.startswith("mws_log."):
        if not fname.endswith(".txt"):
            return True
    return False


def main():
    dir_path = "/"
    selected_items = filter_directory_contents(dir_path, _logfile_file_filter)
    print(f"@@68  MAIN: selected: {selected_items}")
    
if __name__ == "__main__":
    main()