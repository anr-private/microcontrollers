#!/bin/bash
#
# UPLOAD_displays.sh

DBG=false

for fp in displays/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q displays/$fn  /tmp/DISPLAYS/$fn" ; fi
    diff -q displays/$fn  /tmp/DISPLAYS/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  displays/$fn  /tmp/DISPLAYS/$fn" ; fi
        echo \
        "  cp -p displays/$fn  /tmp/DISPLAYS/$fn"
           cp -p displays/$fn  /tmp/DISPLAYS/$fn
    fi

done


#cp -p displays/* /tmp/DISPLAYS/

###
