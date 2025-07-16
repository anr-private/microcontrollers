'''
LM35 Temperature Sensor
The LM35 is an accurate 0 to 150C sensor, rated at .01 V / degree C
To read negative temps, a negative voltage source is required.
If you need to read negative voltages better sensors are available.

We will supply 5V to the sensor for power as a minimum of 4 is required.
If the readings are going to be less than 330C (626F) your PICO will be safe.

The temp is averaged over 10 samples measure .1 seconds apart.
Both Celcius and Fahrenheit are calcuated in the function.
'''


import machine
import utime

LM35 = machine.ADC(0)  #setup analog reading on ADC
Cal_Offset = -550      #Calibration offset value
                       #Determined from practical testing

def Compute_Temp(Avg_A):
    LM35_A = Avg_A + Cal_Offset           #Add Calibration Adjustment
    LM35_V = LM35_A * .00005              #Convert analog reading to volts
    Tmp_C  = round((LM35_V * 100),1)      #Convert volts to temp celcius
    Tmp_F  = round((Tmp_C * 1.8 + 32),1)  #Convert Tmp_C to Tmp_F
    return Tmp_C, Tmp_F                   #Return Temps


Samples = 0            #Variable holds all samples
Num_Samples = 1        #Counter for num samples collected
while True:
    if Num_Samples <= 10:            #storing a total of 10 samples
        LM35_A = LM35.read_u16()     #Read the ADC port to get sensor data
        Samples = Samples + LM35_A   #Add current reading to sample batch
        Num_Samples += 1             #Increment counter
    else:
        Avg_A = Samples / 10             #Get the average of samples
        Samples = 0                      #Reset Samples variable to zero
        Num_Samples = 1                  #Reset counter to one
        T_c, T_f = Compute_Temp(Avg_A)   #Fetch the temps from the function
        print("Celcius=",T_c,"  Fahrenheit=",T_f)
   
    utime.sleep(.1)  #slow the loop down
    
    