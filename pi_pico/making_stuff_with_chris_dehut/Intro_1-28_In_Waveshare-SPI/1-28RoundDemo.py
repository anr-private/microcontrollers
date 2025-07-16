'''
This is a demonstration program showing some of the capability
of the Waveshare 1.28" round LCD display with an SPI interface.

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
import math                       #only needed for some 'razzle dazzle' drawing
import gc9a01                     #load the embeded library that is in the UF2 file
import vga1_16x16 as font_1       #loads a bitmap font
import vga1_16x32 as font_2       #
import vga1_8x8 as font_3         #
import vga1_bold_16x32 as font_4  #
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

def Get_Angle_Line(Xc, Yc, R1, R2, A_Deg):  #Calculates the coordinates of a line at an angle
    angle_in_radians = math.radians(A_Deg)
    sin_Ar = math.sin(angle_in_radians)
    cos_Ar = math.cos(angle_in_radians)
    x1 = round(Xc + (R1 * cos_Ar))
    y1 = round(Yc + (R1 * sin_Ar))
    x2 = round(Xc + (R2 * cos_Ar))
    y2 = round(Yc + (R2 * sin_Ar))
    return x1,y1,x2,y2                      #Returns the coordinates for start and end

def Plot_Arc(Xc, Yc, Sa, Ea, Da, R1, R2, P_Color):         #No built-in circle or arc function
    A  = Sa                                                #this gets the job done - slowly
    while A <= Ea:
        x1, y1, x2, y2 = Get_Angle_Line(Xc, Yc, R1, R2, A)
        A += Da
        tft.line(x1,y1,x2,y2,(P_Color))

#-----------------------------------------------------------------
# Start showing off some of the methods with the library to draw
# text and graphics

tft.fill(gc9a01.BLUE)
tft.text(font_1, "WHITE", 80, 200, gc9a01.WHITE, gc9a01.BLUE)

tft.line(0, 140, 240, 140, gc9a01.YELLOW)
tft.line(0, 141, 240, 141, gc9a01.YELLOW)
tft.line(0, 142, 240, 142, gc9a01.YELLOW)
tft.rect(100, 100, 40, 40, gc9a01.RED)
tft.fill_rect(110, 110, 20, 20, gc9a01.CYAN)

sleep(1)
tft.fill(gc9a01.BLUE)
tft.text(font_1, "vga1_bold_16x16", 10, 100, gc9a01.WHITE, gc9a01.BLACK)
tft.text(font_2, "vga1_bold_16x32", 10, 130, gc9a01.WHITE, gc9a01.BLACK)

sleep(1)
tft.fill(gc9a01.BLUE)
tft.text(font_3, "12", 110, 10, gc9a01.WHITE, gc9a01.BLUE)
tft.text(font_3, "3" , 210, 110, gc9a01.WHITE, gc9a01.BLUE)
tft.text(font_3, "6" , 110, 210, gc9a01.WHITE, gc9a01.BLUE)
tft.text(font_3, "9" , 10,  110, gc9a01.WHITE, gc9a01.BLUE)


sleep(1)
tft.fill(gc9a01.BLACK)
tft.text(font_4, "12", 110, 10, gc9a01.YELLOW, gc9a01.BLACK)
tft.text(font_4, "3" , 210, 110, gc9a01.YELLOW, gc9a01.BLACK)
tft.text(font_4, "6" , 110, 200, gc9a01.YELLOW, gc9a01.BLACK)
tft.text(font_4, "9" , 10,  110, gc9a01.YELLOW, gc9a01.BLACK)

sleep(1)
SA = 0
EA = 360
CA = 0
while CA <= EA:
    Plot_Arc(120, 120, CA, CA+2, .1, 65, 80, gc9a01.MAGENTA)
    CA += 30


sleep(1)
SA = 0
EA = 360
CA = 0
while CA <= EA:
    Plot_Arc(120, 120, CA, CA+2, .1, 55, 60, gc9a01.CYAN)
    CA += 2

