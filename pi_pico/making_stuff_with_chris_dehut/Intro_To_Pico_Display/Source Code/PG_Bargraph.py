'''
Use this Pimoroni uf2 file ---> pimoroni-pico-v1.19.9-micropython.uf2    from PIMORONI website
This example mimics a sound level meter display
Not very optimized!

'''
import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import random

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
    display.set_pen(BLACK)
    display.clear()
    display.update()

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
        
   
  
#- main ---------------------------------------------------------
clear()
Animate_Graph(0)   #Slowly work up the graph 
time.sleep(.05)
Animate_Graph(1)
time.sleep(.05)
Animate_Graph(2)
time.sleep(.05)
Animate_Graph(3)
time.sleep(.05)
Animate_Graph(4)
time.sleep(.05)
Animate_Graph(5)
time.sleep(.05)
Animate_Graph(6)
time.sleep(.05)
Animate_Graph(7)
time.sleep(.05)
Animate_Graph(8)
time.sleep(.05)
Animate_Graph(9)


while True:                    #feeder loop sending random sound levels
    L = random.randint(0,10)
    Animate_Graph(L)
    time.sleep(.005)
    
