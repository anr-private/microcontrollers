# make_pytest_venv_STEP_1.sh
#
# SOURCE THIS - do not execute it ****************
#

# make the venv subdir we use for running pytest
#
# See: /home/art/git/art/src/python3/misc/pytest_examples/
#
# Assumes:
#   ACTIVATE_VENV    # assumes this script already copied to this dir
#   DEACTIVATE_VENV    # assumes this script already copied to this dir
#   ln -s ACTIVATE_VENV    ACTIVATE
#   ln -s DEACTIVATE_VENV  DEACTIVATE

VENV_SUBDIR_NAME=".pytest_ut_trial_venv"
###export VENV_SUBDIR_NAME

# DEACTIVATE any active venv
if [ -f ./DEACTIVATE_VENV ] ; then
    echo '*** DEACTIVATING THE OLD venv  *******'
    echo \
    "source ./DEACTIVATE_VENV"
     source ./DEACTIVATE_VENV
fi


main() {

    echo \
    "rm -rf ${VENV_SUBDIR_NAME}"
     rm -rf ${VENV_SUBDIR_NAME}
    
    echo \
    "python3 -m venv ${VENV_SUBDIR_NAME}"
     python3 -m venv ${VENV_SUBDIR_NAME}

     echo \
     "source ./ACTIVATE_VENV"
      source ./ACTIVATE_VENV

    pip install -U pip
    pip install -U setuptools   wheel
    pip install -U pytest

    # Tell GIT to add .pytest_anr_http_lib1_venv/pyvenv.cfg
    # and then ignore everything else
    cd ${VENV_SUBDIR_NAME}
    git add pyvenv.cfg
    echo bin >>.gitignore
    echo include >>.gitignore
    echo lib >>.gitignore
    echo lib64 >>.gitignore
    git add .gitignore
    cd ..  

    echo '==== THE NEW venv IS ACTIVATED  ==========='
}


#echo 'ACTIVATE the venv  THEN  run this script:'
#echo 'make_pytest_venv_STEP_2.sh'


#. ./ACTIVATE
#
#pip install -U pip
#pip install -U setuptools   wheel
#pip install -U pytest

# Tell GIT to add .pytest_anr_http_lib1_venv/pyvenv.cfg
# and then ignore everything else
#  cd .pytest_anr_http_lib_venv
#  git add pyvenv.cfg
#  echo bin >>.gitignore
#  echo include >>.gitignore
#  echo lib >>.gitignore
#  echo lib64 >>.gitignore
#  git add .gitignore
#  cd ..  
#                                                                                     


# === CREATE THE ACTIVATE AND DEACT SCRIPTS  ========

rm -f ACTIVATE_VENV_ 
rm -f DEACTIVATE_VENV_
cat << 'AV_EOF'  >ACTIVATE_VENV
# SOURCE THIS, do not execute
#
# ACTIVATE_VENV


### NOTE: this venv was not created by pipenv, so don't use:...
###    pipenv shell

#################################################################
#
# HOW TO SET UP A VIRTUAL ENVIRONMENT and use this ACTIVATE_VENV script
#
# The typical way to set up a virtual environment ("virtualenv")
# that is compatible with using this ACTIVATE_VENV script:
# # Create a subdir to hold the virtualenv files.
# # By convention, it is named with a leading dot (".")
# # so that it is not normally visible when searching, etc.
# # Also by convention its name ends with "_venv".
# # This ACTIVATE_VENV script finds the subdir only if
# # the subdir's name follows these 2 conventions.
# # Here is the typical command to create the virtualenv
# # and its subdirs:
#     python3 -m venv .MY_DIR_NAME_HERE_venv
# # 
# # The next step is to install any needed pkgs using 'pip'.
# # First, upgrade PIP itself along with basic tools.
#     pip install -U pip
#     pip install -U setuptools wheel
# # Then install other pkgs as desired/needed.
# # These are just some examples:
#     pip install -U scapy
#     pip install -U strictyaml
#     pip install -U yaml
#
# To use the setup, open a terminal window and do:
#    cd  xxxx   # Change to your development dir
#               #   (It's where your top-level .py files are;
#               #    also this ACTIVATE_VENV should be there.)
#    source ACTIVATE_VENV   # source the ACTIVATE_VENV
#
#    python XXXX.py    # run your Python program(s)
#    pytest            # run unit tests
#                      #   'pytest' is aliased to pytest-3

# 'pip list'   output:
#   Package          Version
#   ---------------- -------
#   pip              20.2.4
#   pkg-resources    0.0.0
#   python-dateutil  2.8.1
#   ruamel.yaml      0.16.12
#   ruamel.yaml.clib 0.2.2
#   scapy            2.4.4
#   setuptools       50.3.2
#   six              1.15.0
#   strictyaml       1.1.0
#   wheel            0.35.1

# NOTE:
# This script adds the current directory to the PYTHONPATH.
# This allows pytest-3 to work as expected when running unit tests
# and simplifies the 'import' statements needed in the tests.

#################################################################


# There should be one and only 'venv' subdir
VENV_SUBDIR=""
EXTRA_SUBDIR=""
for x in .?*_venv ; do
	#echo 'x is ' "$x"
	if [ -d "$x" ] ; then
		if [ -z "$VENV_SUBDIR" ] ; then
			VENV_SUBDIR="$x"
		else
			EXTRA_SUBDIR="$x"
		fi
	fi
done
#echo 'SUBDIR' "$VENV_SUBDIR"
#echo 'EXTRA' "$EXTRA_SUBDIR"
if [ -z "$VENV_SUBDIR" ] ; then
	echo '*** ERROR ***  No "venv" subdir found!'
	echo '               Expected ".XXXX_venv"'
	echo '               Subdir must start with dot (".") and '
	echo '               must end with "_venv"  '
	return
fi
if [ -n "$EXTRA_SUBDIR" ] ; then
	echo '*** ERROR ***  Found more than one "venv" subdir:'
	echo '  ' "$VENV_SUBDIR"
	echo '  ' "$EXTRA_SUBDIR"
	return
fi

echo 'FOUND virtualenv SUBDIR NAMED:' $VENV_SUBDIR

source ${VENV_SUBDIR}/bin/activate

CWD=$(/bin/pwd)
#echo "CWD is $CWD"


# Add the site-packages so installed stuff is accessible 
# (Usually installed using 'pip install -U ...'
export PYTHONPATH="${CWD}/${VENV_SUBDIR}/lib/python3.6/site-packages"
# Add current dir so that sub-pkgs are available to unit test
export PYTHONPATH="${PYTHONPATH}:${CWD}"

###alias pytest=pytest-3
###alias pytest
alias py=python3


#:mode=shellscript:
### end ###
AV_EOF


cat <<'DE_EOF' >DEACTIVATE_VENV
# DEACTIVATE_VENV    - 'SOURCE' this - do not execute

# This is created as a shell-script function by 'activate'
deactivate

#:mode=shellscript:
### end ###
DE_EOF


### BEGIN MAIN EXECUTION #########################

echo 'CREATE THE venv SUBDIRECTORY for running pytest '
echo '    ' ${VENV_SUBDIR_NAME}

main


### end ###
