#!/bin/bash
#
# renumber_lines_QQ_to_pico.sh
#
# Renumber the line numbers in log and print calls

PYTHON_EXE=python3

FDIR="../scripts"
FNAME="QQ_to_pico"
TARGET='QQ@'
MAKE_FILE_EXECUTABLE=true

FPATH="${FDIR}/${FNAME}"
OUT_FPATH="${FPATH}.out"
BAK_FPATH="${FPATH}.bak"
LOG_FPATH="${FPATH}.log"

DBG=false

if $DBG ; then
    echo 'FDIR         ' $FDIR
    echo 'FNAME        ' $FNAME
    echo 'FPATH        ' $FPATH
    echo 'OUT_FPATH    ' $OUT_FPATH
    echo 'BAK_FPATH    ' $BAK_FPATH
    echo 'LOG_FPATH    ' $LOG_FPATH
fi

if $DBG ; then
    echo '$$$   INPUT FILE: ' $FPATH
    echo '$$$   ls -l ' $(ls -l $FPATH)
fi

RENUM_LINES=/home/art/bin/renumber_line_numbers.py


echo \
"$PYTHON_EXE $RENUM_LINES $FPATH  $TARGET"
 $PYTHON_EXE $RENUM_LINES $FPATH  $TARGET  1>>$LOG_FPATH

if $DBG ; then
    echo '$$$   OUT  FILE: ' $OUT_FPATH
    echo '$$$   ls -l ' $(ls -l $OUT_FPATH)
    echo '$$$   BAK FILE: ' $BAK_FPATH
    echo '$$$   ls -l ' $(ls -l $BAK_FPATH)
fi

if $DBG ; then
    echo \
    "mv $OUT_FPATH  $FPATH"
fi
     mv $OUT_FPATH  $FPATH
if $MAKE_FILE_EXECUTABLE ; then
    echo 'MAKING THE FILE EXECUTABLE: ' $FPATH
    echo \
    "chmod +x $FPATH"
    chmod +x $FPATH
fi

if $DBG ; then
    echo \
    "rm -f $BAK_FPATH"
fi
     rm -f $BAK_FPATH

if $DBG ; then
    echo '--- LOG FILE  ------------------'
    cat $LOG_FPATH
    echo '--- end of LOG FILE  ------------------'
fi
     rm -f $LOG_FPATH


###
