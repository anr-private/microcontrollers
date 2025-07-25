import machine

# Initialize I2C bus 0 with specific SCL and SDA pins
# Replace with the correct pins for your board (e.g., Raspberry Pi Pico)
# Example for Pico: SDA on GP0, SCL on GP1
###i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
###i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

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
