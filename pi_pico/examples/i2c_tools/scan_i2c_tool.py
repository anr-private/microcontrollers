# scan_i2c_tool.py

import machine
import time


# NOTE that the SDA and SCL pins act as BOTH INPUT and OUTPUT!!!

def cleanup_the_i2c(i2c_bus_number, data_pin_number, clock_pin_number):

    # 1. Temporarily set pins as standard digital outputs
    #sda_pin = machine.Pin(data_pin_number, machine.Pin.OUT)
    #scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT)
    sda_pin = machine.Pin(data_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
    scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)

    # 2. Manual "Bus Clear": Toggle SCL a few times to clear hung slaves
    for _ in range(9):
        scl_pin.value(0)
        time.sleep_us(5)
        scl_pin.value(1)
        time.sleep_us(5)
    
    # 3. Leave the bus in an explicit HIGH (idle) state
    sda_pin.value(1)
    scl_pin.value(1)
    time.sleep_ms(100) # Let the lines settle
    
    time.sleep(2)

# 4. NOW initialize the true hardware I2C object
    ###i2c = machine.I2C(i2c_bus_number, scl=machine.Pin(clock_pin_number), sda=machine.Pin(data_pin_number), freq=50000)
    i2c = machine.I2C(i2c_bus_number, scl=machine.Pin(clock_pin_number), sda=machine.Pin(data_pin_number),
                          freq=50000)
    time.sleep_ms(500) # Short grace period
    
    time.sleep(2)

    # 5. Scan will now succeed instantly
    devices = i2c.scan()
    #print("Devices:", [hex(d) for d in i2c.scan()])
    print(f"@26 Devices: {devices}")
    return devices
    


def scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number, use_pullups=False):
    print(f"SCAN FOR I2C  ----------------------------------------")
    if use_pullups:
        # The SparkFun Soil Moisture Sensor has NO PULLUP RESISTORS.
        # The sensor expects 4.7K from SDA and SCL pins to 3.3v for pullup.
        # This is a cheesey substitute just for testing:
        #   Manually configure pins and turn on the Pico's internal pull-ups
        sda_pin = machine.Pin(data_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        print(f"@20 USING INTERNAL PULLUP resistors on Data, Clock pins")
    else:
        print(f"@22 Using no pullup resistors")
        # for I2C that has internal pullup resistors: don't need external ones
        sda_pin = machine.Pin(data_pin_number, pull=None)
        scl_pin = machine.Pin(clock_pin_number, pull=None)
        #sda_pin = machine.Pin(data_pin_number, machine.Pin.IN, pull=None)
        #scl_pin = machine.Pin(clock_pin_number, machine.Pin.IN, pull=None)
        #sda_pin = machine.Pin(data_pin_number,  machine.Pin.IN, pull=machine.Pin.PULL_UP)
        #scl_pin = machine.Pin(clock_pin_number, machine.Pin.IN, pull=machine.Pin.PULL_UP)
        #sda_pin = machine.Pin(data_pin_number,  machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        #scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        #sda_pin = machine.Pin(data_pin_number,  machine.Pin.OUT, machine.Pin.PULL_UP)
        #scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        #sda_pin = machine.Pin(data_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
        #scl_pin = machine.Pin(clock_pin_number, machine.Pin.OUT, machine.Pin.PULL_UP)
    
    print(f"@26 Create I2C device  {i2c_bus_number=}  {data_pin_number=}  {clock_pin_number=}")

    ###i2c = machine.I2C(i2c_bus_number, sda=sda_pin, scl=scl_pin)
    i2c = machine.I2C(i2c_bus_number, sda=sda_pin, scl=scl_pin, freq=50000)

    print(f"@31 Got I2c device obj: {i2c}")
    
    time.sleep(2); print(" ... sleep for 2 second ...")


    scan_ctr = 0
    while 1:
        scan_ctr += 1
        print(f"@50 Scan #{scan_ctr} for I2C devices...")
    
        # Scan for devices on the I2C bus
        device_addresses = i2c.scan()
        
        if device_addresses:
            break

        if not device_addresses:
            print("@59  *****  No I2C devices found yet... sleeping  *************")
            time.sleep(1)

    print("@42  Found I2C devices at addresses:")
    for device_address in device_addresses:
        # Convert the address to hexadecimal for common representation
        print(hex(device_address))

    for dev_addr in device_addresses:
        try_writing_to_device(i2c, dev_addr)

    print()


def scan_for_i2c_alternate(i2c_bus_number, data_pin_number, clock_pin_number):
    #
    print(f"SCAN FOR I2C ALTERNATE    Uses PULLUP on GPIO pins  ----------------------------------------")
    
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

def try_writing_to_device(i2c, dev_address):
    print(f"@77 WRITE TO DEVICE  {i2c}  {dev_address} ")
    try:
        # Try to write nothing to the device
        # If it throws an I/O error - the device isn't connected
        i2c.writeto(dev_address, bytearray())
        print(f"@82 WRITE was successful.")
    except Exception as ex:
        print(f"@84 EXCEPTION {ex} {str(ex)} ")
    except:
        print(f"@86 UNKNOWN EXCEPTION ")



def main():

    i2c_bus_number = 0
    data_pin_number = 0
    clock_pin_number = 1
    #data_pin_number = 4
    #clock_pin_number = 5

    while 0:
        print("TRY _________________________________")
        devices = cleanup_the_i2c(i2c_bus_number, data_pin_number, clock_pin_number)
        if devices: break
        print("MAIN - wait 2 secs")
        time.sleep(2)

    scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number)
    #time.sleep(1)
    #scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number)

    #scan_for_i2c(i2c_bus_number, data_pin_number, clock_pin_number, True)

    #scan_for_i2c_alternate(i2c_bus_number, data_pin_number, clock_pin_number)

main()


###
