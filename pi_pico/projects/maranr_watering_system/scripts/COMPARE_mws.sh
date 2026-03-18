#!/bin/bash
#
# COMPARE_mws.sh
 
diff -q mws /tmp/MWS  |grep -v __QPUSH_MARKER__ 


###
