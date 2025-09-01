# threading_using_Global_class.py
#
# Based loosely on threading_w_lock_improved_BUGGY_GLOBAL_VARS.
#  https://bytesnbits.co.uk/multi-thread-coding-on-the-raspberry-pi-pico-in-micropython/
#
# Try to eliminate the problems caused by the use of GLOBAL vars
# by using a Global class that is shared with the threads.
# This eliminates the need for all global vars. One instance of 
# the Global class is created and used for all 'global' stuff.

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
		r1 = self.core1_running
		r2 = self.core2_running
		return(
		  f"GOB[r1={r1} r2={r2}]")


def core1_run(gob):
	""" Runs as the main thread in Core 1 """

	D("CORE1: run started")
	D(f"CORE2:   gob={gob}")
	gob.core1_running = True
	utime.sleep(2)
	D("CORE1: run ended")
	gob.core1_running = False


def core2_run(gob):
	""" Runs as the main thread in Core 2 """

	D("CORE2: started")
	#D(f"CORE2:    gob={gob}")
	gob.core2_running = True
	#D(f"CORE2:    NOW gob={gob}")
	utime.sleep(2)
	D(f"CORE2: gob={gob}")
	D("CORE2: ended")
	gob.core2_running = False




def main():
	main_thread_id = _thread.get_ident()
	print(f"MAIN:  thread-id is {main_thread_id}")
	
	gob = GOB()
	gob.create()

	print(f"MAIN:  globals created: {gob}")

	print(f"MAIN: start thread 2")
	second_thread = _thread.start_new_thread(core2_run, (gob,))
	print(f"MAIN:	  thread2 = {second_thread}")
	#print(f"MAIN:  gob={gob}")

	utime.sleep(0.5)
	print(f"MAIN:  gob={gob} after sleep")
	
	print(f"MAIN: terminating!")

##############

main()

### end ###
