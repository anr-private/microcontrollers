#!/bin/bash
#
# UPLOAD_trivlog.sh

DBG=false

for fp in trivlog/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q trivlog/$fn  /tmp/TRIVLOG/$fn" ; fi
    diff -q trivlog/$fn  /tmp/TRIVLOG/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  trivlog/$fn  /tmp/TRIVLOG/$fn" ; fi
        echo \
        "  cp -p trivlog/$fn  /tmp/TRIVLOG/$fn"
           cp -p trivlog/$fn  /tmp/TRIVLOG/$fn
    fi

done


#cp -p trivlog/* /tmp/TRIVLOG/

###
