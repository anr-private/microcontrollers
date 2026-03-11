#!/bin/bash
#
# UPLOAD_lib2.sh

DBG=false

for fp in lib2/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

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
        "  cp -p lib2/$fn  /tmp/LIB2/$fn"
           cp -p lib2/$fn  /tmp/LIB2/$fn
    fi

done


#cp -p lib2/* /tmp/LIB2/

###
