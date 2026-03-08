#!/bin/bash
#
# DOWNLOAD_displays.sh

DBG=false

for fp in /tmp/DISPLAYS/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/DISPLAYS/$fn  displays/$fn  " ; fi
    diff  -q  /tmp/DISPLAYS/$fn  displays/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  displays/$fn  /tmp/DISPLAYS/$fn" ; fi
        echo \
        "cp -p /tmp/DISPLAYS/$fn  displays/$fn  "
        cp  -p /tmp/DISPLAYS/$fn  displays/$fn
    fi

done


#cp -p displays/* /tmp/DISPLAYS/

###
