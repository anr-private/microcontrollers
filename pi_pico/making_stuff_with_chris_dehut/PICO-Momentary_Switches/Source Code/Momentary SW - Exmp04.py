# Momentary Switch - Polling with comparision to previous state of switch to prevent bounce and repeats
# Good example to perform REPEATING action while PRESSING the button

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin 20/GP15

#load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show switch state

#Create an 'object' for our actual Momentary Button
Repeat_Btn = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
#Create a variable to hold Last State
Repeat_Btn_Prev_State = Repeat_Btn.value()

def Repeat_Btn_Handler():
    global Repeat_Btn_Prev_State
    if (Repeat_Btn.value() == True) and (Repeat_Btn_Prev_State == False): #Pressed, If input is HIGH and different from before
        Repeat_Btn_Prev_State = True
        print("Start Repeater")
        utime.sleep_ms(300)
        while Repeat_Btn.value() == True:  #While button is pressed
            print("Repeating")
            utime.sleep_ms(50)
        Repeat_Btn_Prev_State = False
        print("STOP Repeating")

print("Ready, Set, Go!")
while True:  #run an endless loop - Typical main loop 
    Repeat_Btn_Handler()
    utime.sleep(.01) #slow down the loop to mimic other processing activities
        



