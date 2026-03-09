#!/bin/sh
#
# PUSH_ALL_TO_PICO.sh
#
# copy all files to the pico

SCRIPTS_DIR='../scripts'

rm -rf */__pycache__

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

    ${SCRIPTS_DIR}/PUSH_displays_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_lib_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_logger_elem_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_primitives_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_sensors_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_weblib_to_pico.sh
    echo 'Copy the MAIN program'
    ${SCRIPTS_DIR}/PUSH_sensors_to_pico.sh
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    
    mpremote fs ls /displays
    mpremote fs ls /lib
    mpremote fs ls /logger_elem
    mpremote fs ls /primitives
    mpremote fs ls /sensors
    mpremote fs ls /weblib
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
