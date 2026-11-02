# test_gc_utils.py
#
# test for lib1/gc_utils.py

from lib1.gc_utils import get_memory_status_string, gc_collect

def test_not_yet() -> None:
    assert True

def test_gc_collect() -> None:
    """ """

    got = gc_collect()
    assert got is None, got
    try:
        from lib1.gc_utils import _MOST_RECENT_THRESHOLD_ARG
        assert _MOST_RECENT_THRESHOLD_ARG == 1820 # depends on gc_FAKE values
    except ImportException:
        pass # CPython only 


def test_get_memory_status_string() -> None:
    """ """

    got_stg = get_memory_status_string()

    assert _validate_memory_staus_string(got_stg), got_stg


def test_get_memory_status_string_with_do_garbage_collect_() -> None:
    """ """

    got_stg = get_memory_status_string(do_garbage_collect=False)
    assert _validate_memory_staus_string(got_stg), got_stg

    got_stg = get_memory_status_string(do_garbage_collect=True)
    assert _validate_memory_staus_string(got_stg), got_stg


def test_validate_memory_staus_string() -> None:
    """ Test the validate function """
    ok = _validate_memory_staus_string("gc.mem_alloc()=1234   gc.mem_free()=2345")
    assert ok

def _validate_memory_staus_string(status_string: str) -> bool:
    """ Parse the string, validate it has the expected form
    Returns True if ok, False if unexpected format.
    Expected:  'gc.mem_alloc()=1234   gc.mem_free()=2345'
    """
    # Parts: 'gc.mem_alloc()=1234', 'gc.mem_free()=2345'
    main_parts = status_string.split()

    if len(main_parts) != 2: return False

    print(f"TGU@@41 {main_parts=}")

    mem_alloc_part = main_parts[0]
    mem_free_part = main_parts[1]    

    # Parts: 'gc.mem_alloc()' and '12345'
    parts = mem_alloc_part.split("=")
    if len(parts) != 2: return False
    if parts[0] != 'gc.mem_alloc()': return False
    try:
        _ = int(parts[1])
    except (TypeError, ValueError) as ex:
        print(f"TGU@60  Expected int after '=': {mem_alloc_part}")
        return False

    # Parts: 'gc.mem_alloc()' and '12345'
    parts = mem_free_part.split("=")
    if len(parts) != 2: return False
    if parts[0] != 'gc.mem_free()': return False
    try:
        _ = int(parts[1])
    except (TypeError, ValueError) as ex:
        print(f"TGU@70  Expected int after '=': {mem_free_part}")
        return False

    return True



###
