'''
PICO / Micropython demo program to find / move 180 degree rotation of small RC Servo
 MG90S Servo Specs
 Rotational range 180 degrees
 Signal Frequeny for PWM is 50 hz (20 msecs)
 Duty cycle range for full Rotation range 1~2 msec
 duty_16() takes values of 0 to 65535 for duty cycle of 0 to 100
 0 = 0% = 0 msec        65535 = 100% = 20 msec
 
 
 
 Estimated Min, Mid, Max duty cycles for 0, 90, 180 degrees
 Min 1000
 Mid 4750  = (Min + ((Max - Min) / 2)
 Max 8500
'''

from machine import Pin, PWM
import utime

MG90S_servo = PWM(Pin(15))

MG90S_servo.freq(50)


Ang_000 = 1000
Ang_180 = 7500
Ang_090 = int(Ang_000 + ((Ang_180 - Ang_000)/2))


MG90S_servo.duty_u16(Ang_000)
utime.sleep(2)
MG90S_servo.duty_u16(Ang_090)
utime.sleep(2)
MG90S_servo.duty_u16(Ang_180)

