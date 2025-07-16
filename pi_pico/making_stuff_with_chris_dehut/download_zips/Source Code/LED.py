import machine
import utime

LED = machine.Pin(25, machine.Pin.OUT) #Set pin 25 as output

while True:
    LED.value(1) #Turn on LED
    utime.sleep(.5) 
    LED.value(0) #Turn off LED
    utime.sleep(.25)
