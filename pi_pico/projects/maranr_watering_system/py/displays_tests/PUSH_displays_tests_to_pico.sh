#!/bin/bash
#
# PUSH_displays_tests_to_pico.sh
#
# NOTE you do not need to do this
# You can just run the test_XXX.py directly from the linux filesystem.
# No need to copy to the pico.
# You do need some of the MWS stuff installed - lib/ logger_elem/

if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' || "$PREM_DEVICE" == 'a2' || "$PREM_DEVICE" == 'a3' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi

clean_up_old_dirs_and_files() {
    echo 'CLEANUP: copy the cleanup program and run it'
    echo '*** NOT IMPLEMENETED YET ***'
    #mpremote ${PREM_DEVICE}  fs cp remove_old_watering_files.py  :/
    #echo '   Run the cleanup'
    #mpremote ${PREM_DEVICE}  run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {
    echo 'make remote displays_tests/'
    mpremote ${PREM_DEVICE}  fs mkdir :displays_tests

    echo 'Copy files to displays_tests/ '
    mpremote ${PREM_DEVICE}  fs cp test_displays.py :/displays_tests/test_displays.py 
    
    #echo 'Remove the client files we do not need'
    #mpremote ${PREM_DEVICE}  fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote ${PREM_DEVICE}  fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /displays_tests'
    mpremote ${PREM_DEVICE}  fs ls /displays_tests
}


main() {
    echo "PUSH_DISPLAY_TESTS_FILES_TO_PICO"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
