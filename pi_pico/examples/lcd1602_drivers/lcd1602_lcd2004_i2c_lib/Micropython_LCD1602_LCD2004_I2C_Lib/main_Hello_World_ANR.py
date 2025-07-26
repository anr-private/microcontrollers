# ANR version of hello world

import utime
from machine import Pin, SoftI2C
from lib_lcd1602_2004_with_i2c import LCD
#scl_pin = 26
#sda_pin = 27
scl_pin = 5
sda_pin = 4
lcd = LCD(SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000))

try:
    print("Use ^C to terminate the program and perform cleanup on the LCD device.")
    while True:
        lcd.puts("Hello, World!")
        utime.sleep(1)
        lcd.puts("      ")  # erases just the 'Hello'
        #lcd.clear()     # erases whole screen
        utime.sleep(0.25)
except (KeyboardInterrupt):
    lcd.clear()
    del lcd
print("... end of hello world ANR version ...")

### end ###
