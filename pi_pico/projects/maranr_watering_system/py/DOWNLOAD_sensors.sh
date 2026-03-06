#!/bin/bash
#
# DOWNLOAD_sensors.sh

DBG=false

for fp in /tmp/SENSORS/* ; do

    if $DBG ; then  echo ff is $fp ; fi
    fn=$(basename $fp)
    if $DBG ; then echo fn is $fn ; fi

    if $DBG ; then echo \
    "diff -q  /tmp/SENSORS/$fn  sensors/$fn  " ; fi
    diff  -q  /tmp/SENSORS/$fn  sensors/$fn  
    result="$?"
    if [ "$result" == 0 ] ; then
        if $DBG ; then echo matches ; fi
    fi
    if [ "$result" == 1 ] ; then
        if $DBG ; then echo "NOT matches  sensors/$fn  /tmp/SENSORS/$fn" ; fi
        echo \
        "cp -p /tmp/SENSORS/$fn  sensors/$fn  "
        cp  -p /tmp/SENSORS/$fn  sensors/$fn
    fi

done


#cp -p sensors/* /tmp/SENSORS/

###
