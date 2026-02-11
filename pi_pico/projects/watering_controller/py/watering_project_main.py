# watering_project_main.py
#
# main program for the watering project
#
# Gets install on the Pico as  /main.py
# Runs when Pico powers up.

import sys
import platform

###print(f"{platform.platform().lower()=}")

if "micropython" in platform.platform().lower():
    py_platform = "micropython"
print(f"{py_platform=}")

if py_platform == "micropython":
    sys.path.append("/anr_http")
else:
    py_platform = "cpython"
    sys.path.append("../anr_http")
print(f"{sys.path=}")
    


from AnrHttpServer import AnrHttpServer

server = AnrHttpServer()
server.run()


### end ###

