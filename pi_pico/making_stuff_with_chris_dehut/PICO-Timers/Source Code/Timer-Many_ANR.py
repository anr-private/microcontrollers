# Multiple timers running at timeouts; main loop runs independently  ANR
# Main loop runs without interruption

# LEDs on GPIO 12,13,14,15  (board pins 16,17,19,20)

# See fritzing file for wiring

import machine
import utime

Blue   = machine.Pin(12,machine.Pin.OUT)
Red    = machine.Pin(13,machine.Pin.OUT)
Green  = machine.Pin(14,machine.Pin.OUT)
Yellow = machine.Pin(15,machine.Pin.OUT)

#Create handlers for the timer IRQ
def Blue_Blinker(Source):
    Blue.toggle()

def Red_Blinker(Source):
    Red.toggle()

def Green_Blinker(Source):
    Green.toggle()

def Yellow_Blinker(Source):
    Yellow.toggle()


#Periodic timers to run continuously - 1 for each LED
#Timers run at a base of 1 millisecond (.001) seconds
#1 would be 1 millisecond
#500 would be 1/2 second
#1000 would be 1 second
#10000 would be 10 seconds
Blue_Timer   = machine.Timer(period=2000, mode=machine.Timer.PERIODIC, callback=Blue_Blinker)
Red_Timer    = machine.Timer(period=1000, mode=machine.Timer.PERIODIC, callback=Red_Blinker)
Green_Timer  = machine.Timer(period=500, mode=machine.Timer.PERIODIC, callback=Green_Blinker)
Yellow_Timer = machine.Timer(period=250, mode=machine.Timer.PERIODIC, callback=Yellow_Blinker)

#Create a main loop to keep the program running
#in this loop you would do all your other work
loop_ctr = 0
saved_irq_state = None
try:
    while True:
        loop_ctr += 1
        print(f"   main: loop ctr={loop_ctr}")
        
        # Try disabling - it kills the hardware time, so also kills utime.sleep()!
        # So it never recovers.
        #if loop_ctr > 5:
        #    print("*** DISABLING INTERRUPTS!  ***")
        #    saved_irq_state = machine.disable_irq()
        
        utime.sleep(1)
        
        #if saved_irq_state is not None:
        #    machine.enable_irq(saved_irq_state)
        #    saved_irq_state = None
        #    print("+++ ENABLED interrupts!")
        
except KeyboardInterrupt as ex:
    print(f"MAIN: keyboard interrupt.  Do cleanup.")

    #Turn off the timers so the program terminates cleanly
    Blue_Timer.deinit()
    Red_Timer.deinit()
    Green_Timer.deinit()
    Yellow_Timer.deinit()

    # Give time for the timers to shut down
    # Else the LEDs may not turn off in the steps below
    #utime.sleep(1) NOT NEEDED if you use the try/except(?!)

    #Turn off all the LEDs so keep things tidy
    #Blue.value(0)
    #Red.value(0)
    #Green.value(0)
    #Yellow.value(0)
    # A bit more obvious(!)
    Blue.off()
    Red.off()
    Green.off()
    Yellow.off()

print("End of MAIN")

### end ###

