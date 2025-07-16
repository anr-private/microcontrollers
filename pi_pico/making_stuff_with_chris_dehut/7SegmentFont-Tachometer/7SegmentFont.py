'''
This is a demonstration program showing the implimentation of a
'7 Segment Font' to display a 6 digit number quickly on the
Waveshare 1.28" round LCD display with an SPI interface.

The best performance I found is with a driver (embeded in a custom
UF2 file) that was written in C.  This driver performs substantially
quicker than the standard offerings I found at Waveshare.  This is
a link to the Git page where I found it.  Also lots of other
good information there too.
https://github.com/russhughes/gc9a01_mpy

BLACK = const(0x0000)
BLUE = const(0x001F)
RED = const(0xF800)
GREEN = const(0x07E0)
CYAN = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW = const(0xFFE0)
WHITE = const(0xFFFF)
'''
from machine import Pin, SPI      #need pins and the SPI library
import gc9a01                     #load the embeded library that is in the UF2 file
from time import sleep            # used to slow things down a bit

spi = SPI(0, baudrate=60000000, sck=Pin(2), mosi=Pin(3)) #Configure and startup SPI interface
tft = gc9a01.GC9A01(
    spi,
    240,
    240,
    reset=Pin(26, Pin.OUT),
    cs=Pin(13, Pin.OUT),
    dc=Pin(21, Pin.OUT),
    backlight=Pin(14, Pin.OUT),
    rotation=0)
tft.init()

def Plot_Digit_At(X,Y,scale,Segments):
    Outline = gc9a01.GREEN            # Characters are 28 pixels wide by 56 pixels tall with scale of 1
    Core    = gc9a01.GREEN            # For each segment, set color based on ON or OFF 
    if Segments[0] == 1:              # If segement is displayed it is ON so set to display color
        OutLineColor = Outline        
        DigitColor   = Core
    elif Segments[0] == 0:           # If segment is not displayed, it is OFF so set to background color 
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK
    #Plot the lines that make up the segment
    x1 = 0 + X; y1 = -56 + Y; x2 = 28 + X; y2 = -56 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -55 + Y; x2 = 27 + X; y2 = -55 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -54 + Y; x2 = 26 + X; y2 = -54 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -53 + Y; x2 = 25 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -52 + Y; x2 = 24 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[1] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[1] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 28 + X; y1 = -30 + Y; x2 = 28 + X; y2 = -56 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 27 + X; y1 = -29 + Y; x2 = 27 + X; y2 = -55 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 26 + X; y1 = -28 + Y; x2 = 26 + X; y2 = -54 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 25 + X; y1 = -29 + Y; x2 = 25 + X; y2 = -53 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 24 + X; y1 = -30 + Y; x2 = 24 + X; y2 = -52 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[2] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[2] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 28 + X; y1 = -26 + Y; x2 = 28 + X; y2 = -0 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 27 + X; y1 = -27 + Y; x2 = 27 + X; y2 = -1 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 26 + X; y1 = -28 + Y; x2 = 26 + X; y2 = -2 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 25 + X; y1 = -27 + Y; x2 = 25 + X; y2 = -3 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 24 + X; y1 = -26 + Y; x2 = 24 + X; y2 = -4 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[3] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[3] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 0 + X; y1 = -0 + Y; x2 = 28 + X; y2 = -0 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -1 + Y; x2 = 27 + X; y2 = -1 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -2 + Y; x2 = 26 + X; y2 = -2 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -3 + Y; x2 = 25 + X; y2 = -3 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -4 + Y; x2 = 24 + X; y2 = -4 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[4] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[4] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 0 + X; y1 = -0 + Y; x2 = 0 + X; y2 = -26 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -1 + Y; x2 = 1 + X; y2 = -27 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 2 + X; y1 = -2 + Y; x2 = 2 + X; y2 = -28 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 3 + X; y1 = -3 + Y; x2 = 3 + X; y2 = -27 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
    x1 = 4 + X; y1 = -4 + Y; x2 = 4 + X; y2 = -26 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    if Segments[5] == 1:
        OutLineColor = Outline
        DigitColor   = Core
    elif Segments[5] == 0:    
        OutLineColor = gc9a01.BLACK
        DigitColor   = gc9a01.BLACK   
    x1 = 0 + X; y1 = -30 + Y; x2 = 0 + X; y2 = -56 + Y; tft.line(x1,y1,x2,y2,(OutLineColor))
    x1 = 1 + X; y1 = -29 + Y; x2 = 1 + X; y2 = -55 + Y; tft.line(x1,y1,x2,y2,(DigitColor))
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

def Show_Digit(X, Y, S, Digit):                #Digit is 0~9
    if Digit == "0":                           #Based on what the digit is
        Segments = [1, 1, 1, 1, 1, 1, 0]       #create a list of "segments" to display
    elif Digit == "1":
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
    Plot_Digit_At(X, Y, S, Segments)      #Call the function to plot the 7 segment digit

def Display_Value_At(X, Y, S, Char_Space, Value):
    Char_String = str(Value)                                           #Convert data to string format
    Char_String = "00000" + Char_String                                #Pad the string with leading zeros
    Char_String = Char_String[(len(Char_String)-5):len(Char_String)]   #Truncate at 6 digits
    No_Digits = len(Char_String)                                       
    Total_Width = ((No_Digits * 28) + (Char_Space * (No_Digits - 1)))  #compute width in pixels
    Char_No = 0                                                        #start with Character #0
    while (Char_No >= 0) and (Char_No <= (No_Digits-1)):               #Stp through each character in the string 
        Digit = Char_String[Char_No]                                   #Extract the DIGIT to be shown
        Char_No += 1                                                   #Increment counter
        Show_Digit(X, Y, S, Digit)                                     #call function to show digit 
        X = X + 28 + Char_Space                                        #Shift over the X position of the char  

   
tft.fill(gc9a01.BLACK)             #Clear screen
RPM = 00000                        #Preset a value for RPM
Display_Value_At(40,140,1,5,RPM)   #Call function to show RPM in new font

RPM = 0
while RPM < 100001:
    Display_Value_At(40,140,1,5,RPM)
    RPM += 9999
    sleep(1)

RPM = 0
while RPM < 90000:
    Display_Value_At(40,140,1,5,RPM)
    RPM += 123

