# try_decorators_1.py

print("Deco is being defined...")

def deco(the_orig_func): ###*args, **kw):
	""" """
	###print("DECO called args=%s kw=%s" % (args, kw))
	print("DECO called funct=%s " % (the_orig_func,))

	def anr_deco_wrapper(*args, **kw):
		print("DECOWRAPPER called args=%s kw=%s" % (args, kw))
		print("DECOWRAPPER is now calling the decorated function: %s" % (the_orig_func,))
		result = the_orig_func(*args, **kw)
		print("DECOWRAPPER from the original 'f', got result=%s" % (result,))
		result = result * 100
		print("DECOWRAPPER modifies the result to be: result=%s" % (result,))
		return result
	return anr_deco_wrapper
print("Deco is now defined.\n")

print("f is being defined with 'deco' decorator...")
@deco
def f(a,b,c):
	print("F called a=%s b=%s c=%s  RETURNS %d"  % (a,b,c, a+b+c))
	return a+b+c
print("f is now defined\n")

print("f is being called...")

r = f(1,2,3)
print("F (as decorated) now returns %d" % (r,))

###print("DIR(f) is ..."); print(dir(f))
print("F.__name__ is %s" % (f.__name__, ))

### end ###

