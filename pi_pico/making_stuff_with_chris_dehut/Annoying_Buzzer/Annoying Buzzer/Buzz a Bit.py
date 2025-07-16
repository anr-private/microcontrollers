# Your PICO can make annoying sounds using an inexpesnsive buzzer
# The buzzer used in this demo is:
# Adafruit  Buzzer 5V - Breadboard friendly Product ID: 1536
# With power applied it will oscilate at 2kHz making it very easy to control
#

import machine
import utime

buzzer = machine.Pin(15, machine.Pin.OUT)


def Buzz_a_Bit():
    print("DANGER")
    for i in range(15):
        buzzer.toggle()
        utime.sleep(.025)
    for i in range(5):
        buzzer.toggle()
        utime.sleep(.1)
    utime.sleep(.2)
    for i in range(15):
        buzzer.toggle()
        utime.sleep(.025)
    for i in range(5):
        buzzer.toggle()
        utime.sleep(.1)

Buzz_a_Bit()
print("All done folks!")



