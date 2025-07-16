'''
7/15/2023 - Cleaned up code, removed unused function and related
Tachometer project 02/25/2023
Designed to work with the Waveshare Round 1.28" LCD Module - May work with other displays that use same driver set
https://www.amazon.com/gp/product/B08VGT2T42/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1

Requres a library from Russ Hughes at https://github.com/russhughes/gc9a01_mpy

This is the reflective phototransistor used
https://www.amazon.com/dp/B07K1HVNH7

Video detailing the RPR-220 photo sensor
https://youtu.be/g4_ZpVmTi9g

Video on getting started with the Waveshare Round 1.28" LCD Module
https://youtu.be/77dbz1G_678

Video on creating the '7 segment' font for the Waveshare Round 1.28" LCD Module
https://youtu.be/MAefUZgJP_g

Also need a few resistors - check schematic referenced in the video
'''
import machine, _thread
from machine import Pin, SPI
import math
from time import sleep
import utime, time
import gc9a01
import vga1_bold_16x32 as font
import marker as vector_font

#Global Elements
Max_RPM = 11000  #This is the max RPM to display and is used to calculate graph scale
RPM_DEG = round(Max_RPM / 180)  #Scale -- Number of RPM per Degree
Prev_RPM = 0      #Used to minimize the amount of drawing needed for the graph
Prev_Ang = 90     #Used to minimize the amount of drawing needed for the graph
Prev_Digits = 0   #Tracks number of digits on display

#THIS FUNCTION WILL RUN IN ITS OWN THREAD- INITIALIZED JUST ABOVE MAIN CODE AT BOTTOM
def Read_Sensor_Calc_RPM():                         #This function will be run in the second core
    Photo_pin = machine.Pin(17, machine.Pin.IN)     #Have to load the input pin into this core
    import utime                                    #Import needed library function
    global RPM                 #Make sure RPM is global
    Photo_pin_Was = 0          #Variable to hold previous state of input pin (Sensor state)
    Temp_ST = time.ticks_us()  #Variable to temporarily hold start time until after FALLING edge
    ST = time.ticks_us()       #Actual start time variable used to calculate elapsed cycle time
    Cycle_Time = 0             #Variable holding the elapsed cycle time
    while True:	               #Endless loop
        #Measure Rise edge to Rise edge - then calculate elapsed time to determine RPM
        if (Photo_pin.value() == 1) & (Photo_pin_Was == 0):   #Now ON, Was OFF --> Rising
            Photo_pin_Was = 1                                 #Update previous state variable
            Temp_ST = time.ticks_us()                         #Write start time into temporary variable
            Cycle_Time = Temp_ST - ST                         #Calculate Cycle_Time in Micro Seconds
            RPM = round((1/(Cycle_Time * .000001))*60)        #Collect Sample RPM reading for averaging
        elif (Photo_pin.value() == 0) & (Photo_pin_Was == 1): #Now OFF, Was ON --> FALLING
            Photo_pin_Was = 0                                 #Update previous state variable
            ST = Temp_ST                                      #Copy here to preserve value set next Rise Edge       
        if ((ST + 780000) < time.ticks_us()) : #Zero Speed Detection, Increase the 780000 to allow reading below 100 RPM
            RPM = 0             

###-----------------------------------------------
# Code for handling the tachometer display

def Get_Angle_Line(Xc, Yc, R1, R2, A_Deg):  #Fuction gets end points of line
    angle_in_radians = math.radians(A_Deg)  #Convert Deg to Radians for trig calcs
    sin_Ar = math.sin(angle_in_radians)     #Get Sine of angle
    cos_Ar = math.cos(angle_in_radians)     #Get Cosine of angle
    x1 = round(Xc + (R1 * cos_Ar))          #Calc X of end no 1
    y1 = round(Yc + (R1 * sin_Ar))          #Calc Y of end no 1
    x2 = round(Xc + (R2 * cos_Ar))          #Calc X of end no 2
    y2 = round(Yc + (R2 * sin_Ar))          #Cacl Y of end no 2
    return x1,y1,x2,y2

def Plot_Arc(Xc, Yc, Sa, Ea, Da, R1, R2, P_Color):  #Function plots a series of lines creating an arc
    A  = Sa                                                 #Assign working variable of Angle
    while A <= Ea:                                          #Loop from start angle to end angle  
        x1, y1, x2, y2 = Get_Angle_Line(Xc, Yc, R1, R2, A)  #Fetch coordinates of line
        A += Da                                             #Increment spacing angle
        tft.line(x1,y1,x2,y2,(P_Color))                     #draw the actual line

