'''
Use a photoresistor to measure ambient light in room and then
automatically adjust the brightness of a LED to increase lighting.

Bright room light is     59000 analog reading
Pitch black room          5000 analog reading

The LED brightness would set inversely proportional to the sensor reading.
'''
import machine
import utime

#Configure output as PWM
LED = machine.PWM(machine.Pin(15))  # Use pin GP15 for LED output
LED.freq(1000)                      # A good frequency to avoid flicker
#Configure input as analog
PhotoResistor = machine.ADC(1)  #setup analog reading on ADC #1

def Transform_Readings(Sensor_Reading):
    # Transform sensor reading to inverse proportional PWM setting
    # Range of practical readings from sensor...
    Sen_Bot =  5000      # Which needs to be mapped to 0%
    Sen_Top = 59000      # Which needs to be mapped to 100%
    Shift = 0-Sen_Bot    # Remove deadband portion at bottom
    Range = Sen_Top - Sen_Bot # Get full practical range of readings
    Sensor_Reading = Sensor_Reading - Sen_Bot  #Shift actual reading
    Sensor_Reading_Percentage = Sensor_Reading / Range # Get percentage of current reading
    Set_PWM = int(65535 * Sensor_Reading_Percentage) #set PWM to same percentage of full range of PWM Range
    Set_PWM = 65535 - Set_PWM #Invert PWM setting
    print(Sensor_Reading, Shift, Range, Sensor_Reading_Percentage, Set_PWM)
    return Set_PWM


# Main Code ---------------------------------------------------------------------------------    
while True:
    Bright_Level = PhotoResistor.read_u16()    #Read the Light Sensor
    LED_PWM = Transform_Readings(Bright_Level) #Get the PWM Setting for the LED                                    
    LED.duty_u16(LED_PWM)                      #Set the PWM output for the LED
    utime.sleep(.1)
    