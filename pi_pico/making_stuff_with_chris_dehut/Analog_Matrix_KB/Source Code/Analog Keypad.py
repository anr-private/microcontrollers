#Matrix keypad - ANALOG 4 x 4 - Refined with buffering to remove key repeats and THREADED
#The thread handles the keyboard scanning, leaving the main loop to handle other tasks.
#When a key is pressed, the value is written to a global variable 'User_Key'.
#The thread now stops checking for key presses until User_Key is processed in the main loop.
#The main loop must process User_Key and then set it to 'null' for the thread to start scanning again.

#connect VCC to 3.3V pin 36
#connect GND to GND  pin 33
#connect OUT to ADC0 pin 31 (GP26 ADC0)

'''
Use the program Key Val Utility.py to obtain these values
KEYMAP showing which key is what analog value and the dividing line between key values
No key pressed averages 408
Full analog range was 65535 @ 1 (top left) to 11490 @ D (bot right)
These readings are avg for each key and then the mid-point between 2 keys
1 65535
--- 62305
2 59075
--- 56177
3 53280
--- 50760
A 48240
--- 44140
4 40040
--- 38490
5 36940
--- 35605
6 34270
--- 33075
B 31880
--- 29830
7 27780
--- 26985
8 26190
--- 25470
9 24750
--- 24185
C 23620
--- 22445
* 21270
--- 18910
0 16550
--- 15045
# 13540
--- 12515
D 11490
--- 5745
  408
'''

import machine
import utime
import _thread

LED = machine.Pin(25, machine.Pin.OUT)
Key_Pad = machine.ADC(0)  #setup analog reading on ADC 0
Raw = 0

Last_Key = "null"        #buffer variable to hold a button press value until button is released
User_Key = "null"        #User pressed key, is set in thread, but can be read in main loop

def Analog_Keyboard_Scanner():  #This function will handle the keyboard and run in its own thread.
    global User_Key
    Last_Key = "null"        #buffer variable to hold a button press value until button is released
    while True:                 #loop forever
        #if someone typed fast, User_Key could be written over before it is handled in the main loop
        #to prevent this, the loop will not accept another key press until the main loop
        #reads the User_Key value and resets it to 'null'
        if User_Key == "null":
            Raw = Key_Pad.read_u16()
            Key = 'null'
            if Raw > 62305:
                Key = "1"
            elif (Raw > 56177) and (Raw <= 62305):
                Key = "2"
            elif (Raw > 50760 ) and (Raw <= 56177):
                Key = "3"
            elif (Raw > 44140) and (Raw <= 50760):
                Key = "A"
           
            elif (Raw > 38490) and (Raw <= 44140):
                Key = "4"
            elif (Raw > 35605) and (Raw <= 38490):
                Key = "5"
            elif (Raw > 33075) and (Raw <= 35605):
                Key = "6"
            elif (Raw > 29830) and (Raw <= 33075):
                Key = "B"
            
            elif (Raw > 26985) and (Raw <= 29830):
                Key = "7"
            elif (Raw > 25470) and (Raw <= 26985):
                Key = "8"
            elif (Raw > 24185) and (Raw <= 25470):
                Key = "9"
            elif (Raw > 22445) and (Raw <= 24185):
                Key = "C"

            elif (Raw > 18910) and (Raw <= 22445):
                Key = "*"
            elif (Raw > 15045) and (Raw <= 18910):
                Key = "0"
            elif (Raw > 12515) and (Raw <= 15045):
                Key = "#"
            elif (Raw > 5745) and (Raw <= 12515):
                Key = "D"
            
            if (Key != "null"):  #Button was pressed - put it in buffer until button is released
                Last_Key = Key   #Store key press in buffer 'Last_Key'
            elif (Key == "null") and (Last_Key != "null"):  #Keypress in buffer, and button was released
                User_Key = Last_Key  #Store key press in variable for reading by main loop
                Last_Key = "null"    #reset buffer to empty so another key press can be recorded       
            
        utime.sleep(.02) #slow down the loop a bit as full speed isn't needed
        
_thread.start_new_thread(Analog_Keyboard_Scanner,())  #This starts the thread running 



while True:  #main loop working on other things
    LED.toggle()
    if User_Key != "null":             #Check for value in User_Key and act on it 
        Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
        User_Key = "null"              #Reset User_Key to null so it can be written to again
        print("Key Code =",Key_Code)
    utime.sleep(.1)