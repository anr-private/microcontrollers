#!/bin/bash
#
# DOWNLOAD_lib2.sh

DBG=false

for fp in lib2/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q lib2/$fn  /tmp/LIB2/$fn" ; fi
    diff -q lib2/$fn  /tmp/LIB2/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  lib2/$fn  /tmp/LIB2/$fn" ; fi
        echo \
        "  cp -p /tmp/LIB2/$fn  lib2/$fn  "
           cp -p /tmp/LIB2/$fn  lib2/$fn
    fi

done


#cp -p lib2/* /tmp/LIB2/

###
