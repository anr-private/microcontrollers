#!/bin/bash
#
# UPLOAD_main.sh

FILES='
maranr_watering_system_main.py
'

DBG=false

TMP_DIR=/tmp/MAIN
###LOCAL_DIR=./

mkdir -p $TMP_DIR


for fp in $FILES ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    TMP_F="${TMP_DIR}/${fn}"

    if [ ! -f "${TMP_F}" ] ; then
        if $DBG ; then  echo '*** DOES NOT EXIST *** ' ${TMP_F} ; fi
        touch -d '1980-01-01 12:34:55' ${TMP_F}
    fi

    if $DBG ; then echo \
    "diff -q $fn  ${TMP_DIR}/$fn" ; fi
    diff -q $fn  ${TMP_DIR}/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  $fn  ${TMP_DIR}/$fn" ; fi
        echo \
        "  cp -p $fn  ${TMP_DIR}/$fn"
           cp -p $fn  ${TMP_DIR}/$fn
    fi

done


#cp -p * ${TMP_DIR}/

###
