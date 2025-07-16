# Momentary Switch - Polling with comparison to previous state of switch to prevent bounce and repeats
# Good example to perform action on the PRESS of the button

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin 20/GP15

#load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show switch state

#Create an 'object' for our actual Momentary Button
Down_Btn = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
#Create a variable to hold Last State
Down_Btn_Prev_State = Down_Btn.value()

def Down_Btn_Handler():
    global Down_Btn_Prev_State
    if (Down_Btn.value() == True) and (Down_Btn_Prev_State == False): #Pressed, If input is HIGH and different from before
        Down_Btn_Prev_State = True              #Update previous state variable
        print("Pressed - Start action here")
        #put your code or call your code to execute here
    elif (Down_Btn.value() == False) and (Down_Btn_Prev_State == True): #Released, If input is LOW and different from before
        Down_Btn_Prev_State = False             #Update previous state variable


print("Ready, Set, Go!")
while True:  #run an endless loop - Typical main loop
    Down_Btn_Handler()   
    utime.sleep(.01) #slow down the loop to mimic other processing activities
        



