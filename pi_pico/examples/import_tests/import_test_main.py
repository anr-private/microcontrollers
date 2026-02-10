# import_test_main.py
#
# this is main file for testing the layout of directories containing py files
# Layout:
#  /import_test_main.py  
#  /lib/MyClassA.py
#  /anrlib/MyClassB.py
#  /anrlib/anrsub/MyClassC.py
# You need to create all the dirs 'by hand': /lib, /anrlib, /anrlib/anrsub 


import sys

print(f" type of sys.path is {type(sys.path)}")
print(f"sys.path is '{sys.path}'")
sys.path.append("/anrlib")
sys.path.append("/anrlib/anrsub")
print(f"sys.path NOW '{sys.path}'")

import MyClassA

print(f"MyClassA is {MyClassA=}")

#a = 123
#print(f" A is {a=}")

import MyClassB

#import anrlib.MyClassC
import MyClassC


a = MyClassA.MyClassA()
a.greet()

b = MyClassB.MyClassB()
b.greetings()

c = MyClassC.MyClassC()
c.greeter()


###
