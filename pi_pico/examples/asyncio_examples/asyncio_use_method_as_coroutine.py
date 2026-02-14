# asyncio_use_method_as_coroutine.py

import uasyncio as asyncio
from machine import Pin
import time

class Blinker:
    def __init__(self, pin_number, period):
        self.led = Pin(pin_number, Pin.OUT)
        self.period = period

    # An asynchronous method
    async def blink_task(self):
        while True:
            self.led.on()
            await asyncio.sleep_ms(50) # Yield control to the event loop
            self.led.off()
            await asyncio.sleep_ms(self.period) # Yield control to the event loop

async def main():
    # Create instances of the Blinker class
    blinker1 = Blinker(12, 500)
    blinker2 = Blinker(14, 200)

    # Create tasks from the async methods and schedule them
    asyncio.create_task(blinker1.blink_task())
    asyncio.create_task(blinker2.blink_task())

    # Run the main coroutine for a set duration
    await asyncio.sleep_ms(10000)

# Start the event loop and run the main coroutine
try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
finally:
    asyncio.new_event_loop() # Optional: cleanup the event loop state
