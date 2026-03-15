#!/bin/bash
#
# DOWNLOAD_weblib.sh

DBG=false

TMP_DIR=/tmp/WEBLIB
LOCAL_DIR=weblib

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

    fn_extension="${fn##*.}"
    if $DBG ; then echo "extension of $fn is $fn_extension" ; fi

    if [ "$fn" = "ARCHIVE" ] ; then
        if $DBG ; then echo '@17 SKIP THIS: ' $fn ; fi
        continue
    fi
    if [ "$fn_extension" = "ARCHIVE" ] ; then
        if $DBG ; then echo '@21 SKIP THIS: ' $fn ; fi
        continue
    fi
    if [ "$fn_extension" = "COPY" ] ; then
        if $DBG ; then echo '@25 SKIP THIS: ' $fn ; fi
        continue
    fi

    if $DBG ; then echo \
    "diff -q ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn" ; fi
    diff  -q ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  ${LOCAL_DIR}/$fn  ${TMP_DIR}/$fn" ; fi
        echo \
        "cp -p ${TMP_DIR}/$fn  ${LOCAL_DIR}/$fn  "
        cp  -p ${TMP_DIR}/$fn  ${LOCAL_DIR}/$fn
    fi

done


#cp -p ${LOCAL_DIR}/* ${TMP_DIR}/

###
