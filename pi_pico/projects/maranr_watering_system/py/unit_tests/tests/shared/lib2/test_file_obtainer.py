# test_file_obtainer.py
#
# # LINEMARKER=TFOBT

from logger_elem import ElemLoggerABC

from lib2.FileObtainer import FileObtainer



# CPython only
try: from cpython_test_support import CpythonTestSupport
except ImportError: pass

class Fake_Logger:
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
    fobt = FileObtainer()

    logger = Fake_Logger()

    log_line = "TFOBT@99 test mesg from test_inject_logger"
    logger.log(log_line)

    fobt._set_logger(logger)

    assert len(logger.logged_lines) == 1, len(logger.logged_lines)
    got_line = logger.logged_lines[0]
    exp_line = "LOG:"+log_line
    assert got_line == exp_line

###
