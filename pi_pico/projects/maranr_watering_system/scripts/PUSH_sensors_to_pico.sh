#!/bin/bash
#
# PUSH_SENSORS_to_pico.sh
#
# sensors/ -  push the repo files to the pico
# 
rm -rf sensors/__pycache__


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi


#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo '**** CLEANUP for sensors IS NOT DONE YET ***************'
    # echo 'CLEANUP: copy the cleanup program and run it'
    # mpremote ${PREM_DEVICE} fs cp remove_old_watering_files.py  :/
    # echo '   Run the cleanup'
    # mpremote ${PREM_DEVICE} run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    echo 'Copy contents of dir  sensors'
    mpremote ${PREM_DEVICE} fs cp -r sensors :
    
    #echo 'Remove the files we do not need'
    #mpremote ${PREM_DEVICE} fs rm sensors/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote ${PREM_DEVICE} fs ls 
    
    mpremote ${PREM_DEVICE} fs ls /sensors
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
