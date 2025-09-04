# simple led control

import utime

def main():
    print("MAIN start")
    
    ledA = machine.Pin(14, machine.Pin.OUT)
    ledA.on()
    
    utime.sleep(5)
    
    print("MAIN end")
    
    
main()

### end ###
