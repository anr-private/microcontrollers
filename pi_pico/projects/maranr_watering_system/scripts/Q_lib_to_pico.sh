#!/bin/bash
#
# Q_lib_to_pico.sh
# 
# Quick-push just the updated files to the Pico

TIMESTAMP_MARKER_FILE="__QPUSH_MARKER__"

LOCAL_DIR="lib"

DBG=false
VERBOSE=false
BOTH=false

# touch -d "2024-01-15 14:30:00" report.txt


get_marker_timestamp() {
    # returns the timestamp as an int
    local MARKER="$1"   ###"${LOCAL_DIR}/${TIMESTAMP_MARKER_FILE}"
    if [ ! -f ${MARKER} ] ; then
        echo '********* CANNOT FILE THE TIMESTAMP MARKER  ************'
        echo '  Looking for ' ${MARKER}
        echo '********** SO USING A VERY OLD TIMESAMP  **********'
        touch -d "1980-01-02 00:01:02" ${MARKER}
    fi
    ts=$(stat -c %Y ${MARKER})
    echo $ts
}

#--- copy the new stuff to the Pico ---
copy_changed_files_to_the_pico() {
    # 1 is the marker file path for this dir


    local ts_ref="$1"

    if $VERBOSE ; then
        echo "copy_changed_files_to_the_pico  ts_ref is ${ts_ref}"
    fi
    if $DBG ; then
        echo "Copy contents of ${LOCAL_DIR}/ "
    fi

    for fpath in ${LOCAL_DIR}/* ; do

        if $BOTH ; then  echo ' ' ; echo fpath is $fpath ; fi
        fname=$(basename $fpath)
        if $DBG ; then echo fname is $fname ; fi

        if [ "${fname}" = "${TIMESTAMP_MARKER_FILE}" ] ; then
            if $DBG ; then echo 'SKIP THE MARKER!!!!! ' ; fi
            continue
        fi

        local ts=$(stat -c %Y  ${fpath})
        if $DBG ; then echo 'ts is ' $ts ; fi

        if ((ts <= ts_ref)); then
            if $VERBOSE ; then 
                #local s=$(ls -l ${fpath} | cut -c 24-)
                echo '  Already up-to-date  its TIMESTAMP is OLD  ' $ts '<=' $ts_ref "   " $((ts_ref-ts))
            fi
            ###ls -l ${fpath}
            continue
        fi
        echo 'DO THIS ONE!' $fpath

        echo \
        "mpremote ${PREM_DEVICE} fs cp ${fpath}  :"
         mpremote ${PREM_DEVICE} fs cp ${fpath}  :

    done


    ###mpremote ${PREM_DEVICE} fs cp -r lib   :
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote ${PREM_DEVICE} fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /lib'
    mpremote ${PREM_DEVICE} fs ls /lib
}


main() {
    ###echo "QUICK-PUSH_LIB_FILES_TO_PICO "

    if [ "$1" = "D" -o  "$1" = "d" ] ; then
        echo '________________________ DEBUG ENABLED   _______________'
        DBG=true
    fi
    if [ "$1" = "V" -o  "$1" = "v" ] ; then
        echo '________________________ VERBOSE ENABLED   _______________'
        VERBOSE=true
    fi
    if [ "$1" = "DV"  -o  "$1" = "dv" ] ; then
        echo '________________________ DEBUG and VERBOSE BOTH ENABLED   _______________'
        DBG=true
        VERBOSE=true
        BOTH=true
    fi


    local MARKER_FPATH="${LOCAL_DIR}/${TIMESTAMP_MARKER_FILE}"

    local ref_tstamp=$(get_marker_timestamp ${MARKER_FPATH})
    if $VERBOSE ; then 

        local s=$(ls -l ${MARKER_FPATH} | cut -c 23-)
        echo "MARKER: ${MARKER_FPATH}  ref_tstamp=${ref_tstamp}  ${s}"
    fi

    copy_changed_files_to_the_pico ${ref_tstamp}

    if $VERBOSE ; then echo 'UPDATE the marker file ' ${MARKER_FPATH} ; fi
    touch ${MARKER_FPATH}
}


main $*


###
