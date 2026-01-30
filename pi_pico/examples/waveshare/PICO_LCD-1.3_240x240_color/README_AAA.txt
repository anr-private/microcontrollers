1.3" LCD Display - Waveshare

Box labeled:
 X002XHTHXF
 1.3inch LCD Display ...and MicroPython Demo
 Pico-LCD-1.3
 NEW
 Made in China

website:
https://www.waveshare.com/wiki/Pico-LCD-1.3?srsltid=AfmBOoocDlT5yD9kTegQccgT-L3-8p5tsdxAcL8OidI4xBZrg4GLzVjm
https://www.waveshare.com/wiki/Pico-LCD-1.3

Python Download
  PICO/ 
    Has Rp2...v.1.15.7z file - use script unzip_7z.sh to un-7z it to get the UF2 file
    Install UF2 file on PICO as usual.
  PICO2/
    (not yet attempted - zip file does unzip to a uf2)

=== SPECs  ====================================

  Driver: ST7789
  240 × 240 resolution, IPS screen, 65K RGB colors
  SPI interface, requires minimal IO pins
  1 x joystick and 4 x user buttons for easy interaction
  Operating voltage: 2.6~5.5V
  Communication interface: 4-wire SPI
  Display size: 23.40 × 23.40mm
  Pixel size: 0.0975 × 0.0975mm
  Dimensions: 52.00 × 26.50mm

=== ONLINE Sources  ============================

https://www.instructables.com/WS-Pico-13-IPS-LCD-240x240-Display-Workout/
  See pi_pico_1.3in_LCD_240x240_PINS.png
  See JPG_images_of_code/ for images of code snips from this site.

  GP15  A button       GP2  Joystick Up
  GP17  B button       GP18 Joystick Down
  GP19  X button       GP16 Joystick Left
  GP21  Y button       GP20 Joystick Right
                       GP3  Joystick Center button pressed
  GPIO available: 0, 1 ,4, 5 ,6, 7, 14, 22, 26, 27, 28.
   These include I2C pins for connecting sensors/actuators and the 
   3 ADC pins for voltages/potentiometers.

  There are several screen captures (PNGs).
  They don't quite match the actual code in PY files.
  There is a printstring() method that is similar to LCD.text:
     printstring("Halted", 80, 100,  2,0,0, colour(255,0,0))
  The actual code has this instead:
     LCD.text("Halted", 95, 115, colour(255,0,0))



https://spotpear.com/index/study/detail/id/795.html
 A lot of this is duplicated from the waveshare.com site.
 The ST7789VW is a single-chip controller/driver for 262K-color, 
  graphic type TFT-LCD. It consists of 240 source line and 320 gate 
  line driving circuits. The resolution of this LCD is 240 (H) RGB x 240 (V), 
  it supports horizontal mode and vertical mode, and it doesn't use all the 
  RAM of the controller.
 This LCD accepts 8-bits/9-bits/16-bits/18-bits parallel interface, that are 
  RGB444, RGB565, RGB666. The color format used in demo codes is RGB565.

   e-Paper    Pico    Description
   --------   -----   ---------------------------
     VCC      VSYS    Power Input
     GND      GND     GND
     DIN      GP11    MOSI pin of SPI, slave device data input
     CLK      GP10    SCK pin of SPI, clock pin
     CS       GP9     Chip selection of SPI, low active
     DC       GP8     Data/Command control pin (High for data; Low for command)
     RST      GP12    Reset pin, low active
     BL       GP13    Backlight control
     A        GP15    User button A
     B        GP17    User button B
     X        GP19    User button X
     Y        GP21    User buttonY
     UP       GP2     Joystick-up
     DOWN     GP18    Joystick-down
     LEFT     GP16    Joystick-left
     RIGHT    GP20    Joystick-right
     CTRL     GP3     Joystick-center button pressed
  






=== LOG of activities  ======================================

2026-1-29  GAVE UP trying to get it to work
 - tried 2 different ssd1306.py libraries
 - does not look like the device is available any longer(?)
 - tried i2_scan_tool.py - no I2C device found

2026-1-29 NOT AN I2C DEVICE. PROBABLY NOT A SSD 1306.
Got a working demo in
  ~/git/microcontrollers/pi_pico/examples/waveshare/PICO_LCD-1.3_240x240_color/PICO
It uses SPI not I2C.
Resolution is 240x240 


###

