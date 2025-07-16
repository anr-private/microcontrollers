# Your PICO can make annoying sounds using an inexpesnsive buzzer
# The buzzer used in this demo is:
# Adafruit  Buzzer 5V - Breadboard friendly Product ID: 1536
# With power applied it will oscilate at 2kHz making it very easy to control
#

import machine
import utime

buzzer = machine.Pin(15, machine.Pin.OUT)

buzzer.value(1)
utime.sleep(1)
buzzer.value(0)
print("All done folks!")



