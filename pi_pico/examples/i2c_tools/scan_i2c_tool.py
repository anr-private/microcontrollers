# scan_i2c_tool.py

import machine



# NOTE that the SDA and SCL pins act as BOTH INPUT and OUTPUT!!!



def scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number, use_pullups=False):
    print(f"SCAN FOR I2C  ----------------------------------------")
    if use_pullups:
        # The SparkFun Soil Moisture Sensor has NO PULLUP RESISTORS.
        # The sensor expects 4.7K from SDA and SCL pins to 3.3v for pullup.
        # This is a cheesey substitute just for testing:
        #   Manually configure pins and turn on the Pico's internal pull-ups
        sda_pin = machine.Pin(data_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        print(f"@32 USING INTERNAL PULLUP resistors on Data, Clock pins")
    else:
        # for I2C that has internal pullup resistors: don't need external ones
        sda_pin = machine.Pin(data_pin_number)
        scl_pin = machine.Pin(clock_pin_number)
    
    print(f"@38 Create I2C device  {i2c_bus_number=}  {data_pin_number=}  {clock_pin_number=}")

    ###i2c = machine.I2C(i2c_bus_number, sda=sda_pin, scl=scl_pin)
    i2c = machine.I2C(i2c_bus_number, sda=sda_pin, scl=scl_pin, freq=100000)

    print(f"@42 Got I2c device obj: {i2c}")

    print(f"@44Scanning for I2C devices...")
    
    # Scan for devices on the I2C bus
    devices = i2c.scan()
    
    if devices:
        print("@50Found I2C devices at addresses:")
        for device_address in devices:
            # Convert the address to hexadecimal for common representation
            print(hex(device_address))
    else:
        print("@55  *****  No I2C devices found.  *************")
    print()


def scan_for_i2c_alternate(i2c_bus_number, data_pin_number, clock_pin_number):
    #
    print(f"SCAN FOR I2C ALTERNATE  ----------------------------------------")
    
    # 1. Manually configure pins and turn on the Pico's internal pull-ups
    sda_pin = machine.Pin(data_pin_number,  machine.Pin.OUT, machine.Pin.PULL_UP)
    scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
    
    # 2. Initialize I2C with the configured pins
    i2c = machine.I2C(i2c_bus_number, sda=sda_pin, scl=scl_pin, freq=100000)
    
    print("Scanning I2C bus...")
    devices = i2c.scan()
    
    if len(devices) == 0:
        print("No devices found. Internal pull-ups may be too weak; physical resistors needed.")
    else:
        print(f"Success! Found {len(devices)} device(s).")
        for device in devices:
            print(f"Decimal address: {device} | Hex address: {hex(device)}")

    print()


def main():

    i2c_bus_number = 0
    data_pin_number = 0
    clock_pin_number = 1
    #data_pin_number = 4
    #clock_pin_number = 5

    scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number)
    scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number, True)

    scan_for_i2c_alternate(i2c_bus_number, data_pin_number, clock_pin_number)

main()

###
