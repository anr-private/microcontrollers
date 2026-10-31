#!/bin/bash
#
# UPDATE_pip_installed_pkgs.sh
#
# Update the stuff that PIP has installed

python3 -m pip install -U pip
pip install -U --upgrade-strategy eager pytest mypy mpremote

###