def Plot_Digit_At(X,Y,scale,Segments):             #Custom Text print function to draw a numberic digit
    #Characters are 28 pixels wide by 56 pixels tall with scale of 1 
    Outline = gc9a01.CYAN
    Core    = gc9a01.CYAN     
    if Segments[0] == 1:            #This list defines which segments are displayed or not
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[0] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK
    #Five lines define each of the seven segments- these are shifted to X and Y coordinates provided
    x1 = 4 + X; y1 = -56 + Y; x2 = 24 + X; y2 = -56 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 3 + X; y1 = -55 + Y; x2 = 25 + X; y2 = -55 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -54 + Y; x2 = 26 + X; y2 = -54 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -53 + Y; x2 = 25 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -52 + Y; x2 = 24 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    
    if Segments[1] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[1] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 28 + X; y1 = -30 + Y; x2 = 28 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 27 + X; y1 = -29 + Y; x2 = 27 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 26 + X; y1 = -28 + Y; x2 = 26 + X; y2 = -54 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 25 + X; y1 = -29 + Y; x2 = 25 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 24 + X; y1 = -30 + Y; x2 = 24 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[2] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[2] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 28 + X; y1 = -26 + Y; x2 = 28 + X; y2 = -4 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 27 + X; y1 = -27 + Y; x2 = 27 + X; y2 = -3 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 26 + X; y1 = -28 + Y; x2 = 26 + X; y2 = -2 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 25 + X; y1 = -27 + Y; x2 = 25 + X; y2 = -3 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 24 + X; y1 = -26 + Y; x2 = 24 + X; y2 = -4 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[3] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[3] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 4 + X; y1 = -0 + Y; x2 = 24 + X; y2 = -0 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 3 + X; y1 = -1 + Y; x2 = 25 + X; y2 = -1 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -2 + Y; x2 = 26 + X; y2 = -2 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -3 + Y; x2 = 25 + X; y2 = -3 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -4 + Y; x2 = 24 + X; y2 = -4 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[4] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[4] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 0 + X; y1 = -4 + Y; x2 = 0 + X; y2 = -26 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -3 + Y; x2 = 1 + X; y2 = -27 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -2 + Y; x2 = 2 + X; y2 = -28 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -3 + Y; x2 = 3 + X; y2 = -27 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -4 + Y; x2 = 4 + X; y2 = -26 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[5] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[5] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 0 + X; y1 = -30 + Y; x2 = 0 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -29 + Y; x2 = 1 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -28 + Y; x2 = 2 + X; y2 = -54 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -29 + Y; x2 = 3 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -30 + Y; x2 = 4 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[6] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[6] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 4 + X; y1 = -26 + Y; x2 = 24 + X; y2 = -26 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 3 + X; y1 = -27 + Y; x2 = 25 + X; y2 = -27 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -28 + Y; x2 = 26 + X; y2 = -28 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -29 + Y; x2 = 25 + X; y2 = -29 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -30 + Y; x2 = 24 + X; y2 = -30 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))

def Show_Digit(X, Y, S, Digit):                  #Digit is 0~9
    if Digit == "0":                             #Depending on Digit to display, a list is created
        Segments = [1, 1, 1, 1, 1, 1, 0]         #to define which segments are needed to create the  
    elif Digit == "1":                           #actual digit. 1 is ON, 0 is OFF for each segment.
        Segments = [0, 1, 1, 0, 0, 0, 0]
    elif Digit == "2":
        Segments = [1, 1, 0, 1, 1, 0, 1]
    elif Digit == "3":
        Segments = [1, 1, 1, 1, 0, 0, 1]
    elif Digit == "4":
        Segments = [0, 1, 1, 0, 0, 1, 1]
    elif Digit == "5":
        Segments = [1, 0, 1, 1, 0, 1, 1]
    elif Digit == "6":
        Segments = [1, 0, 1, 1, 1, 1, 1]
    elif Digit == "7":
        Segments = [1, 1, 1, 0, 0, 0, 0]
    elif Digit == "8":
        Segments = [1, 1, 1, 1, 1, 1, 1]
    elif Digit == "9":
        Segments = [1, 1, 1, 0, 0, 1, 1]
    Plot_Digit_At(X, Y, S, Segments)          #Using this list and the coordinates X,Y, plot the digit

def Display_Value_At(X, Y, S, Char_Space, Value):                     #Create * Draw numeric value at X,Y
    Char_String = str(Value)                                          #Convert to string
    Char_String = "00000" + Char_String                               #Pad with leading zeros - 00012
    Char_String = Char_String[(len(Char_String)-5):len(Char_String)]  #Strip off extra leading zeros
    No_Digits = len(Char_String)                                      #should always result in 5  
    Total_Width = ((No_Digits * 28) + (Char_Space * (No_Digits - 1))) #Compute width in pixes - for futre use
    Char_No = 0                                                       #start at first digit
    while (Char_No >= 0) and (Char_No <= (No_Digits-1)):              #Iterate through each digit
        Digit = Char_String[Char_No]                                  #Extract digit from string
        Char_No += 1                                                  #Incrment character counter
        Show_Digit(X, Y, S, Digit)                                    #Show the digit 
        X = X + 28 + Char_Space                                       #Index X,Y to next character location      

