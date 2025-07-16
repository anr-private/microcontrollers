'''
Example program showing the application of ULN2803 as a buffer on the PICO
The purpose of this example is to show the importance of having a buffer
between the PICO and loads.  The PICO outputs can only source approximately
10mA of current on a pin, however, all the pins can only sources a limtted
amount of power as well.  Micro controllers can drive very small currents
but these boundaries should not be pushed or catastrophic failure is assured.

A buffer chip, such as the ULN2803 takes a logic level input and through
a darlington pair of transistors can drive upwards of 500mA of current.

This program simply uses the PICO GPIO pins to switch on/off relays
and a high power LED to demonstrate how to impliment the ULN2803 chip.

There is an associated fritzing diagram to show the wiring.

'''
#load libraries
import machine
import utime

Relays = [0]
Relays.append(machine.Pin(15,machine.Pin.OUT))  #Create a list of output pin objects
Relays.append(machine.Pin(14,machine.Pin.OUT))
Relays.append(machine.Pin(13,machine.Pin.OUT))
Relays.append(machine.Pin(12,machine.Pin.OUT))
Relays.append(machine.Pin(20,machine.Pin.OUT))
Relays.append(machine.Pin(28,machine.Pin.OUT))

for rn in range(1,7):      #Iterate through the list            
    Relays[rn].value(0)    #Turn OFF outputs

while True:
    for rn in range(1,7):      #Iterate through the list
        Relays[rn].value(1)    #Turn ON the outputs
        print("R",rn," ON")
        utime.sleep(1)
        
    for rn in range(1,7):
        print("R",rn," OFF")
        Relays[rn].value(0)    #Turn OFF outputs
        utime.sleep(1) 


