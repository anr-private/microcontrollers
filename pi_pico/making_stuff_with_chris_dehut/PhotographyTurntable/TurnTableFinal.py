'''
TURNTABLE OPERATION
Power is on when plugged in.
Default operational mode is continuous rotation
Speed of rotation is controlled by potentiometer
Direction of rotation is controlled by toggle switch and can be changed when rotating
If powered on while holding Trigger switch, the unit will be in incremental mode
To rotate the pre-set number of degrees, press and release the trigger
You can force continuous rotation by holding in the trigger switch

Pot is wired "backwards" to give a range as such:
CCW = 65535
CW  = 0
practical results with 10k pot were
250 (CW) to 65535 (CCW) --> Range is 65285


Motor is 200 steps per rotation --> 1.8 degrees per step
MS2     MS1
GND     GND     8 microsteps                 1600 steps / rotation 
GND     VCC_IO  2 microsteps (half step)      400 steps / rotation
VCC_IO  GND     4 microsteps (quarter step)   800 steps / rotation
VCC_IO  VCC_IO  16 microsteps
                3200 steps / rotation
------------------------
Reference Data
https://howtomechatronics.com/tutorials/arduino/stepper-motors-and-arduino-the-ultimate-guide/

Audio cable connector - Bulkhead
https://www.amazon.com/dp/B07MN1RK7F

Audio cable used for switch
https://www.amazon.com/dp/B00NO73Q84

TMC2208 Stepper driver
https://www.amazon.com/dp/B08DFVZV5Q
TMC2208 Wiki
https://wiki.fysetc.com/TMC2208/

Stepper Motor - nema 17
https://www.amazon.com/dp/B07THK76QQ

Flanged Bearings
https://www.amazon.com/dp/B07Z3FR688

Push Button Switch
https://www.amazon.com/gp/product/B07F24Y1TB

Power cable connector - Bulkhead
https://www.amazon.com/gp/product/B01N8VV78D

10k Potentiometer
https://www.amazon.com/dp/B07WWLC33K

9V AC to DC power supply
https://www.amazon.com/dp/B0852JLTL9

DC to DC Converter
https://www.amazon.com/gp/product/B079N9BFZC

'''

import machine
from machine import Pin
from time import time, sleep, sleep_us
import _thread

M1_Sig = Pin(18,Pin.OUT)              #MS1 - configures stepping mode at 16 micro steps
M1_Sig.value(1)                       #Set it to ON
M2_Sig = Pin(19,Pin.OUT)              #MS2 - configures stepping mode at 16 micro steps
M2_Sig.value(1)                       #Set it to ON

Step_Sig = Pin(17,Pin.OUT)              #Configure STEP signal for stepper driver
Step_Sig.value(0)                       #Set it to a known state
Dir_Sig = Pin(16,Pin.OUT)               #Configure the DIRECTION signal for the stepper motor
Speed_Control = machine.ADC(28)         #Configure ADC chanel two for use 
Trigger   = Pin(10,Pin.IN,Pin.PULL_UP)  #Use when wanting start-stop type rotation
Direction = Pin(15,Pin.IN,Pin.PULL_UP)  #Selects rotational direction in Continuous mode

Steps_Per_Degree = 8.884         #Used to help calculate steps per Increment of rotation
Degrees_Per_Stop = 10            #Set to how many degrees of rotation per increment in INCRmental mode
Operational_Mode = "Cont"        #Can be CONTinuos or INCRemental - controlled by toggle switch
if Direction.value() == 1:       #Based on Direction Toggle Switch, set rotational direction
    New_Rot_Dir = "CW"
elif Direction.value() == 0:
    New_Rot_Dir = "CCW"
    
Speed_Delay = 12000           #Preset delay so that table doesn't turn too fast at start 
 
