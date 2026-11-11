#!/bin/bash
#
# run_mypy_on_project_code.sh 
#
# Run this script in the directory that holds py/
#
# Usage:
#  Check all production code (same as before)
#   ./run_mypy_on_project_code.sh                          
#  Check only the file(s)/dir(s) given
#   ./run_mypy_on_project_code.sh  py/weblib/MwsWebServer.py  
#
# -v   show verbose output including which files are found/checked ('Found')
#      It generates a lot of output, so pipe it into: ' | grep Found'
#
# A report file. mypy --linecount-report /tmp/rep <your usual arguments> 
# should write /tmp/rep/linecount.txt with one line for every file it processed.
#
# Comment out that file’s ignore_errors = True in mypy.ini first. 
# Otherwise mypy reports nothing for that file.
#
# mypy still follows imports. Errors can show up in modules the 
# file imports, unless those modules are still marked ignore_errors

default_targets=(
    py/maranr_watering_system_main.py
    py/displays
    py/lib1
    py/lib2
    py/logger_elem
    py/mws
    py/primitives
    py/sensors
    py/weblib
)

if [ "$#" -gt 0 ]; then
    targets=("$@")
else
    targets=("${default_targets[@]}")
fi

mypy \
--cache-dir=/dev/null \
--config-file mypy.ini \
--any-exprs-report MYPY_reports/type_Any \
"${targets[@]}" 2>&1

###
