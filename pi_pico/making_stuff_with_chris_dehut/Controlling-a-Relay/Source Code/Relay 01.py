'''
Relay example 1
'''
import machine
import time

Relay1 = machine.Pin(16	,machine.Pin.OUT)  #output pin for relay
OB_LED = machine.Pin(25,machine.Pin.OUT)  #Use onboard LED as indicator

L=0
while (L < 10):  #run 10 times then end program
    L += 1
    Relay1.on()  #Turn relay on 
    OB_LED.on()
    print("ON")
    time.sleep(3)
    Relay1.off()  #Turn relay off
    OB_LED.off()
    print("OFF")
    time.sleep(3)
