#!/bin/bash
#
# renumber_using_apply.sh
# 
# do linemarker renumber using apply_action_to_files and redo_line_markers
#
# ex: apply_action_to_files --version -n --verbose -c redo_line_markers -g '*.py' py/ 
#
# For testing using '-n' to dryrun
# The filtering params are (still) hard-coded in the apply_action_to_files script

echo \
"apply_action_to_files $*  -c redo_line_markers -g '*.py' py/ "
 apply_action_to_files $*  -c redo_line_markers -g '*.py' py/ 

###


