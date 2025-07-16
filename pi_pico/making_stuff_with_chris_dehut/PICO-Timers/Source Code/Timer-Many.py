# Demonstration of multiple timers running at various speeds
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
Limit = 0
while Limit <= 10:  #Main loop
    print(Limit)
    Limit += 1
    utime.sleep(1)


#Turn off the timers so the program terminates cleanly
Blue_Timer.deinit()
Red_Timer.deinit()
Green_Timer.deinit()
Yellow_Timer.deinit()

#Turn off all the LEDs so keep things tidy
Blue.value(0)
Red.value(0)
Green.value(0)
Yellow.value(0)
