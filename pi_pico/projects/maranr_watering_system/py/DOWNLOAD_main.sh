#!/bin/bash
#
# DOWNLOAD_main.sh

FILES='
maranr_watering_system_main.py
'

DBG=false

for fp in $FILES ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q $fn  /tmp/MAIN/$fn" ; fi
    diff  -q $fn  /tmp/MAIN/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  $fn  /tmp/MAIN/$fn" ; fi
        echo \
        "  cp -p tmp/MAIN/$fn  $fn  "
           cp -p tmp/MAIN/$fn  $fn
    fi

done


#cp -p * /tmp/MAIN/

###
