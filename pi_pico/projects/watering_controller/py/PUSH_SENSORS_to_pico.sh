#!/bin/sh
#
# PUSH_SENSORS_to_pico.sh
#
# sensors/ -  push the repo files to the pico
# 
rm -rf sensors/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo '**** CLEANUP for sensors IS NOT DONE YET ***************'
    # echo 'CLEANUP: copy the cleanup program and run it'
    # mpremote fs cp remove_old_watering_files.py  :/
    # echo '   Run the cleanup'
    # mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    echo 'Copy contents of dir  sensors'
    mpremote fs cp -r sensors :
    
    #echo 'Remove the files we do not need'
    #mpremote fs rm sensors/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote fs ls 
    
    mpremote fs ls /sensors
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
