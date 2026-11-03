#!/bin/bash
#
# PUSH_lib1_to_pico.sh

if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' || "$PREM_DEVICE" == 'a2' || "$PREM_DEVICE" == 'a3' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi

THIS_SUBDIR='./lib1'

verify_correct_directory() {
    echo '@@@@@@@@ START verify_correct_directory'
    if [ -d ${THIS_SUBDIR} ] ; then
        echo 'FOUND the expected subdir: '  ${THIS_SUBDIR}
        return
    fi

    echo '** NO SUCH SUBDIR in the current directory **'
    echo '    Expected: ' ${THIS_SUBDIR}
    exit 9
}


remove_pycache() {
    echo \
    "rm -rf __pycache__"
     rm -rf __pycache__
    echo \
    "rm -rf ${THIS_SUBDIR}/__pycache__"
     rm -rf ${THIS_SUBDIR}/__pycache__
}


clean_up_old_dirs_and_files_on_pico() {
    echo 'CLEANUP PICO: copy the cleanup program and run it'
    echo '*** NOT IMPLEMENETED YET ***'
    #mpremote ${PREM_DEVICE} fs cp remove_old_watering_files.py  :/
    #echo '   Run the cleanup'
    #mpremote ${PREM_DEVICE} run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

#--- copy the new stuff to the Pico ---
copy_release_files_to_the_pico() {
    echo 'Copy contents of lib1/ '
    mpremote ${PREM_DEVICE} fs cp -r lib1   :
    
    #echo 'Remove the client files we do not need'
    #mpremote ${PREM_DEVICE} fs rm http/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote ${PREM_DEVICE} fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /lib1'
    mpremote ${PREM_DEVICE} fs ls /lib1
}


main() {
    echo "PUSH_lib1_to_pico.sh"
    verify_correct_directory
    remove_pycache
    clean_up_old_dirs_and_files_on_pico
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
