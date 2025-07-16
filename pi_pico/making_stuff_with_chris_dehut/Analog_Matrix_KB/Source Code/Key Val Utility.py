#Matrix keypad - ANALOG4 x 4 - Refined with buffering to remove key repeats and THREADED
#The thread handles the keyboard scanning, leaving the main loop to handle other tasks.
#When a key is pressed, the value is written to a global variable 'User_Key'.
#The thread now stops checking for key presses until User_Key is processed in the main loop.
#The main loop must process User_Key and then set it to 'null' for the thread to start scanning again.

#connect VCC to 3.3V pin 36
#connect GND to GND  pin 33
#connect OUT to ADC0 pin 31 (GP26-ADC0)

'''
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

Key_Pad = machine.ADC(0)  #setup analog reading on ADC 0
Raw = 0

# simple code to find avg val for each key to obtain
# key code values

Avg = 0
Pointer = 0
while True:
    Raw = 0
    while Pointer <= 19:
        Raw = Raw + Key_Pad.read_u16()
        utime.sleep(.05)
        Pointer += 1
    Pointer = 0
    Avg = Raw / 20
    print("Average is ",Avg)
    Avg = 0
    utime.sleep(.1)

