#!/bin/bash
#
# UPLOAD_lib2.sh

DBG=false

TMP_DIR=/tmp/LIB2
LOCAL_DIR=lib2

mkdir -p $TMP_DIR


for fp in ${LOCAL_DIR}/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    TMP_F="${TMP_DIR}/${fn}"

    if [ ! -f "${TMP_F}" ] ; then
        if $DBG ; then  echo '*** DOES NOT EXIST *** ' ${TMP_F} ; fi
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
        "  cp -p ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn"
           cp -p ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn
    fi

done


#cp -p ${LOCAL_DIR}/* ${TMP_DIR}/

###
