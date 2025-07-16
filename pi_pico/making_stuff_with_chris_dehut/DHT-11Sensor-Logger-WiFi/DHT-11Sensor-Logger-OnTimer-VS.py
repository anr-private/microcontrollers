'''
This version or the original program impliments a timer
to control when the sensor is read and data is recorded.
Also added is the inclusion of the PICO's internal
Real Time Clock.

DHT11 sensor Temperature and Humidity sensor
How to access and read data from the sensor
This example also saves the data into a CVS file for analysis in a spreadsheet
Source:
https://www.amazon.com/s?k=%E2%80%8EB09TKTZMSL&crid=1QO56RZCKGA7X


This library appears to be from a ESP8266 library,
perhaps ported to work with the PICO.  Not sure of
origin.
'''
from machine import Pin
from dht import DHT11, InvalidChecksum   #Import library for the DHT11 sensor
from machine import Timer
from machine import RTC
from time import sleep

rtc = RTC()  # Startup the internal Real Time Clock
             # The current time will have to be set from a web browser 

#Calibration Offset Variables
Temp_Offset_C   = 0    #set an amount to offset actual reading
Humidity_Offset = 0    #Same as above
Temperature_F = ""     #Create and preset the variables
Temperature_C = ""
Humidity      = ""


Log_File = open("TH-LOG.CSV","w")      # Creates/Opens a file called TH-LOG.CSV for writing

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)  #Setup the pin for communications with the DHT11
sensor = DHT11(pin)                    #Create the sensor object
sleep(1.0)                             #IMPORTANT - must sleep a min of 1 second to allow DHT11 to start up

#Create handler for the timer IRQ that reads DHT-11 and records data
def Process_DHT11_Data(Source):
    Tries = 10
    while Tries > 0:
        Tries -= 1 
        try:                                 #Use try with exception to bypass failed readings
            tc  = (sensor.temperature)       #Read the temp in celcius
            h = (sensor.humidity)            #Read the humidity
            tc = tc + Temp_Offset_C          #Perform calibration offset adjustments
            h  = h + Humidity_Offset             
            h = round(h)                     #Refine the data
            tf = ((tc * 1.8)+32)             #Convert from celius to Fahrenheit for Americans
            tf = round(tf)                   #Refine the data
            Temperature_C = str(tc)          #convert into strings for display
            Temperature_F = str(tf)
            Humidity      = str(h)
            print(">>",Temperature_F,Humidity)
            # Format data for writing in a comma sepperated line
            T = rtc.datetime()                  #Copy data (tuple) into a variable for easy manipulation
            #print(T[1],T[2],T[0],T[4],T[5])
            Text = str(T[1]) + "," + str(T[2]) + "," + str(T[0]) + "," + \
                   str(T[4]) + "," + str(T[5]) + "," + \
                   Temperature_C + "," + Temperature_F + "," + Humidity + "\n"
            Log_File.write(Text)               # Write data to the file
            Log_File.flush()                   # Writes buffer to file so more data can be written without closing file  
            break                              # All done, exit the loop
        except:                                #not much we can do, but print fail
            print("read fail",Tries)
            sleep(1)

#Periodic timer to run continuously
#1000 would be 1 second
#900000 = 15 minutes
Process_DHT11_Data(1)
DHT11_Timer = Timer(period=2000, mode=Timer.PERIODIC, callback=Process_DHT11_Data)

Reads = 30				#Set number of reads to make in this loop
while Reads > 0:        #Loop until Reads <= zero
    Reads -= 1          #Decrement the Reads variable by one
    print(Reads)
    sleep(1)            #Take a nap between readings - should be more than 1 second

DHT11_Timer.deinit()
print("This is the end")