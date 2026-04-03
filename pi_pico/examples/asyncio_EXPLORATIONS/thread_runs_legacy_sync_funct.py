#

# Example: the official way to signal asyncio from another thread

import time
import _thread
import asyncio
###from machine import idle 

def legacy_blocking_task_function(duration):
    # simulate a legacy function that would block the asyncio event loop
    # It gets run in a different thread than the asyncio loop runs.
    # This 'sleep' loop would normally stall asyncio
    secs = 0
    while secs < duration:
        time.sleep(1)
        secs += 1
        print(f"@28   legacy function sleeping;  secs={secs}  timeout(duration)={duration}")
    print("@39  Legacy function has completed.")
    return "Task Complete"


async def run_sync_in_thread(func, *args, **kwargs):
    # Run a syncronous task using a second thread.
    # This keeps the sync task from stalling the asyncio event loop.

    # 1. Create a flag for cross-thread synchronization
    flag = asyncio.ThreadSafeFlag()

    # This var is used by the thread wrapper to return the 
    # result from the simulated sync function.
    # It is 'NONLOCAL' (hence the funky name, to underscore this fact).
    # That means the thread_wrapper() function can access it,
    # kinda like a global variable.
    # It might be less confusing if we just used a Result class / obj
    # that we would pass to thread_wrapper (via start_new_thread)
    # But using a nonlocal is cheap and easy if somewhat icky.
    NONLOCAL_result = None

    def thread_wrapper():
        # this function runs in the second thread
        nonlocal NONLOCAL_result
        # 2. Execute the legacy synchronous function
        NONLOCAL_result = func(*args, **kwargs)
        # 3. Signal the asyncio task that we are done
        flag.set()

    # 4. Start the blocking function in its own ('second') thread
    _thread.start_new_thread(thread_wrapper, ())

    # 5. Await the flag without stalling other asyncio tasks
    # The flag is set from the 'second' thread, which is why 
    # it must be a ThreadSafeFlag.
    await flag.wait()

    return NONLOCAL_result


async def primary_work_function():
    # this is the 'main' worker thread - it uses the legacy function
    # but does not allow it to block the asyncio event loop.
    # So it uses a separate thread to call the legacy function.
    print(f"@46 primary_work_function has STARTED.")
    await asyncio.sleep(1) # pretend to do something

    # Invoke the 'legacy' function by using the 'run it on a different thread'
    # function.
    print(f"@63    PRIMARY: invoke the 'legacy' function")
    # We are performing this invocation, using the 'second' thread:
    #    legacy_blocking_task_function(4)
    res = await run_sync_in_thread(legacy_blocking_task_function, 4)
    print(f"@72    PRIMARY legacy function result: {res}")

    print(f"@48 primary_work_function has COMPLETED.")


async def ctr_task_function(secs_limit):
    # this is 'another' task that is running - we don't want it to get
    # blocked when the 'legacy' function is invoked
    secs = 0
    while secs < 6:
        print(f"@46         ctr_task 'working'  secs={secs}  limit={secs_limit}")
        await asyncio.sleep(1)
        secs += 1

async def main():
    ctr_task = asyncio.create_task(ctr_task_function(7))
    print(f"MAIN@52  ctr_task is {ctr_task}")
    worker_task = asyncio.create_task(primary_work_function())
    print(f"MAIN@52  ctr_task is {worker_task}")

    secs = 0
    while secs < 15:
        worker_done = worker_task.done()
        ctr_done = ctr_task.done()
        #print(f"@56 MAIN:  WORKER-DONE: {worker_done}  CTR.done={ctr_done}")
        if worker_done and ctr_done:
            print(f"@72 MAIN: both tasks are done, so MAIN will now finish.")
            break
        await asyncio.sleep(1)
        secs += 1

    print(f"@74 MAIN has completed in {secs} seconds.")


    if 0:
        print("@43 Starting background task...")
        # This call is non-blocking for the event loop
        res = await run_sync_in_thread(legacy_blocking_task_function, 5)
        print(f"@46  result={res}")

asyncio.run(main())

###
