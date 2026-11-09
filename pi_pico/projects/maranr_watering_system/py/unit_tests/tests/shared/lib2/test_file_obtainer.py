# test_file_obtainer.py
#
# # LINEMARKER=TFOBT

import os

from logger_elem import ElemLoggerABC

from lib2.FileObtainer import FileObtainer

try: from cpython_glue import get_scratch_path, remove_scratch_path
except ImportError: pass


class Z_Fake_Logger:
    """ Fake - fakes ElemLogger """

    def __init__(self) -> None:
        """ """
        self.logged_lines: list[str] = []


    def log(self, mesg: str) -> None:
        print(f"LOG: {mesg}")
        self.log_one_line("LOG:"+mesg)

    def logrt(self, mesg: str) -> None:
        print(f"LOG: {mesg}")
        self.log_one_line("LOGR:"+mesg)
        ###raise RuntimeError(mesg)

    def logi(self, mesg: str) -> None:
        print(f"LOG: {mesg}")
        self.log_one_line("LOGI:"+mesg)

    def log_one_line(self, m:str) -> None:
        print("ZfakeLogger {m=!r}")
        self.logged_lines.append(m)


def test_ctor() -> None:
    fobt = FileObtainer()
    assert fobt is not None


def test_inject_logger() -> None:
    """ test the use of Z_Fake_Logger """
    fobt = FileObtainer()

    logger = Z_Fake_Logger()

    log_line = "TFOBT$52 test mesg from test_inject_logger"
    logger.log(log_line)

    fobt._set_logger(logger)

    assert len(logger.logged_lines) == 1, len(logger.logged_lines)
    got_line = logger.logged_lines[0]
    exp_line = "LOG:"+log_line
    assert got_line == exp_line


def test_simple_case() -> None:
    """ Simple case: file exists - prefix not needed """

    scratch_dir = get_scratch_path("TFOBT_simple_case")
    remove_scratch_path(scratch_dir)
    _make_subdir(scratch_dir)

    try:
        fobt = FileObtainer()
    
        logger = Z_Fake_Logger()
        log_line = "TFOBT@99 test mesg from test_inject_logger"
        logger.log(log_line)
        fobt._set_logger(logger)
    
        assert len(logger.logged_lines) == 1, len(logger.logged_lines)
        got_line = logger.logged_lines[0]
        exp_line = "LOG:"+log_line
        assert got_line == exp_line

        fpath = scratch_dir + "/" + "file_1.txt"
        print(f"TFOBT$85 {fpath=!r} ")

        content = "this is file 1\n"
        _create_file(fpath, content)

        got = fobt.obtain_entire_text_file_contents(fpath, prefix_dir="", w="TFOBT$90")

        assert got is not None
        assert len(got) == len(got) == len(content), (len(got), len(content))
        assert got == content, (got, content)

    finally:
        remove_scratch_path(scratch_dir)


def test_needs_prefix() -> None:
    """ Simple case: file exists with a prefix """

    scratch_dir = get_scratch_path("TFOBT_needs_prefix")
    remove_scratch_path(scratch_dir)
    _make_subdir(scratch_dir)

    print(f"TFOBT$107 scratch_dir with prefix: {scratch_dir!r}")
    try:

        fobt = FileObtainer()
    
        logger = Z_Fake_Logger()
        log_line = "TFOBT@99 test mesg from test_inject_logger"
        logger.log(log_line)
        fobt._set_logger(logger)
    
        assert len(logger.logged_lines) == 1, len(logger.logged_lines)
        got_line = logger.logged_lines[0]
        exp_line = "LOG:"+log_line
        assert got_line == exp_line

        base_fpath = "file_2.txt"
        full_path = scratch_dir + "/" + base_fpath
        print(f"TFOBT$124 {full_path=!r} ")
        content = "this is file 2\n"
        _create_file(full_path, content)

        got = fobt.obtain_entire_text_file_contents(base_fpath,
                                            prefix_dir=scratch_dir, w="TFOBT$129")

        if 1:
            found_success = False
            print(f"TFOBT$132 LOG CONTENTS:")
            for lno, line in enumerate(logger.logged_lines):
                print(f" {lno}. {line!r}")
                if "SUCCESS" in line:
                    found_success = True
            assert found_success

        assert got is not None
        assert len(got) == len(got) == len(content), (len(got), len(content))
        assert got == content, (got, content)

    finally:
        remove_scratch_path(scratch_dir)

def _make_subdir(dirpath: str) -> None:
    os.mkdir(dirpath)
    

def _create_file(fpath: str, content: str) -> None:
    """ Create a file of `size` bytes. """
    with open(fpath, "w") as f:
        f.write(content)



###
