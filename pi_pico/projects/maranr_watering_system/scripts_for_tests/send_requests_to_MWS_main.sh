#!/bin/bash
#
# send_requests_to_MWS_main.sh
#
# Send continuous requests to MARANR watering system asking for main page.
# Sleep in between requests

i=0
while true ; do
    wget http://192.168.1.49:8000
	wget http://192.168.1.49:8000/squares_red.html
    wget http://192.168.1.49:8000/maranr_logo.png

    ((i++))
    echo 'Counter: ' $i '   ' $(date)
    sleep 10
done
