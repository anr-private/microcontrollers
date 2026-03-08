#!/bin/bash
#
# UPLOAD_sensors.sh

DBG=false

for fp in sensors/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    # ignore
    if [ "$fn" = "__pycache__" ] ; then
        continue
    fi

    if $DBG ; then echo \
    "diff -q sensors/$fn  /tmp/SENSORS/$fn" ; fi
    diff -q sensors/$fn  /tmp/SENSORS/$fn
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  sensors/$fn  /tmp/SENSORS/$fn" ; fi
        echo \
        "  cp -p sensors/$fn  /tmp/SENSORS/$fn"
           cp -p sensors/$fn  /tmp/SENSORS/$fn
    fi

done


#cp -p sensors/* /tmp/SENSORS/

###
