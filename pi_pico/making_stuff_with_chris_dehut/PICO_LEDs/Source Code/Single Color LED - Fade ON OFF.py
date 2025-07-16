# Simple Single Color LED
# FADE on and OFF using PWM control

#ALSO REQUIRED!!!
#120 ohm resistor
#Red LED (not high power)
#Wire according to information provided on associated video on YouTube
#use pin 4/GP2 for LED output

#load libraries
import machine
import utime

#Configure output as PWM
LED = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
LED.freq(1000)  # A good frequency to avoid flicker

Fade_Rate = .0001  #Time delay at each step change in PWM Duty
V = 0 # Variable holding the duty for the PWM signal
print("Ready, Set, GO!")
while True:
    while V <= 65535:          #V will be the duty cycle for PWM - Range is 0(off) to 65535(Bright)
        V += 3                 #Stepping by 2 through the range for smooth transitions 
        LED.duty_u16(V)        #Fade LED on by change the PWM duty cycle
        utime.sleep(Fade_Rate) #Ramp up duty delaying this much time per increment
    print("Full ON")
    utime.sleep(.1)
    while V > 0:
        V -= 3
        LED.duty_u16(V)         
        utime.sleep(Fade_Rate)  
    print("Full OFF")
    utime.sleep(.1)


