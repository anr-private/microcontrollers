#!/bin/bash
#
# PUSH_DISPLAYS_to_pico.sh
#
# displays/ -  push the repo files to the pico


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi

rm -rf displays/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo '**** CLEANUP for displays IS NOT DONE YET ***************'
    # echo 'CLEANUP: copy the cleanup program and run it'
    # mpremote fs cp remove_old_watering_files.py  :/
    # echo '   Run the cleanup'
    # mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    echo 'Copy contents of dir  displays'
    mpremote $PREM_DEVICE fs cp -r displays :
    
    #echo 'Remove the files we do not need'
    #mpremote fs rm displays/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote $PREM_DEVICE fs ls 
    
    mpremote  $PREM_DEVICE fs ls /displays
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
