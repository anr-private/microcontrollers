
'''
 WiFi enabled Temperature and Humidity data logger with real time clock.
  > Utilizes the DHT-11 temp and humidity sensor.
  > Logs: Date, Time, Temp C, Temp F, and Relative humidity.
  > Frequency of data collection can be changed.
  > Data is written to CVS file - internal to the PICO-W.
  > Adjustable delay on start to allow extraction of CVS file using Thonny.
  > WiFi connection and web page display of data.
  > Using web interface, current date and time can be set.
  > Data collection runs until power is removed.
  
 This code is heavily based on the example from:
 https://core-electronics.com.au/guides/raspberry-pi-pico-w-create-a-simple-http-server/
 
 Data is displayed in 5 sections from top to bottom:
   > TOP TITLE
   > KEYPAD 
   > STATIC TEXT LINE(S)
   > BUFFER DATA TEXT LINE
   > FORMATED DATA TEXT LINE
 
 When run, access the unit via the IP address assigned to the PICO W from a browser on
 on the same network.
   > Clicking on the number buttons adds that number of a buffer variable.
   > Clicking on the B key removes the last number from the buffer.
   > Clicking on the E key transfers the buffer into the variable of
   > your choice and clears the buffer. 
'''

import network
import socket
from machine import Pin
from machine import RTC
from time import sleep
from machine import Timer
from dht import DHT11, InvalidChecksum   #Import library for the DHT11 sensor

rtc = RTC()  # Startup the internal Real Time Clock
             # The current time will have to be set from a web browser
             # when run from Thonny, the time is set automatically via USB connection

led = Pin("LED", Pin.OUT)  #This LED will be on when network connection is made
led.value(0)               #Set to off

#========================================
# Startup delay to allow time to        <
# connect to Thonny so that you can     <
# extract the TH-LOG.CSV                <
# Set to a duration long enough for     <
# you to connect with thonny and stop   <
# the program.                          <
sleep(1)
#==================================     <

# ssid = ''
# password = ''

#Configure Data/variables, file for writing data to, and create DHT11 object
#Calibration Offset Variables
Temp_Offset_C   = 0    #set an amount to offset actual reading
Humidity_Offset = 0    #Same as above
Temperature_F = ""     #Create and preset the variables - these are global variables
Temperature_C = ""     #
Humidity      = ""     #
Log_File = open("TH-LOG.CSV","w")      #Creates/Opens a file called TH-LOG.CSV for writing
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)  #Setup the pin for communications with the DHT11
sensor = DHT11(pin)                    #Create the sensor object
sleep(1.0)                             #IMPORTANT - must sleep a min of 1 second to allow DHT11 to start up

wlan = network.WLAN(network.STA_IF)  #Access the WiFi network and login
wlan.active(True)
wlan.connect(ssid, password)

