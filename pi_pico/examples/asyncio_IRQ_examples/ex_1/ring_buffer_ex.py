import asyncio
import micropython
import machine

# --- 1. Fixed-Size Ring Buffer Class ---
class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [0] * size  # Pre-allocate all memory once
        self.head = 0  # Write pointer
        self.tail = 0  # Read pointer
        self.count = 0

    def put(self, val):
        """Adds data; returns False if buffer is full."""
        if self.count == self.size:
            return False 
        self.buffer[self.head] = val
        self.head = (self.head + 1) % self.size
        self.count += 1
        return True

    def get(self):
        """Removes and returns data; returns None if empty."""
        if self.count == 0:
            return None
        val = self.buffer[self.tail]
        self.tail = (self.tail + 1) % self.size
        self.count -= 1
        return val

# --- 2. Shared Resources ---
rb = RingBuffer(20)          # Buffer for 20 incoming integers
signal = asyncio.ThreadSafeFlag()

# --- 3. IRQ & Scheduler Logic ---
def scheduled_put(val):
    """Runs in 'main' context: safe to interact with the buffer."""
    if not rb.put(val):
        print("Buffer Overflow!")
    signal.set() # Wake up the processor task

def irq_handler(pin):
    """Hardware IRQ: very fast, schedules the data transfer."""
    # Example: use pin ID as the data value
    pin_id = 1 
    micropython.schedule(scheduled_put, pin_id)

# --- 4. Asyncio Tasks ---
async def data_processor():
    """Wakes up on signal and clears the ring buffer."""
    print("[Processor] Waiting for data...")
    while True:
        await signal.wait()  # Sleep efficiently
        
        while rb.count > 0:
            item = rb.get()
            print(f"[Processor] Handled: {item}")

async def background_checker():
    """Periodically checks buffer status without blocking."""
    while True:
        # We can check 'rb.count' anytime to see how full it is
        print(f"[Monitor] Buffer usage: {rb.count}/{rb.size}")
        await asyncio.sleep(5)

async def main():
    # Setup your pins here
    # p1 = machine.Pin(0, machine.Pin.IN).irq(handler=irq_handler)
    
    print("--- System Ready ---")
    asyncio.create_task(data_processor())
    asyncio.create_task(background_checker())
    
    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopped")

###

