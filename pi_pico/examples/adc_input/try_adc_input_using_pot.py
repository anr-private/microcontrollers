# try_adc_input_using_pot.py
#
# Read raw 16 bits from Pi Pico
#
# Use 10k pot: wiper goes to the ADC pin.
#  Outer ends of pot go to GND and 3v3.
# Draws only .33mA (using 3.3v of the Pico)
#
# See:
#  ~/git/microcontrollers/pi_pico/docs/pi_pico_pins.txt

from machine import ADC, Pin
import time

# Initialize ADC2 on GPIO 28
# You can use the Pin object or just the GPIO number
potentiometer = ADC(Pin(28)) 

# Conversion factor for 16-bit ADC (3.3V / 65535)
conversion_factor = 3.3 / 65535

def force_PWM_mode():
    # Forces PWM mode in the 3.3v power supply.
    # This prevents the PS from using PFM mode
    # (Pulse freq): PFM mode is more efficient
    # but PWM mode is needed when load on the PS
    # increases. By default the PS will flip
    # between the two modes as needed.

    # Initialize GPIO23 as an output
    # Using .on() or .value(1) sets it high (3.3V)
    gp23 = machine.Pin(23, machine.Pin.OUT)
    gp23.on()  # or gp23.value(1)
    print("PWM MODE is being forced to reduce power supply mode!")
    return gp23

def get_gp23_value(gp23):
    if 1:
        return -1
    
    if gp23 is None: return None
    return gp23.value()


def calibrate(gp23):
    
    gp23_value = get_gp23_value(gp23)
    
    print(f"=== CALIBRATE ============  GP23.value={gp23_value}")
    
    # starting values
    high = 0       # <= 0
    low = 66000  # > 65535

    while True:
        gp23_value = get_gp23_value(gp23)
        
        raw_val = potentiometer.read_u16()
        if raw_val > high: high = raw_val
        if raw_val <  low:  low = raw_val
        
        delta = high - low
        if delta > 0:
            curr_pct = raw_val * 100 / delta
        else:
            curr_pct = 0
        
        print(f"  low={low:6d}  high={high:6d}   raw={raw_val:6d}  pct={curr_pct:5.2f}    gp23.value={gp23_value}")
        time.sleep(0.33)
        

def run(gp23):

    while True:
        # Read raw 16-bit value (0 to 65535)
        raw_value = potentiometer.read_u16()
        
        # Convert raw value to voltage
        voltage = raw_value * conversion_factor

        gp23_value = get_gp23_value(gp23)
        
        # Print results to the console
        print(f"Raw Value: {raw_value} | Voltage: {voltage:.2f}V    gp23.value={gp23_value}")
        
        # Small delay to prevent flooding the serial monitor
        time.sleep(0.5)

def main():
    gp23 = None
    if 1:
        gp23 = force_PWM_mode()

    calibrate(gp23)
    run(gp23)
    
    
if __name__ == "__main__":
    main()
    

###
