README_AAA.txt for Analog v1.2 Capacitive Soil Sensor


DFRobot SEN0193.
https://www.digikey.com/en/products/detail/dfrobot/SEN0193/6588605

The RP2350 processor on the Pico 2 W features a 12-bit ADC. In MicroPython, this resolution is scaled up to a uniform 16-bit range spanning from 0 to 65535.

https://www.youtube.com/watch?v=4XPDyKujcxI&t=5s
https://core-electronics.com.au/videos/raspberry-pi-pico-workshop-chapter-26-reading-analog-inputs
https://www.youtube.com/watch?v=FUfPjqmCDS0&t=632s
https://www.youtube.com/watch?v=9lelfdwoKKA&t=10s


=== CONNECTION  ==================================================

Sensor Pin  Pico 2 W    Physical
            pin label     pin       Purpose
----------  -----------  --------- -----------
VCC (Red)     3V3Pin      36       Powers the sensor with clean 3.3V power.
GND (Black) GND or AGND   33,38    Standard system ground.
AOUT / S    GP26_A0       31       Sends the moisture voltage to the ADC.
                                     (Analog Output)
In addition to GPIO26:  GP27 (pin 32) or GP28 (pin34)


=== CALIBRATION  ===========================================

Calibration Step (Crucial for Analog)Because analog capacitive sensors measure relative electrical variance rather than absolute percentages, you must record your specific upper and lower limits

Dry Target Value: 
Hold the sensor in the air completely dry and run the script. Note the raw integer value (it is usually around 48000 to 55000).

Wet Target Value: 
Submerge the blade of the sensor into a cup of water up to the marked stop-line. Note the updated raw value (it will drop significantly, usually to around 20000 to 25000).

ForumsJan 18, 2024 — Also, I was using the ADC on pin 28, so change that. The sensor I used has a disable pin, so it shuts completely off when not in u...Raspberry Pi ForumsUltimate Starter Kit for Raspberry Pi Pico 2 WH - 52Pi DocsApplication Scenario. Monitor the moisture level of a plant's soil to automate watering. Working Principle. The soil moisture sens...52Pi StoreShow all

===================================================
From search:

import machine
import time

# 1. Initialize the Analog-to-Digital Converter on GP26
soil_sensor = machine.ADC(machine.Pin(26))

print("Reading analog soil moisture sensor...")
print("---------------------------------------")

while True:
    # Read the raw 16-bit value (0 = 0V, 65535 = 3.3V)
    raw_value = soil_sensor.read_u16()
    
    # Calculate the exact voltage passing over your 12-inch wire
    voltage = raw_value * (3.3 / 65535)
    
    # Print data format for easy scanning
    print(f"Raw Register: {raw_value:<6} | Signal Voltage: {voltage:.2f}V")
    
    time.sleep(1.0)

=======================================================


:wrap=soft:
###
