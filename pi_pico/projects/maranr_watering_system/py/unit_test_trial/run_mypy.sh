#!/bin/bash
#
# run_mypy.sh
# Run mypy on unit_test_trial/

mypy --config-file mypy.ini tests/shared tests/cpython 2>&1

###

