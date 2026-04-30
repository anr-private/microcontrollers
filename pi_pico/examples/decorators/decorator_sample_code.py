# decorator_sample_code.py
#
# This is a basic template for creating a decorator:

### NOT AVAILABLE IN MICROPYTHON 1.27   #####################################

import functools


# This is a basic template for creating a decorator:

def decorator(func):
	""" This gets invoked to create the wrapper function;
		when invoked, the wrapper function calls the original func.
		"""

	@functools.wraps(func)
	def wrapper_decorator(*args, **kwargs):
		""" This is the actual wrapper; it 'encloses' the
		original func with some 'extra' stuff.
		It gets invoked in place of the original func
		in the 'user code'
		It preserves things from the original function:
		name, docstring, annotations. 
		These would otherwise get obscured by the wrapper.
		"""
		# Do something before
		value = func(*args, **kwargs)
		# Do something after
		return value
	return wrapper_decorator


# Simple example usage:

@decorator
def fun(a,b):
	""" This 'fun' gets wrapped by the decorator. 
	It is the 'original' fun.
	"""
	return a+b

# 'user code' invokes 'fun' - which actually invokes the wrapper,
# which it turn invokes the original 'fun'
r = fun(11,22)
print("  result is %s" % (r,))

### end ###
