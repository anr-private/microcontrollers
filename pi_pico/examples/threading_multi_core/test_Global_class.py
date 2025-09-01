# test_Global_class.py

import gc
import utime
import _thread

def D(s):
	print(s)

class GOB:
	""" global objects """

	def __init__(self):
		self.lock = None
		self.core1_running = None
		self.core2_running = None

	def create(self):
		""" Create the globals """

		self.lock = _thread.allocate_lock()
		D(f"  lock is {self.lock}")
		D(f"   dir(self.lock) {dir(self.lock)}")
		utime.sleep(0.25) # delay so user can read the above

	def __str__(self):
		lkd = self.lock.locked()
		r1 = self.core1_running
		r2 = self.core2_running
		return(
		  f"GOB[lock={lkd} r1={r1} r2={r2}]")



def main():
	main_thread_id = _thread.get_ident()
	print(f"MAIN:  thread-id is {main_thread_id}")
	
	gob = GOB()
	gob.create()

	print(f"MAIN:  globals created: {gob}")

	D("MAIN: set r1")
	gob.core1_running = True
	D(f"MAIN: after set r1 gob={gob}")

	D("MAIN: set r2")
	gob.core2_running = True
	D(f"MAIN: after set r2 gob={gob}")



	utime.sleep(0.5)
	print(f"MAIN:  gob={gob} after sleep")
	
	print(f"MAIN: terminating!")

##############

main()

### end ###
