# thread sync using a Lock
#
#  https://bytesnbits.co.uk/multi-thread-coding-on-the-raspberry-pi-pico-in-micropython/
#
# This version tries to do a cleanup
# Gets very odd error(s) claiming global variable(s) are not defined.
# Mainly in the second thread.
# Sometimes reports NameError "VARNAME" isn't defined but gives a line number that does
# not contain a reference to that variable(!!??)

import gc
import utime
import _thread

### GLOBALS  ####################
the_lock = None

# Used for cleanup
running = True

# Core-2 reports here when it concludes
core2_active = True

# Debug: the thread id for Core-2
#####core2_thread_id = None

def core1_thread_polled():
    """ Use lock.locked() to poll the lock instead of blocking """
    global the_lock
    print(f"C1 lock is {the_lock}")

    # Expect it is same as main thread id
    core1_thread_id = _thread.get_ident()
    
    while running:
        wait_counter = 0
        # try to acquire lock but don't wait
        while not the_lock.acquire(0):  # lock.acquire(waitflag=1, timeout=-1)
            # count the number of times the lock is polled
            # Our code is not in a waiting state
            # we are just polling the lock at the end of each loop iteration
            wait_counter += 1
        print(f"CORE 1  I counted to {wait_counter} while waiting.")

        secs = 0.5
        print(f"CORE 1:  core ident={core1_thread_id}  secs={secs}")
        letters = ('C', 'O', 'R', 'E', '1')
        for ltr in letters:
            # The test for 'not running' is not really needed:
            # this function runs in the same thread as the main pgm,
            # and that thread catches the KeyboardInterrupt.
            # When that happens, this method is interrupted
            # and control never returns here.
            # But it doesn't hurt to do the check much...
            if not running:
                print("CORE-1: interrupting while doing 'work'")
                break
            print(f"{ltr} 1")
            utime.sleep(secs)
        print("            end core 1 ")

        print("Core-1: release lock")
        the_lock.release()
        # let the other guy run before we re-acquire the lock
        utime.sleep(0.1)
        gc.collect()
        
    print(f"Core-1: exiting")


def core2_thread():
    """ 'second' thread (not the main thread) """
    global the_lock
    global core2_active
    global running
    #####global core2_thread_id
    
    # Weird behavior: the print() below was obtaining the _thread.get_ident() value
    # but it sometimes gets an exception if the program is KeyboardInterrupt'ed.
    # Error is "_thread" is not defined(!?)
    # So we just grab it here, once.
    core2_thread_id = _thread.get_ident()
    
    if 0:
        print(f"   Core-2: start looping.  lock={the_lock}  locked={the_lock.locked()}")
    while running:
        
        print(f"   Core-2: lock={the_lock} locked={the_lock.locked()}")
        # Acquire lock, waiting until it's available
        the_lock.acquire()
        print("   Core-2:  acquired lock")
        
        #print("   Core-2:  sleep a bit")
        #utime.sleep(1)
        secs = 0.5
        print(f"CORE 2:  core ident={core2_thread_id}  secs={secs}")
        letters = ('c', 'o', 'r', 'e', '2')
        for ltr in letters:
            ###print(f" LTR {ltr}")
            if not running:
                print("CORE-2: interrupting while doing 'work'")
                break
            print(f"   {ltr} 2")
            utime.sleep(secs)
        print("            end core 2 ")

        print("   Core-2:  releasing the lock")
        try:
            the_lock.release()
        except Exception as ex:
            # @@@??? captures nothing - 
            print(f"   Core-2: lock.release  EXC={ex}")
            if 0:
                print(f">>{str(ex)}<<")
                print(f">>{type(ex)}<<")
                print(f">>{dir(ex)}<<") # RuntimeError
                print(f"args   >> {ex.args}")   # ()  empty tuple
                print(f"value  >> {ex.value}")  # None
                print(f"errno  >> {ex.errno}")  # None
            
        # give the other  guy a chance
        utime.sleep(0.1)
        gc.collect()
        
    # we are done, exiting
    core2_active = False
    print("   Core-2: exiting")
    
utime.sleep(1) # @@@@@@@@@@@@@@

main_thread_id = _thread.get_ident()
print(f"MAIN:  thread-id is {main_thread_id}")


print("MAIN: create the lock")
the_lock = _thread.allocate_lock()
print(f"  lock is {the_lock}")
print(f"   dir(the_lock) {dir(the_lock)}")
utime.sleep(0.25) # so I can read the above

print(f"MAIN: start thread 2")
second_thread = _thread.start_new_thread(core2_thread, ())
print(f"MAIN:     thread2 = {second_thread}")

utime.sleep(1) #@@@@@@@@@@@@@@@

print(f"MAIN: start thread 1")
#core1_thread()
try:
    core1_thread_polled()
except KeyboardInterrupt:
    print(f"    KEYBOARD INTERRUPT!   thread-id={main_thread_id}")
    print()
print("MAIN: PERFORM CLEANUP -------")
print("MAIN: set 'running' to False")
running = False
print("MAIN: try to release the lock")
try:
    the_lock.release()
    print("MAIN: released the lock successfully.")
except Exception as ex:
    print(f"MAIN: got exc doing lock.release:  {ex}")


ctr = 0
while ctr < 10 and core2_active:
    ctr += 1
    print("MAIN:  waiting for core2 to stop")
    utime.sleep(1)
if core2_active:
    print("MAIN: core2 FAILED TO STOP")
else:
    print("MAIN: core2 has stopped")

print(f"MAIN: exiting")

###
