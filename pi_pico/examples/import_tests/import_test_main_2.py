# import_test_main.py
#
# this is main file for testing the layout of directories containing py files
# Layout:
#  /import_test_main.py  
#  /lib/MyClassA.py
#  /anrlib/MyClassB.py
#  /anrlib/anrsub/MyClassC.py
# You need to create all the dirs 'by hand': /lib, /anrlib, /anrlib/anrsub 
# THIS TEST USES THESE __init__.py to provide access to the classes:
#  /anrlib/__init__.py
#  /anrlib/anrsub/__init__.py
# WE DO NOT ADD ANY PATHS TO THE sys.path

print("\n==========  IMPORT TEST 2 ========================")

import sys
#print(f" type of sys.path is {type(sys.path)}")
#print(f"sys.path is '{sys.path}'")
#sys.path.append("/anrlib")
#sys.path.append("/anrlib/anrsub")
print(f"sys.path = '{sys.path}'")
print("")

import MyClassA  # comes from /lib, which is in sys.path by default
print(f"MyClassA is {MyClassA=}")

import anrlib.MyClassB as MyClassB
print(f"MyClassB is {MyClassB=}")

import anrlib.anrsub.MyClassC as MyClassC
#import MyClassC
print(f"MyClassC is {MyClassC=}")
print("")

a = MyClassA.MyClassA()
a.greet()

b = MyClassB.MyClassB()
b.greetings()

c = MyClassC.MyClassC()
c.greeter()


###
