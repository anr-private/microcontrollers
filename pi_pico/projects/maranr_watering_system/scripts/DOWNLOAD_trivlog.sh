#!/bin/bash
#
# DOWNLOAD_trivlog.sh

DBG=false

for fp in /tmp/TRIVLOG/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/TRIVLOG/$fn  trivlog/$fn  " ; fi
    diff  -q  /tmp/TRIVLOG/$fn  trivlog/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  trivlog/$fn  /tmp/TRIVLOG/$fn" ; fi
        echo \
        "cp -p /tmp/TRIVLOG/$fn  trivlog/$fn  "
        cp  -p /tmp/TRIVLOG/$fn  trivlog/$fn
    fi

done


#cp -p trivlog/* /tmp/TRIVLOG/

###
