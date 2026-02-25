#!/bin/bash
#
# DELETE_ALL_from_pico.sh

clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    #mpremote fs cp remove_old_watering_files.py  :/
    #echo '   Run the cleanup'
    #mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

main() {
    echo "DELETE_ALL_from_pico -- MAIN"
    clean_up_old_dirs_and_files
}

main $*


###
