README_AAA.txt


ABANDONED this sensor

It uses ATtiny85 microprocessor and is too old and slow to do i2c reliably.
Did several tests and could not get the sensor to respond on i2c reliably.
Trying instead:
  Adafruit STEMMA sensor
https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor

Analog Capacitive Soil Moisture Sensor v1.2.


=================================================================================
SparkFun Capacitive Soil Moisture Sensor

(Not the resistance sensor!)

Downloaded library, examples, etc from Sparkfun

  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/
  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html


Default I2C address:  0x37   but code shows 0x28 (for resistance sensor)

NOTE that the sensor does not provide PULLUP resistors on its SDA and SCL pins.
So you need to add 4.7K pullup resistors from the GPIO pins to Vcc 3.3v
else the pins will not read the data and clock correctly.
As a kluge for testing, you can use:
    sda_pin = machine.Pin(DATA_PIN, machine.Pin.OUT, machine.Pin.PULL_UP)
    scl_pin = machine.Pin(CLOCK_PIN, machine.Pin.OUT, machine.Pin.PULL_UP)
where DATA_PIN, CLOCK_PIN are 0,1 or 4,5 or etc.
NOTE you must specify the correct I2C bus (0 or 1) when you call
machine.I2C(BUS#, pins...)!
See pi_pico/examples/i2c_tools/scan_i2c_tool.py for example.

---- How I Installed ---------------------------------------

On an 'empty Pico 2:  did this install using mpremote (default Ubuntu version worked ok, did not create a venv to get newest mpremote)
  
    mpremote mip install github:sparkfun/qwiic_soil_moisture_sensor_py

It installed in the lib/ dir on the pico:
   lib/
     qwiic_soil_moisture_sensor.py
     qwiic_i2c/
        __init__.py
        i2c_driver.py
        micropython_i2c.py
Added these to lib/ in the Maranr Watering System py/lib/

Manually copied them to the examples dir:
   ~/git/microcontrollers/pi_pico/examples/soil_moisture_sensor
Also copied examples to the above dir. Copied from here:
   ~/git_not_mine/qwiic_soil_moisture_sensor_py_SPARKFUN/qwiic_soil_moisture_sensor_py/examples

--- Running the SOIL MOISTURE SENSOR examples.

See details in sections below. Ran the examples in this dir,
created as noted above:
   ~/git/microcontrollers/pi_pico/examples/soil_moisture_sensor

It is set up with a lib/ dir like this:
   /lib:
     -rw-rw-r-- 1 art art 6075 May 31 21:20 qwiic_soil_moisture_sensor.py
   
   ./lib/qwiic_i2c:
      -rw-rw-r-- 1 art art 11072 May 31 21:20 i2c_driver.py
      -rw-rw-r-- 1 art art  6326 May 31 21:20 __init__.py
      -rw-rw-r-- 1 art art  7371 May 31 21:20 micropython_i2c.py
The Example*py are at the top level (at same level as lib/).

To download all to the Pico:
Right-click on lib/; choose 'Upload to /'. This creates lib/ and lib/qwiic_i2c/
on the pico.
Right-click on an Example...py file and choose Upload to /.




Loaded the 





--- GITHUB soil moisture sensor ---------------------------------------

git clone  git@github.com:sparkfun/qwiic_soil_moisture_sensor_py.git

Install using mpremote:
    mpremote mip install github:sparkfun/qwiic_soil_moisture_sensor_py


See README in examples/ subdir.
It lists these links (see docs_web_pages/ subdir for copies of the pages):
   https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#ad3b91fdbd9f8190798af7ee2227d4d63

  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#a344fb9aa9120ca97555afc052aa94aa4

  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#a9799401c60ab796e346a49718a98f601

--- GITHUB qwiic I2C  --------------------------------------------

git clone git@github.com:sparkfun/Qwiic_I2C_Py.git

Saved here:
  ~/git_not_mine/qwiic_i2c

mpremote install
   mpremote mip install github:sparkfun/qwiic_i2c_py


--- QWIIC CABLE and wiring

QWIIC cable 
  VCC 3.3v      RED
  GND           BLACK
  SDA data      BLUE
  SCL clock     YELLOW



###

