# main_Hello_World_ANR_fancy.py
#
# ANR version of hello world - fancier version
#
# Works with PCF8754T LCD displays  ('non-waveshare')
# such as QAPASS LCDs.
# Works with 16x2 and 16x4  (2 or 4 line by 16 chars wide).
#
# The LCD is powered from a separate power supply - 5 Volts.
# Various LCDs that were tried either do not work on much less than 4.5 v or
# are unreliable / dim / etc esp at the 3.3v as used by the Pico.
#
# SETUP:
#  Connect the LCD's I2C Clock and Data (SDA, SCL) lines to the pins specified in the code below.
#  Connect the LCD's negative power input (GND) to 'external' 5V power supply and to the negative/GND
#   of the Pico. The I2C lines use the GND as the return path for those signals.
#  Connect positive of the external 5v supply to the positive pin of the LCD 
#    aka VCC.
#  LCD VCC  - to 5 volt supply positive terminal (separate from Pico's pins/supply)
#  LCD GND  - to 5 volt supply negative terminal AND a GND pin on PICO
#  LCD SCL  - to SCL GPIO pin on Pico (ex: pin 1  -- alternate is GPIO 5, etc).
#  LCD SDA  - to SDA GPIO pin on Pico (ex: pin 0  -- alternate is GPIO 4, etc).
#  **** NOTE ****
#  Powering the LCD using 5v likely means the LCD will run its I2C at 5v, which is too
#  high for the Pico GPIO I2C (3.3v max). Seems to work but will probably damage the Pico.

import utime
from machine import Pin, SoftI2C
from lib_lcd1602_2004_with_i2c import LCD

# SoftI2C is software I2C - works on ANY GPIO pins(!)
# these are  GPIO pin numbers  (NOT physical pins)
##scl_pin = 26
##sda_pin = 27
###scl_pin = 5
###sda_pin = 4
sda_pin = 2
scl_pin = 3


def locate_the_lcd():
    print(f"  init: try to locate the LCD device...")
     # SoftI2C is software I2C - works on ANY GPIO pins(!)
     # 100K is default freq.  Can go higher ex 400K
    lcd = LCD(SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000))
    
    if lcd:
        print(f"Hello World init: ... located the LCD device...")
    else:
        print(f" **ERROR**  failed to locate the LCD device!")
    return lcd

# Works with 2 line and 4 line by 16 chars LCDs
NUM_ROWS = 2
#NUM_ROWS = 4

def just_show_some_hello_lines(lcd, secs_total=9999999):
    secs_so_far = 0
    while secs_so_far < secs_total:
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
            
        utime.sleep(1); secs_so_far += 1
        
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
        
        utime.sleep(1); secs_so_far += 1
    
def OLD_show_star_running(lcd, secs_total=999999):
    row = 0
    col = 0
    prev_row = row
    prev_col = col
    secs_so_far = 0
    while secs_so_far < secs_total:
        lcd.puts(" ", prev_row, prev_col)
        lcd.puts("*", row, col)
        
        #utime.sleep(1) ###0.25)
        utime.sleep(0.2); secs_so_far += 0.2

        prev_row = row
        prev_col = col
        col += 1
        if col >= 16:
            col = 0
            row += 1
            if row >= 2:
                row = 0
                
def show_star_running(lcd, secs_total=999999):
    row = 0
    col = 0
    prev_row = row
    prev_col = col
    start_time = utime.time()
    secs_so_far = 0
    while secs_so_far < secs_total:
        
        # do top row
        for row in range(2):
            prev_col = 0
            for col in range(16):
                lcd.puts(" ", row, prev_col)
                lcd.puts(f"{row}", row, col)
                prev_col = col
                utime.sleep(0.2);
            lcd.puts(" ", row, col)
            
        secs_so_far = utime.time() - start_time
            
                
def show_alternating_rows_of_stars(lcd, secs_total=999999):
    # fewer calls to lcd.puts() - runs faster
    spaces = " " * 16
    stars  = "*" * 16
    lcd.puts(spaces, 0, 0)
    lcd.puts(spaces, 1, 0)

    start_secs = utime.time()
    print(f"  start secs {start_secs}")
    secs_so_far = 0
    stars_row = 0
    while secs_so_far < secs_total:
        if stars_row == 0:
            lcd.puts(stars,  0, 0)
            lcd.puts(spaces, 1, 0)
        else:
            lcd.puts(stars,  1, 0)
            lcd.puts(spaces, 0, 0)
        stars_row += 1
        if stars_row >= 2:
            stars_row = 0
        ###print(f"  stars_row={stars_row}")
        
        utime.sleep(0.05)
        secs_so_far = utime.time() - start_secs
        print(f"  secs so far {secs_so_far}    secs total {secs_total}")
            

def main():
  print(f"Hello World ANR FANCY version.  SCLock=GPIO{scl_pin} SDAta=GPIO{sda_pin}")

  print(f"HELLO WORLD TEST FOR PCF8754T style LCD displays.  num_rows={NUM_ROWS}")
  print(f"   Pins:  DATA={sda_pin}  CLOCK={scl_pin}  I2C-addr={'see-the-driver-code'}")

  lcd = locate_the_lcd()
  
  try:
    print("Use ^C to terminate the program and perform cleanup on the LCD device.")
    #just_show_some_hello_lines(lcd, 5)
    show_star_running(lcd,6)
    #show_alternating_rows_of_stars(lcd, 5)
  except (KeyboardInterrupt):
    lcd.clear()
    del lcd
  #         1234567890123456
  lcd.puts("END hello FANCY!", 0,0)
  lcd.puts("++_++__++__++_++", 1,0)
  #         1234567890123456
  print("... end of hello world ANR FANCY version ...")

main()

### end ###
