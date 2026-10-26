#!/bin/bash
#
# DOWNLOAD_lib1_tests.sh
#
# Download the lib1 tests from /tmp/
# This is used to interchange the files with the CPYthon support in
# ~/git/art/src/python3/pico_support_tests/maranr_watering_system/

DBG=false

TMP_DIR=/tmp/LIB1
LOCAL_DIR=lib1

if [ ! -d ${TMP_DIR} ] ; then
    echo '*******************************************************'
    echo '*******************************************************'
    echo 'NO SUCH DIR: '  ${TMP_DIR}
    echo '*******************************************************'
    echo '*******************************************************'
    exit 9
fi


for fp in ${LOCAL_DIR}/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if [[ $fn == *QPUSH_MARK* ]] ; then
        continue
    fi
    if [[ $fn == *DEPRECATED ]] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn" ; fi
    diff -q ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn" ; fi
        echo \
        "  cp -p ${TMP_DIR}/$fn  ${LOCAL_DIR}/$fn  "
           cp -p ${TMP_DIR}/$fn  ${LOCAL_DIR}/$fn
    fi

done


#cp -p ${LOCAL_DIR}/* ${TMP_DIR}/

###
