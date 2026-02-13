# GRAB_primitives_FROM_PETERHINCH_REPO.sh
#
# Grab selected files from the Peter Hinch repo

PETERHINCH_SUBDIR="/home/art/git_not_mine/micropython_LIBRARIES/peterhinch_micropython-async/micropython-async/v3"

#echo $PETERHINCH_SUBDIR
#ls   $PETERHINCH_SUBDIR

mkdir -p primitives

cp -p ${PETERHINCH_SUBDIR}/primitives/queue.py primitives/


### end ###
