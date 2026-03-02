#!/bin/bash
#
# UPLOAD_logger.sh

DBG=false

for fp in logger/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q logger/$fn  /tmp/LOGGER/$fn" ; fi
    diff -q logger/$fn  /tmp/LOGGER/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  logger/$fn  /tmp/LOGGER/$fn" ; fi
        echo \
        "  cp -p logger/$fn  /tmp/LOGGER/$fn"
           cp -p logger/$fn  /tmp/LOGGER/$fn
    fi

done


#cp -p logger/* /tmp/LOGGER/

###
