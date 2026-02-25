# try_logger_w_control.py
#
# See LoggerABC for details

import sys

from my_classes.ClassA import ClassA
from my_classes.ClassB import ClassB
from logger.LoggerABC import LoggerABC
from logger.EasyLogger import EasyLogger

def test1():
    print(f"===  TEST 1  ++++++++++++++++++++++++++++++++++++")
    print(f"@@T1@14 This is test 1")

    if 0:
        print(f"@@T1@17  enable logger in ClassA")
        r = ClassA.enable_logger(True)
        assert r is True

    # This sets up the log() in ClassA; by default it is enabled
    print(f"@@T1@22  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True

    print(f"\n@@T1@25  Try logging something while ENABLED - should get some output")
    ca = ClassA()
    ca.do_logging("+++ Logging this message from Test 1  EXPECT IT SHOULD BE OUTPUT  +++ @@T1@27 +++")
    del ca
    latest_mesg = EasyLogger.get_instance()._latest_mesg_
    print(f"@@T1@30  latest log mesg is {latest_mesg}")
    assert "EXPECT IT SHOULD BE OUTPUT" in latest_mesg

    print(f"\n@@T1@33  DISABLE logging for ClassA")
    r = ClassA.enable_logger(False)
    assert r is False
    del r
    print(f"@@T1@37  Get the logger status; expect FALSE: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is False

    print(f"\n@@T1@40  Try logging something while DISABLED - should get no output")
    ca = ClassA()
    ca.do_logging("+++ Logging this message from Test 1    EXPECT IT SHOULD BE MUTED  +++ @@T1@42 +++")
    print(f"@@T1@43  latest log mesg is {latest_mesg}")
    assert "EXPECT IT SHOULD BE OUTPUT" in latest_mesg

    print(f"===  TEST 1  ++++++++++++++++++++++++++++++++++++\n")




def test2():
    print(f"===  TEST 2  ++++++++++++++++++++++++++++++++++++")
    print(f"@@T2@53 This is test 1")

    # Override any previous test
    print(f"@@T2@56  enable logger in ClassA")
    r = ClassA.enable_logger(True)
    assert r is True

    # This sets up the log() in ClassA; by default it is enabled
    print(f"@@T2@61  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True

    print(f"\n@@T2@64  Try logging something while ENABLED - should get some output")
    ca = ClassA()
    ca.do_logging("+++ Logging this message from Test 1  EXPECT IT SHOULD BE OUTPUT  +++ @@T2@66 +++")
    ca = None
    latest_mesg = EasyLogger.get_instance()._latest_mesg_
    print(f"@@T2@69  latest log mesg is {latest_mesg}")
    assert "EXPECT IT SHOULD BE OUTPUT" in latest_mesg
    del latest_mesg

    print(f"\n@@T2@73  DISABLE logging for ClassA")
    r = ClassA.enable_logger(False)
    assert r is False
    del r
    print(f"@@T2@77  Get the logger status; expect FALSE: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is False

    print(f"\n@@T2@80  Try logging something while DISABLED - should get no output")
    ca = ClassA()
    ca.do_logging("+++ Logging this message from Test 1    EXPECT IT SHOULD BE MUTED  +++ @@T2@82 +++")
    latest_mesg = EasyLogger.get_instance()._latest_mesg_
    print(f"@@T2@84  latest log mesg is {latest_mesg}")
    assert "EXPECT IT SHOULD BE MUTED" in latest_mesg
    del latest_mesg


    print(f"\n@@T2@89  RE-ENABLE  logging for ClassA")
    r = ClassA.enable_logger(True)
    assert r is True
    del r
    print(f"@@T2@93  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True

    print(f"\n@@T2@96  Try logging something while RE-ENABLED - should get output")
    ca = ClassA()
    ca.do_logging("+++ Logging this message from Test 1  EXPECT IT SHOULD BE OUTPUT +++ @@T2@98 +++")
    latest_mesg = EasyLogger.get_instance()._latest_mesg_
    print(f"@@T2@100  latest log mesg is {latest_mesg}")
    assert "EXPECT IT SHOULD BE OUTPUT" in latest_mesg
    del latest_mesg

    print(f"\n@@T2@104  Second time: ===  DISABLE logging for ClassA")
    r = ClassA.enable_logger(False)
    assert r is False
    del r
    print(f"@@T2@108  Get the logger status; expect FALSE: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is False

    print(f"\n@@T2@111 CREATE A SECOND ClassA - it should NOT re-enable logging")
    caa = ClassA()
    print(f"@@T@64  Verify logging is still DISABLED")
    print(f"@@T2@114  Get the logger status; expect FALSE: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is False

    print(f"\n@@T2@117  Try logging something while RE-DISABLED - using extant ClassA objs - should get NO output")
    ca.do_logging("+++ Logging this message from Test 1 obj 'ca' -- EXPECT IT SHOULD BE MUTED +++ @@T2@118 +++")
    assert "EXPECT IT SHOULD BE MUTED" in EasyLogger.get_instance()._latest_mesg_
    caa.do_logging("+++ Logging this message from Test 1 obj 'caa' --  EXPECT IT SHOULD BE MUTED +++ @@T2@120 +++")
    assert "EXPECT IT SHOULD BE MUTED" in EasyLogger.get_instance()._latest_mesg_

    print(f"===  end of TEST 2  ++++++++++++++++++++++++++++++++++++\n")


def test3():
    # First, notice/check that logging may not enabled for ClassB
    # Other tests run before this one may have already done the
    # initialization of logging for ClassB - and because the logging
    # control is at the Class (and Module) level, any setup done
    # by a previous test will persist.
    # Then just test turning logging on and off.

    print(f"===  TEST 3  ++++++++++++++++++++++++++++++++++++")

    print(f"@@T3@136  enable logger in ClassA")
    r = ClassA.enable_logger(True)
    assert r is True

    print(f"@@T3@140  Get status using ClassB.get_logger_status()")
    print(f"@@T3@141  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True
    print()

    print(f"@@T3@145  Make sure logging is enabled for ClassB")
    r = ClassB.enable_logger(True)
    print(f"@@T3@147  ClassB.enable_logger(True) returns {r}")
    assert r is True
    del r
    print()

    r = ClassB.enable_logger(True)
    print(f"@@T3@153  ClassB.enable_logger(True) returns {r}")
    assert r is True
    del r
    print()

    r = ClassB.enable_logger(False)
    print(f"@@T3@159  ClassB.enable_logger(False) returns {r}")
    assert r is False
    del r
    print()

    r = ClassB.enable_logger(True)
    print(f"@@T3@165  ClassB.enable_logger(True) returns {r}")
    assert r is True
    del r
    print()

    print(f"===  end of TEST 3  ++++++++++++++++++++++++++++++++++++\n")


def test4():
    # First, notice/check that logging is not enabled for ClassB
    # (see notes above: a previous test may have already initialized
    # the logging state of ClassB)

    print(f"===  TEST 4  ++++++++++++++++++++++++++++++++++++")

    r = ClassB.get_logger_status()
    print(f"@@T4@181  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True
    print()

    print(f"===  end of TEST 4  ++++++++++++++++++++++++++++++++++++\n")



def test5():
    print(f"===  TEST 5  ++++++++++++++++++++++++++++++++++++")

    b = ClassB()

    # is logging on (True)?  muted (False)?   not even set up yet (None)?
    # Currently we expect the subclass to turn on logging in its __init__.
    # See details in LoggerABC.
    print(f"@@T5@197  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True
    print()

    print(f"+++ turn on logging +++")
    r = b.enable_logger(True)
    print(f"@@T5@203   set logger(True) returned {r=}")
    assert r is True
    del r
    #
    # is it on?
    print(f"@@T5@208  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True
    b.do_logging("from Test3@61  EXPECT THIS GETS LOGGED")

    print()
    print("+++ turn logging off +++++")
    r = b.enable_logger(False)
    print(f"@@T5@215   set logger(False) returned {r=}")
    assert r is False
    del r
    b.do_logging("from Test3@69   EXPECTED THIS IS MUTED")

    print()
    print(f"+++ re-enable logging +++")
    r = b.enable_logger(True)
    print(f"@@T5@223   Reenable: set logger(True) returned {r=}")
    assert r is True
    del r
    #
    # is it on?
    print(f"@@T5@228  Get the logger status; expect True: {ClassA.get_logger_status()}")
    assert ClassA.get_logger_status() is True
    b.do_logging("from Test @T5@230  RE-ENABLE  EXPECT THIS GETS LOGGED ALSO")

    print(f"===  end of TEST 5  ++++++++++++++++++++++++++++++++++++\n")


def test6():
    print(f"===  TEST 6  ++++++++++++++++++++++++++++++++++++")

    b = ClassB()

    got_ex_stg = ""
    try:
        b.get_logger_status()
    except Exception as ex:
        got_ex_stg = str(ex)
        print(f"@@T6@244  Got expected exception: ex.repr={repr(ex)}")
        print(f"@@T6@245  Got expected exception: ex.str ={repr(ex)}")
    print(f"@@T6@247  Got exception: {got_ex_stg=}")
    assert "SHOULD NEVER BE CALLED BEFORE LOGGING IS INITIALIZED" in got_ex_stg
    print(f"===  end of TEST 6  ++++++++++++++++++++++++++++++++++++\n")


def main(args):
    test6()
def SAVED():
    if len(args) > 0:
        print(f"MAIN: {args=}")
        tests = list(args)
    else:
        tests = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ]
    print(f"MAIN: {tests=}")
    if '1' in tests: test1()
    if '2' in tests: test2()
    if '3' in tests: test3()
    if '4' in tests: test4()
    if '5' in tests: test5()
    if '6' in tests: test6()

if __name__ == "__main__":
    main(sys.argv[1:])

###
