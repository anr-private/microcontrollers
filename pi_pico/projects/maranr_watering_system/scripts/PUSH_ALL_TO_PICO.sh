#!/bin/bash
#
# PUSH_ALL_TO_PICO.sh
#
# copy all files to the pico

SCRIPTS_DIR='../scripts'


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' || "$PREM_DEVICE" == 'a2' || "$PREM_DEVICE" == 'a3' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi


rm -rf */__pycache__

# USE  'REMOVE_ALL_from_pico.sh'
###
####--- get rid of the old stuff ---
###clean_up_old_dirs_and_files() {
###    echo 'CLEANUP: copy the cleanup program and run it'
###    mpremote ${PREM_DEVICE} fs cp remove_old_watering_files.py  :/
###    echo '   Run the cleanup'
###    mpremote ${PREM_DEVICE} run remove_old_watering_files.py
###    echo 'CLEANUP is done'
###    echo '----------------'
###}


#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    ${SCRIPTS_DIR}/PUSH_displays_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_lib_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_lib2_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_logger_elem_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_mws_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_primitives_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_sensors_to_pico.sh
    ${SCRIPTS_DIR}/PUSH_weblib_to_pico.sh
    echo 'Copy the MAIN program'
    ${SCRIPTS_DIR}/PUSH_main_to_pico.sh
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    
    mpremote ${PREM_DEVICE} fs ls /displays
    mpremote ${PREM_DEVICE} fs ls /lib
    mpremote ${PREM_DEVICE} fs ls /lib2
    mpremote ${PREM_DEVICE} fs ls /logger_elem
    mpremote ${PREM_DEVICE} fs ls /mws
    mpremote ${PREM_DEVICE} fs ls /primitives
    mpremote ${PREM_DEVICE} fs ls /sensors
    mpremote ${PREM_DEVICE} fs ls /weblib
    mpremote ${PREM_DEVICE} fs ls 
}

main() {
    echo "PUSH_ALL_TO_PICO.sh  MAIN-PGM"
    ###clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
