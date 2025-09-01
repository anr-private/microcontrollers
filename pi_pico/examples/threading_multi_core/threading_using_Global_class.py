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
		###self.core1_running = None
		self.core2_running = None
		self.stop_requested = False


	def create(self):
		""" Create the globals """

		self.lock = _thread.allocate_lock()
		D(f"  lock is {self.lock}")
		D(f"   dir(self.lock) {dir(self.lock)}")
		utime.sleep(0.25) # delay so user can read the above

	def request_stop(self, who):
		""" Somebody wants to stop """
		print(f"GOB: stop_requested by {who}")
		self.stop_requested = True

	def __str__(self):
		lkd = self.lock.locked()
		###r1 = self.core1_running
		r2 = self.core2_running
		sr = self.stop_requested
		return(
		  f"GOB[lock={lkd} r2={r2} stopReqd={sr}]")
		  ###f"GOB[lock={lkd} r1={r1} r2={r2}]")


def core1_run(gob):
	""" Runs as the main thread in Core 1 """

	D("CORE1: run started")
	D(f"CORE2:   gob={gob}")
	###gob.core1_running = True

	while True:
		D("  CORE1 running")
		
		utime.sleep(1)
		if gob.stop_requested:
			print("CORE1 stop requested! So stopping!")
			break

	D("CORE1: run ended")
	###gob.core1_running = False


def core2_run(gob):
	""" Runs as the main thread in Core 2 """

	D("CORE2: started")
	#D(f"CORE2:    gob={gob}")
	gob.core2_running = True
	#D(f"CORE2:    NOW gob={gob}")

	stop_ctr = 10
	while True:
		D("  CORE2 running")
		D(f"      CORE2 stop_ctr={stop_ctr}")
		utime.sleep(1)
		stop_ctr -= 1
		if stop_ctr <= 0:
			gob.request_stop("Core2")
		if gob.stop_requested:
			print("CORE2 stop requested! So stopping!")
			break

	D(f"CORE2: ending.  gob={gob}")
	D("CORE2: ended")
	gob.core2_running = False


def  wait_for_thread2(gob):
	""" """
	#D("wait_for_thread2")
	#D(f"   wait_for_thread2  gob={gob}")
	while True:
		if gob.core2_running == False:
			break
		utime.sleep(0.5)
		D("wait_for_thread2")
	D(f"wait_for_thread2  thread2 ENDED!  gob={gob}")

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
	
	print(f"MAIN: start thread 1")
	try:
		core1_run(gob)
	except KeyboardInterrupt:
		print(f"    KEYBOARD INTERRUPT! Core1 stopped as a result.  thread-id={main_thread_id}")
		print()

	print("MAIN: tell thread2 to stop")
	gob.stop_requested = True

	wait_for_thread2(gob)

	print(f"MAIN: terminating!")

##############

main()

### end ###
