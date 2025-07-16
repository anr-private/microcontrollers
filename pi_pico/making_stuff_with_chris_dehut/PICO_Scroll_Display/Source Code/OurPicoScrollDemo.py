'''
Our Pico Scroll Demo.py
This demo takes the existing demos from Pimoroni and changes them up a bit.

Some very basic functions are used to facilite some graphic manipulations;
draw_x_line    --> plots a horizontal line
draw_y_line    --> plots a verticle line
plot_pixel     --> plots a pixel and doesn't crash if out of bounds
move_snowflake --> Animates a falling snowflake

The main code section:
plots some lines
fills the screen with a gadient fill
scrolls some text across the screen
Button press example -- MUST PRESS Y to exit loop
Animate a falling snowflake
Scroll another text message

'''
import time
import picoscroll as scroll

width = scroll.get_width()
height = scroll.get_height()

print(width, height)


def draw_x_line(xs,xe,y,intensity):
    x = range(xs, xe)
    for n in x:
        scroll.set_pixel(n, y, intensity)
        time.sleep(.01)
        scroll.update()

def draw_y_line(ys,ye,x,intensity):
    y = range(ys, ye)
    for n in y:
        scroll.set_pixel(x, n, intensity)
        time.sleep(.01)
        scroll.update()

def plot_pixel(x,y,intensity):
    try:
        scroll.set_pixel(x, y, intensity)
        scroll.update()
    except:
        pass

def move_snowflake(x):
    y = -2
    while y < 8:        
        plot_pixel(x,y-1,0)
        plot_pixel(x,y,150)
        plot_pixel(x-1,y,0)
        plot_pixel(x-1,y+1,150)
        plot_pixel(x+1,y,0)
        plot_pixel(x+1,y+1,150)
        plot_pixel(x,y+1,0)
        plot_pixel(x,y+2,150)
        y += 1
        time.sleep(.25)

# MAIN CODE -----------------------------------------------------------------------------

# Draw a couple of lines
scroll.clear()
scroll.update()
draw_x_line(0,17,4,40)
draw_y_line(0,7,8,40)
time.sleep(2)

#Line drawing with change in LED brightness
scroll.clear()
scroll.update()
draw_x_line(0,16,0,140)
draw_y_line(0,7,16,140)
draw_x_line(0,15,1,120)
draw_y_line(1,7,15,120)
draw_x_line(0,14,2,100)
draw_y_line(2,7,14,100)
draw_x_line(0,13,3,80)
draw_y_line(3,7,13,80)
draw_x_line(0,12,4,60)
draw_y_line(4,7,12,60)
draw_x_line(0,11,5,40)
draw_y_line(5,7,11,40)
draw_x_line(0,11,6,20)
#time.sleep(2)

# Scrolling Text message
scroll.clear()
scroll.update()
scroll.scroll_text("Welcome to Making Stuff With Chris DeHut", 128, 80)#text, brightness, delay in ms
 
# Button examples
scroll.clear()
scroll.update()
while True:
    if scroll.is_pressed(scroll.BUTTON_A):
        draw_x_line(0,2,1,140)
        draw_x_line(0,2,2,140)
        scroll.update()
        time.sleep(1)
    elif scroll.is_pressed(scroll.BUTTON_B):
        draw_x_line(0,2,4,140)
        draw_x_line(0,2,5,140)
        scroll.update()
        time.sleep(1)
    elif scroll.is_pressed(scroll.BUTTON_X):
        draw_x_line(15,17,1,140)
        draw_x_line(15,17,2,140)
        scroll.update()
        time.sleep(1)
    elif scroll.is_pressed(scroll.BUTTON_Y):
        draw_x_line(15,17,4,140)
        draw_x_line(15,17,5,140)
        scroll.update()
        time.sleep(1)
        break
 
 
# Animate a snowflake falling
scroll.clear()
scroll.update()
move_snowflake(5)
   
# Scrolling Text message
scroll.clear()
scroll.update()
scroll.scroll_text("That's All Folks!", 128, 80)#text, brightness, delay
print("All done folks!")

