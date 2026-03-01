#!/bin/bash
#
# UPLD_http.sh

DBG=false

for fp in http/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q http/$fn  /tmp/HTTP/$fn" ; fi
    diff -q http/$fn  /tmp/HTTP/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  http/$fn  /tmp/HTTP/$fn" ; fi
        echo \
        "  cp -p http/$fn  /tmp/HTTP/$fn"
           cp -p http/$fn  /tmp/HTTP/$fn
    fi

done


#cp -p http/* /tmp/HTTP/

###
