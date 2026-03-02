#!/bin/bash
#
# DOWNLOAD_logger.sh

DBG=false

for fp in /tmp/LOGGER/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/LOGGER/$fn  logger/$fn  " ; fi
    diff  -q  /tmp/LOGGER/$fn  logger/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  logger/$fn  /tmp/LOGGER/$fn" ; fi
        echo \
        "cp -p /tmp/LOGGER/$fn  logger/$fn  "
        cp  -p /tmp/LOGGER/$fn  logger/$fn
    fi

done


#cp -p logger/* /tmp/LOGGER/

###
