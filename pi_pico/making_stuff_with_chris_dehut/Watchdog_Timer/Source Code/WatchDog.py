'''
Watch Dog timer demonstration.  The Watch Dog timer needs to be constant updated
with the time frame defined in its initialization.   It you fail to replenish the
timer, the PICO will reboot.

This is a GREAT feature for those control projects that MUST keep running as it
can self-diagnose a hangup in the program and reboot itself.  Ideally you program
and the PICO would run perfectly and never get stuck, but should it happen, this
feature can save the day!

In this demonstration, the user must press a button within 2 seconds which feeds
the timer and keeps things running.  If it isn't fed within the time frame, the
PICO reboots as it is setup for Auto running because its name is main.py
'''

from machine import WDT   #Watch Dog Timer class
from machine import Pin
from time import sleep

LED    = machine.Pin(25,machine.Pin.OUT)                       # use GP25 as an ouput for the Onboard LED
StallProgram = machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_UP)    # Use GP16 as an INPUT for the switch

for x in range(1,10):  #a simple routine just to flash the LED to alert us it rebooted.
    LED.value(1)
    sleep(.25)
    LED.value(0)
    sleep(.25)

wdt = WDT(timeout=2000)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!
wdt.feed()               # must feed it right away!!

while True:                        # Endless loop
    sleep(.5)                      # Take a brief nap to mimic work being done
    wdt.feed()                     # Replenish (Feed) the timer to keep it running
    print("Thanks!")               # Always thank someone for feeding you!
    if StallProgram.value() != 1:  # If Button is pressed
        while StallProgram.value() != 1:  #Prevent the timer from being fed while held down
            sleep(.1)
        
    




