README_AAA.txt for mpremote install

'mpremote' is installed here:
  ~/git/microcontrollers/pi_pico/VENVs/mpremote_installed_in_venv/


=== INSTALLATION STEPS  ==================================

   # Based on 
      ~/git/art/src/python/misc/virtualenv_venv_SAMPLE

   # Due to bug, had to do these else python -m venv does not work:
   sudo apt update
   sudo apt install python3-venv

   # make a place for mpremote
   mkdir ...this subdir ...
   cd ...to this subdir...

   # Copy the scripts from there and create symlinks - from the above SAMPLE subdir
   cp ...  # the ACTIVATE_VENV and DEACTIVATE_VENV scripts
   ln -s DEACTIVATE_VENV DEACTIVATE
   ln -s ACTIVATE_VENV ACTIVATE

   # create the VENV
   python3 -m venv .mpremote_pgm_venv

   # activate using my script
   . ./ACTIVATE   # symlink to ACTIVATE_VENV script

   # Update the tools
   pip install -U pip setuptools wheel

   # Install mpremote
   pip install mpremote

   # Test it by getting the version
   mpremote --version
   # expected output looks like this:
      mpremote 1.26.0

   # Deactivate the VENV using my script
   . ./DEACTIVATE    # symlink to DEACTIVATE_VENV script


















  mkdir ~/mpremote_env
  python3 -m venv ~/mpremote_env
  source ~/mpremote_env/bin/activate
  # you're now inside the venv
    pip install mpremote
    mpremote --version
    deactivate
  # now back outside the venv







### end ###
