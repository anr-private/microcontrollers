'''
Example program showing ability of analog sound sensor.
Based on the reading from the sensor, an LED bar graph shows sound level
on a LCD display (Pimoroni PICO Display).

Source for analog sound level sensor
https://www.amazon.com/dp/B09VNWMJ4G?psc=1&ref=ppx_yo2ov_dt_b_product_details

Source for PICO Display (In the UK) Many places in the US as well
https://shop.pimoroni.com/products/pico-display-pack?variant=32368664215635

Source of instructions for the PICO Display
https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics#supported-displays

Pimoroni UF2 Files
https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.19.10
pimoroni-pico-v1.19.10-micropython.uf2


A similar project was done using and LED Bar graph display. 
Advatage of using LED Bar graph is the very fast response and display time.
Using a graphic LCD type display, the response is much slower due to the
slower speed of creating the graphics.
'''
import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import random

#Configure hardware for analaog
Sound_Analog = machine.ADC(0)  #setup analog reading on ADC channel 0

#-- Configure PICO Display, create variables needed for displaying bar graph
# Only using a few colors, we can use a 4 bit/16 colour palette.
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=270)
X_max = 134
Y_max = 239
X_Bar_Width = 40     #set a width for the bars - smaller = faster
X_Bar_Start = round(((X_max / 2) - (X_Bar_Width / 2))) #Find start point so bar is centered

display.set_backlight(1.0)     #Set backlight to max so display is very bright
display.set_font("bitmap8")    

#DEFINE bar graph segment colors
BLACK = display.create_pen(0, 0, 0)
txt_clr = display.create_pen(255, 255, 255)        #White
b_color = []                                       #List to hold the colors
b_color.append(display.create_pen(255, 255, 255))  #White
b_color.append(display.create_pen(210, 210, 210))  #Gray
b_color.append(display.create_pen(000, 255, 255))  #Cyan
b_color.append(display.create_pen(000, 200, 200))  #Cyan
b_color.append(display.create_pen(100, 100, 255))  #Blue
b_color.append(display.create_pen(000, 000, 255))  #Blue
b_color.append(display.create_pen(155, 155, 000))  #Yellow
b_color.append(display.create_pen(255, 255, 000))  #Yellow
b_color.append(display.create_pen(255, 125, 000))  #Orange
b_color.append(display.create_pen(255, 000, 000))  #Red

# Function we can call to clear the screen
def clear():
    display.set_pen(BLACK)                  #Set color to background color
    display.clear()                         #Run the libraries clear function
    display.update()                        #Always run update when you change the graphic data

def Animate_Graph(level):  #level = 0 to 9
    display.set_pen(BLACK)                  #Erase text at top
    display.rectangle(0,0,X_max,30)         #
    display.set_pen(txt_clr)                #
    level_s = str(level)                    #Convert INT to String
    display.text(level_s, 50, 0, 135, 4)    #show the text at top=center
    B_height = 20                           #Bar height setting for each segment
    Y_POS = Y_max -B_height                 #Start at bottom, move upwards
    for b in range(0, 10):                  #Step through all 10 segments
        if (b <= level):                    #If this segment 'b' is within level range
            display.set_pen(b_color[b])     #Set it's color for this position
        else:                               #
            display.set_pen(BLACK)          #Set color to erase a previous color
                                            #Draw the rectangle to create the bar
        display.rectangle(X_Bar_Start,Y_POS,X_Bar_Width,B_height)  
        display.update()                    #Update display to reflect new data
        Y_POS -= B_height                   #Decrement position for next bar

def show_level(lvl):           #Pass in analog reading from sensor        
    #1k  = 10%  quiet           Range levels detected
    #30k = 100% loud
    #.033 per 1% increase       used to factor level for display
    Rank = int(lvl*.00033)
    if Rank > 10: Rank = 10    #limit ranking to level 10
    Animate_Graph(Rank)
    print(lvl , Rank)

delay = .05
clear()
while True:
    Sound_Level = Sound_Analog.read_u16()  #Read the analog value from the sensor
    show_level(Sound_Level)                #light up the bar graph according to sound level
    time.sleep(delay)                      #Slow things down a bit - analog reads take a bit of time
        

