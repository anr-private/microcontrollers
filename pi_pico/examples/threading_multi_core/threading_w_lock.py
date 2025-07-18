# thread sync using a Lock

# from time import sleep
import time
import _thread

def core0_thread():
    global lock
    while True:
        # try to acquire lock - wait if in use
        lock.acquire()

        if 1:
            print(f"   lock.locked() = {lock.locked()}")

        print('C')
        time.sleep(0.25)
        print('O')
        time.sleep(0.25)
        print('R')
        time.sleep(0.25)
        print('E')
        time.sleep(0.25)
        print('0')
        time.sleep(0.25)
        print("            end core 0 ")
        
        # release lock
        lock.release()
        
        # let the other guy have a shot at the lock
        time.sleep(0.25)

def core0_thread_polled():
    """ Use lock.locked() to poll the lock instead of blocking """
    global lock
    while True:
        wait_counter = 0
        # try to acquire lock but don't wait
        while not lock.acquire(0):  # lock.acquire(waitflag=1, timeout=-1)
            # count the number of times the lock is polled
            # Our code is not in a waiting state
            # we are just polling the lock at the end of each loop iteration
            wait_counter += 1

        print("CORE 0 - I counted to " + str(wait_counter) + " while waiting")
        print('C')
        time.sleep(0.5)
        print('O')
        time.sleep(0.5)
        print('R')
        time.sleep(0.5)
        print('E')
        time.sleep(0.5)
        print('0')
        time.sleep(0.5)

        # release lock
        lock.release()

def core1_thread():
    global lock
    while True:
        # try to acquire lock - wait if in use
        lock.acquire()

        print('c')
        time.sleep(0.25)
        print('o')
        time.sleep(0.25)
        print('r')
        time.sleep(0.25)
        print('e')
        time.sleep(0.25)
        print('1')
        time.sleep(0.25)
        print("            end core 1 ")
        # release lock
        lock.release()
       
        # let the other guy have a shot at the lock
        time.sleep(0.25)


print("MAIN: create the lock")
lock = _thread.allocate_lock()
print(f"  lock is {lock}")
print(f"   dir(lock) {dir(lock)}")
time.sleep(0.25) # so I can read the above

print(f"MAIN: start thread 2")
second_thread = _thread.start_new_thread(core1_thread, ())
print(f"   thread2 = {second_thread}")

print(f"MAIN: start thread 1")
#core0_thread()
core0_thread_polled()

print(f"MAIN: exiting")

###

        