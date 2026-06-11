import time
import machine

# Initialize ADC on GP26 (ADC0)
sensor_pin = 26
sensor = machine.ADC(sensor_pin)

# REPLACE THESE with your actual calibrated values
MIN_RAW_VALUE = 20000  # Example: Completely submerged in water
MAX_RAW_VALUE = 50000  # Example: Held dry in the air

def read_soil_moisture():
    # Read the 16-bit raw ADC value (0 to 65535)
    raw_value = sensor.read_u16()
    
    # Constrain the raw value to our limits
    constrained_value = min(max(raw_value, MIN_RAW_VALUE), MAX_RAW_VALUE)
    
    # Invert and scale to a 0-100% percentage
    # (Subtracting from max value because lower voltage = wetter soil)
    percentage = 100 - ((constrained_value - MIN_RAW_VALUE) / (MAX_RAW_VALUE - MIN_RAW_VALUE) * 100)
    
    return percentage, raw_value

while True:
    moisture_pct, raw_val = read_soil_moisture()
    print("Moisture: {:.2f}% | Raw ADC: {}".format(moisture_pct, raw_val))
    time.sleep(2)

###
