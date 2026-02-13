# queue_simple_ex_2.py
#
# Simple Queue example #2
#
# Producer loops, producing numbers

import asyncio
from primitives.queue import Queue, QueueEmpty

async def producer(q):
    """ puts a number in the Q once a second """
    ctr  = 100
    while 1:
        print(f"PRODUCER: put {ctr=}")
        await q.put(ctr)  # Produce data
        await asyncio.sleep(1)
        ctr += 1
        
async def consumer(q):
    """ Consumes as much as it can, as fast as items appear in the Q
    When the Q is emptied, it waits for a while.
    NOTE it uses 'q.get_nowait() with no 'await' -- get_nowait() is NOT a coro.
    NOTE the QueueEmpty evals to an empty string - you need to use repr(ex)!
    """
    while 1:
        try:
            item = q.get_nowait()  # Consume data
            print(f"                  CONSUMER: got {item=}")
        except QueueEmpty as ex:
            print(f"                  CONSUMER got ex='{ex}'  s='{str(ex)}'  repr='{repr(ex)}' ")
            await asyncio.sleep(3)
        
async def SIMPLER_consumer(q):
    """ Consumes as much as it can, as fast as items appear in the Q
    NOTE it uses 'await q.get()' - get() is a coro
    """
    while 1:
        item = await q.get()  # Consume data
        print(f"CONSUMER: got {item=}")

async def main_loop(q):
    asyncio.create_task(producer(q))
    asyncio.create_task(consumer(q))
    
    # just do some 'work' in main
    ctr = 0
    while 1:
        print(f"                                                                   Main: count={ctr}")
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
