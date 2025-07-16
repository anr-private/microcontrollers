# 7 Segment 4 Digit Code Example
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

def Marker_Code():
    A_LED.value(1)       #Turn ON needed LED segments for marker 
    D_LED.value(1)       #3 horizontal segments
    G_LED.value(1)       
    


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
      

def Four_Digit_Code(Code):
    T = 3                   #Counter for 3 iteration loop to flash marker code
    while T > 0:            #start loop
        Clear_Display()     #Turn all segments off
        utime.sleep(.05)    #brief delay
        Marker_Code()       #Turn on marker code
        utime.sleep(.05)    #brief delay
        T -= 1              #Decrement loop counter flag
    Clear_Display()         #Turn off all segments
    utime.sleep(.1)         #delay 100 milliseconds
    
    if len(Code) < 4:       #Check to make sure code is 4 characters long
        print("Code must be 4 characters long!")
    else:
        for c in Code:        #Setup loop to get each character in Code
            Show_Code = c     #Assign it to local variable for readability
            Show_Number(Show_Code,"") #Show number but no Decimal Point
            utime.sleep(1)            #Sleep 1 second then show next character



print("Ready, Set, GO!")
Seq_Del = 1
while True:
    
    Code = "1961"          #Create the code as a string of 4 numeric digits
    Four_Digit_Code(Code)  #Call the function to display the Code
    utime.sleep(1)         #Wait a second, then show next digit    
    
