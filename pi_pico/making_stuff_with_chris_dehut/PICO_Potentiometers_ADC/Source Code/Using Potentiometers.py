#Interfacing potentiometers to the PICO
#Read and display analog value generated with two potentiometers
'''
PICO has 3 ADC channels
    PIN31 = GP26 = ADC0
    PIN32 = GP27 = ADC1
    PIN38 = GP28 = ADC2
    Internal Temp Sensor = ADC3
    
    ADC is 12 bit resolution internal to the RP2040 meaning a range of 0 ~ 4095
    ADC value from Micropython is 16 bits meaning a range of 0 ~ 65535
    Micropython maps the 12 bit range to 16 bits for ease of use on various micros
    
    Wire up according to the fritzing diagram refernecd in the video's description
'''

import machine
import time

Rot_POT = machine.ADC(0)  #setup analog reading on ADC 0 for 10 rotary pot
Lin_POT = machine.ADC(1)  #setup analog reading on ADC 1 for 30k linear pot
Trm_POT = machine.ADC(2)  #setup analog reading on ADC 1 for 1K Trimmer pot

while True:
    R_Val = Rot_POT.read_u16()
    L_Val = Lin_POT.read_u16()
    T_Val = Trm_POT.read_u16()
    print("Rotary 10k =",R_Val,"  Linear 30k=",L_Val,"   Trimer 1k=",T_Val)   
    time.sleep(.1)
    
    
    
    
    