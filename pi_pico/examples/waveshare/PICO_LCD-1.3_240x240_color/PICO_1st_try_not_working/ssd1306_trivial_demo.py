#
#
# SRC:  https://github.com/stlehmann/micropython-ssd1306/blob/master/README.md
# This shows an example usage on an ESP32 board with an SSD1306 display 
# with an resolution of 128x32 pixels. The display is connected via I2C. 
# On the ESP32 the I2C pins are: SDA: 23, SCL: 22.

#First we set up the I2C bus on our ESP32 and scan for devices.

from machine import Pin
import utime
import os
import ssd1306
from ssd1306 import SSD1306_I2C

print("=== Trivial demo of SSD1306 1.3 inch LCD display   =========")

print(f"ssd1306 library is {ssd1306}")

# First we set up the I2C bus on our ESP32 and scan for devices.
# Expected output is 60  0x3C  the address of the device
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
print("   Scan for the device:")
i2c.scan()
print("     after scanning")
utime.sleep(5)  # Pause for 0.5 seconds

# Create an object for our OLED display.
#                 width, hgt, device
oled = SSD1306_I2C(128, 32, i2c)

# This fills the whole display with white pixels. To clear the display do:
oled.fill(1)
oled.show()

# clear the display
oled.fill(0)
oled.show()

# write some text
oled.text('Hello', 0, 0)
oled.text('World', 0, 10)
oled.show()

### end ###
