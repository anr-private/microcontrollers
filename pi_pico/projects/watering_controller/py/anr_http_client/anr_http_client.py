# anr_http_client.py
#
# main program for the Client

import sys
import platform


sys.path.append("../anr_http")

py_platform = "cpython"

print(f"{platform.platform().lower()=}")

if "micropython" in platform.platform().lower():
    py_platform = "micropython"
print(f"{py_platform=}")

if py_platform == "micropython":
    sys.path.append("/anr_http")
else:
    sys.path.append("../anr_http")
print(f"{sys.path=}")
    


from AnrHttpClient import AnrHttpClient

client = AnrHttpClient()
client.run()


### end ###

