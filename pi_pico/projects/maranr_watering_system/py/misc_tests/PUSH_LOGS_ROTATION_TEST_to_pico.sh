#!/bin/bash
#
# PUSH_LOGS_ROTATION_TEST_to_pico.sh


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' ]] ; then
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
    #echo 'Make subdir :pages/ on pico'
    #mpremote ${PREM_DEVICE} fs mkdir :pages

    echo 'Copy logs_rotation_test.py to Pico'
    mpremote ${PREM_DEVICE} fs cp ./logs_rotation_test.py   :
    
    #echo 'Remove the client files we do not need'
    #mpremote ${PREM_DEVICE} fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote ${PREM_DEVICE} fs ls 
    #echo ' '    
    #echo 'LIST THE PICO CONTENTS: /pages'
    #mpremote ${PREM_DEVICE} fs ls /pages
}


main() {
    echo "PUSH_LOGS_ROTATION_TEST_to_pico:"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
