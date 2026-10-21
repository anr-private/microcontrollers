#!/bin/bash

mypy \
py/maranr_watering_system_main.py \
py/displays \
py/lib2 \
py/logger_elem \
py/mws \
py/primitives \
py/sensors \
py/weblib 

# OMITTED DUE TO conflicting ways of importing from lib
# due to lib being on micropython's default sys.path
#   py/lib  \

###

