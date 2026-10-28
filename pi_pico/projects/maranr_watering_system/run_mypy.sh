#!/bin/bash

# -v   show verbose output including which files are found/checked ('Found')
# A report file. mypy --linecount-report /tmp/rep <your usual arguments> should write /tmp/rep/linecount.txt with one line for every file it processed.

mypy \
py/maranr_watering_system_main.py \
py/displays \
py/lib1 \
py/lib2 \
py/logger_elem \
py/mws \
py/primitives \
py/sensors \
py/weblib \
2>&1


# OMITTED DUE TO conflicting ways of importing from lib
# due to lib being on micropython's default sys.path
#   py/lib  \
# Also nothing in lib0/ yet
#   py/lib0 \
###

