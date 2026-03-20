import uasyncio as asyncio
import _thread
import time

# Shared state to communicate between threads
result_message = ""
done_event = asyncio.Event()

def blocking_function_thread(data):
    global result_message
    # ... perform blocking work ...
    time.sleep(2)
    result_message = f"Processed: {data}"
    done_event.set() # Signal completion

async def run_blocking_in_thread(data):
    global result_message
    result_message = "" # Reset
    done_event.clear() # Reset event

    # Start the blocking function on the second core
    _thread.start_new_thread(blocking_function_thread, (data,))

    # Await the event in the main asyncio loop
    await done_event.wait()
    print(f"Received result in main loop: {result_message}")

async def main():
    await asyncio.gather(
        run_blocking_in_thread("some data"),
        # Other async tasks can run concurrently
        # For example, a task to blink an LED
    )

# asyncio.run(main())

###

