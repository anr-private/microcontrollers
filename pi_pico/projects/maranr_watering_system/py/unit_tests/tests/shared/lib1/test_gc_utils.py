# test_gc_utils.py
#
# test for lib1/gc_utils.py

from lib1.gc_utils import get_memory_status_string, gc_collect

def test_not_yet() -> None:
    assert True

def test_gc_collect() -> None:
    """ """

    gc_collect()


def test_get_memory_status_string() -> None:
    """ """

    exp_stg = "gc.mem_alloc()=1234   gc.mem_free()=2345"
    got_stg = get_memory_status_string()
    assert exp_stg == got_stg, got_stg

###
