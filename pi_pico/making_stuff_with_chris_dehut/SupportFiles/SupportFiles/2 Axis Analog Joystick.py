''' Demo program to read a 2 axis analog joystick, then break the readings down into -Range and +range
    with range being any amount such as -10 to +10 or -100 to +100 etc.
    
    Adafruit part number 512 is the unit used in this video
    
    The Pots are configured as voltage dividers, and return a voltage value between 0 and 3.3 volts to the PICO.
    The PICO has a 16 bit resolution, so that 0 to 3.3V is represented as 0 to 65535 from reading the analog value.
    Mechanically, the center position of the joystick would return a value of about 32500.
    Using a value of 32500 in your code can be difficult to understand in code and use, therefore, we convert it as such.
    A value of zero, would be the stick in center position
    A value of POSTIVE 10 would be the stick all the way in one direction.
    A value of NEGATIVE 10 would be the stick all the way in the other direction.
    -10 ~ 0 ~ +10  
    
    With many cheap analog joysticks available, be sure to check them for full range
    of 0 to 10k ohms during stick movement from min to max
'''
import machine
import utime

#Configure hardware
ForRev = machine.ADC(0)  #setup analog reading on ADC
LftRht = machine.ADC(1)  #setup analog reading on ADC
SW = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_UP) #the switch reading will be inverse logic

def Convert_Raw(Reading,Center_Val):
    #This function will return a range of values from -10 to 10 or any range of values such as -100 to 100
    #The center value must be passed into this function for "centering" calculations
    #The Center_Val is used to calculate -10 units and +10 units from that value
    #There will be a dead zone that will range from -DeadBand to + DeadBand from Center_Val
    DeadBand = 1200  #this is a good starting value for the deadband, adjust to get a zero reading with stick in middle.
    if (Reading <(Center_Val - DeadBand)) or (Reading >(Center_Val + DeadBand)): #Lower or higher than DeadBand
        Top = 65535     #Theoretical Max analog value - often is very close to this value
        Bot = 0         #Theoretical min analog value - often is a few hundred higher
        #Break the 16 bit value down in minus values and plus values with zero in the middle
        Delta = Center_Val + DeadBand      
        Shifted_Reading = Reading - Delta
        Shifted_Max     = Top - Delta
        Index           = Shifted_Reading / Shifted_Max
        Reduced_Range = 10  #this sets the minus to plus range of values returned
        return round(Index * Reduced_Range)
    else:
        zero = 0
        return(0)

Text = ""
while True:
    #Read the analog pin values from the joysticks
    ForRev_Val = ForRev.read_u16()
    LftRht_Val = LftRht.read_u16()
    #Read the push button switch values
    S_V = SW.value()
    #Break down analog values into more useful values
    FR = Convert_Raw(ForRev_Val,31500)
    LR = Convert_Raw(LftRht_Val,31000)
    
    print("FR=",FR, " LR=",LR, " Switch=",S_V)  
      
    utime.sleep(.1)