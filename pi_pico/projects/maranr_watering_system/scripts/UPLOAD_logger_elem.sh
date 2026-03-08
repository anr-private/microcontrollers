#!/bin/bash
#
# UPLOAD_logger_elem.sh

DBG=false

for fp in logger_elem/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q logger_elem/$fn  /tmp/LOGELEM/$fn" ; fi
    diff -q logger_elem/$fn  /tmp/LOGELEM/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  logger_elem/$fn  /tmp/LOGELEM/$fn" ; fi
        echo \
        "  cp -p logger_elem/$fn  /tmp/LOGELEM/$fn"
           cp -p logger_elem/$fn  /tmp/LOGELEM/$fn
    fi

done


#cp -p logger_elem/* /tmp/LOGELEM/

###
