#!/bin/bash
#
# COMPARE_pico_lib1_tests.sh

TMP_DIR=/tmp/PICO_LIB1_TESTS
LOCAL_DIR=.


diff -q lib1 /tmp/LIB1  |grep -v __QPUSH_MARKER__ |grep -v DEPRECATED


###
