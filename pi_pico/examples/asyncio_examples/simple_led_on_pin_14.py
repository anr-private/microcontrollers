# simple led control
#
# Uses LED on pin 14.
# Just blinks the LED endlessly

import utime

def main():
    print("MAIN start")
    
    ledA = machine.Pin(14, machine.Pin.OUT)

    while 1:
        ledA.on()    
        utime.sleep(0.5)
        ledA.off()    
        utime.sleep(0.25)
    
    print("MAIN end")
    
    
main()

### end ###
