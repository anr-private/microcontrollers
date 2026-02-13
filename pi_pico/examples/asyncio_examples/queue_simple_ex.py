import asyncio
from primitives.queue import Queue  # Requires copying queue.py

async def producer(q):
    await q.put(1)  # Produce data
    
async def consumer(q):
    item = await q.get()  # Consume data
    print(item)

# Setup
q = Queue()
# ... run with loop
