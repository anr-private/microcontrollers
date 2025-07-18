# using PWM control to fade an LED up/down   ANR
#
# GPIO 2 (physical pin 4)  -> LED -> resistor 330  -> gnd  (physical pin 3)

import machine
import utime


PWM_Sig = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
PWM_Sig.freq(1000)  # 1000
# 10 Hz causes obvious flicker - it is worst at the lower duty cycles
#PWM_Sig.freq(10)  # 1000

print("Main: begin")

# fade up
Duty_Cycle = 0     #range = 0 ~ 65535
while Duty_Cycle <= 65535:
    Duty_Cycle += 1
    PWM_Sig.duty_u16(Duty_Cycle)
    utime.sleep(.0001)

# fade down
Duty_Cycle = 65535
while Duty_Cycle >= 0:
    Duty_Cycle -= 1
    PWM_Sig.duty_u16(Duty_Cycle)
    utime.sleep(.0001)


PWM_Sig.duty_u16(1)
PWM_Sig.deinit()
print("PROGRAM ENDED")

