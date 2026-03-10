#!/bin/bash
#
# PUSH_lib_tests_to_pico.sh
#
# NOTE you do not need to do this
# You can just run the test_file_utils.py directly from the linux filesystem.
# No need to copy to the pico.
# You do need the MWS stuff installed - lib/ logger_elem/



clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    echo '*** NOT IMPLEMENETED YET ***'
    #mpremote fs cp remove_old_watering_files.py  :/
    #echo '   Run the cleanup'
    #mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {
    echo 'make remote lib_tests/'
    mpremote fs mkdir :lib_tests

    echo 'Copy files to lib_tests/ '
    mpremote fs cp test_file_utils.py :/lib_tests/test_file_utils.py 
    
    #echo 'Remove the client files we do not need'
    #mpremote fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /lib_tests'
    mpremote fs ls /lib_tests
}


main() {
    echo "PUSH_LIB_FILES_TO_PICO -- MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
