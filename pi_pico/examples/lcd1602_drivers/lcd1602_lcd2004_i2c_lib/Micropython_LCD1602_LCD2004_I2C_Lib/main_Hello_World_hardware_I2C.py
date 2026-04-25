# -*- coding: utf-8 -*-
###__author__ = 'LiYuanhe'
# main_Hello_World_hardware_I2C.py
#
# Using hardware I2C to talk to LCD

import time
import sys
from machine import Pin
from lib_lcd1602_2004_with_i2c import LCD
#scl_pin = 26
#sda_pin = 27
###scl_pin = 5
###sda_pin = 4
sda_pin = 2
scl_pin = 3

i2c = machine.I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100_000)

print(i2c)

lcd = LCD(i2c)

ctr = 0
while 1:
    print(f"  ctr={ctr}")
    lcd.puts(f"Hello, World! {ctr}")
    lcd.puts("Hello World row2", x=0, y=1)
    ctr += 1
    time.sleep(1)
    
###
