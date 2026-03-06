#!/bin/bash
#
# UPLOAD_primitives.sh

DBG=false

for fp in primitives/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q primitives/$fn  /tmp/PRIMITIVES/$fn" ; fi
    diff -q primitives/$fn  /tmp/PRIMITIVES/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  primitives/$fn  /tmp/PRIMITIVES/$fn" ; fi
        echo \
        "  cp -p primitives/$fn  /tmp/PRIMITIVES/$fn"
           cp -p primitives/$fn  /tmp/PRIMITIVES/$fn
    fi

done


#cp -p primitives/* /tmp/PRIMITIVES/

###
