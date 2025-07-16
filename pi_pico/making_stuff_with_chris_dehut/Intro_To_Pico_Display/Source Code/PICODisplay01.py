from pimoroni import Button                    #Need this if using buttons
from picographics import PicoGraphics          #Universal graphics library - part of the UF2 file
from picographics import DISPLAY_PICO_DISPLAY  #Class for this model display
from picographics import PEN_P4                #Class for the "color depth" we want

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)  #Create display object in horizontal orientation
X_max = 240            #Helpful variables that define the graphic bounds
Y_max = 135            

