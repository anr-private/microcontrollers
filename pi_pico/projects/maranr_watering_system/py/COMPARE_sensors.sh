#!/bin/bash
#
# COMPARE_sensors.sh

diff -q sensors /tmp/SENSORS |grep -v 'Only in sensors:'


###
