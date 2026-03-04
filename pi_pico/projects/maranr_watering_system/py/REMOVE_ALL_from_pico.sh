#!/bin/sh
#
# REMOVE_ALL_from_pico.sh
#
# remove everything from pico

rm -rf displays/__pycache__
rm -rf http/__pycache__
rm -rf lib/__pycache__
rm -rf primitives/__pycache__
rm -rf sensors/__pycache__
rm -rf trivlog/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    mpremote fs cp remove_old_watering_files.py  :/
    echo '   Run the cleanup'
    mpremote run remove_old_watering_files.py
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
