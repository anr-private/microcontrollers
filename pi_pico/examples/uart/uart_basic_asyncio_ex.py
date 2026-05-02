# uart_basic_asyncio_ex.py
#
# Using asyncio to read and write on a UART.
#
# Setup:
#   Connect two PICOs back to back on a UART channel.
#   Connect the TX of one pico to the Rx of the other and vice versa.
#     Ex: #  UART 0  GPIO 0,1 as Tx,Rx   Connect GPIO0 <--> GPIO1
#     Ex: #  UART 1  GPIO 4,5 as Tx,Rx   Connect GPIO4 <--> GPIO5
#   Ex: Pico #1 using UART1 and Pico #2 using UART 0
#         Pico #1 GPIO-4 Tx  <--->  Pico #2 GPIO-1 Rx
#         Pico #1 GPIO-5 Rx  <--->  Pico #2 GPIO-0  Tx
#
# LOOPBACK CONFIG
# This also can be run as a loopback test.
# Just connect the Tx and Rx pins on a single Pico to each other.
#   Ex:   GPIO-4 Tx  <--->  GPIO-5 Rx


import sys
import time
import asyncio
from machine import UART, Pin

# VERBOSE
V = False

# Sample code showed this alternative:
####  uart = UART(0, baudrate=9600, tx=0, rx=1, timeout=0)

# Init the UART (pick one of these:
#uart = UART(1, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=0)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), timeout=0)

async def uart_sender(writer):
    ctr = 0
    while True:
        ctr += 1
        msg = f"Hello from async UART!  ctr={ctr}\n"
        writer.write(msg.encode())
        await writer.drain()  # Ensure data is sent
        if V: print("Sent message")
        #await asyncio.sleep(1)
        await asyncio.sleep(0.2)

async def uart_receiver(reader):
    while True:
        # 2. Non-blocking read (waits for a newline)
        res = await reader.readline()
        if res:
            print("Received:", res.decode().strip())

async def main():
    # 3. Create StreamReader and StreamWriter wrappers
    reader = asyncio.StreamReader(uart)
    writer = asyncio.StreamWriter(uart, {})

    # Start tasks concurrently
    asyncio.create_task(uart_receiver(reader))
    await uart_sender(writer)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopped")

###
