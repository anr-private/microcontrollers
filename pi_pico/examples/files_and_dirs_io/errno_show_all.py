# errno_show_all.py

import errno
import sys

print(f"--- OSError codes for the current MicroPython port ({sys.platform}) ---")
print(f"NOTE!!  Run this using Py3 as well as on the Pico.")
print(f"        Some of the errno codes are used by  micropython but they ")
print(f"        do not appear in the errno.errorcode.items() dict.")
print(f"        Ex:  28  ENOSPC  - file system out of space")

# Output v1.27.0 March 9 2026
# Code: 1     Name: EPERM
# Code: 2     Name: ENOENT
# Code: 5     Name: EIO
# Code: 9     Name: EBADF
# Code: 11    Name: EAGAIN
# Code: 12    Name: ENOMEM
# Code: 13    Name: EACCES
# Code: 17    Name: EEXIST
# Code: 19    Name: ENODEV
# Code: 21    Name: EISDIR
# Code: 22    Name: EINVAL
# Code: 95    Name: EOPNOTSUPP
# Code: 98    Name: EADDRINUSE
# Code: 103   Name: ECONNABORTED
# Code: 104   Name: ECONNRESET
# Code: 105   Name: ENOBUFS
# Code: 107   Name: ENOTCONN
# Code: 110   Name: ETIMEDOUT
# Code: 111   Name: ECONNREFUSED
# Code: 113   Name: EHOSTUNREACH
# Code: 114   Name: EALREADY
# Code: 115   Name: EINPROGRESS

# errno.errorcode is a dictionary that maps numeric error codes to symbolic error code strings
for code, name in errno.errorcode.items():
    print(f"Code: {code:<5} Name: {name}")

print("----------------------------------------------------------------------")
