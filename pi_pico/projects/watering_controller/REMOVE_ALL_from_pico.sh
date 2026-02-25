#!/bin/bash
#
# REMOVE_ALL_from_pico.sh

clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    mpremote fs cp remove_all_mws_dirs_and_files.py  :/
    echo '   Run the cleanup'
    mpremote run remove_all_mws_dirs_and_files.py
    mpremote fs rm remove_all_mws_dirs_and_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

main() {
    echo "REMOVE_ALL_from_pico -- MAIN"
    clean_up_old_dirs_and_files
}

main $*


###
