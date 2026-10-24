#!/bin/bash
# 
# Create the stubs dir 'typings' used by mypy

rm -rf typings

# For 1.29.0 need to CHANGE THE VERSION HERE    vvvvvv
####pip install "micropython-rp2-rpi_pico2_w-stubs==1.27.*" --target ./typings
pip install "micropython-rp2-rpi_pico2_w-stubs==1.29.*" --target ./typings

echo '--- Verifying ---'
pip list --path ./typings
ls -d typings/*.dist-info
ls typings/machine.pyi
###
