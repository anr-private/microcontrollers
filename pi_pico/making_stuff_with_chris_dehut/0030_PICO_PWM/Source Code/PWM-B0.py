# using PWM control     ANR 
#
# Sample duty cycles - manually selected
# GPIO 2 (physical pin 4)  -> LED -> resistor 330  -> gnd  (physical pin 3)

import machine
import utime

PWM_Sig = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
PWM_Sig.freq(1000)  # 1000 is good starting point; try higher and lower
#PWM_Sig.freq(10)  # 1000 is good starting point; try higher and lower

#65535 * 0.05 =  3276  #5% Duty Cycle
#65535 * 0.25 = 16383  #25% Duty Cycle
#65535 * 0.50 = 32767  #50% Duty Cycle
#65535 * 0.75 = 49151  #75% Duty Cycle
#65535 * 1.00 = 65535  #100% Duty Cycle

#Duty_Cycle5 = round(65535 * .05)
#Duty_Cycle25 = round(65535 * .25)
#Duty_Cycle50 = round(65535 * .50)
#Duty_Cycle75 = round(65535 * .75)
#Duty_Cycle100 = round(65535 * 1.00)

# percent duty cycle  0..100
pct = 75

duty_cycle = round (65535.0 * (pct / 100.0))

print(f"Duty cycle  pct={pct}%  cycle_count={duty_cycle}     Use ^C to terminate this program.")
PWM_Sig.duty_u16(duty_cycle)

try:
    while True:
        utime.sleep(0.25)
except KeyboardInterrupt:
    print("   ended by ctrl-C")

#x = input("Hit enter to end") #Run the program till the user hits a key
###utime.sleep(2)
print("  Cleanup...")
###PWM_Sig.duty_u16(65000)
PWM_Sig.duty_u16(10)
utime.sleep(0.001) # not sure why, but this allows LED to go dark
PWM_Sig.deinit()

print("PROGRAM ENDED")