def Plot_Pointer(RPM):                  #Erase then plot new pointer          
    #     0 RPM =   0% = 135 degrees
    #99,999 RPM = 100% = 405 degrees
    # Delta Angle is 405-135 = 270 degrees
    global Prev_RPM                         
    PointerColor = gc9a01.WHITE              #Assign color for pointer
    PA = round((Prev_RPM / Max_RPM)* 270)    #Calc absolute position of 'old' pointer
    NPA = round((RPM / Max_RPM)* 270)        #Calc absolute position of 'new' pointer
    if PA != NPA:                                #Test if RPM/Angle changed, update only if changed
        PA = 135 + PA                            #Set base angle
        angle_in_radians = math.radians(PA)      #Get angle in radians so we can do some trig
        sin_Ar = math.sin(angle_in_radians)      #Get Sine
        cos_Ar = math.cos(angle_in_radians)      #Get Cosine
        Xc = round((107 * cos_Ar)) + 120         #Get X position of pointer tip
        Yc = round((107 * sin_Ar)) + 120         #Get X position of pointer tip
        Plot_Arc(Xc, Yc, (PA-30), (PA+30), 1, 1, 15, gc9a01.BLACK)  #Erase old pointer
        PA = round((RPM / Max_RPM)* 270)         #Calc absolute position of 'new' pointer
        PA = 135 + PA
        angle_in_radians = math.radians(PA)      #Get angle in radians so we can do some trig
        sin_Ar = math.sin(angle_in_radians)      #Get Sine
        cos_Ar = math.cos(angle_in_radians)      #Get Cosine
        Xc = round((107 * cos_Ar)) + 120         #Get X position of pointer tip
        Yc = round((107 * sin_Ar)) + 120         #Get Y position of pointer tip
        Plot_Arc(Xc, Yc, (PA-30), (PA+30), 1, 1, 15, gc9a01.YELLOW) #Draw new pointer
        Prev_RPM = RPM                           #Update Previous RPM variable
  
spi = SPI(0, baudrate=60000000, sck=Pin(2), mosi=Pin(3))    #Initialize spi protocol
tft = gc9a01.GC9A01(                                        #Define & Initialize our display object (tft)
    spi,                            #Define protocol
    240,                            #display width  - zero at left
    240,                            #display height - zero at top
    reset=Pin(26, Pin.OUT),         #define reset pin
    cs=Pin(13, Pin.OUT),            #'Chip Select' pin 
    dc=Pin(21, Pin.OUT),            #'Data Command' pin used to select read/write 
    backlight=Pin(14, Pin.OUT),     #define pin to control backlight
    rotation=0)                     #Set rotation angle -- See bottom of program for code
tft.init()                          #Initialize the display

def Draw_Background():
    tft.fill(gc9a01.BLACK)   #Make background Black
    tft.text(font, "RPM", 95, 200, gc9a01.WHITE, gc9a01.BLACK) #print 'RPM' in white 
    Plot_Arc(120, 120, 135, 351, .1, 95, 105, gc9a01.GREEN)    #draw Green arc on BG
    Plot_Arc(120, 120, 352, 378, .1, 95, 105, gc9a01.YELLOW)   #draw Yellow arc on BG
    Plot_Arc(120, 120, 379, 405, .1, 95, 105, gc9a01.RED)      #draw Red arc on BG
    SA = 135   #Start angle for white tick-marks
    EA = 405   #End angle for white tick-marks
    CA = 135   #Current Angle = Starting angle
    while CA <= EA:
        Plot_Arc(120, 120, CA, CA+2, .1, 85, 107, gc9a01.WHITE) #Plot white tick mark
        CA += 27                                                #step over and plot again

###-----------------------------------------------
# Main code

_thread.start_new_thread(Read_Sensor_Calc_RPM,()) #Starts a thread to handle speed computations

Draw_Background()                   #Draw graphics on display
RPM = 00000                         #Set variable so display be be updated
Display_Value_At(40,140,1,5,RPM)    #Update display - text version of RPM
Plot_Pointer(RPM)                   #Update display - pointer version of RPM

while True:                #Endless Main Loop
    Display_Value_At(40,140,1,5,RPM)  #Display value
    Plot_Pointer(RPM)                 #Move pointer to reflect new RPM
    sleep(.1)                         #This controls display refresh rate


'''
DISPLAY ROTATION CODES
     0     | 0 degrees
     1     | 90 degrees
     2     | 180 degrees
     3     | 270 degrees
     4     | 0 degrees mirrored
     5     | 90 degrees mirrored
     6     | 180 degrees mirrored
     7     | 270 degrees mirrored
'''