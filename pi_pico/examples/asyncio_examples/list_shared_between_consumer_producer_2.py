# list_shared_between_consumer_producer_2.py
#
# Using a list to pass data from producer to consumer
#
# Adjusting these determines how the consumer and producer
# react.
# If producer sleep is much smaller than consumer, it can
# produce and en-Q a number of data items before the
# consumer wakes up. Then the consumer consumes them
# all at once.

NUM_ITEMS_PRODUCED = 25
CONSUMER_SLEEP = 0.5
PRODUCER_SLEEP = 0.05


import asyncio

shared_data = []

async def data_producer():
    for i in range(NUM_ITEMS_PRODUCED):
        data_item = i+1        
        await asyncio.sleep(PRODUCER_SLEEP) # Yield control
        shared_data.append(data_item)
        print(f"@26 Produced: {data_item}")

async def data_consumer():
    ###while len(shared_data) < 5:
    while True:
        if len(shared_data) > 0:
            v = shared_data.pop(0)
            print(f"@33        Received {v} ")
            continue
        # no data yet, wait a bit
        await asyncio.sleep(CONSUMER_SLEEP) # Yield control while waiting

async def main():
    producer_task = asyncio.create_task(data_producer())
    consumer_task = asyncio.create_task(data_consumer())
    await producer_task
    await consumer_task
    print("Done")

# Run the main coroutine
try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
finally:
    asyncio.new_event_loop() # Clear the event loop for potential re-runs

###

