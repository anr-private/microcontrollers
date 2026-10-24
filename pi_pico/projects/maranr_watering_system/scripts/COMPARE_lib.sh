#!/bin/bash
#
# COMPARE_lib.sh

diff -q lib /tmp/LIB  |grep -v __QPUSH_MARKER__ |grep -v DEPRECATED


###
