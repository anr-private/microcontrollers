# gc_utils.py
#
def gc_collect():
    # per https://docs.micropython.org/en/latest/reference/constrained.html#the-heap
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

try:
    import gc
    _ = gc.mem_free
except Exception as ex:
    print(f"UTILS@15 utils.py  CANNOT IMPORT MICROPYTHON VERSION of 'gc' !!!!!")
    del gc   
    #                       # 'type ignore' is for mypy                         
    import gc_FAKE as gc    # type: ignore
    print(f"UTILS@18 utils.py  USING FAKE VERSION OF 'gc'  !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#@@@@@@@@@@ TODO fake the GC using CpythonTestSupport  see TestElemLogControl.py

def get_memory_status_string(do_garbage_collect:bool=False) -> str:
    ### # prints memory map of block usage
    ###micropython.mem_info(1)
    if do_garbage_collect: gc.collect()
    return f" {gc.mem_alloc()=}   {gc.mem_free()=}"


def main() -> None:
    print(f"GC_UTILS@9999 MEMORY: {get_memory_status_string()} ")

if __name__ == "__main__":
    main()


###
