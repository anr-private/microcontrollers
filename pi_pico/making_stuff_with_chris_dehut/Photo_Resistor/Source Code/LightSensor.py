# Use a photoresistor to determine if it is day or night or inbetween
# The example photoresistor is initially measured using a meter

# Bright room light is     5.5k Ohms       58000 analog reading
# Ambient room light is   27.0k Ohms       36000 analog reading
# Dark room is            65.0k Ohms       18000 analog reading
# Pitch black room         1.2m Ohms        1750 analog reading

import machine
import utime

PhotoResistor = machine.ADC(1)  #setup analog reading on ADC

while True:
    Bright_Level = PhotoResistor.read_u16()
    
    if Bright_Level > 55000 :
        print("Wear Sunglasses Bright  @",Bright_Level)
    elif Bright_Level > 35000:
        print("Comfortable Viewing    @",Bright_Level)
    elif Bright_Level > 1000:
        print("Get a flashlight       @",Bright_Level)
    else:
        print("Get MANY Flashlights   @",Bright_Level)
    utime.sleep(.1)
    
    