'''
Example program showing ability of analog sound sensor.
Based on the reading from the sensor, an LED bar graph shows sound level.

Advatage of using LED Bar graph is the very fast response and display time.
Using a graphic LCD type display, the response is much slower due to the
slower speed of creating the graphics.

'''
import machine,time

LVL=[0]                                      #Create a list of Pins as output to control bar graph
LVL.append(machine.Pin(16,machine.Pin.OUT))
LVL.append(machine.Pin(17,machine.Pin.OUT))
LVL.append(machine.Pin(18,machine.Pin.OUT))
LVL.append(machine.Pin(19,machine.Pin.OUT))
LVL.append(machine.Pin(20,machine.Pin.OUT))
LVL.append(machine.Pin(21,machine.Pin.OUT))
LVL.append(machine.Pin(22,machine.Pin.OUT))
LVL.append(machine.Pin(15,machine.Pin.OUT))
LVL.append(machine.Pin(14,machine.Pin.OUT))
LVL.append(machine.Pin(13,machine.Pin.OUT))
#Configure hardware for analaog
Sound_Analog = machine.ADC(2)  #setup analog reading on ADC channel 2

def show_level(lvl):           #Pass in analog reading from sensor
    for l in range(1,10):      #Turn off all bars
        LVL[l].value(0)
        time.sleep(.005)        
    #1k  = 10%  quiet           Range levels detected
    #30k = 100% loud
    #.033 per 1% increase       used to factor level for display
    Rank = int(lvl*.00033)     #Calculate the peak level in range of 0 to 10   
    if Rank > 10: Rank = 10    #limit ranking to level 10   
    print(lvl , Rank)
    for l in range(1,Rank):    #Loop runs from 1 to peak level (Rank)
        LVL[l].value(1)
        time.sleep(.005)

delay = .05                      
while True:
    Sound_Level = Sound_Analog.read_u16()  #Read the analog value from the sensor
    show_level(Sound_Level)                #light up the bar graph according to sound level
    time.sleep(delay)                      #Slow things down a bit - analog reads take a bit of time
        
    

