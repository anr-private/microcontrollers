# EX_rapid_reading_the_ADC.py
#
# Reads soil moisture sensor connected to ADC GPIO pin,
# Outputs the current value as raw value and as a percentage.
#
# Chinese sensor #1  MIN,MAX: moisture%: 31.94% 70.17%  volts: 2.25V 0.00V  raw: 44602.00 0.98  12bit: 2787.00 1222.00
# DFROBOT sensor #1  MIN,MAX: moisture%: 29.90% 65.87%  volts: 2.31V 0.00V  raw: 45942.37 1.13  12bit: 2871.00 1397.00

import machine
import time

#Calibraton values
CAL_MIN_MOISTURE = 0
CAL_MAX_MOISTURE = 65535
CALIBRATION_RANGE = CAL_MAX_MOISTURE - CAL_MIN_MOISTURE


sensor_obj = machine.ADC(26)

# delay between sample batches, secomds
delay_between_batches_secs = 1

# delay between individual samples, milliseconds
sample_interval_msecs = 1   

num_samples_per_attempt = 30


# got_min_raw = CAL_MAX_MOISTURE
# got_max_raw = CAL_MIN_MOISTURE
# got_min_12bit = CAL_MAX_MOISTURE
# got_max_12bit = CAL_MIN_MOISTURE
# got_min_pct = 100
# got_max_pct = 0


def get_smoothed_reading(num_samples, interval_ms):
    total = 0
    for _ in range(num_samples):
        total += sensor_obj.read_u16()
        time.sleep_ms(interval_ms) # 1ms rapid interval delay
    # Return the clean mathematical average
    return total / num_samples

def perform_sampling():
    got_min_raw = CAL_MAX_MOISTURE
    got_max_raw = CAL_MIN_MOISTURE
    got_min_12bit = CAL_MAX_MOISTURE
    got_max_12bit = CAL_MIN_MOISTURE
    got_min_pct = 100
    got_max_pct = 0
    got_min_volts = 99999
    got_max_volts = 0

    while True:
        # 1. Take a clean, smoothed 16-bit average
        clean_raw = get_smoothed_reading(num_samples=num_samples_per_attempt, 
                                         interval_ms=sample_interval_msecs)
        
        # 2. Scale to 12-bit native RP2350 resolution
        raw_12bit = int(clean_raw) >> 4
        
        # 3. Calculate actual voltage
        voltage = (raw_12bit / 4095.0) * 3.3
        
        moisture_pct = (CAL_MAX_MOISTURE - clean_raw) * 100 / CALIBRATION_RANGE

            
        if moisture_pct > got_max_pct:
            got_max_pct = moisture_pct
            got_max_raw = clean_raw
            got_max_12bit = raw_12bit
            got_max_raw = voltage
        if moisture_pct < got_min_pct:
            got_min_pct = moisture_pct
            got_min_raw = clean_raw
            got_min_12bit = raw_12bit
            got_min_volts = voltage

        print(f"moisture: {moisture_pct:.2f}%   raw: {str(clean_raw)}  12bit: {str(raw_12bit)} ")

        s_pct = f"{got_min_pct:.2f}% {got_max_pct:.2f}%"
        s_volts = f"{got_min_volts:.2f}V {got_max_volts:.2f}V"
        s_raw = f"{got_min_raw:.2f} {got_max_raw:.2f}"
        s_12bit = f"{got_min_12bit:.2f} {got_max_12bit:.2f}"
        print(f"MIN,MAX: moisture%: {s_pct}  volts: {s_volts}  raw: {s_raw}  12bit: {s_12bit}")

        ###print(f"moisture min,max: {got_min_pct:.2f}% {got_max_pct:.2f}%  raw min,max: {got_min_raw:.2f} {got_max_raw:.2f}  12bit min,max: {got_min_12bit:.2f} {got_max_12bit:.2f}")
        ###print(f"Filtered Voltage: {voltage:.2f}V   Moisture: {moisture_pct:.2f}")
        ###print("Filtered Voltage: {:.2f}V".format(voltage))
        
        # Soil moisture changes slowly. Wait 5 minutes between main cycles.
        time.sleep(delay_between_batches_secs) 
        ####time.sleep(300) 

perform_sampling()

###
