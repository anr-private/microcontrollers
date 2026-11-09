#!/bin/bash

# This saves the scratch dirs / files if there is ANY arg on the commandline
if (( $# >= 1 )) ; then
    # This is created only in the local environ, not globally
    # So it disappears from the env when this script ends
    export MWS_SAVE_SCRATCH=1
    echo ' '; echo ' '
    echo '************************************************************************************************************************************'
    echo 'run_cpython_unit_tests.sh: ****** SAVING THE SCRATCH DIRS and FILES using env var MWS_SAVE_SCRATCH    ******************************'
fi

pytest $*

###
