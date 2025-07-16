#HC-SR04 Sonar Demo
#Takes a measurement every 200 milliseconds
#Returns Inch and MM values - if bad reading returns -999 for both
#
#Follow wiring provided on YouTube video
#It is important to add a voltage divider on TRIG & ECHO between the PICO & HCSR04

from machine import Pin
import utime

Trig = Pin(15, Pin.OUT)
Echo = Pin(14, Pin.IN, Pin.PULL_DOWN)

def Get_Measurement():
    MMPerMicroSecond = 0.343                #varible for handling conversion from time to MM distance
    InchesPerMicroSecond = 0.0135039        #varible for handling conversion from time to INCH distance
    Read_Quality = "GOOD"
    
    Trig.low()          #Start with device in known, LOW state
    utime.sleep_us(20)  #Give time for sensor to clear itself
    Trig.high()         #This tells the sensor to send the sound pulses
    utime.sleep_us(10)  #This is the duration of trigger signal
    Trig.low()          #Set low to end trigger signal
    
    while Echo.value() == 0:           #loop until the transmitting sound pulses end
        StartTime = utime.ticks_us()   #Record that moment in time
    
    while Echo.value() == 1:           #loop until the echo is heard
        EndTime = utime.ticks_us()     #Record that moment in time
        Dur  = EndTime - StartTime
        if Dur > 24000:                #It has taken too much time, bad reading so abort
            Read_Quality = "FAIL"
            break
    
    if Read_Quality == "GOOD":
        Dur  = EndTime - StartTime           #Duration of bi-direction sound movement
        Dur  = Dur / 2                       #Divide the duration by two - only measure one-way trip
        I_Dist = (Dur * InchesPerMicroSecond)#Multiply Duration * Inches Per micro-second
        I_Dist = round(I_Dist)               #Round the value to a whole inch
        M_Dist = (Dur * MMPerMicroSecond)    #Multiply Duration * MM Per micro-second
        M_Dist = round(M_Dist)               #Round the value to a whole inch
        return I_Dist, M_Dist
    else:
        I_Dist = -999                        #Make it obvious there is a bad reading
        M_Dist = -999
        return I_Dist, M_Dist  



while True:
    Inch_Dist, MM_Dist = Get_Measurement()   #Run the function and fetch the values from the device
    #print(Inch_Dist,MM_Dist)                #Print all results, including the bad ones (-999, -999)
    if Inch_Dist > 0:                        #Filter out the bad results to make it easier for processing
        print(Inch_Dist," IN   ",MM_Dist," MM")             #Print only good results
    utime.sleep(.2)                          #slow down the loop - Do not reduce this without checking
                                             #to make sure we are not calling the function while it is
                                             #processing the previous readings.
