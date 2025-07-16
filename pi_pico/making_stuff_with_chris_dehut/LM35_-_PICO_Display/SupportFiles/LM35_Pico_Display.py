'''
This example program demostrates the functions of a LM35 temp sensor by
displaying the resulting temps graphically on a PICO Display.

Use this Pimoroni uf2 file ---> pimoroni-pico-v1.19.9-micropython.uf2    from PIMORONI website
Use the PICO Display 1.14" unit - running in vertical (portrait) orientation

Documentation for 'pico graphics" library useage
https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics#supported-displays


The scale to handle Celcius is a bit of a kludge, but it works.  
'''
import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

#--- Configure display variables and functions to display data ---------------------------------------------------------

# Only using a few colors, we can use a 4 bit/16 colour palette.
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=270) #270 = vertical orientation
#135 x 240 pixels
display.set_backlight(1.0)                   #Set backlight to max so display is very bright
display.set_font("bitmap8")                  #select a font for text

RED = display.create_pen(255, 000, 000)      #Define some colors to use (R,G,B)
WHITE = display.create_pen(255, 255, 255)
GRAY = display.create_pen(125, 125, 125)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(33, 177, 255)

#Defined X positions for the thermometer positions
Xp1 = 67      #Center of Thermometer
Xp2 = 57      #Left edge of outline
Xp3 = 58      #Left edge of Red part of stem

# Function we can call to clear the screen
def clear():
    display.set_pen(BLACK)           # Set back ground color to black
    display.clear()                  # Clear the screen by making it all black
    display.update()                 # Always have to do a update to show results

def Draw_Base_Thermometer():
    display.set_pen(GRAY)            #Set drawing color to gray -- Draw bulb portion
    display.circle(Xp1, 218, 20)     #Draw a circle at X, Y, Radius
    display.set_pen(RED)         
    display.circle(Xp1, 218, 19)
    display.set_pen(GRAY)            #Draw stem part  
    display.rectangle(Xp2,5,20,196)  #Draw rectangle: X, Y, Width, Height 
    display.set_pen(WHITE)          
    display.rectangle(Xp3,6,18,195)
    display.set_pen(RED)
    display.rectangle(Xp3,190,18,15)
    display.update()

def Show_Temp_Ticks():
    #F Scale 
    L = Xp1 + 12                                              #Define some variable for positioning & sizes
    R = 105
    B = 190
    T_Mark = B
    Temp = 60                                                 #Starting value at base of thermometer
    while T_Mark > 6:
        display.set_pen(CYAN)
        display.line(L, T_Mark, R, T_Mark)                    #Draw line to right of stem
        display.set_font("bitmap6")                           #Set font to be used
        S_Temp = str(Temp)                                    #Text can only use strings 
        display.text(S_Temp, (R + 5), (T_Mark - 5), scale=2)  #print text (text, x, y, scale=)
        display.update() 
        Temp += 2
        T_Mark -= 18                                          #Not enough room so only every 2 degrees
    display.text("F", 110, 205, scale=3)                      #Print the text at X, Y, using scale
    #C Scale
    L = 40
    R = 58
    B = 190
    T_Mark = B
    Temp = 60  #F                                             #Starting value at base of thermometer
    while T_Mark > 6:
        display.set_pen(WHITE)
        display.line(L, T_Mark, R, T_Mark)                    #Draw line to right of stem
        display.set_font("bitmap6")
        C_Temp = round((Temp-32)*.555,1)
        S_Temp = str(C_Temp)                                  #Text can only use strings 
        display.text(S_Temp, 3, (T_Mark - 5), scale=2)        
        display.update()
        Temp += 2
        T_Mark -= 18                                          #Not enough room so only every 2 degrees
    display.text("C", 15, 205, scale=3)                       #Print the text at X, Y, using scale
    
def Show_Temp(f):           #Pass in temp in F scale
    W = 18                  #Define some variables for size and location
    B = 190
    #Top of White is 10
    #Bottom of Red is 190
    F_f = (f-60)           #in range of 0 to 20
    F_f = round(F_f * 9)   #convert to pixels of temp from base
    Y1 = 10                #Y1 is the top of Stem
    Y2 = 190 - F_f         #Y2 is the position at the top of the 'mercury"
    Y1H = Y2 - Y1          #Y1H is the height of the white area above the 'mercury'
    Y2H = 190 - Y2         #Y2H is the height of the red area showing the temp
    display.set_pen(WHITE)
    display.rectangle(Xp3,Y1,W,Y1H)
    display.set_pen(RED)
    display.rectangle(Xp3,Y2,W,Y2H)
    display.update()   
 

#--- Configure LM35 and analog input and functions needed to convert to temperature value  ------------------------------------------------

LM35 = machine.ADC(0)  #setup analog reading on ADC
Cal_Offset = -550      #Calibration offset value
                       #Determined from practical testing
def Compute_Temp(Avg_A):
    LM35_A = Avg_A + Cal_Offset           #Add Calibration Adjustment
    LM35_V = LM35_A * .00005              #Convert analog reading to volts
    Tmp_C  = round((LM35_V * 100),1)      #Convert volts to temp celcius
    Tmp_F  = round((Tmp_C * 1.8 + 32),1)  #Convert Tmp_C to Tmp_F
    return Tmp_C, Tmp_F                   #Return Temps


# --- MAIN PROGRAM - ENDLESS LOOP ------------------------------------------------------------------------------------------------------
clear()                  # Prepare the display so that it clear
Draw_Base_Thermometer()  # Draw the image of the thermometer
Show_Temp_Ticks()        # Add the text to define the scale

Samples = 0              # Variable holds all samples
Num_Samples = 1          # Counter for num samples collected
while True:
    if Num_Samples <= 10:            #storing a total of 10 samples
        LM35_A = LM35.read_u16()     #Read the ADC port to get sensor data
        Samples = Samples + LM35_A   #Add current reading to sample batch
        Num_Samples += 1             #Increment counter
    else:
        Avg_A = Samples / 10             #Get the average of samples
        Samples = 0                      #Reset Samples variable to zero
        Num_Samples = 1                  #Reset counter to one
        T_c, T_f = Compute_Temp(Avg_A)   #Fetch the temps from the function
        print("Celcius=",T_c,"  Fahrenheit=",T_f)
        Show_Temp(T_f)
    time.sleep(.1)  #slow the loop down
    
    