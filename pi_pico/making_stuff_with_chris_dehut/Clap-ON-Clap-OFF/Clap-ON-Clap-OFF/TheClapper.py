''' This is a demo program featuring a digital sound sensor
to replicate the functionality of the "Clapper".  The Clapper
was a sound activated switch to turn a light ON/OFF. It was
one of those classic "Seen on TV" products.
See commercial here --> https://www.youtube.com/watch?v=3lBWjLJeKkQ

You clap twice, within a specific period of time to turn
the 'Switch" on or off.

The sound sensor is inexpensive and can be purchased here...
https://www.amazon.com/HiLetgo-Sensor-Module-Detect-Control/dp/B00LW14ZEI
While advertised as a "Voice Detect", don't expect much in that way.

The device has a Trimmer Pot to set the threshold between Quiet and LOUD
We will monitor the output to see if the sound level is low or high with
digital input of the PICO.
'''
import machine
import time

#Create an input for our digital pin
Sound_Sensor = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
#Create an output object for our LED
LED = machine.Pin(14,machine.Pin.OUT)  #use GP14 for LED output

Prev_Time = time.ticks_ms() #Record current milliseconds

# Establish an acceptable timing window between claps
Min_Tween_Time = 250 #milliseconds
Max_Tween_Time = 1250 #milliseconds

while True:
    if Sound_Sensor.value() == 1:         # Heard the clap
        Cur_time = time.ticks_ms()        # Get current milliseconds 
        Etime = Cur_time - Prev_Time      # Calulate time since last clap
        # Check if timing between claps is between acceptable range
        print(Etime)
        #print(Min_Tween_Time,Max_Tween_Time,Etime)
        if (Etime >= Min_Tween_Time) & (Etime <= Max_Tween_Time):
            print("TOGGLE IT!")
            LED.toggle()            # Toggle the LED ON or OFF
        Prev_Time = time.ticks_ms() # Record current milliseconds
    time.sleep(.005)
    