#!/bin/sh
#
# copy all files to the pico

rm -rf http/__pycache__

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

    ./PUSH_LIB_FILES_to_pico.sh
    ./PUSH_PRIMITIVES_to_pico.sh
    ./PUSH_HTTP_to_pico.sh
    ./PUSH_DISPLAYS_to_pico.sh

    echo 'Copy the MAIN program'
    mpremote fs cp watering_project_main.py :/main.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    
    mpremote fs ls /lib
    mpremote fs ls /primitives
    mpremote fs ls /http
    mpremote fs ls /displays
    mpremote fs ls 
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
