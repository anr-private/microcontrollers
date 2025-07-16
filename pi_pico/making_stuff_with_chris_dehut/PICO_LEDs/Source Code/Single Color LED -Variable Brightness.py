# Simple Single Color LED
# Step brightness level of LED using PWM control    led.duty_u16(float)  ANR

# pin 4/GP2 for LED output

#ALSO REQUIRED!!!
#120 ohm resistor
#Red LED (not high power)
#Wire according to information provided on associated video on YouTube

#load libraries
import machine
import utime

#Configure output as PWM
LED = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
LED.freq(1000)  # A good frequency to avoid flicker

print("Ready, Set, GO!")
Max_Duty = 65535
while True:
    D_V = round(0 * Max_Duty)
    LED.duty_u16(D_V)        #Set the duty cycle of the PWM cycle to value in D_V
    utime.sleep(.5)
    
    D_V = round(.25 * Max_Duty)  #25%
    LED.duty_u16(D_V)        
    utime.sleep(.5)
    
    D_V = round(.50 * Max_Duty) #50%
    LED.duty_u16(D_V)        
    utime.sleep(.5)
    
    D_V = round(.75 * Max_Duty) #75%
    LED.duty_u16(D_V)        
    utime.sleep(.5)
    
    D_V = round(1 * Max_Duty)   #100%
    LED.duty_u16(D_V)        
    utime.sleep(.5)
    

