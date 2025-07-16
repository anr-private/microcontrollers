'''
Humidity Sensor, HIH-4030
Analog output

Convert sensor reading into Relative Humidity (RH%) 
using equation from Datasheet and Sparkfun's website

See notes at bottom for reconditioning sensor.
'''

import machine
import utime

Humidity_Sensor = machine.ADC(2)  #setup analog reading on ADC 2
while True:
    Reading = Humidity_Sensor.read_u16()         #Read the value from the sensor - in range of 0 to 65535
    VOUT= (Reading  * 3.3 / 65535)               #Calculate Reading into volts - from datasheet
    RH = ((VOUT / (.0062 * 5.1)) - 25.81)        #Calculate the approxiimate RH - from datasheet
    Temp_C = 20                                  #Using average temp in house at 20C = 68F
                                                 #substitute with temp sensor reading
    A_RH = (RH / (1.0546 - (0.00216 * Temp_C)))  #Calc Actual RH - from datasheet

    print("Actual Relative Humidity is: ",A_RH,"%")
    utime.sleep(.25)
    
    
    
'''
Humidity Sensors make use of a conductive polymer to measure relative humidity. If that polymer
gets too dry (or over-saturated) the sensor won't function properly, but that can be reversed.
Whenever we use one of these sensors on our designs, we put them through a re-conditioning
procedure to ensure that they keep their factory calibration. If you expose your sensor to a really dry
environment for a prolonged period of time (or saturate it with water) you may have to run it through
the same process.
The datasheet for the SHT15 recommends baking at 100-105°C and < 5%RH for 10
hours followed by re-hydration at 20-30°C and ~ 75%RH for 12 hours.
The datasheet for the HIH6130 recommends re-hydration at room temperature under
ambient conditions (>50 %RH) for a minimum of five hours.
For more information on the re-conditioning procedures, check out the datasheets (which can be
found on the product page)
'''

    
    
    
    
    