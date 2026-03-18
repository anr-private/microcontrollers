import asyncio
import micropython
import machine
import time

# --- Global Buffers & Signaling ---
# A standard list to hold data from the IRQs
data_queue = []
# Special flag for signaling across IRQ/Main contexts
data_signal = asyncio.ThreadSafeFlag()

# --- IRQ & Scheduler Logic ---

def scheduled_data_arrival(val):
    """Runs in the main context (allowed to allocate memory)."""
    data_queue.append(val)
    # Signal the asyncio Task that new data is ready
    data_signal.set()

def irq_handler(pin):
    """Minimal Hardware IRQ handler."""
    # We pass the pin ID (1, 2, or 3) to the scheduler
    # We use a simple logic here to identify which pin triggered
    pin_id = int(str(pin)[4:6]) # Simple string slice to get pin number
    micropython.schedule(scheduled_data_arrival, pin_id)

# Setup 3 Input Pins with IRQs
pins = [machine.Pin(i, machine.Pin.IN, machine.Pin.PULL_UP) for i in (0, 1, 2)]
for p in pins:
    p.irq(trigger=machine.Pin.IRQ_FALLING, handler=irq_handler)

# --- asyncio Tasks ---

async def incoming_data_consumer():
    """
    Main handler task. It waits for the signal, then processes 
    ALL items in the queue before yielding.
    """
    print("[Consumer] Ready and waiting for IRQ data...")
    while True:
        # Wait for the flag (this is non-blocking to other tasks)
        await data_signal.wait()
        
        # Process every item that arrived since we last woke up
        while data_queue:
            val = data_queue.pop(0)
            print(f"[Consumer] Handled data from IRQ Pin: {val}")
        
        # In MicroPython, ThreadSafeFlag.wait() self-clears upon return.

async def periodic_status_checker():
    """
    Illustrates a task checking for data periodically while 
    performing other background work.
    """
    while True:
        queue_size = len(data_queue)
        print(f"[Monitor] Current queue size: {queue_size}")
        
        # Perform some "periodic" work or checks here
        if queue_size > 10:
            print("[Monitor] Warning: High IRQ traffic detected!")
            
        # Non-blocking pause; allows consumer and other tasks to run
        await asyncio.sleep(3)

async def main():
    print("--- System Booted ---")
    
    # Schedule our tasks into the event loop
    # They will now run 'concurrently'
    asyncio.create_task(incoming_data_consumer())
    asyncio.create_task(periodic_status_checker())
    
    # Run forever
    while True:
        await asyncio.sleep(1)

# Start the application
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("System Shutdown")

###

