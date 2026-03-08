#!/bin/bash
#
# DOWNLOAD_lib.sh

DBG=false

for fp in lib/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q lib/$fn  /tmp/LIB/$fn" ; fi
    diff -q lib/$fn  /tmp/LIB/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  lib/$fn  /tmp/LIB/$fn" ; fi
        echo \
        "  cp -p /tmp/LIB/$fn  lib/$fn  "
           cp -p /tmp/LIB/$fn  lib/$fn
    fi

done


#cp -p lib/* /tmp/LIB/

###
