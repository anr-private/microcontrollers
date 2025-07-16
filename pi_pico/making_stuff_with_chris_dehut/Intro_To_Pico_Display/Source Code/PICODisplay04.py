from pimoroni import Button                    #Need this if using buttons
from picographics import PicoGraphics          #Universal graphics library - part of the UF2 file
from picographics import DISPLAY_PICO_DISPLAY  #Class for this model display
from picographics import PEN_P4                #Class for the "color depth" we want

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)  #Create display object in horizontal orientation
X_max = 240            #Helpful variables that define the graphic bounds
Y_max = 135            

#-------------------------------------------------------------------------------------------------------------------------

display.set_backlight(1.0)                   #Set backlight to max so display is very bright
display.set_font("bitmap8")                  #Easy to use and see font

RED   = display.create_pen(255, 000, 000)    #Define some colors to use (R,G,B)
GREEN = display.create_pen(000, 255, 000)
BLUE  = display.create_pen(000, 000, 255)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

def clear():                  # Function we can call to clear the screen - used often
    display.set_pen(BLACK)    # Assuming we want a black background
    display.clear()           # Clears the screen setting it all to black
    display.update()          #Performs the actual screen update
    
#-------------------------------------------------------------------------------------------------------------------------

clear()


display.set_pen(WHITE)    # Set drawing color to White
display.pixel(10,10)      # plot pixel at X & Y coordinate
display.pixel(10,50)
display.pixel(10,100)
display.update()

#-------------------------------------------------------------------------------------------------------------------------

display.set_pen(GREEN)    
display.pixel_span(5,5,50)      # plot pixels horizontally
display.update()













    
    
    
    
    
    