# Momentary Switch - Polling with comparision to previous state of switch to prevent bounce and repeats
# Good example to maintain ON while holding button

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin 20/GP15

#load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show switch state

#Create an 'object' for our actual Momentary Button
Jog_Btn = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
#Create a variable to hold Last State
Jog_Btn_Prev_State = Jog_Btn.value()
def Jog_Btn_Handler():
    global Jog_Btn_Prev_State
    if (Jog_Btn.value() == True) and (Jog_Btn_Prev_State == False): #Pressed, If input is HIGH and different from before
        Jog_Btn_Prev_State = True
        print("Start the Jogging")
        LED.value(1)
        #put your code or call your code to execute here
    elif (Jog_Btn.value() == False) and (Jog_Btn_Prev_State == True): #Released, If input is LOW and different from before
        Jog_Btn_Prev_State = False
        print("STOP the Jogging")
        LED.value(0)
        #put your code or call your code to execute here


print("Ready, Set, Go!")
while True:  #run an endless loop - Typical main loop 
    Jog_Btn_Handler()
    utime.sleep(.01) #slow down the loop to mimic other processing activities
        

        



