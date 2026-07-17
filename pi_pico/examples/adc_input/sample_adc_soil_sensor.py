# sample from
# https://peppe8o.com/download/micropython/capacitive-soil-moisture/capacitive-soil-pico.py
#
# Chinese sensor #1   moisture: 32.45%   min,max: 31.97 69.57  raw: 44266  min,max: 44586.00 19940.00
# DFROBOT sensor #1   moisture: 63.61%   min,max: 26.64 65.10  raw: 23845  min,max: 48075.00 22869.00

from machine import ADC, Pin
import utime

# use variables instead of numbers:
soil = ADC(Pin(26)) # Soil moisture PIN reference

#Calibraton values
min_moisture=0
max_moisture=65535
calibration_range = max_moisture - min_moisture


# delay between readings
#sleep_secs = 0.5
sleep_secs = 1 

got_min_raw = max_moisture
got_max_raw = min_moisture
got_min_12bit = 99999
got_max_12bit = 0
got_min_pct = 100
got_max_pct = 0

while True:
	# read moisture value and convert to percentage into the calibration range
	###moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture)
	raw_val = soil.read_u16()
	moisture_pct = (max_moisture - raw_val) * 100 / calibration_range
	
	if moisture_pct > got_max_pct:
	    got_max_pct = moisture_pct
	    got_max_raw = raw_val
	if moisture_pct < got_min_pct:
	    got_min_pct = moisture_pct
	    got_min_raw = raw_val


	# print values
	###print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
	print(f"moisture: {moisture_pct:.2f}%   min,max: {got_min_pct:.2f} {got_max_pct:.2f}  raw: {str(raw_val)}  min,max: {got_min_raw:.2f} {got_max_raw:.2f}")

	utime.sleep(sleep_secs)
	
###
