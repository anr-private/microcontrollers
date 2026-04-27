#!/bin/bash
#
# renumber_lines_mws_displays.sh
#
# Renumber the line numbers in log and print calls

PYTHON_EXE=python3

FDIR="displays"
FNAME="MwsDisplays.py"

FPATH="${FDIR}/${FNAME}"
OUT_FPATH="${FPATH}.out"
BAK_FPATH="${FPATH}.bak"

if true ; then
    echo 'FDIR         ' $FDIR
    echo 'FNAME        ' $FNAME
    echo 'FPATH        ' $FPATH
    echo 'OUT_FPATH    ' $OUT_FPATH
    echo 'BAK_FPATH    ' $BAK_FPATH
fi

if true ; then
    echo '$$$   INPUT FILE: ' $FPATH
    echo '$$$   ls -l ' $(ls -l $FPATH)
fi

TARGET='MwsDisplays@'

RENUM_LINES=/home/art/bin/renumber_line_numbers.py


echo \
"$PYTHON_EXE $RENUM_LINES $FPATH  $TARGET"
 $PYTHON_EXE $RENUM_LINES $FPATH  $TARGET


if true ; then
    echo '$$$   OUT  FILE: ' $OUT_FPATH
    echo '$$$   ls -l ' $(ls -l $OUT_FPATH)
    echo '$$$   BAK FILE: ' $BAK_FPATH
    echo '$$$   ls -l ' $(ls -l $BAK_FPATH)
fi

echo \
"mv $OUT_FPATH  $FPATH"
 mv $OUT_FPATH  $FPATH

echo \
"rm -f $BAK_FPATH"
 rm -f $BAK_FPATH



###
