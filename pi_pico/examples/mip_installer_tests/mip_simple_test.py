# mip_simple_test.py
#
# REQUIRES A NETWORK CONNECTION - wifi connection

import mip

if 0:
    print("mip.install is a function ...")
    print(mip.install)

import errno

print(errno.errorcode)

try:
    mip.install("github:peterhinch/nosuch")
except OSError as ex:
    print("EX is:")
    print(ex)
    print(ex.errno)    

###
