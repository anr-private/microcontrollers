# Encoder test 1
# Non-functioning example 
# load libraries
import machine
import utime

LED = machine.Pin(25,machine.Pin.OUT) #use on board LED to show switch state

Last_Chnl = "B"
Counter = 0

def A_Handler(pin):
    global Last_Chnl
    global Counter
    if (Encoder_A.value() == True):
        if Last_Chnl == "B":  # Was B, now A
            Counter -= 1
            print(Last_Chnl,"-> A  LEFT ",Counter)
            Last_Chnl = "A"
   
    
def B_Handler(pin):
    global Last_Chnl
    global Counter
    if (Encoder_B.value() == True):
        if Last_Chnl == "A":  # Was A, now B
            Counter += 1
            print(Last_Chnl, "-> B  RIGHT ",Counter)
            Last_Chnl = "B"
    

Encoder_A = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
Encoder_A.irq(trigger=machine.Pin.IRQ_RISING, handler=A_Handler)

Encoder_B = machine.Pin(14,machine.Pin.IN,machine.Pin.PULL_DOWN)
Encoder_B.irq(trigger=machine.Pin.IRQ_RISING, handler=B_Handler)


#Create a variable to hold Last State
Momentary_Sw_State = Encoder_A.value()

#Interrupt method of handling an input with State Checking
print("Ready")
while True:  #run an endless loop
    utime.sleep(.11)
