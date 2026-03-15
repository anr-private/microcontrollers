#!/bin/bash
#
# DOWNLOAD_main.sh

FILES='
maranr_watering_system_main.py
'

DBG=false

TMP_DIR=/tmp/MAIN
###LOCAL_DIR=./

if [ ! -d ${TMP_DIR} ] ; then
    echo '*******************************************************'
    echo '*******************************************************'
    echo 'NO SUCH DIR: '  ${TMP_DIR}
    echo '*******************************************************'
    echo '*******************************************************'
    exit 9
fi


for fp in $FILES ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q $fn  ${TMP_DIR}/$fn" ; fi
    diff  -q $fn  ${TMP_DIR}/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  $fn  ${TMP_DIR}/$fn" ; fi
        echo \
        "  cp -p ${TMP_DIR}/$fn  $fn  "
           cp -p ${TMP_DIR}/$fn  $fn
    fi

done


#cp -p * ${TMP_DIR}/

###
