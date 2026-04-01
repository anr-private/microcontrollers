# try_adc_input_using_pot.py
#
# Read raw 16 bits from Pi Pico
#
# Use 10k pot: wiper goes to the ADC pin.
#  Outer ends of pot go to GND and 3v3.
# Draws only .33mA (using 3.3v of the Pico)
#
# This program reads an analog value using an ADC pin.
# The default pin specified below is GPIO28, which is ADC2.
# There are also pins GPIO26 (ADC0) and GPIO26 (ADC1).
# There are 2 modes for sampling the data; they are 
# controlled in get_scaled_raw_value_value(). One mode uses the data
# as it comes directly from the pin; the other divides by 
# 16 (shifts >>4), which reduces the noise seen in the lower bits.
# See values SCALE_BY_xxx defined below.
#
# Noise is also caused by the power supply (PS) and its two modes
# of operation. It has a lower power mode Pulse Frequence modulation
# and a higher power mode Pulse Width modulation.
# Aka PFM and PWM.
# PFM saves on power but produces more noise in the power supply.
# PWM forces constant switching so uses more power (5-10mA)
# when idle.
# You can force the Pico to run in PWM mode using GPIO23;
# see force_PWM_mode() below. Doing so increases accuracy
# at the expense of using more power.
#
# This version of the program by default uses a fixed
# low/high reference for the sampled value.
# The defaults are determined by the scale mode:
# SCALE_BY_16 uses 0 to 4095 
# SCALE_BY_1  uses 0 to 65535
# 
# You can also turn on 'adative' scaling, which modifies
# the low and high scaling values on the fly by looking
# at each received ('raw') value to see if it is lower
# than the current low or higher than the current high 
# reference values.
# If so the reference value is lower/raised respectively.
#
# See:
#  ~/git/microcontrollers/pi_pico/docs/pi_pico_pins.txt

from machine import ADC, Pin
import time

# Enables the 'adaptive' updating of the low/high values
# used to obtain the final input value.
ADAPTIVE_MODE = True

LOW_VALUE = 0
HIGH_VALUE = 4095

# If True, forces PWM mode.
# Else allows the power supply to switch between PFM and PWM modes
# as it desires.
FORCE_PWM_MODE = True

# Aka gp23  - GPIO23 is the internal PW control GPIO pin
PS_MODE_CONTROL_PIN = None

# Turn only one on at a time!
SCALE_BY_1 = False
SCALE_BY_16 = True


# Initialize ADC2 on GPIO 28
# You can use the Pin object or just the GPIO number
potentiometer = ADC(Pin(28)) 

# Conversion factor for 16-bit ADC (3.3V / 65535)
conversion_factor = 3.3 / 65535

def get_scaled_raw_value():
    raw_value = potentiometer.read_u16()
    if SCALE_BY_1:
        return raw_value
    if SCALE_BY_16
        return raw_value >> 4  # div by 16
    raise RuntimeError("Line 65: no SCALE mode is specified")


def force_PWM_mode():
    # Forces PWM mode in the 3.3v power supply.
    # This prevents the PS from using PFM mode
    # (Pulse freq): PFM mode is more efficient
    # but PWM mode is needed when load on the PS
    # increases. By default the PS will flip
    # between the two modes as needed.

    # Initialize GPIO23 as an output
    # Using .on() or .value(1) sets it high (3.3V)

    globalPS_MODE_CONTROL_PIN

    gp23 = machine.Pin(23, machine.Pin.OUT)
    gp23.on()  # or gp23.value(1)
    print("PWM MODE is being forced to reduce power supply mode!")
    PS_MODE_CONTROL_PIN = None 

    return gp23

def get_gp23_value():
    if PS_MODE_CONTROL_PIN is None:
        return -1
    return PS_MODE_CONTROL_PIN.value()


def calibrate(gp23):
    # Originally an attempt to do scaling dynamically.
    # Now used as the main 'get some values' function

    gp23_value = get_gp23_value()
    
    print(f"=== CALIBRATE ============  GP23.value={gp23_value}")
    
    # starting values
    high = 0       # <= 0
    low = 66000  # > 65535

    while True:
        gp23_value = get_gp23_value(gp23)
        
        raw_val = get_scaled_raw_value_value()

        if ADAPTIVE_MODE:
            if raw_val > high: high = raw_val
            if raw_val <  low:  low = raw_val
        
        delta = high - low
        if delta > 0:
            curr_pct = raw_val * 100 / delta
        else:
            curr_pct = 0
        
        print(f"  low={low:6d}  high={high:6d}   raw={raw_val:6d}  pct={curr_pct:5.2f}    gp23.value={gp23_value}")
        time.sleep(0.33)
        

def run__NOTUSED(gp23):
    # Originally was the 'get values' function, called after calibrate()
    # Now calibrate() is being used for this,
    # so this function is not currently used.
    while True:
        # Read raw 16-bit value (0 to 65535)
        raw_value = get_scaled_raw_value_value()
        
        # Convert raw value to voltage
        voltage = raw_value * conversion_factor

        gp23_value = get_gp23_value()
        
        # Print results to the console
        print(f"Raw Value: {raw_value} | Voltage: {voltage:.2f}V    gp23.value={gp23_value}")
        
        # Small delay to prevent flooding the serial monitor
        time.sleep(0.5)

def main():
    global LOW_VALUE
    global HIGH_VALUE

    if FORCE_PWM_MODE:
        force_PWM_mode()

    if SCALE_BY_16:
        LOW_VALUE = 0
        HIGH_VALUE = 4095
    elif SCALE_BY_1: 
        LOW_VALUE = 0
        HIGH_VALUE = 65535
    else:
        raise RuntimeError("Line 163: No SCALE_BY_xxx value has been selected.")

    if ADAPTIVE_MODE:
        # Set the the LIMIT values conservatively so that they can
        # be adjusted adaptively as the program runs.
        # The adjustment values are just SWAG guesses so far...
        if SCALE_BY_16:
            LOW_VALUE += 150
            HIGH_VALUE -= 150
        elif SCALE_BY_1: 
            LOW_VALUE += 500
            HIGH_VALUE -= 500

    calibrate()
    ###run()
    
    
if __name__ == "__main__":
    main()
    

###
