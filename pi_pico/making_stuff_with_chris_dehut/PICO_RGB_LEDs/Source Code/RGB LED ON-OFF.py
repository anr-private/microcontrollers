# RGB Color LED
# Full ON OFF control

#Wire according to information provided on associated video on YouTube

#Connect Red leg to GP26 through a 68 ohm resistor
#Connect Green leg to GP27 through a 10 ohm resistor
#Connect Blue leg to GP28 through a 10 ohm resistor

#NOTE - COMMON CATHODE LED USED

#load libraries
import machine
import utime

#Configure outputs for each LED
R_LED = machine.Pin(26,machine.Pin.OUT)  
G_LED = machine.Pin(27,machine.Pin.OUT)  
B_LED = machine.Pin(28,machine.Pin.OUT)  

Pause = 2
print("Ready, Set, GO!")
while True:
        R_LED.value(0)     #Turn all Off
        G_LED.value(0)    
        B_LED.value(0)    

    
        R_LED.value(1)     #Turn ON LED
        utime.sleep(Pause) #Pause 
        R_LED.value(0)     #Turn OFF LED
        G_LED.value(1)    
        utime.sleep(Pause) 
        G_LED.value(0)    
        B_LED.value(1)    
        utime.sleep(Pause) 
        B_LED.value(0)        
        
        # Red and green on at same time
        R_LED.value(1)     
        G_LED.value(1)    
        utime.sleep(Pause) 
        G_LED.value(0)    
        R_LED.value(0)    
        utime.sleep(Pause)
        
        # Red and blue on at same time
        R_LED.value(1)     
        B_LED.value(1)    
        utime.sleep(Pause) 
        B_LED.value(0)    
        R_LED.value(0)    
        utime.sleep(Pause)     
        
        # Blue and green on at same time
        B_LED.value(1)     
        G_LED.value(1)    
        utime.sleep(Pause) 
        G_LED.value(0)    
        B_LED.value(0)    
        utime.sleep(Pause)
       
        R_LED.value(0)     #Turn all Off
        G_LED.value(0)    
        B_LED.value(0)    
      
        utime.sleep(Pause)  #pause a little while to indicate end
 