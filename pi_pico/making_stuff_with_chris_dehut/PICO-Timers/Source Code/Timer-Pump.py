# Use a one-shot timer to do a task for a specific period of time.  ANR
# Main loop runs in parallel

# see fritzling/ for wiring - uses 2 LEDs  GPIO 12, 13

#load libraries
import machine
import utime
from machine import Timer

#Create outputs for each LED
Blue   = machine.Pin(12,machine.Pin.OUT)
Pump   = machine.Pin(13,machine.Pin.OUT)

#Create handlers for the timer IRQ
def Blue_Blinker(Source):
    Blue.toggle()
    
def Pump_Off(Source):
    Pump.value(0)

#Periodic timer to run continuously
#Timers run at a base of 1 millisecond (.001) seconds
#1 would be 1 millisecond
#500 would be 1/2 second
#1000 would be 1 second
#10000 would be 10 seconds
Blue_Timer = Timer(period=2000, mode=Timer.PERIODIC, callback=Blue_Blinker)


#Create a main loop to keep the program running
#in this loop you would do all your other work
Limit = 0
while Limit <= 20:  #Main loop
    print(Limit)
    Limit += 1
    utime.sleep(1)
    
    if Limit == 10:  #start pump running
        Pump.value(1)  #Turn pump on by setting its value to 1
        Pump_Timer = Timer(period=9000, mode=Timer.ONE_SHOT, callback=Pump_Off)
       

#Turn off the timer so the program terminates cleanly
Blue_Timer.deinit()
Pump_Timer.deinit()

#Turn off the LED to keep things tidy
Blue.value(0)
