This is a project from YouTube channel Bytes N Bits.
See README.md

It uses a webserver running on a Pi Pico. You connect to it using a browser.
It provides commands for reading analog value from the Pico and for controlling
GPIO pins.
The fancy version also allows for a 'worker' activity to run at the same time,
with the webserver not interfering with it or holding onto the processor
so that the activity gets starved.

Attempted to make it runnable under Linux by providing some simulated
classes etc that are normally found on the Micropython on the Pico.
Ex:  utime.py
    network.py
    uasyncio.py
    machine.py

###

