from pimoroni import Button                    #Need this if using buttons
from picographics import PicoGraphics          #Universal graphics library - part of the UF2 file
from picographics import DISPLAY_PICO_DISPLAY  #Class for this model display
from picographics import PEN_P4                #Class for the "color depth" we want
from pimoroni import RGBLED
from time import sleep
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)  #Create display object in horizontal orientation
X_max = 239            #Helpful variables that define the graphic bounds
Y_max = 134            

#-------------------------------------------------------------------------------------------------------------------------

display.set_backlight(1.0)                   #Set backlight to max so display is very bright
display.set_font("bitmap8")                  #Easy to use and see font

led = RGBLED(6, 7, 8)
button_y = Button(15)

RED   = display.create_pen(255, 000, 000)    #Define some colors to use (R,G,B)
GREEN = display.create_pen(000, 255, 000)
BLUE  = display.create_pen(000, 000, 255)
CYAN  = display.create_pen(000, 255, 255)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

def clear():                  # Function we can call to clear the screen - used often
    display.set_pen(BLACK)    # Assuming we want a black background
    display.clear()           # Clears the screen setting it all to black
    display.update()          #Performs the actual screen update

def rolling(xs,ys,xe,ye):
    xp = xs
    yp = ys
    while xp < xe:
        display.set_pen(CYAN)
        display.circle(xp,70,40)
        xp += 1
        display.set_pen(RED)
        display.circle(xp,70,40)
        
        if xp == 60:
            display.set_pen(BLACK)
            display.text("STOP!!!",150,60,angle=20)
            display.update()
            sleep(1)
            display.set_pen(CYAN)
            display.text("STOP!!!",210,50,angle=20)          
            display.update()
        if xp == 190:
            display.set_pen(RED)
            display.text("OUCH!!!",160,10,angle=20)
            display.update()
            
        display.update()
        
#-------------------------------------------------------------------------------------------------------------------------

while True:
    clear()
    led.set_rgb(000, 000, 000)
    display.set_pen(GREEN)           #GRASS
    display.rectangle(0,110,240,25)
    display.set_pen(CYAN)            #SKY
    display.rectangle(0,0,240,110)
    display.update()
    display.set_pen(BLACK)
    display.line(230,125,220,85)
    display.line(210,125,220,85)
    display.line(220,85,220,50)
    display.line(220,60,255,35)
    display.line(220,60,185,35)
    display.circle(220,40,10)
    display.update()
    display.set_pen(RED)
    display.circle(45,70,40)
    display.update()
    rolling(45,70,280,70)
    
    while True:                #Flash Red and Blue and wait for Y to be pressed
        led.set_rgb(000, 000, 255)
        if button_y.read():
            break
        sleep(.1)
        led.set_rgb(255, 000, 000)
        sleep(.1)







#-------------------------------------------------------------------------------------------------------------------------
# 
# display.set_pen(RED)    
# display.rectangle(20,20,200,95)      # draw a rectangle starting at  
# display.update()
# 
# #-------------------------------------------------------------------------------------------------------------------------
# 
# display.set_pen(WHITE)    
# display.circle(120,67,50)      # draw a circle at 120, 67 with a radius of 50
# display.update()
# 
# #-------------------------------------------------------------------------------------------------------------------------
# 
# display.set_pen(BLACK)    
# display.triangle(120,17,163,92,77,92) # draw a triangle with points at 3 coordinats  
# display.update()
# 
# #-------------------------------------------------------------------------------------------------------------------------
# 
# 
# display.set_pen(BLUE)    
# display.polygon([(25,25),(60,45),(60,90),(25,110)]) # draw a polygon
# display.update()
# 
# 
# 







    
    
    
    
    
    