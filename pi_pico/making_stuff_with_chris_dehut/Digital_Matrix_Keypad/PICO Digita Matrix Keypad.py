#Matrix keypad - digital 4 x 4 - Threaded and with buffering to remove key repeats
#The thread handles the keyboard scanning, leaving the main loop to handle other tasks.
#When a key is pressed, the value is written to a global variable 'User_Key'.
#The thread now stops checking for key presses until User_Key is processed in the main loop and
#the button is released.
#The main loop must process User_Key and then set it to 'null'.

from machine import Pin
import utime
import _thread

#setup the inputs and outputs according to the matrix keypad's wiring
R1 = machine.Pin(15,machine.Pin.OUT)
R2 = machine.Pin(14,machine.Pin.OUT)
R3 = machine.Pin(13,machine.Pin.OUT)
R4 = machine.Pin(12,machine.Pin.OUT)
C1 = machine.Pin(11,machine.Pin.IN,machine.Pin.PULL_DOWN)
C2 = machine.Pin(10,machine.Pin.IN,machine.Pin.PULL_DOWN)
C3 = machine.Pin(9,machine.Pin.IN,machine.Pin.PULL_DOWN)
C4 = machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_DOWN)

User_Key = "null"        #User pressed key, is set in thread, but can be read in main loop

def Keyboard_Scanner():  #This function will handle the keyboard and run in its own thread.
    global User_Key
    Lock = "UNLOCKED"    #Variable Lock is used to compare against for action to occur
    
    while True:                 #loop forever
        Key_Pressed = "null"    #Set variable to 'null' at start of scan
        
        #Power each row one by one. While a row is powered, test the four columns
        #to see if any are "high", thus being pressed.  If a button is pressed
        #record that button value in variable Key_Pressed.
        R1.value(1)             #set power ON for row 1, off for the other three
        R2.value(0)
        R3.value(0)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = "1" #check each button in column
        if C2.value() == True: Key_Pressed = "2"
        if C3.value() == True: Key_Pressed = "3"
        if C4.value() == True: Key_Pressed = "A"
                  
        R1.value(0)             #set power ON for row 2, off for the other three
        R2.value(1)
        R3.value(0)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = "4"
        if C2.value() == True: Key_Pressed = "5"
        if C3.value() == True: Key_Pressed = "6"
        if C4.value() == True: Key_Pressed = "B"
            
        R1.value(0)             #set power ON for row 3, off for the other three
        R2.value(0)
        R3.value(1)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = "7"
        if C2.value() == True: Key_Pressed = "8"
        if C3.value() == True: Key_Pressed = "9"
        if C4.value() == True: Key_Pressed = "C"
            
        R1.value(0)             #set power ON for row 4, off for the other three
        R2.value(0)
        R3.value(0)
        R4.value(1)    
        if C1.value() == True: Key_Pressed = "*"
        if C2.value() == True: Key_Pressed = "0"
        if C3.value() == True: Key_Pressed = "#"
        if C4.value() == True: Key_Pressed = "D"
 
        # if lock was Locked, check to see if it can be unlocked
        # If we get through the keypad scan without seeing a Key_Press
        # value other than null, no key is pressed, so lets unlock the function.  
        if (Lock == "LOCKED") and (Key_Pressed == "null"):
            Lock = "UNLOCKED"
            
        # Key was pressed and because Lock wasn't locked, this is a new key press
        # Lock the routine from processing another keypress until
        # User_Key is processed in the main loop AND the the button was released
        # which prevents key repeating
        #
        if (Lock == "UNLOCKED") and (Key_Pressed != "null"):
            Lock = "LOCKED"
            User_Key = Key_Pressed
        
        utime.sleep(.02) #slow down the loop a bit as full speed isn't needed

_thread.start_new_thread(Keyboard_Scanner,())  #This starts the thread running 



#Main Loop to do all the other work needed
while True:
    if User_Key != "null":             #Check for value in User_Key and act on it 
        Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
        User_Key = "null"              #Reset User_Key to null so it can be written to again
        print("Key Code =",Key_Code)
    
    utime.sleep(.1)  # A sleep just to slow things down to mimic work being performed
    #here in the main loop is where all the normal processing happens
    
    