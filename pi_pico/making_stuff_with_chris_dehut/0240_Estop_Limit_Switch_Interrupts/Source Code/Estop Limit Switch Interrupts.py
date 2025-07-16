# E-Stop and Limit Switch - Interrupt Handling
# Uses IRQ to run reaction function

#Wire according to associated Fritzing diagram
#NOT RECOMMENDED FOR ANY DEVICE THAT CAN CAUSE PERSONAL HARM!!!!

#load libraries
import machine
import utime

#create LED objects to act as driven circuit
Limit_SW_LED = machine.Pin(15,machine.Pin.OUT)
E_Stop_LED   = machine.Pin(16,machine.Pin.OUT)

#Turn on LEDs to similute a running circuit
Limit_SW_LED.on()
E_Stop_LED.on()

#create Switch objects for physical switches
Limit_SW  = machine.Pin(14,machine.Pin.IN,machine.Pin.PULL_UP)
E_Stop_SW = machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_UP)

#Create Interrupt handler for Limit Switch
def Limit_SW_Handler(pin):
    Limit_SW_LED.off()
    print("LIMIT REACHED - CORRECT PROBLEM AND RESTART PROGRAM")

#Create Interrupt handler for E-Stop Switch
def EStop_SW_Handler(pin):
    E_Stop_LED.off()
    print("E-Stop Pressed - CORRECT PROBLEM AND RESTART PROGRAM")


#Start the interrupt handler routines
Limit_SW.irq( trigger=machine.Pin.IRQ_FALLING, handler=Limit_SW_Handler)
E_Stop_SW.irq(trigger=machine.Pin.IRQ_FALLING, handler=EStop_SW_Handler)

# A loop just to keep things running, but does nothing constructive
print("Ready, Set, Go!")
x=0
while True:  #run an endless loop
    x += 1
    print(x)
    utime.sleep(.5)
    
