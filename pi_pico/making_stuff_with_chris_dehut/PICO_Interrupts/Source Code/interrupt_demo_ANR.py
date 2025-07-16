# Interrupt Handling - PB Switch Input
# ANR
# GPIO 16 LED to Resistor to gnd
# GPIO 15 'button' to physical 36 '3V3'
#
# See wiring - to Fritzing diagram
# Items needed:
# Latching switch (or just use a wire to go from +5 to the button pin 15)
# 220 Ohm Resistor or 330
# LED

#load libraries
import machine
import utime
import _thread

###  CONSTANTS  ##########################

PUSHBUTTON_IRQ_TRIGGER = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING

### GLOBALS  #########################
#Preset the STATE variable for the pushbutton
pushbutton_state = 0

# the button obj
pushbutton = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)

# the indicator LED
btn_state_led = machine.Pin(16,machine.Pin.OUT)  #Create an output pin for warning LED
###btn_state_led.value(0)                           #Set it to OFF


def set_pushbutton_state(new_state=None):
    """ Set the state of the pushbutton """
    global pushbutton_state;
    
    if new_state is None:
        new_state = pushbutton.value()
        print(f"set_pushbutton_state: set initial state to {new_state}")
        
    if new_state:
        pushbutton_state = True
        btn_state_led.value(1)
    else:
        pushbutton_state = False
        btn_state_led.value(0)
        
        
def pushbutton_handler(pin):
    """ interrupt handler  """
    global pushbutton_state
    
    pushbutton.irq(handler=None)
    #r = pushbutton.irq(handler=None)
    #print(f"@@@ irq(none) is {type(r)}  {r}")
    #print(f"@@@ {dir(r)}")
    ###print(f"@@@ irq(none) is 0x{r:04x}")

    pb_value = pushbutton.value()
    
    if 0:
        print(f"HANDLER: pb.val={pb_value}  pb-state={pushbutton_state}")
    
    # Use the state to prevent unwanted state changes due to button bounce
    if pb_value and not pushbutton_state:
        set_pushbutton_state(True)
        print("ON")
        
    elif not pb_value and pushbutton_state:
        set_pushbutton_state(False)
        print("OFF")
    else:
        print(f"  BOUNCED: pb.val={pb_value}  pb-state={pushbutton_state}")
        
    pushbutton.irq(trigger=PUSHBUTTON_IRQ_TRIGGER, handler=pushbutton_handler)
    

#Setup the Interrupt Request Handling for pushbutton change of state
###@@@pushbutton.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=pushbutton_handler)
pushbutton.irq(trigger=PUSHBUTTON_IRQ_TRIGGER, handler=pushbutton_handler)

# Get the initial state
set_pushbutton_state()
print("pushbutton State=", pushbutton_state)

# A loop just to keep things running, but does nothing constructive
print("--- start main loop ----")
if 1:
    print(f"Thread ")
    
while True:  #run an endless loop as the main loop
    utime.sleep(.0001)
    #Perform all other activites here

### end ###
    