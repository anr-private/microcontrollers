from pimoroni import Button                    #Need this if using buttons
from picographics import PicoGraphics          #Universal graphics library - part of the UF2 file
from picographics import DISPLAY_PICO_DISPLAY  #Class for this model display
from picographics import PEN_P4                #Class for the "color depth" we want
from time import sleep
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)  #Create display object in horizontal orientation
X_max = 239            #Helpful variables that define the graphic bounds
Y_max = 134            

button_y = Button(15)

def wait_for_y():
    while True:
        state = button_y.read()
        if (state == True):
            break
        sleep(.15)
#-------------------------------------------------------------------------------------------------------------------------

display.set_backlight(1.0)                   #Set backlight to max so display is very bright
display.set_font("bitmap8")                  #Easy to use and see font

RED   = display.create_pen(255, 000, 000)    #Define some colors to use (R,G,B)
GREEN = display.create_pen(000, 255, 000)
BLUE  = display.create_pen(000, 000, 255)
CYAN  = display.create_pen(000, 255, 255)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

def clear():                  # Function we can call to clear the screen - used often
    display.set_pen(BLACK)    # Assuming we want a black background
    display.clear()           # Clears the screen setting it all to black
    display.update()          # Performs the actual screen update


#-------------------------------------------------------------------------------------------------------------------------

clear()

display.set_pen(CYAN)
display.set_font("bitmap6")
display.text("PICO Man", 5, 5, scale=1)
display.text("PICO Man", 5, 30, scale=2)
display.text("PICO Man", 5, 60, scale=3)
display.text("PICO Man", 5, 90, scale=4)
display.update()

wait_for_y()

clear()
display.set_pen(RED)
display.set_font("bitmap8")
display.text("PICO Man", 5, 5, scale=1)
display.text("PICO Man", 5, 30, scale=2)
display.text("PICO Man", 5, 60, scale=3)
display.text("PICO Man", 5, 90, scale=4)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("bitmap14_outline")
display.text("PICO Man", 5, 5, scale=1)
display.text("PICO Man", 5, 30, scale=2)
display.text("PICO Man", 5, 60, scale=3)
display.text("PICO Man", 5, 90, scale=4)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("sans")
display.text("PICO Man", 5, 45, scale=1)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("gothic")
display.text("PICO Man", 5, 45, scale=1)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("cursive")
display.text("PICO Man", 5, 45, scale=1)
display.update()


wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("serif_italic")
display.text("PICO Man", 5, 45, scale=1)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)
display.set_font("serif")
display.text("PICO Man", 5, 45, scale=1)
display.update()


wait_for_y()

clear()
display.set_pen(WHITE)                       #Effects of Y position on Font selection
display.set_font("sans")
display.text("PICO Man", 5, 30, scale=1)
display.set_pen(WHITE)                      
display.set_font("bitmap8")
display.text("PICO Man", 5, 80, scale=2)
display.set_pen(RED)                      
display.line(0,30,100,30)
display.line(0,80,100,80)
display.update()


wait_for_y()

clear()
display.set_pen(WHITE)                       #Effects of wordwrap                     
display.set_font("bitmap8")
display.text("PICO Man is a happy man", 5, 20, wordwrap=240, scale=2)
display.text("PICO Man is a happy man", 5, 70, wordwrap=120, scale=2)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)                       #Effects of letter spacing                     
display.set_font("bitmap8")
display.text("PICO Man is a happy man", 5, 20, spacing = 0, wordwrap=240, scale=2)
display.text("PICO Man is a happy man", 5, 70, spacing = 2, scale=2)
display.update()

wait_for_y()

clear()
display.set_pen(WHITE)                       #Effects of angle                    
display.set_font("sans")
display.text("PICO Man happy", 5, 20, angle = 5, scale=1)
display.text("PICO Man happy", 5, 80, angle = -5, scale=1)
display.update()


wait_for_y()

clear()
display.set_pen(WHITE)                       #Measure text for accurate positioning                    
display.set_font("bitmap8")      
text = "PICO Man "
L = display.measure_text(text,2,0)                   #text, scale, spacing
text = text + str(L)
display.text(text, 5, 20, scale=2)
display.set_font("sans")
text = "PICO Man "
L = display.measure_text(text,1,0)
text = text + str(L)
display.text(text, 5, 80, scale=1)
display.update()

wait_for_y()


clear()
display.set_font("bitmap8")      
display.set_pen(RED)        #print letter using ASCII code                   
display.character(80,75,50,scale=5)        # P code is 80
display.set_pen(WHITE)                                         
display.character(73,100,50,scale=5)        # I code is 73
display.set_pen(BLUE)                                        
display.character(67,125,50,scale=5)        # C code is 67
display.set_pen(GREEN)                                         
display.character(79,150,50,scale=5)        # O code is 79
display.update()


