#!/bin/bash
#
# COMPARE_pico_lib1_tests.sh

TMP_DIR=/tmp/PICO_LIB1_TESTS
LOCAL_DIR=.


diff -q ${LOCAL_DIR} ${TMP_DIR}  | \
 grep -v __QPUSH_MARKER__ | \
 grep -v DEPRECATED | \
 grep -v COMPARE_pico_lib1_tests.sh | \
 grep -v DOWNLOAD_pico_lib1_tests.sh | \
 grep -v UPLOAD_pico_lib1_tests.sh | \
 grep -v PUSH_pico_lib1_tests_to_PICO.sh | \
 grep -v PUSH_test_files_to_pico.sh



###
