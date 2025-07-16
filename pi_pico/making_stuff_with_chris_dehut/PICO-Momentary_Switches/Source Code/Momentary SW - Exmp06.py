# Momentary Switch - Polling with comparision to previous state of switch to prevent bounce and repeats
# Good example to mimic the function of a TOGGLE SWITCH or a ROCKER SWITCH

#Connect wire #1 to Pin 36/3.3V
#Connect wire #2 to Pin 20/GP15

#load libraries
import machine
import utime

#This is needed to indicate the state of the toggle switch
Toggle_Indicator_LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show switch state

#Create a variable to hold the state of the "Toggle Switch"
Toggle_State = False
Toggle_Indicator_LED.value(False)

#Create an 'object' for our actual Momentary Button
Toggle_Sw = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
#Create a variable to hold Last State
Toggle_Sw_Prev_State = Toggle_Sw.value()

def Toggle_Btn_Handler():
    global Toggle_Sw_Prev_State
    global Toggle_State
    #utime.sleep_ms(1)  #If the switch has a lot of bounce- a dwell here can help
    if (Toggle_Sw.value() == True) and (Toggle_Sw_Prev_State == False): #Pressed, If input is HIGH and different from before
        Toggle_Sw_Prev_State = True              #Update previous state variable
        if Toggle_State == False: #Was OFF, now turn it ON
            Toggle_State = True
        elif Toggle_State == True: # Was ON, now turn it OFF
            Toggle_State = False
        Toggle_Indicator_LED.value(Toggle_State)
    elif (Toggle_Sw.value() == False) and (Toggle_Sw_Prev_State == True): #Released, If input is LOW and different from before
        Toggle_Sw_Prev_State = False             #Update previous state variable


print("Ready, Set, Go!")
while True:  #run an endless loop - Typical main loop
    Toggle_Btn_Handler()   
    #utime.sleep(.01) #slow down the loop to mimic other processing activities
   