#The following code is HTML code that defines the webpage that will be served by the PICO
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: left;}
.button7 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button8 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button9 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button4 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button5 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button6 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button1 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button2 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button3 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.buttonB { background-color: #85C1E9; border: 2px solid #000000;; color: red; padding: 14px 18px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.button0 { background-color: #85C1E9; border: 2px solid #000000;; color: white; padding: 14px 20px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
.buttonE { background-color: #85C1E9; border: 2px solid #000000;; color: black; padding: 14px 18px; text-align: left; text-decoration: none; display: inline-block; font-size: 30px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><h1>Temp & Humidity</h1>
<form>
<button class="button9" name="key" value="9" type="submit">9</button>
<button class="button8" name="key" value="8" type="submit">8</button>
<button class="button7" name="key" value="7" type="submit">7</button>
<br>
<button class="button6" name="key" value="6" type="submit">6</button>
<button class="button5" name="key" value="5" type="submit">5</button>
<button class="button4" name="key" value="4" type="submit">4</button>
<br>
<button class="button3" name="key" value="3" type="submit">3</button>
<button class="button2" name="key" value="2" type="submit">2</button>
<button class="button1" name="key" value="1" type="submit">1</button>
<br>
<button class="buttonB" name="key" value="B" type="submit">B</button>
<button class="button0" name="key" value="0" type="submit">0</button>
<button class="buttonE" name="key" value="E" type="submit">E</button>
</form>
<br><br>
Enter in order as follows:<br>   mmddyyhhmm
<p style="color:#D35400;font-size:22px;";>%s<p></body></html>
"""

max_wait = 20                  # Wait for WiFi connection or fail
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...Attempts left>',max_wait)
    sleep(2)
    
if wlan.status() != 3:           # Handle connection error
    raise RuntimeError('network connection failed' , wlan.status())
else:
    led.value(1)  #Set to ON
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
      
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] # Open socket for communications
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

#Create handler for the timer IRQ that reads DHT-11 and records data
def Process_DHT11_Data(Source):
    global Temperature_C
    global Temperature_F
    global Humidity
    Tries = 10
    while Tries > 0:
        Tries -= 1 
        try:                                 #Use try with exception to bypass failed readings
            m = (sensor.measure)
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
            print(">>",Temperature_F,Temperature_C,Humidity)
            # Format data for writing in a comma separated line
            # mm/dd/yyyy |  hh:mm  |  Temp C  |  Temp F  | Humidity
            T = rtc.datetime()                  #Copy data (tuple) into a variable for easy manipulation
            D_Text = str(T[1]) + "/" + str(T[2]) + "/" + str(T[0]) + ","            # mm/dd/yyyy
            T_Text = str(T[4]) + ":" + str(T[5]) + ","                              # hh:mm
            TH_Text = Temperature_C + "," + Temperature_F + "," + Humidity + "\n"   # Temp C , Temp F , Humidity , new line
            Text = D_Text + T_Text + TH_Text
            Log_File.write(Text)               # Write data to the file
            Log_File.flush()                   # Writes buffer to file so more data can be written without closing file  
            break                              # All done, exit the loop
        except:                                # not much we can do, but print fail
            print("read fail",Tries)
            sleep(.1)

#Periodic timer to run continuously
#1000 would be 1 second
#900000 = 15 minutes
Process_DHT11_Data(1)   #Process 1 read right away before starting the timer
#DHT11_Timer = Timer(period=900000, mode=Timer.PERIODIC, callback=Process_DHT11_Data)  #start the timer interupt routine
DHT11_Timer = Timer(period=5000, mode=Timer.PERIODIC, callback=Process_DHT11_Data)  #start the timer interupt routine

#===============================================================================================================
# Listen for connections, serve client
InputVal = ""
while True:
    try:       
        cl, addr = s.accept()       #Fetch data if there is any from the remote computer
        request = cl.recv(1024)
        request = str(request)
        
        #handle the incomming data 
        v = request[12:13]  #this is the location of character that is embeded in the REQUEST from the user
        if v == "/":        #Do nothing --> Eliminate unexpected / character
            pass              
        elif v == "B":                            #Backspace to remove character
            L = len(InputVal)-1                   #Get length of string
            InputVal = InputVal[0:L]              #Remove last character of the string 'InputVal'
            print("Back spaced to get",InputVal)
        elif v == "E":                            #E key as ENTER to end input of data
            if len(InputVal) >= 10:               #Make sure the data string contains enough characters  
                text = InputVal                   #Copy to another variable for further manipulation
                print("E pressed",InputVal)       #Data format is:  mmddyyhhmm with the last mm being minutes
                Year = int("20" + text[4:6])      #Extract the Year characters and convert to Integer
                Day= int(text[2:4])               #Extract the Day characters and convert to Integer
                Month= int(text[0:2])             #Extract the Month characters and convert to Integer
                Hour= int(text[6:8])              #Extract the Hour characters and convert to Integer
                Min= int(text[8:10])              #Extract the Minute characters and convert to Integer  
                rtc.datetime((Year, Month, Day, 1, Hour, Min, 0, 0)) #Set the realtime clock to the input values
                InputVal = ""                     #clear the character input buffer InputVal
        else:                                     #Add character to input string
            InputVal = InputVal + v               #Add new character to the input buffer InputVal
            print("You pressed ",v, " now InputVal =",InputVal)            
        
        #Prepare dynamic data for display in the served html web page and send it
        Inp_Data = InputVal  + " <br> "     #Copy to another variable and add a line break
        T = rtc.datetime()                  #Copy data (tuple) into a variable for easy manipulation
        P_Date_Time =  str(T[1]) + "/" + str(T[2])  + "/" + str(T[0]) + "  " +  str(T[4]) + ":" +  str(T[5])  + " <br> "
                                            #Put together the string representing 'mm/dd/yy  hh:mm'
        Temp_Humidity = "    " + Temperature_F + "F   " + Humidity + "%" 
        #Combine both data sets and place into a variable that will be shown on the web page
        Show_Data = Inp_Data + P_Date_Time + Temp_Humidity
        response = html % Show_Data         #Format the data for use with the HTLM code defined above   

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #Send the "web page data"
        cl.send(response)                                             #Send the formatted string data
        cl.close()                                                    #Close the operation
        
    except OSError as e:            # Upon major "OS" error, clean up what can be cleaned up and terminate
        cl.close()                  # Close the operation if any
        DHT11_Timer.deinit()        # Terminate the timer/interrupt
        print('connection closed')

DHT11_Timer.deinit()
