#!/bin/bash
#
# DOWNLOAD_primitives.sh

DBG=false

for fp in /tmp/PRIMITIVES/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/PRIMITIVES/$fn  primitives/$fn  " ; fi
    diff  -q  /tmp/PRIMITIVES/$fn  primitives/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  primitives/$fn  /tmp/PRIMITIVES/$fn" ; fi
        echo \
        "cp -p /tmp/PRIMITIVES/$fn  primitives/$fn  "
        cp  -p /tmp/PRIMITIVES/$fn  primitives/$fn
    fi

done


#cp -p primitives/* /tmp/PRIMITIVES/

###
