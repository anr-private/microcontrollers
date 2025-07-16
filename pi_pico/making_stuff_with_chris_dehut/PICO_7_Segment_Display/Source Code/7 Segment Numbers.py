# 7 Segment LED display - Common cathode
# Function that displays number 0-9 with or without the decimal point

#ALSO REQUIRED!!!
#220 ohm resistor for each Segment
#Wire according to information provided on associated video on YouTube

#Check the data sheet for your display, adjust connections as needed
#Connect Common Cathode pins to GND pins on PICO
#Connect the segment LEDS to these pins

#A_LED  to pin 21/GP16
#B_LED  to pin 22/GP17
#DP_LED to pin 25/GP19
#C_LED  to pin 26/GP20
#D_LED to pin 16/GP12
#E_LED to pin 17/GP13
#G_LED to pin 19/GP14
#F_LED to pin 20/GP15

#load libraries
import machine
import utime

A_LED  = machine.Pin(16,machine.Pin.OUT)  #Create an output pin for each segment
B_LED  = machine.Pin(17,machine.Pin.OUT)  
DP_LED = machine.Pin(19,machine.Pin.OUT)  
C_LED  = machine.Pin(20,machine.Pin.OUT)  
D_LED  = machine.Pin(12,machine.Pin.OUT)  
E_LED  = machine.Pin(13,machine.Pin.OUT)  
G_LED  = machine.Pin(14,machine.Pin.OUT)  
F_LED  = machine.Pin(15,machine.Pin.OUT)  

def Clear_Display():
    A_LED.value(0)       #Turn OFF all LED segments
    B_LED.value(0)       
    DP_LED.value(0)       
    C_LED.value(0)       
    D_LED.value(0)       
    E_LED.value(0)       
    G_LED.value(0)       
    F_LED.value(0)       

def Show_Number(Number, DecimalPoint):
    Clear_Display()
    if   Number == "0":
        A_LED.value(1)       #Turn ON needed LED segments
        B_LED.value(1)       
        C_LED.value(1)       
        D_LED.value(1)       
        E_LED.value(1)       
        F_LED.value(1)       
    elif Number == "1":
        B_LED.value(1)       
        C_LED.value(1)       
    elif Number == "2":
        A_LED.value(1)
        B_LED.value(1)       
        G_LED.value(1)       
        E_LED.value(1)       
        D_LED.value(1)            
    elif Number == "3":
        A_LED.value(1)
        B_LED.value(1)       
        G_LED.value(1)       
        C_LED.value(1)       
        D_LED.value(1)             
    elif Number == "4":
        B_LED.value(1)       
        G_LED.value(1)       
        C_LED.value(1)                   
        F_LED.value(1)       
    elif Number == "5":
        A_LED.value(1)     
        F_LED.value(1)       
        G_LED.value(1)       
        C_LED.value(1)       
        D_LED.value(1)              
    elif Number == "6":
        A_LED.value(1) 
        F_LED.value(1)       
        E_LED.value(1)       
        D_LED.value(1)       
        C_LED.value(1)       
        G_LED.value(1)             
    elif Number == "7":
        A_LED.value(1)
        B_LED.value(1)       
        C_LED.value(1)             
    elif Number == "8":
        A_LED.value(1)
        B_LED.value(1)              
        C_LED.value(1)       
        D_LED.value(1)       
        E_LED.value(1)       
        G_LED.value(1)       
        F_LED.value(1)       
    elif Number == "9":
        A_LED.value(1)
        B_LED.value(1)             
        C_LED.value(1)              
        G_LED.value(1)       
        F_LED.value(1)       
    if DecimalPoint == ".":  #Add decimal point if needed  
        DP_LED.value(1)       
      

print("Ready, Set, GO!")
Seq_Del = 1
while True:
    Show_Number("0","")      #call function to display a number and decimal point
    utime.sleep(Seq_Del)     #Pause a bit
    Show_Number("1","")       
    utime.sleep(Seq_Del) 
    Show_Number("2","")       
    utime.sleep(Seq_Del) 
    Show_Number("3","")       
    utime.sleep(Seq_Del) 
    Show_Number("4","")       
    utime.sleep(Seq_Del) 
    Show_Number("5","")       
    utime.sleep(Seq_Del) 
    Show_Number("6","")       
    utime.sleep(Seq_Del) 
    Show_Number("7","")       
    utime.sleep(Seq_Del) 
    Show_Number("8","")       
    utime.sleep(Seq_Del) 
    Show_Number("9","")       
    utime.sleep(Seq_Del) 
    Show_Number("9",".")       
    utime.sleep(Seq_Del) 
    
    utime.sleep(1) 
    
