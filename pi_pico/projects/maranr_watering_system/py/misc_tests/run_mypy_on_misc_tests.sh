#!/bin/bash
#
# run_mypy_on_misc_tests.sh 
#
# Run this script in py/misc_tests
#
# Usage:
#  Check all code
#   ./run_mypy_on_misc_tests.sh                          
#  Check only the file(s)/dir(s) given
#   ./run_mypy_on_misc_tests.sh  ./some_test.py
#
# -v   show verbose output including which files are found/checked ('Found')
#      It generates a lot of output, so pipe it into: ' | grep Found'
#
# A report file. mypy --linecount-report /tmp/rep <your usual arguments> 
# should write /tmp/rep/linecount.txt with one line for every file it processed.
#
# Comment out that file’s ignore_errors = True in mypy_for_project_code.ini first. 
# Otherwise mypy reports nothing for that file.
#
# mypy still follows imports. Errors can show up in modules the 
# file imports, unless those modules are still marked ignore_errors

# Ensure this script runs in py/misc-tests/
cd "$(dirname "$0")"
for required_path in ../../typings .. ./logs_rotation_test.py ../lib1 ../lib2 ../logger_embed_module ; do
    if [ ! -e "${required_path}" ] ; then
        echo "*ERROR* missing path: ${required_path}  (cwd: $(pwd))"
        exit 2
    fi
done


INI_FILE="mypy_for_misc_tests.ini"

default_targets=(
    ./logs_rotation_test.py
    ../lib1
    ../lib2
    ../logger_embed_module
)


if [ "$#" -gt 0 ]; then
    targets=("$@")
    RUN_ANY_REPORTS_1=""
    RUN_ANY_REPORTS_2=""
else
    targets=("${default_targets[@]}")
    #RUN_ANY_REPORTS_1="--any-exprs-report"
    #RUN_ANY_REPORTS_2="MYPY_reports/type_Any"
    RUN_ANY_REPORTS_1=""
    RUN_ANY_REPORTS_2=""
fi

mypy \
--cache-dir=/dev/null \
--config-file ${INI_FILE} \
${RUN_ANY_REPORTS_1} ${RUN_ANY_REPORTS_2} \
"${targets[@]}" 2>&1

if [ -n "${RUN_ANY_REPORTS_2}" ] ; then
    echo "The 'Any Reports' are available in ${RUN_ANY_REPORTS_2}"
fi


###
