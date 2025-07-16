'''
STEP-DIR

This example shows how to control a stepper motor using
a Step & Direction drive.  Velocity is controled by
specifying the time delay between steps, but in this
example we specify the desired RPM.

Motor is 200 steps / rev
Stepping is set to 8 microsteps
200 * 8 = 1600 steps / revolution
'''

import machine
from time import sleep_us
from time import ticks_ms

#assign output pins for driver
Step_P = machine.Pin(14,machine.Pin.OUT) #Connect to PUL+
Dir_P  = machine.Pin(15,machine.Pin.OUT) #Connect to DIR+
LED    = machine.Pin(25,machine.Pin.OUT) #On PICO LED

Steps_Per_Rev = 1600
Calibration_Factor = .915   #Adjusted from practical testing 

def Make_Step():
    Step_P.value(1)     #Set step pin high
    sleep_us(3)         #Sleep for a very short time
    Step_P.value(0)     #Set step pin to LOW - thus creating a "pulse"
    LED.toggle()        #Toggle the LED

def RPM_2_Dwell(RPM):
    Revs_Per_Sec = RPM / 60                       #Convert RPM to R/Seconds
    Steps_Per_Sec = Steps_Per_Rev * Revs_Per_Sec  #Calc the total steps / second  
    Dwell = (1 / Steps_Per_Sec) * 1000000         #Calc Dwell time in microseconds
    Dwell = round(Dwell * Calibration_Factor)     #Adjust delay with calibration factor   
    return Dwell

Dir_P.value(0)   #Set direction pin LOW
sleep_us(5)     

Steps = 0       #This is a counter for number of steps made
RPM = 500        #You specify the RPM you want the motor to run here
Rotations = 20  #You specify the number of rotations for the motor to make

Dwell = RPM_2_Dwell(RPM)   #Calcualate the dwell time
print("Start run",Dwell)

Revs = 0                #Counter to track number of rotations made
Start = ticks_ms()      #Record ending millisecond counter
print(Start)
while True:             #Endless loop
    Make_Step()         #Make 1 step
    Steps += 1          #Increment counter
    sleep_us(Dwell)     #Sleep microseconds!!!!
    if Steps >= Steps_Per_Rev:  #test if a full revolution is made
        Revs += 1       #Increment the revolutions made counter
        print(Revs)
        Steps = 0       #Reset the Steps made counter 
        if Revs >= Rotations:  #Test if all desired rotations have been made
            End = ticks_ms()   #Record ending millisecond counter
            print(End)
            break              #Exit the loops
Elapsed = round(((End - Start)/1000),2)  #Compute the run time
print(Elapsed , "Seconds Run Time.  \nThat's all folks!")    