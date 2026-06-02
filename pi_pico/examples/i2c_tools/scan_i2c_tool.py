import machine


I2C_BUS = 0
DATA_PIN = 0
CLOCK_PIN = 1

#I2C_BUS = 1
#DATA_PIN = 2
#CLOCK_PIN = 3

#these are the original settings
#I2C_BUS = 0
###DATA_PIN = 4
###CLOCK_PIN = 5


# NOTE that the SDA and SCL pins act as BOTH INPUT and OUTPUT!!!


if 0:
    # for I2C that has internal pullup resistors: don't need external ones
    sda_pin = machine.Pin(DATA_PIN)
    scl_pin = machine.Pin(CLOCK_PIN)
else:
    # The SparkFun Soil Moisture Sensor has NO PULLUP RESISTORS.
    # The sensor expects 4.7K from SDA and SCL pins to 3.3v for pullup.
    # This is a cheesey substitute just for testing:
    #   Manually configure pins and turn on the Pico's internal pull-ups
    sda_pin = machine.Pin(DATA_PIN, machine.Pin.OUT, machine.Pin.PULL_UP)
    scl_pin = machine.Pin(CLOCK_PIN, machine.Pin.OUT, machine.Pin.PULL_UP)

# Initialize I2C bus 0 with specific SCL and SDA pins
# Replace with the correct pins for your board (e.g., Raspberry Pi Pico)
# Example for Pico: SDA on GP0, SCL on GP1

###i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
###i2c = machine.I2C(I2C_BUS, scl=machine.Pin(CLOCK_PIN), sda=machine.Pin(DATA_PIN))
###i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
i2c = machine.I2C(I2C_BUS, sda=sda_pin, scl=scl_pin)

print("Scanning for I2C devices...")

# Scan for devices on the I2C bus
devices = i2c.scan()

if devices:
    print("Found I2C devices at addresses:")
    for device_address in devices:
        # Convert the address to hexadecimal for common representation
        print(hex(device_address))
else:
    print("No I2C devices found.")
    
### end ###
import machine
import time

# 1. Manually configure pins and turn on the Pico's internal pull-ups
sda_pin = machine.Pin(0, machine.Pin.OUT, machine.Pin.PULL_UP)
scl_pin = machine.Pin(1, machine.Pin.OUT, machine.Pin.PULL_UP)

# 2. Initialize I2C with the configured pins
i2c = machine.I2C(0, scl=scl_pin, sda=sda_pin, freq=100000)

print("Scanning I2C bus...")
devices = i2c.scan()

if len(devices) == 0:
    print("No devices found. Internal pull-ups may be too weak; physical resistors needed.")
else:
    print(f"Success! Found {len(devices)} device(s).")
    for device in devices:
        print(f"Decimal address: {device} | Hex address: {hex(device)}")
