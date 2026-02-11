#!/bin/sh
#
# copy all files to the pico

rm -rf anr_http/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    mpremote fs cp remove_old_watering_files.py  :/
    echo '   Run the cleanup'
    mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {
    echo 'Copy contents of dir  anr_http'
    mpremote fs cp -r anr_http :
    
    echo 'Copy anr_http_client.py'
    mpremote fs cp anr_http_client/anr_http_client.py :/
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote fs ls 
    
    mpremote fs ls /anr_http
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
