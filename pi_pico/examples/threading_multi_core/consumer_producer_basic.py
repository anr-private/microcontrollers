import uasyncio as asyncio
from machine import Pin # Assuming a board like ESP32 or Pico with GPIO

print(asyncio.Queue)

# Example: Producer coroutine
async def producer(queue, led_pin):
    led = Pin(led_pin, Pin.OUT)
    count = 0
    while True:
        await asyncio.sleep(1) # Simulate some work
        message = f"Data item {count}"
        await queue.put(message)
        print(f"Producer: Put '{message}' into queue")
        led.value(not led.value()) # Toggle LED to show activity
        count += 1

# Example: Consumer coroutine
async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"Consumer: Got '{item}' from queue")
        await asyncio.sleep(0.5) # Simulate processing the item

async def main():
    q = asyncio.Queue()
    # Assuming LED is connected to GPIO pin 2 (adjust for your board)
    await asyncio.gather(
        producer(q, 2),
        consumer(q)
    )

# Start the event loop
asyncio.run(main())