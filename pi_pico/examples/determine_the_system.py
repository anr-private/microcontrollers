# determine_the_system.py

import os
import sys
import platform

print(f"dir platform is {dir(platform)}")
#print(f"{os.name=}")

print(f"{sys.platform=}")
#print(f"{platform.system()=}")
print(f"{platform.platform()=}")

#, sys.platform, or platform.system().