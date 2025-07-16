'''
This demonstration shows the performance gain by using _thread.  The PICO has two cores
that can run simultaneously, thus "doubling" the speed it can process data.

This example runs two identical functions, one is in a thread the other runs
from the main program.  When run, it will take approximately 9.5 seconds to
process all the counting and blinking.  If we comment out the _thread.start line
in the main code and run it, the program still takes approximately 9.5 to
run.  Essentially doing half the amount of work in the same time.

To help visualize this, think of all non-threaded programs running in core 0 and
core 1 is sitting idle, doing nothing.  When using the _thread.start to call a
function, it is being run in core 1.

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
_thread.start_new_thread(core_1,()) #Starts the thread running in core 1
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
