# list_shared_between_consumer_producer.py
#
# Using a list to pass data from producer to consumer

#import uasyncio as asyncio
import asyncio

shared_data = []

async def data_producer():
    for i in range(5):
        await asyncio.sleep(0.5) # Yield control
        shared_data.append(i)
        print(f"Produced: {i}")

async def data_consumer():
    while len(shared_data) < 5:
        await asyncio.sleep(0.1) # Yield control while waiting
    print(f"Consumer sees all data: {shared_data}")

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

