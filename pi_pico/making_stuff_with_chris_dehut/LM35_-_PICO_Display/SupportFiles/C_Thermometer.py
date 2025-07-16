'''
Use this Pimoroni uf2 file ---> pimoroni-pico-v1.19.9-micropython.uf2    from PIMORONI website
Use the PICO Display 1.14" unit - running in vertical (portrait) orientation

This demo is an animation of a traditional thermometer.   It shows the use of text and graphics.
This can be easily modified to work with a temp sensor.

'''
import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import random

# Only using a few colors, we can use a 4 bit/16 colour palette.
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=270) #270 = vertical orientation

display.set_backlight(1.0)     #Set backlight to max so display is very bright
display.set_font("bitmap8")    

RED = display.create_pen(255, 000, 000)      #Define some colors to use (R,G,B)
WHITE = display.create_pen(255, 255, 255)
GRAY = display.create_pen(125, 125, 125)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(33, 177, 255)


# Function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

def Draw_Base_Thermometer():
    display.set_pen(GRAY)            #Draw bulb portion
    display.circle(30, 218, 20)
    display.set_pen(RED)         
    display.circle(30, 218, 19)
    display.set_pen(GRAY)            #Draw stem part  
    display.rectangle(20,5,20,196)
    display.set_pen(WHITE)          
    display.rectangle(21,6,18,195)
    display.set_pen(RED)
    display.rectangle(21,190,18,15)
    display.update()

def Show_Temp_Ticks():
    L = 42
    R = 75
    B = 190
    T_Mark = B
    Temp = 60                                                 #Starting value at base of thermometer
    while T_Mark > 6:
        display.set_pen(CYAN)
        display.line(L, T_Mark, R, T_Mark)                    #Draw line to right of stem
        display.set_font("bitmap6")
        S_Temp = str(Temp)                                    #Text can only use strings 
        display.text(S_Temp, 85, (T_Mark - 5), scale=2)       #Print the text, offset 5 pixels up from line
        display.update()
        Temp += 2
        T_Mark -= 18                                          #Not enough room so only every 2 degrees

def Show_Temp(f):
    L = 21
    W = 18
    B = 190
    #Top of White is 10
    #Bottom of Red is 190
    F_f = (f-60) #in range of 0 to 20
    F_f = round(F_f * 9)   #convert to pixels of temp from base
    Y1 = 10                #Y1 is the top of Stem
    Y2 = 190 - F_f         #Y2 is the position at the top of the 'mercury"
    Y1H = Y2 - Y1          #Y1H is the height of the white area above the 'mercury'
    Y2H = 190 - Y2         #Y2H is the height of the red area showing the temp
    display.set_pen(WHITE)
    display.rectangle(L,Y1,W,Y1H)
    display.set_pen(RED)
    display.rectangle(L,Y2,W,Y2H)
    display.update()   
 
#- main ---------------------------------------------------------
clear()
Draw_Base_Thermometer()
Show_Temp_Ticks()

while True:                              #feeder loop sending random Temps
    Random_Temp = random.randint(60,80)  #Keep temps in range of 60 to 80
    Show_Temp(Random_Temp)
    time.sleep(.5)


