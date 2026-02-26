#!/bin/bash
#
# PUSH_LOGGER_FILES_to_pico.sh


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
    echo 'Copy contents of logger/ '
    mpremote fs cp -r logger   :
    
    #echo 'Remove the client files we do not need'
    #mpremote fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /logger'
    mpremote fs ls /logger
}


main() {
    echo " PUSH_LOGGER_FILES_to_pico -- MAIN()"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
