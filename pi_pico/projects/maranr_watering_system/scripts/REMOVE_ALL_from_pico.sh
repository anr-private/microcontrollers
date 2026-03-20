#!/bin/sh
#
# REMOVE_ALL_from_pico.sh
#
# remove everything from pico

rm -rf */__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    mpremote ${PREM_DEVICE} fs cp remove_MWS_files.py  :/
    echo '   Run the cleanup'
    mpremote ${PREM_DEVICE} run remove_MWS_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}


main() {
    echo "REMOVE_ALL_from_pico.sh  MAIN-PGM"
    clean_up_old_dirs_and_files
#    copy_release_files_to_the_pico
#    list_pico_filesystem_contents
}

main $*


###
