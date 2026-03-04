#!/bin/sh
#
# PUSH_ALL_TO_PICO.sh
#
# copy all files to the pico

rm -rf displays/__pycache__
rm -rf http/__pycache__
rm -rf lib/__pycache__
rm -rf primitives/__pycache__
rm -rf sensors/__pycache__
rm -rf trivlog/__pycache__

# USE  'REMOVE_ALL_from_pico.sh'
###
####--- get rid of the old stuff ---
###clean_up_old_dirs_and_files() {
###    echo 'CLEANUP: copy the cleanup program and run it'
###    mpremote fs cp remove_old_watering_files.py  :/
###    echo '   Run the cleanup'
###    mpremote run remove_old_watering_files.py
###    echo 'CLEANUP is done'
###    echo '----------------'
###}


#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    ./PUSH_displays_to_pico.sh.sh
    ./PUSH_http_to_pico.sh.sh
    ./PUSH_lib_to_pico.sh.sh
    ./PUSH_primitives_to_pico.sh.sh
    ./PUSH_sensors_to_pico.sh.sh
    ./PUSH_trivlog_to_pico.sh

    echo 'Copy the MAIN program'
    ./PUSH_sensors_to_pico.sh.sh
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    
    mpremote fs ls /displays
    mpremote fs ls /http
    mpremote fs ls /lib
    mpremote fs ls /primitives
    mpremote fs ls /sensors
    mpremote fs ls /trivlog
    mpremote fs ls 
}

main() {
    echo "PUSH_ALL_TO_PICO.sh  MAIN-PGM"
    ###clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
