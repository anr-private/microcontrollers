#!/bin/sh
#
# copy all files to the pico

rm -rf anr_http/__pycache__

mpremote fs cp -r anr_http :

mpremote fs cp anr_http_client/anr_http_client.py :/

mpremote fs ls 

mpremote fs ls /anr_http


###
