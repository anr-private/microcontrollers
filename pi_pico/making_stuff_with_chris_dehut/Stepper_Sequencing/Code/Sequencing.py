'''
Demonstration of sequencer/driver for stepper motor using ULN2003APG module

Source for ULN2003APG module and stepper motor
https://www.amazon.com/sourcing-map-Electronics-Accessories-ULN2003APG/dp/B0B28XRYZX/ref=sr_1_1?crid=8XZ8GWCL6I8I

CALCULATING STEPS PER REVOLUTION at OUTPUT SHAFT
Motor is 5.625 degrees / step
360 degrees / 5.625 = 64 Steps / revolution of MOTOR
Gear ratio is 1:64
64 steps/rev * 64 Gear Ratio = 4096 Steps / revolution at OUTPUT SHAFT
360 / 4096 = .08789 degrees / step at OUTPUT SHAFT

MAX RPM @ 5V
From testing, 800 microseconds between steps was the fastest
1 / .0008 = 1250 steps per second
1250 steps per second * 60 seconds = 75000 steps per minute
75000 / 4096 steps per revolution = 18.31 revolutions per minute

No external libraries needed
'''


import machine
from time import sleep_us

#assign output pins for motor coils
C_1 = machine.Pin(1,machine.Pin.OUT) #Connect to IN1 on module
C_2 = machine.Pin(2,machine.Pin.OUT) #Connect to IN2 on module
C_3 = machine.Pin(3,machine.Pin.OUT) #Connect to IN3 on module
C_4 = machine.Pin(4,machine.Pin.OUT) #Connect to IN4 on module


Phase_Pointer = 0
def Phase_Sequence(Direction):
    global Phase_Pointer
    Phase_Pointer = Phase_Pointer + Direction #Increment to next phase to make step
    if Phase_Pointer < 1 : Phase_Pointer = 8  #Handle negative direction roll-over
    if Phase_Pointer > 8 : Phase_Pointer = 1  #Handle positive direction roll-over
    #Depending on sequence phase desired, set the output pins accordingly
    if Phase_Pointer == 1: # Sequence = 0001
        C_1.value(0); C_2.value(0); C_3.value(0); C_4.value(1) 
    elif Phase_Pointer == 2: # Sequence = 0011
        C_1.value(0); C_2.value(0); C_3.value(1); C_4.value(1) 
    elif Phase_Pointer == 3: # Sequence = 0010
        C_1.value(0); C_2.value(0); C_3.value(1); C_4.value(0) 
    elif Phase_Pointer == 4: # Sequence = 0110
        C_1.value(0); C_2.value(1); C_3.value(1); C_4.value(0) 
    elif Phase_Pointer == 5: # Sequence = 0100
        C_1.value(0); C_2.value(1); C_3.value(0); C_4.value(0) 
    elif Phase_Pointer == 6: # Sequence = 1100
        C_1.value(1); C_2.value(1); C_3.value(0); C_4.value(0) 
    elif Phase_Pointer == 7: # Sequence = 1000
        C_1.value(1); C_2.value(0); C_3.value(0); C_4.value(0) 
    elif Phase_Pointer == 8: # Sequence = 1001
        C_1.value(1); C_2.value(0); C_3.value(0); C_4.value(0)
    
Steps = 0 
while Steps < 4096:   # run for 1 revolution
    Steps += 1        # Increment number of steps counter
    Phase_Sequence(1) # 1=CCW  -1=CW
    sleep_us(10800)     # Sleep microseconds!!!!
    #print(Steps, Phase_Pointer)
    
    