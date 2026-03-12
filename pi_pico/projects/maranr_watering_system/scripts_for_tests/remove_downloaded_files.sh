#!/bin/bash

while true ; do
    echo ' '
    echo "$(date)   REMOVE THE FILES grabbed by send_requests_to_MWS_main.sh  ==============="
    rm -f index.html*
    rm -f maranr_logo.png*
    rm -f squares_red.html*
    rm -f log*number*
    ls -l
    sleep 10
done

###

