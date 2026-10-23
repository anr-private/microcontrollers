#!/bin/bash
#
# COMPARE_lib1.sh

diff -q lib1 /tmp/LIB1  |grep -v __QPUSH_MARKER__ |grep -v DEPRECATED


###
