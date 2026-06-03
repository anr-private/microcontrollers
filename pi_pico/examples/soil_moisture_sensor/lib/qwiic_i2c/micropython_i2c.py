# micropython_i2c.py
#
# Encapsulate MicroPython port I2C interface
# Written by  oclyke, Feb 2021

from .i2c_driver import I2CDriver

import sys

_PLATFORM_NAME = "MicroPython"

# used internally in this file to get i2c class object 
def _connectToI2CBus(sda=None, scl=None, freq=100000, *args, **argk):
    print(f"mp_i2c.py@14:_connectToI2CBus@14 sda={sda} scl={scl} freq={freq}")
    print(f"mp_i2c.py@15:_connectToI2CBus@15 args={args} kw={argk}")
    try:
        from machine import I2C, Pin
        if sys.platform == 'rp2':
            if sda is not None and scl is not None:
                # I2C busses follow every other pair of pins
                scl_id = (scl // 2) % 2
                sda_id = (sda // 2) % 2
                # Check if both pins are on the same bus
                if scl_id != sda_id:
                    raise Exception("I2C SCL and SDA pins must be on same ports")
                #@@@@@@@@@@@@@@@@return I2C(id=scl_id, scl=Pin(scl), sda=Pin(sda), freq=freq)
                print(f"mp_i2c@27  create I2C: {scl_id=} {scl=} {sda=}  {freq=}  ")
                i2c__obj = I2C(id=scl_id, scl=Pin(scl), sda=Pin(sda), freq=freq)
                print(f"mp_i2c@27  create I2C: obj={i2c__obj}  ")
                return i2c__obj
            else:
                i2c__obj = I2C()
                print(f"mp_i2c.py@29 I2C type is {type(I2C)}")
                print(f"mp_i2c.py@30 I2C name  {I2C.__name__}")
                print(f"mp_i2c.py@30 I2C dir  {dir(I2C)}")
                print(f"mp_i2c.py@31 returns I2C() is {i2c__obj}")
                return i2c__obj

        elif 'xbee' in sys.platform:
            return I2C(id=1, freq=freq)
        elif 'esp32' in sys.platform:
            if sda is not None and scl is not None:
                return I2C(scl=Pin(scl), sda=Pin(sda), freq=freq)
            else:
                return I2C()
        elif 'mimxrt' in sys.platform:
            # Default freq for mimxrt (400k) is too fast for some devices, so we pass freq in
            return I2C(id=0, freq=freq) # TODO: We can remove the id=0 argument once the MicroPython PR #16956 is merged
        else:
            raise Exception("Unknown MicroPython platform: " + sys.platform)
    except Exception as e:
        print(str(e))
        print('error: failed to connect to i2c bus')
    return None

def _connect_to_i2c_bus(*args, **argk):
    return _connectToI2CBus(*args, **argk)


class MicroPythonI2C(I2CDriver):

    # Constructor
    name = _PLATFORM_NAME
    _i2cbus = None

    def __init__(self, sda=None, scl=None, freq=100000, *args, **argk):
        I2CDriver.__init__(self) # init super

        self._sda = sda
        self._scl = scl
        self._freq = freq

        print(f"MPI2C.init@63  sda={self._sda} scl={self._scl} freq={self._freq}  args={args} kw={argk}")

        self._i2cbus = _connectToI2CBus(sda=self._sda, scl=self._scl, freq=self._freq)

    @classmethod
    def isPlatform(cls):
        try:
            return 'micropython' in sys.implementation
        except:
            return False

    @classmethod
    def is_platform(cls):
        return cls.isPlatform()

#-------------------------------------------------------------------------      
    # General get attribute method
    #
    # Used to intercept getting the I2C bus object - so we can perform a lazy
    # connect ....
    #
    def __getattr__(self, name):

        if(name == "i2cbus"):
            return self._i2cbus

        else:
            # Note - we call __getattribute__ to the super class (object).
            return super(I2CDriver, self).__getattribute__(name)

    #-------------------------------------------------------------------------
    # General set attribute method
    #
    # Basically implemented to make the i2cbus attribute readonly to users 
    # of this class. 
    #
    def __setattr__(self, name, value):

        if(name != 'i2cbus'):
            super(I2CDriver, self).__setattr__(name, value)

    # read commands ----------------------------------------------------------
    def readWord(self, address, commandCode):
        if (commandCode == None):
            buffer = self._i2cbus.readfrom(address, 2)
        else:
            buffer = self._i2cbus.readfrom_mem(address, commandCode, 2)

        return (buffer[1] << 8 ) | buffer[0]

    def read_word(self, address, commandCode):
        return self.readWord(address, commandCode)

    def readByte(self, address, commandCode = None):
        if (commandCode == None):
            return self._i2cbus.readfrom(address, 1)[0]

        return self._i2cbus.readfrom_mem(address, commandCode, 1)[0]

    def read_byte(self, address, commandCode = None):
        return self.readByte(address, commandCode)

    def readBlock(self, address, commandCode, nBytes):
        if (commandCode == None):
            return self._i2cbus.readfrom(address, nBytes)

        return self._i2cbus.readfrom_mem(address, commandCode, nBytes)

    def read_block(self, address, commandCode, nBytes):
        return self.readBlock(address, commandCode, nBytes)

    # write commands----------------------------------------------------------
    def writeCommand(self, address, commandCode):
        self._i2cbus.writeto(address, commandCode.to_bytes(1, 'little'))

    def write_command(self, address, commandCode):
        return self.writeCommand(address, commandCode)

    def writeWord(self, address, commandCode, value):
        self._i2cbus.writeto_mem(address, commandCode, value.to_bytes(2, 'little'))

    def write_word(self, address, commandCode, value):
        return self.writeWord(address, commandCode, value)

    def writeByte(self, address, commandCode, value):
        self._i2cbus.writeto_mem(address, commandCode, value.to_bytes(1, 'little'))

    def write_byte(self, address, commandCode, value):
        return self.writeByte(address, commandCode, value)

    def writeBlock(self, address, commandCode, value):
        self._i2cbus.writeto_mem(address, commandCode, bytes(value))

    def write_block(self, address, commandCode, value):
        return self.writeBlock(address, commandCode, value)

    def writeReadBlock(self, address, writeBytes, readNBytes):
        # micropython I2C doesn't have a corresponding "i2c_rdwr" function like smbus2, so we will make our own by passing stop=False to not send stop bits between repeated transfers
        self._i2cbus.writeto(address, bytes(writeBytes), False)
        return self._i2cbus.readfrom(address, readNBytes)
    
    def write_read_block(self, address, writeBytes, readNBytes):
        return self.writeReadBlock(address, writeBytes, readNBytes)

    def isDeviceConnected(self, devAddress):
        print(f"mp_i2c.isDeviceConnected@174  devAddress=0x{devAddress:02X}")

        isConnected = False
        try:
            # Try to write nothing to the device
            # If it throws an I/O error - the device isn't connected
            self._i2cbus.writeto(devAddress, bytearray())
            isConnected = True
        except Exception as ex:
            print(f"mp_i2c.isDeviceConnected@187 EXCEPTION {ex} {str(ex)} ")
        except:
            print(f"mp_i2c.isDeviceConnected@189 UNKNOWN EXCEPTION ")
            raise
            #@@@@@@@@@@@@@@ pass

        return isConnected

    def is_device_connected(self, devAddress):
        return self.isDeviceConnected(devAddress)

    def ping(self, devAddress):
        return self.isDeviceConnected(devAddress)

    # scan -------------------------------------------------------------------
    def scan(self):
        """ Returns a list of addresses for the devices connected to the I2C bus."""
        return self._i2cbus.scan()

###
