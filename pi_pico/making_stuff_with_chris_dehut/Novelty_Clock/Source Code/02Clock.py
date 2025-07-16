'''
 ---  SOFTWARE REVISED TO MICROSECOND TIMING  ---

PICO Powered and controlled Novelty Clock 

The design and credit for this clock goes to
'Hollow Clock' by Shiura which can be found here
https://www.thingiverse.com/thing:5142739
please download the files from thingiverse.
Follow all instructions for printing and assembly with the exception of electronics.

The base (electronics enclosure) and source code can be downloaded from
MakingStuffWithChrisDeHut.com

The stepper motor and driver can be purchased from here:
https://www.amazon.com/Longruner-Stepper-Uln2003-arduino-LK67/dp/B015RQ97W8/ref=sr_1_53?keywords=Longruner&qid=1671795791&sr=8-53
As of 12/23/2022 price was $11.99 for 5 motors and drivers
Use the extras for other cool projects!

Use a standard PICO, no WiFi needed.

Look in the video description for updated
sourcing.

----------------------
Calculating the steps per second and
time per step.

Motor Specifications:
    1:64 gear reduction
    5.625 step angle 64 steps/rev before gearing
    64 x 64 = 4096 steps / output shaft rotation

Output shaft gear is 8 teeth
Ring gear has 110 teeth
110 / 8 = 13.75 output shaft rotations / hour
4096 x 13.75 = 56320 steps / hour
56320 / 3600 (seconds/hour) = 15.6444 steps per second
1 (second) / 15.6444 = .0639 seconds per step

------------------------
'''

import machine
import time

P1 = machine.Pin(10,machine.Pin.OUT)        #Create 4 output pins that are used to control
P2 = machine.Pin(11,machine.Pin.OUT)        #the stepper driver/motor phases
P3 = machine.Pin(12,machine.Pin.OUT)
P4 = machine.Pin(13,machine.Pin.OUT)

Green  = machine.Pin(18,machine.Pin.IN,machine.Pin.PULL_UP)  #Create 3 inputs for the buttons
Yellow = machine.Pin(19,machine.Pin.IN,machine.Pin.PULL_UP)
Red    = machine.Pin(20,machine.Pin.IN,machine.Pin.PULL_UP)
'''

Press-Hold RED button to fast-reverse time
Press-Hold GREEN button to fast-advance time
Press-Hold YELLOW - press RED button reverse time 1 hour
Press-Hold YELLOW - press GREEN button advance time 1 hour
once the "hour" adjusments starts, you can release both buttons


phase sequence 
1 1 0 0
0 1 0 0
0 1 1 0
0 0 1 0
0 0 1 1
0 0 0 1
1 0 0 1
1 0 0 0
'''

Normal_Speed = (63810)   #This is the "running speed" for the clock to maintain time.
                         #This value was refined over a period of about 6 weeks.
                         #Lower the value to make the clock run faster.
                         #Raise the value to make the clock run slower.

Adjust_Speed = (1000)    #revised to microseconds
Phase = 1                #Keeps track of the motor phase 
P1.on(); P2.on(); P3.off(); P4.off() #set initial phase for motor

def Step(dir,speed):        #Function that actually steps the motor
    global Phase
    global cnt
    time.sleep_us(speed)    #Revised to sleep micro seconds for better resolution
    Phase += dir
    if Phase == 9:          #Fix positive rollover
        Phase = 1
    if Phase < 1:           #Fix negative rollover
        Phase = 8
    #print(Phase,dir,speed)
    if Phase == 1:                             #for each phase position, set appropriate outputs on/off
        P1.on(); P2.on(); P3.off(); P4.off()
    elif Phase == 2:
        P1.off(); P2.on(); P3.off(); P4.off()
    elif Phase == 3:
        P1.off(); P2.on(); P3.on(); P4.off()        
    elif Phase == 4:
        P1.off(); P2.off(); P3.on(); P4.off()        
    elif Phase == 5:
        P1.off(); P2.off(); P3.on(); P4.on()        
    elif Phase == 6:
        P1.off(); P2.off(); P3.off(); P4.on()        
    elif Phase == 7:
        P1.on(); P2.off(); P3.off(); P4.on()        
    elif Phase == 8:
        P1.on(); P2.off(); P3.off(); P4.off()

    
    
CW  =  1      #Variables to define forward and reverse time
CCW = -1
print("Starting the clock")
while True:                                               #Endless main loop
    if (Red.value() == 0) and (Yellow.value() == 1):      #Adjust time backwards
        Step(CCW,Adjust_Speed)
    elif (Green.value() == 0) and (Yellow.value() == 1):  #Adjust time forwards
        Step(CW,Adjust_Speed)
    elif (Red.value() == 0) and (Yellow.value() == 0):    #Adjust time backwards 1 hour
        Adjust_Time = 0
        for at in range(56320):
            Step(CCW,Adjust_Speed)        
    elif (Green.value() == 0) and (Yellow.value() == 0):  #Adjust time forwards 1 hour
        Adjust_Time = 0
        for at in range(56320):
            Step(CW,Adjust_Speed)        
    else:                                                 #Clock running at normal speed
        Step(CW,Normal_Speed)
    