#!/bin/bash
#
# PUSH_PRIMITIVES_TO_PICO.sh
#
# Peter Hinch primitives/


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' || "$PREM_DEVICE" == 'a2' || "$PREM_DEVICE" == 'a3' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi


clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    echo '*** NOT IMPLEMENETED YET ***'
    #mpremote ${PREM_DEVICE} fs cp remove_old_watering_files.py  :/
    #echo '   Run the cleanup'
    #mpremote ${PREM_DEVICE} run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {
    echo 'Copy contents of primitives/ '
    mpremote ${PREM_DEVICE} fs cp -r primitives   :
    
    #echo 'Remove the client files we do not need'
    #mpremote ${PREM_DEVICE} fs rm primitives/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote ${PREM_DEVICE} fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /primitives'
    mpremote ${PREM_DEVICE} fs ls /primitives
}


main() {
    echo "PUSH_LIB_FILES_TO_PICO -- MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
