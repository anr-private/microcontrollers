# test2.py

print(f"DIR is {dir()}")
print(f"locals is {locals().keys()}")
print()

import sys

print(f"DIR is {dir()}")
print(f"locals is {locals().keys()}")
print()

print(f" {sys.modules}")
print()

from utils import *

print(f"DIR is {dir()}")
print(f"locals is {locals().keys()}")
print()

#from lib.utils import loggg

print(f" {sys.modules}")

print(f" loggg is {loggg=}")