def Table_Control():          #Function that actually steps the motor
    import time               #This is a thread, so library needs loading
    global Speed_Delay
    global New_Rot_Dir
    global Operational_Mode
    global Step_Cntr
    global loops
    global test_cntr
    loops=0
    Rot_Dir = "xx"            #Set to a default value
    if Operational_Mode == "CONT":         #Run in continuous rotation mode
        while True:                        #Endless loop            
            if New_Rot_Dir != Rot_Dir:     #Handle a changed in rotational direction
                sleep(.5)                  #Stop rotation
                Rot_Dir = New_Rot_Dir      #Match the variables
                if Rot_Dir == "CW":        #Depending on requested direction...
                    Dir_Sig.value(1)       #Set the output for the stepper driver
                elif Rot_Dir == "CCW":
                    Dir_Sig.value(0)
            if Speed_Delay < 9990:       #Movement okay as long as speed is high enough
                Step_Sig.value(1)          #Turn on STEP signal
                sleep_us(1)                #for only 1 micro-second
                Step_Sig.value(0)          #then turn it off to create a pulse
                time.sleep_us(Speed_Delay) #This sleep regulates rotational speed
                Step_Cntr += 1
                if Step_Cntr >= 3200:            #(round(Steps_Per_Degree * 360)):  #If moved far enough
                    #print("made it to 360")
                    Step_Cntr = 0
                    loops += 1
            else:                           #Do thing so rotation stops.
                sleep(.25)
                
            test_cntr += 1
    elif Operational_Mode == "INCR":
        Step_Cntr = 0                      #Local counter used to limit rotational distance
        while True:                        #Endless loop 
            Step_Sig.value(1)              #Turn on STEP signal
            sleep_us(1)                    #for only 1 micro-second
            Step_Sig.value(0)              #then turn it off to create a pulse
            time.sleep_us(Speed_Delay)     #This sleep regulates rotational speed        
            Step_Cntr += 1                 #Increment step counter to determine end of increment            
            if Step_Cntr >= (round(Steps_Per_Degree * Degrees_Per_Stop)):  #If moved far enough
                while True:                  #Wait for Trigger button press to make next move                    
                    Step_Cntr = 0            #Reset counter
                    if Trigger.value() == 0: #Button is pressed
                        break                #Exit loop
        
def Map_Analog(A):    
    #POT full CW   = 250
    #POT full CCW  =  65,535
    #Range of POT is 65,285 units
    #Base value of POT is 65,535 units
    #---
    #Fast speed is a sleep_us of 2000
    #Slow speed is a sleep_us of 10,000
    #Range of sleep_us is 8,000 units
    #Base of sleep_us is 2000 units
    #---
    # Desired output is
    # POT CCW at 65,535 outputs slowest speed of 10,000 microseconds delay
    # POT CW  at  2500 outputs fastest speed of  2,000 microseconds delay
    global Speed_Delay                     
    Map_Factor  = 65285 / 8000             #Divide range by time range
    Base_Time   = 2000                     #lowest time delay in microseconds
    Base_Analog = 250                      #lowest analog reading (full CW)
    A_Base_Shifted = (A - Base_Analog)     #Shift reading to base of full range
    D = round(A_Base_Shifted / Map_Factor) #Dwell is from mapping factor
    Speed_Delay = round(D + Base_Time)     #Shift the Dwell up to the base line
    #print("SD",Speed_Delay)

test_cntr = 0
Step_Cntr = 0
Step_Counter = 0
print("Starting the run")

#At start up, determine which mode of operation based on the Trigger switch position
if Trigger.value() == 1:                        #Switch is OPEN or not connected, thus HIGH
    Operational_Mode = "CONT"
    _thread.start_new_thread(Table_Control, ()) #START Table_Control running in its own thread
elif Trigger.value() == 0:                      #Switch is CLOSED, thus LOW
    Operational_Mode = "INCR"
    _thread.start_new_thread(Table_Control, ()) #START Table_Control running in its own thread
print("Operational Mode =",Operational_Mode)
while True:                                #Endless main loop   
    A_Raw = Speed_Control.read_u16()       #Read analog channel
    Map_Analog(A_Raw)                      #Convert analog reading into dwell time
    if Direction.value() == 1:             #Depending on direction switch position
        New_Rot_Dir = "CW"                 #set variable to control table rotational direction
    elif Direction.value() == 0:
        New_Rot_Dir = "CCW"
    sleep(.05)                            #Slow down the loop a bit to free resources
    #print(A_Raw,Speed_Delay,Trigger.value(),Direction.value(),Operational_Mode,Step_Cntr, loops,test_cntr)
