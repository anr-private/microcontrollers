'''
Demo program for PICO RGB Keypad
REQUIRES the UF2 file from PIMORONI that is suitable for your PICO configuration

Pimoroni UF2 Files
https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.19.10
pimoroni-pico-v1.19.10-micropython.uf2

This shows the use of "Latching key states" as indicated by their color.
This is useful for turning something ON or OFF.

Within the main loop, you can see how to just see if a key was pressed.

Create a List containing the state of each button numbered 0 ~ 15 to match legends
Row 1 buttons are Red, 2 are Green, 3 are Blue, and 4 are Yellow
When a button is off it is set to very dim Blue

Key Code Table - Button number on left - Code on right
0 = 1
1 = 2
2 = 4
3 = 8
4 = 16
5 = 32
6 = 64
7 = 128
8 = 256
9 = 512
A = 1024
B = 2048
C = 4096
D = 8192
E = 16384
F = 32768
'''


import time
import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)
keypad.update()
NUM_PADS = keypad.get_num_pads()
Button_State=[]
for i in range(0, 16):
    Button_State.append('O') # Prepopulate with all set to OFF
for i in range(0, NUM_PADS):
    keypad.illuminate(i, 0x00, 0x00, 0x03)
    keypad.update()


def Light_Key(key,color):
    #key = 1 ~ 16
    #Color = R, G, B, Y, O
    global Button_State  
    if (color == "R") & (Button_State[key] != "R") :  #Was off, turning on
        keypad.illuminate(key, 0x20, 0x00, 0x00) #Red
        Button_State[key] = "R"
    elif (color == "R") & (Button_State[key] == "R") :  #Was on, turning off
        keypad.illuminate(key, 0x00, 0x00, 0x03) #O OFF
        Button_State[key] = "O"
    elif (color == "G") & (Button_State[key] != "G") :  #Was off, turning on
        keypad.illuminate(key, 0x00, 0x20, 0x00) #Green
        Button_State[key] = "G"
    elif (color == "G") & (Button_State[key] == "G") :  #Was on, turning off
        keypad.illuminate(key, 0x00, 0x00, 0x03) #O OFF
        Button_State[key] = "O"
    elif (color == "B") & (Button_State[key] != "B") :  #Was off, turning on
        keypad.illuminate(key, 0x00, 0x00, 0x20) #Blue
        Button_State[key] = "B"
    elif (color == "B") & (Button_State[key] == "B") :  #Was on, turning off
        keypad.illuminate(key, 0x00, 0x00, 0x03) #O OFF
        Button_State[key] = "O"
    elif (color == "Y") & (Button_State[key] != "Y") :  #Was off, turning on
        keypad.illuminate(key, 0x20, 0x20, 0x00) #Yellow
        Button_State[key] = "Y"
    elif (color == "Y") & (Button_State[key] == "Y") :  #Was on, turning off
        keypad.illuminate(key, 0x00, 0x00, 0x03) #O OFF
        Button_State[key] = "O"
    keypad.update()
    

def Get_Key(Rk):               #The code from the library is 1, 2, 4, 8, .....  16384, 32768 
    if Rk == 1:                #This routine creates a key number from 0 ~ 15 - Easier to understand
        key = 0                #Also, based on the key number a color is assigned.
        color = "R"
    elif Rk == 2:
        key = 1
        color = "R"
    elif Rk == 4:
        key = 2
        color = "R"
    elif Rk == 8:
        key = 3
        color = "R"
    elif Rk == 16:
        key = 4
        color = "G"
    elif Rk == 32:
        key = 5
        color = "G"
    elif Rk == 64:
        key = 6
        color = "G"
    elif Rk == 128:
        key = 7
        color = "G"
    elif Rk == 256:
        key = 8
        color = "B"
    elif Rk == 512:
        key = 9
        color = "B"
    elif Rk == 1024:
        key = 10
        color = "B"
    elif Rk == 2048:
        key = 11
        color = "B"
    elif Rk == 4096:
        key = 12
        color = "Y"
    elif Rk == 8192:
        key = 13
        color = "Y"
    elif Rk == 16384:
        key = 14
        color = "Y"
    elif Rk == 32768:
        key = 15
        color = "Y"
    Light_Key(key,color)      #Set the key's LED to the color depending on its state
    return key                #Return the key number (0-15) to the caller  
    
    
Last_Key = 0      #Used to help prevent auto repeat of button
while True:
    button_states = keypad.get_button_states()  #Get code for button being pressed 1 ~ 32768
    if (button_states != 0) & (Last_Key == 0):  #Ignore '0' and insure key isn't repeating 
        Pressed_key = Get_Key(button_states)    #Get the button pressed number in range of 1 ~ 16
        print("You Pressed ",Pressed_key)
        Last_Key = button_states                #Update variable holding the last key pressed value
        if Pressed_key == 15:                   # a way out of the demo loop
            break
    else:
        Last_Key = button_states                #Update variable holding the last key pressed value
    

for i in range(0,16):           #Iterate through the list showing the state of each button
    if Button_State[i] == "O":  #Button state is OFF
        B_S = "OFF"
    else:
        B_S = "ON"              #Button_State is ON -- either R, G, B, or Y
    print("Button ", i, " is set to ",B_S)  
    
    
