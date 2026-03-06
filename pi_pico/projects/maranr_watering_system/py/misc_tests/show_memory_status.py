# show_memory_status.py

import gc
import micropython

def show_mem():
    ###micropython.mem_info(1)
    gc.collect()
    print(f" {gc.mem_alloc()=}   {gc.mem_free()=}")
    
    
show_mem()

###
