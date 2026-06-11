Using ADC input to read values from ADC Capacitive Soil Moisture Sensor
or similar sensor.

ADC_VREF  - physical pin 35. Provide a stable reference voltage for ADC use.
Otherwise ADC relies on 3.3v which may fluctuate as Pico operates.

ADC 0   Gpio 26  physical pin
 0       26       31
 1       27       32
 2       28       34

Use 0.1uF cap on the ADC pin to reduce noise.

Using GPIO23 to switch power converter to PWM can increase accuracy
See force_PWM_mode() function below.

An ADC pin returns values 0..65535 (16 bits).
Actual precision is 0..4095  - 12 bit ADC.
Shifting this >>2 or >>4 can filter noise at the expense of losing
precision.


--- forcing PWM mode in power supply  ----------------------------

def force_PWM_mode():
    # Forces PWM mode in the 3.3v power supply.
    # This prevents the PS from using PFM mode
    # (Pulse freq): PFM mode is more efficient
    # but PWM mode is needed when load on the PS
    # increases. By default the PS will flip
    # between the two modes as needed.

    # GPIO23 controls PWM mode
    # NOTE it is not available as a physical pin on the Pico board.
   # Initialize GPIO23 as an output
    # Using .on() or .value(1) sets it high (3.3V)
    gp23 = machine.Pin(23, machine.Pin.OUT)
    gp23.on()  # or gp23.value(1)
    print("PWM MODE is being forced to reduce power supply noise!")
    ###return gp23



###
