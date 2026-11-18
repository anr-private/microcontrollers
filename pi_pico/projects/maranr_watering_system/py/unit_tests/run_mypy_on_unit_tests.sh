#!/bin/bash
#
# run_mypy.sh
# Run mypy on unit_tests/

mypy --cache-dir /dev/null --config-file mypy_for_unit_tests.ini tests/shared tests/cpython 2>&1

###

