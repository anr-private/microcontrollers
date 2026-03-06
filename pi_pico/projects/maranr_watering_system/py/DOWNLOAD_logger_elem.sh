#!/bin/bash
#
# DOWNLOAD_logger_elem.sh

DBG=false

for fp in /tmp/TRIVLOG/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/TRIVLOG/$fn  logger_elem/$fn  " ; fi
    diff  -q  /tmp/TRIVLOG/$fn  logger_elem/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  logger_elem/$fn  /tmp/TRIVLOG/$fn" ; fi
        echo \
        "cp -p /tmp/TRIVLOG/$fn  logger_elem/$fn  "
        cp  -p /tmp/TRIVLOG/$fn  logger_elem/$fn
    fi

done


#cp -p logger_elem/* /tmp/TRIVLOG/

###
