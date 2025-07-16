# RGB Color LED
# FADE on and OFF using PWM control

#Wire according to information provided on associated video on YouTube

#Connect Red leg to GP26 through a 68 ohm resistor
#Connect Green leg to GP27 through a 10 ohm resistor
#Connect Blue leg to GP28 through a 10 ohm resistor

#NOTE - COMMON CATHODE LED USED


#load libraries
import machine
import utime

#Configure outputs as PWM for each LED
R_LED = machine.PWM(machine.Pin(26))  
R_LED.freq(1000)  # A good frequency to avoid flicker
G_LED = machine.PWM(machine.Pin(27))  
G_LED.freq(1000)  
B_LED = machine.PWM(machine.Pin(28))  
B_LED.freq(1000)  


Fade_Rate = .0001  #Time delay at each step change in PWM Duty
V = 0 # Variable holding the duty for the PWM signal
print("Ready, Set, GO!")
while True:

    R_LED.duty_u16(0) #Turn all LEDs off        
    G_LED.duty_u16(0)        
    B_LED.duty_u16(0)         
    utime.sleep(1)  #pause a little while to indicate end
      

    #Red LED
    while V <= 65535:          #V will be the duty cycle for PWM - Range is 0(off) to 65535(Bright)
        V += 2                 #Stepping by 2 through the range for smooth transitions 
        R_LED.duty_u16(V)      #Fade LED on by change the PWM duty cycle
        utime.sleep(Fade_Rate) #Ramp up duty delaying this much time per increment
    while V > 0:               #Fade out LED
        V -= 2
        R_LED.duty_u16(V)         
        utime.sleep(Fade_Rate)  

    
    #Green LED
    while V <= 65535:          
        V += 2                  
        G_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        G_LED.duty_u16(V)         
        utime.sleep(Fade_Rate)  

    #Blue LED
    while V <= 65535:          
        V += 2                 
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        B_LED.duty_u16(V)         
        utime.sleep(Fade_Rate)  


    #Red and Green LEDs
    while V <= 65535:          
        V += 2                  
        R_LED.duty_u16(V)        
        G_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        R_LED.duty_u16(V)         
        G_LED.duty_u16(V)        
        utime.sleep(Fade_Rate)  


    #Red and Blue LEDs
    while V <= 65535:          
        V += 2                  
        R_LED.duty_u16(V)        
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        R_LED.duty_u16(V)         
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate)  


    #Green and Blue LEDs
    while V <= 65535:          
        V += 2                  
        G_LED.duty_u16(V)        
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        G_LED.duty_u16(V)         
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate)  



    #Red Green and Blue LEDs
    while V <= 65535:          
        V += 2                  
        R_LED.duty_u16(V)        
        G_LED.duty_u16(V)        
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate) 
    while V > 0:
        V -= 2
        R_LED.duty_u16(V)         
        G_LED.duty_u16(V)        
        B_LED.duty_u16(V)        
        utime.sleep(Fade_Rate)
        
    utime.sleep(1)  #pause a little while to indicate end

