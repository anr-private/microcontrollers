# using PWM control

#load libraries
import machine
import utime

#Create a PWM object called PWM_Sig
PWM_Sig = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
PWM_Sig.freq(1000)  # 1000

print("Ready, Set, GO!")

Duty_Cycle = 0     #range = 0 ~ 65535
while Duty_Cycle <= 65535:
    Duty_Cycle += 1
    PWM_Sig.duty_u16(Duty_Cycle)
    utime.sleep(.0001)


Duty_Cycle = 65531     #range = 0 ~ 65535
while Duty_Cycle >= 0:
    Duty_Cycle -= 1
    PWM_Sig.duty_u16(Duty_Cycle)
    utime.sleep(.0001)


PWM_Sig.duty_u16(1)
PWM_Sig.deinit()
print("PROGRAM ENDED")

