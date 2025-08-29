# ANR version of hello world
#
# Works with PCF8754T LCD displays  ('non-waveshare')
# The LCD is powered from a separate power supply - 5 Volts.
# Various LCDs that were tried either do not work on much less than 4.5 v or
# are unreliable / dim / etc esp at the 3.3v as used by the Pico.
#
# SETUP:
#  Connect the LCD's I2C Clock and Data (SDA, SCL) lines to the pins specified in the code below.
#  Connect the LCD's negative power input to 'external' 5V power supply and to the negative/GND
#   of the Pico. The I2C lines use the GND as the return path for those signals.
#  Connect positive of the external 5v supply to the positive pin of the LCD.
#  
import utime
from machine import Pin, SoftI2C
from lib_lcd1602_2004_with_i2c import LCD

print(f"Hello World init: try to locate the LCD device...")
#scl_pin = 26
#sda_pin = 27
scl_pin = 5
sda_pin = 4
lcd = LCD(SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000))
print(f"Hello World init: ... located the LCD device...")

# Works with 2 line and 4 line by 16 chars LCDs
NUM_ROWS = 2
#NUM_ROWS = 4

print(f"HELLO WORLD TEST FOR PCF8754T style LCD displays.  num_rows={NUM_ROWS}")
print(f"   Pins:  DATA={sda_pin}  CLOCK={scl_pin}  I2C-addr={'see-the-driver-code'}")

try:
    print("Use ^C to terminate the program and perform cleanup on the LCD device.")
    while True:
        if NUM_ROWS == 2:
            lcd.puts("Hello, World ANR")
            lcd.puts("Hello World row2", x=0, y=1)
        elif NUM_ROWS == 4:
            lcd.puts("Hello World ANR", x=0, y=0)
            lcd.puts("Hello World ANR row2", x=0, y=1)
            lcd.puts("Hello World ANR row3", x=0, y=2)
            lcd.puts("Hello World ANR row4", x=0, y=3)
        else:
            print(f"***ERROR*** Unexpected NUM_ROWS={NUM_ROWS}")
            
        utime.sleep(1)
        
        if NUM_ROWS == 2:
            lcd.puts("      ")  # erases just the 'Hello'
            #lcd.clear()     # erases whole screen
        elif NUM_ROWS == 4:
            lcd.puts("      ", x=0, y=0)
            lcd.puts("Hello ..... ANR row2", x=0, y=1)
            lcd.puts("Hello World ... row3", x=0, y=2)
            lcd.puts("Hello +++++ === row4", x=0, y=3)
            #lcd.clear()
        else:
            print(f"***ERROR*** Unexpected NUM_ROWS={NUM_ROWS}")
        
        utime.sleep(0.25)
except (KeyboardInterrupt):
    lcd.clear()
    del lcd
print("... end of hello world ANR version ...")

### end ###
