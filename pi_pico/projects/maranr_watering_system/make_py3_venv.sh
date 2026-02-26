#!/bin/bash
#
# ~/git/art/src/python3/misc/virtualenv_venv_SAMPLE/make_py3_venv.sh
#
# First: copy this make_py3_venv.sh into your new project directory:
#    cd .../python3/.../my_new_proj
#    cp ~/git/art/src/python3/misc/virtualenv_venv_SAMPLE/make_py3_venv.sh  .
# Then edit this script: create a name for the 'dot' subdir that the venv
# will use. Typically you use your project name as the basis for the
# dot-venv subdir. Ex: for my_proj  create .mws_venv.
# That is what is used in the example below.
#
# Edit the python3 -m venv ... line below to use that name.

echo '==== Do these steps:  ===='

echo '    python3 -m venv .mws_venv  # MUST end with "_venv"'
echo '    cp ../virtualenv_venv_SAMPLE/ACTIVATE_VENV . '
echo '    cp ../virtualenv_venv_SAMPLE/DEACTIVATE_VENV .  '

echo '    Add these convenience links if desired:'
echo '    ln -s   ACTIVATE_VENV  ACTIVATE'
echo '    ln -s DEACTIVATE_VENV  DEACTIVATE'

echo '    source ACTIVATE     '
echo '       # use source DEACTIVATE to deactivate the virtual env'
echo '  '
echo '    # Pip will be the version installed when O/S was installed - old!'
echo '    pip --version    # old!'
echo '    # Update the tools:   "-U" means "update if already installed"  '
echo '    pip install -U pip'
echo '    pip install -U setuptools'
echo '    pip install -U wheel '
echo '       May also want scapy, toml, prettytoml, strictyaml, etc.'
echo '    pip list    # shows what is installed'
echo '    pip install -U pytest   # install pytest '
echo '  Installed pkgs are here:'
echo '    ls -ld ${VIRTUAL_ENV}/lib/python*/site-packages'
echo ' '
echo 'ADD THE PROJECT TO GIT'
echo 'git add make_py3_venv.sh  ACTIVATE_VENV  DEACTIVATE_VENV'
echo '   add or ignore the sym-links ACTIVATE, DEACTIVATE'
echo 'Add the .xxx_venv subdir'
echo '  cd .xxx_venv/ '
echo '  git add pyvenv.cfg  '
echo '  add everything else to .gitignore'
echo '  git add .gitignore  '
echo '  cd ..'





### OLD NOTES  ##############################################

# # The local venv subdir name MUST end with '_venv' 
# # so the ACTIVATE_VENV.sh script can find it.
# MY_VENV_DIR=XXXXXXXX_venv
# 
# python3 -m venv ${MY_VENV_DIR}
# echo '+++ Created venv subdir:' ${MY_VENV_DIR}                 
# 
# echo '+++ Updating pip,.. to latest versions.'
# source ./*_venv/bin/activate
# python -m pip install --user --upgrade pip setuptools wheel
# 
# 
# #echo '--- Use this script to enable the python exe to open raw sockets: '
# #echo "    In the venv\'s bin/ subdir:"
# #echo '        PYTHON3.6_VIRTENV_FIXES_FOR_RAW_SOCKETS.sh'
# 
# exit 88
# 
# 
# 
# 
# # Add this dir to GIT
# git add ACT*
# git add make_py3_venv.sh
# git add README*txt
# # Ignore the bulk of the venv stuff - just keep the cfg file.
# ls ${MY_VENV_DIR}/ |grep -vF pyvenv.cfg >${MY_VENV_DIR}/.gitignore
# git add ${MY_VENV_DIR}/pyvenv.cfg 
# git add ${MY_VENV_DIR}/.gitignore 
# 
# echo '+++ ADDED TO GIT: '
# git status .
# 
### end ###
