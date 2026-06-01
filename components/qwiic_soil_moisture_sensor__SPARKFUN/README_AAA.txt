Downloaded library, examples, etc from Sparkfun

  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/
  https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html

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

