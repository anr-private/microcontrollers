# using PWM control

#load libraries
import machine
import utime

#Create a PWM object called PWM_Sig
PWM_Sig = machine.PWM(machine.Pin(2))  #use pin 4/GP2 for LED output
PWM_Sig.freq(1000)  # 1000

#65535 * 0.05 =  3276  #5% Duty Cycle
#65535 * 0.25 = 16383  #25% Duty Cycle
#65535 * 0.50 = 32767  #50% Duty Cycle
#65535 * 0.75 = 49151  #75% Duty Cycle
#65535 * 1.00 = 65535  #100% Duty Cycle

Duty_Cycle = round(65535 * .50)
PWM_Sig.duty_u16(Duty_Cycle)

x = input("Hit enter to end") #Run the program till the user hits a key

PWM_Sig.duty_u16(1)
PWM_Sig.deinit()

print("PROGRAM ENDED")

