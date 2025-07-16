# Multiple timers running at timeouts; main loop runs independently  ANR
# Main loop runs without interruption

# LEDs on GPIO 12,13,14,15  (board pins 16,17,19,20)

# See fritzing file for wiring

import machine
import utime
from machine import Timer

Blue   = machine.Pin(12,machine.Pin.OUT)
Red    = machine.Pin(13,machine.Pin.OUT)
Green  = machine.Pin(14,machine.Pin.OUT)
Yellow = machine.Pin(15,machine.Pin.OUT)

#Create handlers for the timer IRQ
def Blue_Blinker(Source):
    Blue.toggle()

def Red_Blinker(Source):
    Red.toggle()

def Green_Blinker(Source):
    Green.toggle()

def Yellow_Blinker(Source):
    Yellow.toggle()


#Periodic timers to run continuously - 1 for each LED
#Timers run at a base of 1 millisecond (.001) seconds
#1 would be 1 millisecond
#500 would be 1/2 second
#1000 would be 1 second
#10000 would be 10 seconds
Blue_Timer = Timer(period=2000, mode=Timer.PERIODIC, callback=Blue_Blinker)
Red_Timer = Timer(period=1000, mode=Timer.PERIODIC, callback=Red_Blinker)
Green_Timer = Timer(period=500, mode=Timer.PERIODIC, callback=Green_Blinker)
Yellow_Timer = Timer(period=250, mode=Timer.PERIODIC, callback=Yellow_Blinker)

#Create a main loop to keep the program running
#in this loop you would do all your other work
loop_ctr = 0
try:
    while True:
        loop_ctr += 1
        print(f"   main: loop ctr={loop_ctr}")
        utime.sleep(1)
except KeyboardInterrupt as ex:
    print(f"MAIN: keyboard interrupt.  Do cleanup.")

    #Turn off the timers so the program terminates cleanly
    Blue_Timer.deinit()
    Red_Timer.deinit()
    Green_Timer.deinit()
    Yellow_Timer.deinit()

    # Give time for the timers to shut down
    # Else the LEDs may not turn off in the steps below
    #utime.sleep(1) NOT NEEDED if you use the try/except(?!)

    #Turn off all the LEDs so keep things tidy
    Blue.value(0)
    Red.value(0)
    Green.value(0)
    Yellow.value(0)

print("End of MAIN")

### end ###

