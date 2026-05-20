#!/bin/bash
#
# PUSH_fake_logs_to_pico.sh
#
# Push fake log files to pico - for testing log rollover, etc.


if [[ "$PREM_DEVICE" == 'a0' || "$PREM_DEVICE" == 'a1' || "$PREM_DEVICE" == 'a2' || "$PREM_DEVICE" == 'a3' ]] ; then
    echo 'PREM_DEVICE is currently ok: "'${PREM_DEVICE}'"'
else
    echo '***** PREM_DEVICE does not have a proper value: "'${PREM_DEVICE}'"'
    exit 9
fi

###rm -rf displays/__pycache__

#--- get rid of the old stuff ---
clean_up_old_dirs_and_files() {
    echo '**** CLEANUP for displays IS NOT DONE YET ***************'
    # echo 'CLEANUP: copy the cleanup program and run it'
    # mpremote ${PREM_DEVICE} fs cp remove_old_watering_files.py  :/
    # echo '   Run the cleanup'
    # mpremote ${PREM_DEVICE} run remove_old_watering_files.py
    echo 'CLEANUP is done'
    echo '----------------'
}

push_fake_log_files_to_the_pico() {

    echo 'Push fake log files to PICO'
    for fname in mws_log.??? ; do
        echo '  Push file ' $fname
        echo \
        "mpremote ${PREM_DEVICE}  fs cp $fname :"
         mpremote ${PREM_DEVICE}  fs cp $fname : 
    done
    ###mpremote ${PREM_DEVICE} $PREM_DEVICE fs cp -r displays :
    
    #echo 'Remove the files we do not need'
    #mpremote ${PREM_DEVICE} fs rm displays/AnrHttpClient.py
}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS:'
    mpremote ${PREM_DEVICE} $PREM_DEVICE fs ls 
    
    ###mpremote ${PREM_DEVICE}  $PREM_DEVICE fs ls /displays
}

main() {
    echo "PUSH FAKE LOG FILES to Pico"
    push_fake_log_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
