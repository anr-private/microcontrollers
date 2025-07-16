'''
Demonstration of the RPR-220 Reflective Optical Sensor
With the addition of a few resistors to complete the circuit,
this demonstraiton program shows how to detect the change in
state of the sensor and how to deal with that via an interrupt.

This is the reflective phototransistor used
https://www.amazon.com/dp/B07K1HVNH7

check schematic referenced in the video
'''
from time import sleep_ms
from machine import Pin

#Global Elements
Photo_pin = machine.Pin(15, machine.Pin.IN)
Pulse_Counter = 0


###-----------------------------------------------
# Interrupt handler for the RPR220 sensor 
def Sensor_Counter(p):                                       #function to count each pulse from sensor
    global Pulse_Counter                                     #Global variable    
    Pulse_Counter += 1                                       #Increment Pulse_Counter by 1 
Photo_pin.irq(handler=Sensor_Counter, trigger=machine.Pin.IRQ_RISING)  #Define interrupt handler trigger and Function

###-----------------------------------------------
# Endless Loop Section
Last_Cntr = 0              # Used for reducing print statements below     
while True:                #Endless Main Loop
    if Last_Cntr != Pulse_Counter:
        print("Pulse Counter",Pulse_Counter)
        Last_Cntr = Pulse_Counter
    sleep_ms(10)                   

