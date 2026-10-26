#!/bin/bash
#
# PUSH_pico_lib1_tests_to_PICO.sh
#
# 

REMOTE_DIR="pico_lib1_tests"
REMOTE_LIBFAKE_DIR="lib1_FAKE"

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
    echo 'make remote dir: '${REMOTE_DIR}/
    mpremote ${PREM_DEVICE} fs mkdir :${REMOTE_DIR}

    echo 'make remote subdir: '${REMOTE_LIBFAKE_DIR}/
    mpremote ${PREM_DEVICE} fs mkdir :${REMOTE_LIBFAKE_DIR}

    echo 'Copy files to ' ${REMOTE_DIR}/
    mpremote ${PREM_DEVICE} fs cp pico_test_read_last_n_lines.py :/${REMOTE_DIR}/pico_test_read_last_n_lines.py 

    echo 'Copy files to ' ${REMOTE_LIBFAKE_DIR}/
    mpremote ${PREM_DEVICE} fs cp read_last_n_lines.py :/${REMOTE_LIBFAKE_DIR}/read_last_n_lines.py 
    
    #echo 'Remove the client files we do not need'
    #mpremote fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote fs ls 
    echo ' '    
    echo 'LIST THE PICO remote dir CONTENTS: '${REMOTE_DIR}/
    mpremote ${PREM_DEVICE} fs ls /${REMOTE_DIR}
    echo 'LIST THE PICO remote subdir CONTENTS: '${REMOTE_LIBFAKE_DIR}/
    mpremote ${PREM_DEVICE} fs ls /${REMOTE_LIBFAKE_DIR}
}


main() {
    echo "PUSH_PICO_LIB1_TESTS_TO_PICO:"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*

#${REMOTE_DIR}

###
