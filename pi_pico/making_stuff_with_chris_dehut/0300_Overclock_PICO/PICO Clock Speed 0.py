'''
PICO default clock speed is 125 MHz
Demo to show time to make a bunch of basic math calculations
'''
import machine
import time
import machine

led_onboard = machine.Pin(25, machine.Pin.OUT)

def Do_Stuff():
    st = time.ticks_ms()    
    Y = 0                   #do lots of calculations to consume processing time
    while Y < 100000:
        Y += 1
        Z = 57
        Z1 = Z + Y
        Z2 = Z - Y
        Z3 = Z * (Z + Y)
    led_onboard.value(0)
    print(Y)
    et = time.ticks_ms()
    #print(et, st, et-st)
    return et-st


led_onboard.value(1)
t = Do_Stuff()
print("Time to run =", t, "ms")

print("\n All Done Folks!")
