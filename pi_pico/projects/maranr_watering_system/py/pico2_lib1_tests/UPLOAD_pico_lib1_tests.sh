#!/bin/bash
#
# UPLOAD_pico_lib1_tests.sh
#
# Upload the PICO-based lib1 tests to /tmp/
# This is used to interchange the files with the CPYthon support in
# ~/git/art/src/python3/pico_support_tests/maranr_watering_system/

DBG=false

TMP_DIR=/tmp/PICO_LIB1_TESTS
LOCAL_DIR=.

mkdir -p $TMP_DIR


for fp in ${LOCAL_DIR}/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [[ $fn = "__pycache__" ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == *QPUSH_MARK* ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == *DEPRECATED ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == COMPARE*.sh ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == PUSH*.sh ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == DOWNLOAD*.sh ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi
    if [[ $fn == UPLOAD*.sh ]] ; then
        if $DBG ; then echo ' SKIP THIS ' $fn ; fi
        continue
    fi


    TMP_F="${TMP_DIR}/${fn}"

    if [ ! -f "${TMP_F}" ] ; then
        if $DBG ; then  echo '*** DOES NOT EXIST *** ' ${TMP_F} ' -- CREATING IT.'; fi
        touch -d '1980-01-01 12:34:55' ${TMP_F}
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
        "  cp -a ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn"
           cp -a ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn
    fi

done

rm -f ${TMP_DIR}/*QPUSH_MARKER*
rm -f ${TMP_DIR}/*DEPRECATED

###
