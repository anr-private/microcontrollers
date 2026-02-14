# asyncio_independent_tasks.py
#
# Demonstrates how one coroutine can start another coroutine
# and let it run in parallel, without the first coroutine
# waiting for it.

import uasyncio

async def independent_task(name, duration):
    print(f"Task {name} started and will run for {duration} seconds independently.")
    await uasyncio.sleep(duration)
    print(f"Task {name} finished.")
    return "this is the result from independent_task"

async def main_coroutine():
    print("Main coroutine started.")
    
    # Start the independent task
    # create_task schedules the coroutine but does not await it
    task = uasyncio.create_task(independent_task("A", 3))
    
    print("Task A scheduled, main coroutine continues immediately.")
    
    # Perform other work in the main coroutine
    await uasyncio.sleep(1)
    print("Main coroutine just did some 'work'.")
    
    # To ensure the event loop has a chance to run other tasks, 
    # the current task must yield control at some point.
    # asyncio.sleep(x) or asyncio.sleep(0) are common ways.
    await uasyncio.sleep(1)
    print("Main coroutine just did more work.")

    # The main coroutine will finish before 'independent_task' unless 
    # something keeps the event loop running or the main coroutine awaits 
    # the task at some point (which defeats the "independent" part if you 
    # need the result).
    
    # For a continuously running system, your main coroutine might have 
    # a while True: loop that occasionally yields with await asyncio.sleep(0) 
    # or await asyncio.sleep(some_time).

    # In this specific example, without a final await on the task or 
    # a continuous loop in main, the program would exit when main finishes and
    # the independent task would never get a chance to run if it's not done.
    # We can await a long sleep in main to show the independent task running.
    if 0:
        print("Main coroutine sleeping for a while to let other tasks run.")
        await uasyncio.sleep(4)
    # Another approach is to wait on the Task object - to tell when the task is done.
    if 1:
        print("MAIN: wait for the independent task to finish  Use the Task object from create_task()")
        r = await task
        print(f"MAIN:  await task   has returned, result = {r}")
        
    print("Main coroutine finished.")

# Start the event loop with the main coroutine as the entry point
uasyncio.run(main_coroutine())

###

