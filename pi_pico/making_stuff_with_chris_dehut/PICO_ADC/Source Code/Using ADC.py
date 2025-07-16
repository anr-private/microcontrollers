#Reading Analaog values on the Raspberry Pi PICO
#Read and display analog value generated with a potentiometer
'''
PICO has a ADC channels
    PIN31 = GP26 = ADC0
    PIN32 = GP27 = ADC1
    PIN38 = GP28 = ADC2
    Internal Temp Sensore = ADC3
    
    ADC is 12 bit resolution internal to the RP2040 meaning a range of 0 ~ 4095
    ADC value from Micropython is 16 bits meaning a range of 0 ~ 65535
    Micropython maps the 12 bit range to 16 bits for ease of use on various micros
    
    10k LINEAR taper pots provide good results
    (Log or Audio pots output a 'curve' range as opposed to linear range)
    
    connect 3.3V out to one of the end terminals
    connect GND  other end terminal
    connect Wiper (middle terminal) to pin 31/ADC0
'''

import machine
import utime

POT = machine.ADC(0)  #setup analog reading on ADC 0
while True:
    A_Val = POT.read_u16()
    print(A_Val)   
    utime.sleep(.1)
    
    
    
    
    