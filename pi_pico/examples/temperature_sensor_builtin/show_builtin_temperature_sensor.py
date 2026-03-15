# show_builtin_temperature_sensor.py
#
# Models:  Pi Pico W
# Presumably sensor is also available on other Pico model(s)?
#
# Source: googling 'how to access the temperature on pi pico w'

import machine
import time
###import dht for DHT11 or DHT11 sensors

adcpin = 4
sensor = machine.ADC(adcpin)

def read_internal_temperature():
    adc_value = sensor.read_u16()
    voltage = (3.3 / 65535) * adc_value
    temperature_celsius = 27 - (voltage - 0.706) / 0.001721
    return temperature_celsius

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

try:
    print("Press ^C to end this program...")
    while True:
        temperature_c = read_internal_temperature()
        temperature_f = celsius_to_fahrenheit(temperature_c)
        #print("Internal Temperature:", temperature_c, "°C")
        #print("Internal Temperature:", temperature_f, "°F")
        print(f"  Internal Temperature: {temperature_c:10.4f} °C   {temperature_f:10.4f} °F")
        time.sleep(3)
except (KeyboardInterrupt):
    print("  ... end of showing builtin temperature sensor ...")
    

### end ###

