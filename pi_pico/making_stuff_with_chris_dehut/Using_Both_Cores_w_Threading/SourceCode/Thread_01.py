'''
This demonstration shows the performance loss when only using 1 core.  The PICO has two cores
that can run simultaneously, thus "doubling" the speed it can process data.

This example runs two identical functions, each one is called succesively and thus they
are run sequentially.  When run, it will take approximately 19 seconds to
process all the counting and blinking.  

The use of threading can cause the two functions to run at the same time, thus
doubling the processing speed.

'''
import machine, _thread, time
RED   = machine.Pin(16,machine.Pin.OUT)  #Setup a couple LEDs to show some work
GREEN = machine.Pin(15,machine.Pin.OUT)

core_0_Dur = 0            #preset some GLOBAL variables 
core_1_Dur = 0


def core_1():             #This function will be run in the second core
    global core_1_Dur     #because it is started with the _thread.start command
    st = time.ticks_us()  #record the start time in micro-seconds
    x = 0
    while x < 1000000:    #Count to a million
        x += 1            #increment the counter
        RED.toggle()      #Turn the LED on / off 500,000 times
    et = time.ticks_us()  #record the end time in micro-seconds
    core_1_Dur = et - st  #Calcuate the runtime in micro-seconds
 
def core_0():              #Just an ordinary function, NO THREADING!!!!
    global core_0_Dur      #this function is called in the traditional way
    st = time.ticks_us()
    x = 0
    while x < 1000000:
        x += 1
        GREEN.toggle()
    et = time.ticks_us()
    core_0_Dur = et - st

#main code
st = time.ticks_us()                #record the start time for everything
core_1()							#calls this function to execute
core_0()                            #calls this function to execute
et = time.ticks_us()                #record the end time for everthing

RED.value(0)                        #turn the LEDs off
GREEN.value(0)
duration = et - st                  #duration of everthing in micro-seconds
print("\nTOTAL run time",(duration / 1000000), " Seconds")
print("Core 0 run time",core_0_Dur)
print("Core 1 run time",core_1_Dur)
Difference_us = core_0_Dur - core_1_Dur  #calculate the time difference between the cores
Difference_s = Difference_us / 1000000   #Convert to seconds
print("Time difference between core 0 and 1 =",Difference_us," -- ",Difference_s, " Seconds")
