'''
PICO default clock speed is 125 MHz
Demo to show time to make a bunch of basic math calculations
at varaious clock speeds that the PICO can handle
'''
import machine
import time
import machine

led_onboard = machine.Pin(25, machine.Pin.OUT)

def Do_Stuff():
    st = time.ticks_ms()
    Y = 0
    while Y < 100000:
        Y += 1
        Z = 57
        Z1 = Z + Y
        Z2 = Z - Y
        Z3 = Z * (Z + Y)
        #print(Y, Z1, Z2, Z3)
    led_onboard.value(0)
    #print(Y)
    et = time.ticks_ms()
    #print(et, st, et-st)
    return et-st


cntr = 0
while cntr < 2:    #run whole test several times for observation
    cntr += 1
    
    machine.freq(125000000)  #set clock to 125 MHz
    x = machine.freq()
    t = Do_Stuff()
    print("\n@", x, " time to run =", t, "ms")


    machine.freq(140000000)   #set clock to 140 MHz
    x = machine.freq()
    t = Do_Stuff()
    print("\n@ ", x, " time to run =", t, "ms")


    machine.freq(200000000)  #set clock to 200 MHz
    x = machine.freq()
    t = Do_Stuff()
    print("\n@ ", x, " time to run =", t, "ms")

    machine.freq(250000000)  #set clock to 250 MHz
    x = machine.freq()
    t = Do_Stuff()
    print("\n@ ", x, " time to run =", t, "ms")

machine.freq(125000000)  #set clock to 125 MHz to clean things up
print("\n All Done Folks!")
