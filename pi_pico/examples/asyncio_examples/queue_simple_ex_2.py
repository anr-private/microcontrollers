# queue_simple_ex_2.py
#
# Simple Queue example #2
#
# Producer loops, producing numbers

import asyncio
from primitives.queue import Queue  # Requires copying queue.py

async def producer(q):
    ctr  = 100
    while 1:
        print(f"PRODUCER: put {ctr=}")
        await q.put(ctr)  # Produce data
        await asyncio.sleep(1)
        ctr += 1
        
async def consumer(q):
    while 1:
        item = await q.get()  # Consume data
        print(f"CONSUMER: got {item=}")

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
