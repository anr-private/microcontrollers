# asyncio_write_a_file.py

##import uasyncio as asyncio
import asyncio
import machine

MAIN_TASK = None
OTHER_TASK = None

def tname(the_task = None):
    if the_task is None:
        the_task = asyncio.current_task()
    if the_task is OTHER_TASK:
        return "OTHER-TASK"
    if the_task is MAIN_TASK:
        return "MAIN-TASK"
    return "UNK-TASK"
        
async def write_to_file(filename, data):
    global MAIN_TASK, OTHER_TASK
    print(f"[{tname()}] Starting file write...")
    try:
        # Standard synchronous file opening and writing
        with open(filename, "a") as f:
            f.write(data + "\n")
        print(f"[{tname()}] Finished file write.")
    except Exception as e:
        print(f"Error writing to file: {e}")
    # Yield control back to the event loop
    await asyncio.sleep_ms(1)

async def other_task():
    global MAIN_TASK, OTHER_TASK
    while True:
        print(f"[{tname()}] Doing other things...")
        await asyncio.sleep_ms(500) # Yield for other tasks

async def main():
    global MAIN_TASK, OTHER_TASK
    print(f"CURRENT TASK: {asyncio.current_task()} ")
    print(f"DIR(task) {dir(asyncio.current_task())} ")
    MAIN_TASK = asyncio.current_task()
    # Set task names for easier debugging in this example
    ###asyncio.current_task()._name = "Main"
    
    # Create tasks
    ###OTHER_TASK = asyncio.create_task(other_task(), name="Task 1")
    OTHER_TASK = asyncio.create_task(other_task())
    
    # Write to file
    await write_to_file("log.txt", "Hello, Async World!")
    await write_to_file("log.txt", "Another line of data.")
    
    # Keep the main loop running
    await asyncio.sleep_ms(5000)
    
    # Optional: Read back the file content to verify
    with open("log.txt", "r") as f:
        print("--- File Contents ---")
        print(f.read())
        print("---------------------")

# Run the event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    # Cleanup the event loop after the main task completes or is cancelled
    asyncio.new_event_loop()
print(f"END OF asyncio_write_a_file EXAMPLE PGM")


###
