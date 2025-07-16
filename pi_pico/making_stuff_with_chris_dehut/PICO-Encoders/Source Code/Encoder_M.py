#Main example program using class Encoder_R from library Encoder_C

from Encoder_C import R_Encoder
import time

last_Enc_Counter_1 = 0      #Preset variables for first encoder 
Enc_Counter_1 = 0
Last_Qtr_Cntr_1 = 0
Qtr_Cntr_1 = 0
error_1 = 0


last_Enc_Counter_2 = 0    #Preset variables for second encoder
Enc_Counter_2 = 0
Last_Qtr_Cntr_2 = 0
Qtr_Cntr_2 = 0
error_2 = 0


Enc_1 = R_Encoder(15,14)  #Instaniate the encoder class for encoder 1
Enc_1.DisplayPins()       #Use the method to show state of channels/pins
Enc_1.Reset_Counter()     #Reset counter to a known value

Enc_2 = R_Encoder(12,11)  #Same as above but for encoder 2
Enc_2.DisplayPins()
Enc_2.Reset_Counter()

Enc_1_SW = machine.Pin(13,machine.Pin.IN,machine.Pin.PULL_UP) #Configure pin for push button switch
Enc_1_SW_State = "UP" #preset the state of the push button switch

# Main program loop which runs continuously
while True:
    time.sleep(.01)                # Sleep for a moment to slow things down.

    Qtr_Cntr_1 = round(Enc_1.Enc_Counter / 4)   #Reduce to 'Dentent' count      
    if Qtr_Cntr_1 != Last_Qtr_Cntr_1:           #Only do something if the counter changed 
        print(Qtr_Cntr_1)
        last_Enc_Counter_1 = Enc_1.Enc_Counter  #Update counters
        Last_Qtr_Cntr_1 = Qtr_Cntr_1

    if (Enc_1_SW.value() == True) and (Enc_1_SW_State == "DOWN"):   #Handle the switch input - detect UP or DOWN position
        Enc_1_SW_State = "UP"
        print("Switch is UP")
    elif (Enc_1_SW.value() == False) and (Enc_1_SW_State == "UP"):
        Enc_1_SW_State = "DOWN"
        print("Switch is DOWN")
        

    Qtr_Cntr_2 = round(Enc_2.Enc_Counter / 4)     #May or may not want to divide by 4 for motor shaft encoder   
    if Qtr_Cntr_2 != Last_Qtr_Cntr_2:             #Only do something if the counter changed
        #print(Enc_1.Enc_Counter, Qtr_Cntr_1, Enc_2.Enc_Counter, Qtr_Cntr_2)
        print(Qtr_Cntr_1, Qtr_Cntr_2)
        last_Enc_Counter_2 = Enc_2.Enc_Counter    #Update counters
        Last_Qtr_Cntr_2 = Qtr_Cntr_2
       
