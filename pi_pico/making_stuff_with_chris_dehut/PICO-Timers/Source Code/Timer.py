# Demonstration of a timer calling back to a function
# Main loop runs without interruption

#ALSO REQUIRED!!!
#220 ohm resistors
#LEDs (not high power)
#Wire according to information provided on associated video on YouTube

#load libraries
import machine
import utime
from machine import Timer

#Create outputs for each LED
Blue   = machine.Pin(12,machine.Pin.OUT)

#Create handlers for the timer IRQ
def Blue_Blinker(Source):
    Blue.toggle()

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
while Limit <= 10:  #Main loop
    print(Limit)
    Limit += 1
    utime.sleep(1)


#Turn off the timer so the program terminates cleanly
Blue_Timer.deinit()

#Turn off the LED to keep things tidy
Blue.value(0)
