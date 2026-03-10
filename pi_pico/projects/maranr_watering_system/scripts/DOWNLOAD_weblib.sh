#!/bin/bash
#
# DOWNLOAD_weblib.sh

DBG=false

for fp in weblib/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    fn_extension="${fn##*.}"
    if $DBG ; then echo "extension of $fn is $fn_extension" ; fi

    if [ "$fn" = "ARCHIVE" ] ; then
        if $DBG ; then echo '@17 SKIP THIS: ' $fn ; fi
        continue
    fi
    if [ "$fn_extension" = "ARCHIVE" ] ; then
        if $DBG ; then echo '@21 SKIP THIS: ' $fn ; fi
        continue
    fi
    if [ "$fn_extension" = "COPY" ] ; then
        if $DBG ; then echo '@25 SKIP THIS: ' $fn ; fi
        continue
    fi

    if $DBG ; then echo \
    "diff -q weblib/$fn  /tmp/WEBLIB/$fn" ; fi
    diff  -q weblib/$fn  /tmp/WEBLIB/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  weblib/$fn  /tmp/WEBLIB/$fn" ; fi
        echo \
        "cp -p /tmp/WEBLIB/$fn  weblib/$fn  "
        cp  -p /tmp/WEBLIB/$fn  weblib/$fn
    fi

done


#cp -p weblib/* /tmp/WEBLIB/

###
