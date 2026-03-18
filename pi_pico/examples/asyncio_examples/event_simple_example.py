import uasyncio as asyncio
from machine import Pin # Example import for a generic board

# Assuming an LED is connected to Pin(1)
# led_pin = Pin(1, Pin.OUT) 

async def signalling_task(event):
    print("Signalling task: Doing some work...")
    await asyncio.sleep(2) # Simulate some work
    print("Signalling task: Setting the event.")
    event.set() # Set the event flag

async def waiting_task(event):
    print("Waiting task: Waiting for the event to be set...")
    await event.wait() # Pause here until event is set
    print("Waiting task: Event received! Continuing execution.")
    event.clear() # Clear the event for future use, if needed
    # You can add more logic here after the signal

async def main():
    event = asyncio.Event() # Create an Event object
    
    # Create and schedule both tasks
    asyncio.create_task(signalling_task(event))
    asyncio.create_task(waiting_task(event))
    
    # Keep the main loop running long enough to see the result
    await asyncio.sleep(5) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.new_event_loop() # Optional: clear the event loop state


###

