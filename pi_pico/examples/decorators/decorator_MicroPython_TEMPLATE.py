# decorator_MicroPython_TEMPLATE.py
#
# THE BEST WAY to do a decorator in MicroPython
#   as of version 1.27
#
# Cannot use functools to make the wrapper behave better when debugging -
# not (yet?) available in MicroPython.
#
# MicroPython does NOT support __name__, so this does not work.
# You can use a class as the wrapper (instead of a function like
# myDecoWrapper), but that requires more memory.
# So maybe wrapping using a decorator is not a great technique
# for MicroPython.

# NOTE  not available in MicroPython!
#####import functools

def myDeco(theFunct):
	""" Decorator """

	# Comment this out to see the wrapper info when you ask
	# for fun.__name__, etc (see below, line 45)
	##### NOT AVAILABLE @functools.wraps(theFunct)
	def myDecoWrapper(*args, **kwargs):
		""" This is myDecoWrapper !! """
		print("    >>> myDecoWrapper called:  args=%s kw=%s" % (args, kwargs))
		result = theFunct(*args, **kwargs)
		# 'decorate' the result
		print("    >>> myDecoWrapper gets result from original function: result=%s" % (result,))
		result *= 100
		print("    >>> myDecoWrapper returns result=%s" % (result,))
		return result

    # MicroPython does NOT support __name__, so this does not work.
    # You can use a class as the wrapper (instead of a function like
    # myDecoWrapper), but that requires more memory.
    # So maybe wrapping using a decorator is not a great technique
    # for MicroPython.
	######myDecoWrapper.__name__ = theFunct.__name__
	return myDecoWrapper


@myDeco
def fun(a,b):
	""" This is function 'fun'! """
	print("  FUN(a=%s b=%s)  is being called..." % (a,b))
	return a+b

print()
print("MAIN: Call fun(11, 22)")
r = fun(11,22)
print("MAIN:    fun(11, 22) returns %s" %(r,))
print()

print("MAIN: str(fun) is a CLOSURE.")
print("  str(fun) is %s" % (str(fun),))
print("MAIN: name is the name of the decorator, NOT the original function (sigh).")
print("  fun.__name__ is %s" % (fun.__name__,))

if 0:
    # help() clears the screen, makes the above harder to read...
    print("  help(fun) is ...")
    help(fun) # outputs directly to stdout

# The output when functools.wraps it NOT used is ...
#    fun is <function myDeco.<locals>.myDecoWrapper at 0x7fb48532a790>
#     fun.__name__ is myDecoWrapper
#     help(fun) is ...
#   Help on function myDecoWrapper in module __main__:
#         myDecoWrapper(*args, **kwargs)
#             This is myDecoWrapper !!

# If you uncomment the '@functools.wraps(...)' call above, 
# the output is:
#     fun is <function fun at 0x7fc2fc498790>
#     fun.__name__ is fun
#     help(fun) is ...
#         fun(a, b)
#              This is function 'fun'!




### end ###
