import asyncio
from primitives.queue import Queue  # Requires copying queue.py

async def producer(q):
    await q.put(1)  # Produce data
    
async def consumer(q):
    item = await q.get()  # Consume data
    print(item)



async def main_loop(q):
    asyncio.create_task(producer(q))
    asyncio.create_task(consumer(q))
    
    # just do some 'work' in main
    ctr = 0
    while 1:
        print(f"Main: counted to {ctr}")
        ctr += 1 
        await asyncio.sleep_ms(2_000)



def main():

    # Setup
    q = Queue()
    print(f"MAIN: Created Q {q}")

    try:
        asyncio.run(main_loop(q))
    except KeyboardInterrupt:
        print(f"=== Interrupted by USER control-C")


main()

### end ###
