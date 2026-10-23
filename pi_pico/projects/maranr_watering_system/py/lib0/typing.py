# typing.py
#
# Fake version for micropython

# typing.py - Dummy module for MicroPython runtime compatibility
# Supports stuff like 'from typing import Callable'
def __getattr__(name):
  # Dynamically return a dummy object for any requested type hint
  return object

###
