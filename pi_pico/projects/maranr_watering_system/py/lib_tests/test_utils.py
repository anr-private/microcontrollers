# test_utils.py
#
# You can run this either locally on the linux system by
# opening this file in Thonny and then running it.
# (That is the easiest way)
#
# Or you can copy the file to the Pico, go to the Pico's remote files/dirs
# window, double-click it (downloads it back into Thonny), and then run
# it in Thonny.
# NOTE that the /lib/utils.py must exist on the Pico in order for the import to work!

import sys

print(f"SYS.PATH {sys.path}")

import lib.utils as utils

#print(f"DIR(utils)")
#print(dir(utils))



def test1():
    mtype = utils.determine_machine_type()
    print(f"  Machine type is {mtype}")
    

def main(*args):
    test1()


if __name__ == "__main__":
    main(sys.argv[1:])




###
