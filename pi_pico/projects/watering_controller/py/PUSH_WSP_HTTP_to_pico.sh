#!/bin/sh
#
# PUSH_WSP_HTTP_to_pico.sh
#
# wsp_http/ -  push the repo files to the pico
# 
rm -rf wsp_http/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo '**** CLEANUP for wsp_http IS NOT DONE YET ***************'
    # echo 'CLEANUP: copy the cleanup program and run it'
    # mpremote fs cp remove_old_watering_files.py  :/
    # echo '   Run the cleanup'
    # mpremote run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {

    echo 'Copy contents of dir  wsp_http'
    mpremote fs cp -r wsp_http :
    
    #echo 'Remove the files we do not need'
    #mpremote fs rm wsp_http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote fs ls 
    
    mpremote fs ls /wsp_http
}

main() {
    echo "MAIN"
    clean_up_old_dirs_and_files
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
