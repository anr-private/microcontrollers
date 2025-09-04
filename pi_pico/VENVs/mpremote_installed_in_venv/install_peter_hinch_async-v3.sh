#!/bin/bash
#
# install_peter_hinch_async-v3.sh
# 
# /home/art/git/microcontrollers/pi_pico/VENVs/mpremote_installed_in_venv/install_peter_hinch_async-v3.sh
#
# Use mpremote to install Peter Finch version of async (formerly uasync)
# NOTE THONNY MUST NOT BE RUNNING as it will 'own' the Pico and prevent
# mpremote from accessing the pico  (/dev/ttyACM0)


mpremote mip install github:peterhinch/micropython-async/v3/primitives

mpremote mip install github:peterhinch/micropython-async/v3/threadsafe

# Show the file system
mpremote tree

echo '=== Expect the TREE command shows /lib/primitives and /lib/threadsafe'

### end ###
