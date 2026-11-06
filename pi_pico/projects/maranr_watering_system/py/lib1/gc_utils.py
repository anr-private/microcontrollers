# gc_utils.py
#
# Interface to the 'gc' module
# LINEMARKER=GCUTL


try:
    import gc
    _ = gc.mem_free
except Exception as ex:
    print(f"GCUTL$11 utils.py  CANNOT IMPORT MICROPYTHON VERSION of 'gc' !!!!!")
    del gc   
    #                       # 'type ignore' is for mypy                         
    import gc_FAKE as gc    # type: ignore
    print(f"GCUTL$15 utils.py  USING FAKE VERSION OF 'gc'  !!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def gc_collect() -> None:
    # per https://docs.micropython.org/en/latest/reference/constrained.html#the-heap
    gc.collect()
    new_threshold = gc.mem_free() // 4 + gc.mem_alloc()
    gc.threshold(new_threshold)


def get_memory_status_string(do_garbage_collect:bool=False) -> str:
    ### # prints memory map of block usage
    ###micropython.mem_info(1)
    if do_garbage_collect: gc.collect()
    return f"{gc.mem_alloc()=}   {gc.mem_free()=}"


def main() -> None:
    print(f"GCUTL$33 MEMORY: {get_memory_status_string()} ")

if __name__ == "__main__":
    main()


###
