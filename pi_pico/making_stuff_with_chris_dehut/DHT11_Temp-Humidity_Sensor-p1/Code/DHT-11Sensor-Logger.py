'''
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
from time import sleep
from dht import DHT11, InvalidChecksum   #Import library for the DHT11 sensor


#Calibration Offset Variables
Temp_Offset_C   = 0    #set an amount to offset actual reading
Humidity_Offset = 0    #Same as above
Temperature_F = ""     #Create and preset the variables
Temperature_C = ""
Humidity      = ""

#sleep(120)                             #VERY IMPORTANT --> Sleep for a few minutes here. This will give
                                        # you enough time to connect with Thonny so that you can download
                                        # the file before it is overwritten on the next line.
                                        
Log_File = open("TH-LOG.CVS","w")      # Creates/Opens a file called TH-LOG.CVS for writing

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)  #Setup the pin for communications with the DHT11
sensor = DHT11(pin)                    #Create the sensor object
sleep(1.0)                             #IMPORTANT - must sleep a min of 1 second to allow DHT11 to start up



Reads = 20				#Set number of reads to make in this loop
while Reads > 0:        #Loop until Reads <= zero
    Reads -= 1          #Decrement the Reads variable by one
    sleep(.25)          #Take a nap between readings - should be more than 1 second
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
    except:                              #not much we can do, but print fail
        print("read fail")
        pass

    print(Temperature_F,"F  ",Temperature_C,"C  ",  Humidity, "%  Number of Reads ",Reads)
    
    # Format data for writing in a comma sepperated line
    Text = Temperature_C + "," + Temperature_F + "," + Humidity + "\n"
    Log_File.write(Text)               # Write data to the file
    Log_File.flush()                   # Writes buffer to file so more data can be written without closing file  


print("This is the end")