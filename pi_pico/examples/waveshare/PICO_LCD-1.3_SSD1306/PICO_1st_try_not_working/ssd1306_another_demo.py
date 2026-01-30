# ssd1306_another_demo.py
# Found using google: "example of ssd1306 in micropython for pi pico"

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# --- Configuration ---
# Set the display dimensions (128x64 is common, adjust if different)
WIDTH = 128
HEIGHT = 64

# Configure I2C communication
# Using I2C(0) with GP16 for SDA and GP17 for SCL
### ORIG  i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Initialize the SSD1306 display
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# --- Display Content ---

# Clear the display buffer
oled.fill(0)

# Display text at coordinates (x, y)
oled.text("Hello, World!", 0, 0)
oled.text("Raspberry Pi Pico", 0, 10)
oled.text("MicroPython", 0, 20)

# Update the display with the buffer's contents (vital step)
oled.show()

# Optional: Add a pause before clearing again
time.sleep(2)

# Clear the display and show a new message
oled.fill(0)
oled.text("Display Cleared", 0, 0)
oled.show()
