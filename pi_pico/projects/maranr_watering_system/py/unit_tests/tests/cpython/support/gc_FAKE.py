# gc_FAKE.py
#

_MOST_RECENT_THRESHOLD_ARG = -1


print(f"______ USING gc_FAKE.py  - NO MICROPTYON VERSION AVAILABLE _________________")

def collect() -> None:
    print(f"______ USING gc.collect()  from gc_FAKE.py  - NO MICROPTYON VERSION AVAILABLE _________________")

def mem_alloc() -> int:
    print(f"______ USING gc.mem_alloc()  from gc_FAKE.py  - NO MICROPTYON VERSION AVAILABLE _________________")
    return 1234

def mem_free() -> int:
    print(f"______ USING gc.mem_free()  from gc_FAKE.py  - NO MICROPTYON VERSION AVAILABLE _________________")
    return 2345

def threshold(threshold_value: int) -> None:
    # save for unit test
    global _MOST_RECENT_THRESHOLD_ARG
    _MOST_RECENT_THRESHOLD_ARG = threshold_value



###
