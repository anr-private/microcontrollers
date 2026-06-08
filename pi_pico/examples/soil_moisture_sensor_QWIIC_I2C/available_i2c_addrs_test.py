SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS = 0x28

###############################################################################
###############################################################################
# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_FULL_ADDRESS_LIST = list(range(0x08,0x40))				    	# Full I2C Address List (excluding resrved addresses)
print(f" starting {_FULL_ADDRESS_LIST}")
_FULL_ADDRESS_LIST.remove(SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS) # Remove Default Address of Soil Moisture Sensor from list
_AVAILABLE_I2C_ADDRESS = [SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS]	# Initialize with Default Address of Soil Moisture Sensor
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST)				# Add Full Range of I2C Addresses

print(_AVAILABLE_I2C_ADDRESS)


FAL = list(range(0x08, 0x40))

print(f"  len(FAL)={len(FAL)}   len.avail={len(_AVAILABLE_I2C_ADDRESS)}")
same = FAL == _AVAILABLE_I2C_ADDRESS
print(f" {same=}")

sorted = sorted(FAL) == sorted(_AVAILABLE_I2C_ADDRESS)
print(f" {sorted=}")


for j in FAL:
    if j not in _AVAILABLE_I2C_ADDRESS:
        print(f"  NOT IN AVAIL {j=}")
        
for j in _AVAILABLE_I2C_ADDRESS:
    if j not in FAL:
        print(f"  NOT IN FAL {j=}")
        

###
