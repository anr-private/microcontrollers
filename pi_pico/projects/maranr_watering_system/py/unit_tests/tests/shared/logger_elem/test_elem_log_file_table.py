# test_elem_log_file_table.py
#
# Test for logger_elem.ElemLogFileTable.py


from logger_elem.ElemLogFileTable import ElemLogFileTable
from logger_elem.ElemLogFileTable import Z__set_log_file_dir
from logger_elem.ElemLogFileTable import Z__set_max_log_file_size
from logger_elem.ElemLogFileTable import Z__set_log_fspace_high_watermark
from logger_elem.ElemLogFileTable import Z__set_log_fspace_low_watermark
from logger_elem.ElemLogFileTable import EMPTY_LOG_FPATH_MARKER_STG

def test_get_current_log_fpath() -> None:
    elft = ElemLogFileTable()
    got_path = elft.get_current_log_fpath()
    assert got_path == EMPTY_LOG_FPATH_MARKER_STG, got_path

    got_fsize = elft.get_current_log_fsize()
    assert got_fsize == 0, got_fsize


def test_get_log_table_item_when_empty() -> None:
    elft = ElemLogFileTable()

    # Table is empty initially
    item = elft.get_log_table_item(0)
    assert item is None





###
