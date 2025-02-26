/*
  ReadAnalogVoltage

  Based on 01.Basic example
  
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/ReadAnalogVoltage

This was based on the ReadAnalogVoltage and FadePwm examples.

  Circuit:  UNO R3
    // For analog input from pot
    10K pot
    Low end = gnd
    High end = 5v
    Wiper = Analog pin A0
    // for analog output to LED:
    Pin-9   220-ohm  LED  gnd
    Pin-10  220-ohm  LED  gnd
    Pin-11  220-ohm  LED  gnd
  Pins 9,19,11 are Pwm capable.

*/

// === ANALOG INPUT FROM 10K Potentiometer ====

int ANALOG_PIN = A0;

// Range of input values from the analog pin
int LOWEST_INPUT = 0;
int HIGHEST_INPUT = 1023;

// If the current and prev differ by this much (or less), ignore the value
int MIN_DIFF = 4;

// previous raw value from analog pin input
int PREV_RAW = -1;


// ANALOG OUTPUT to control LED BRIGHTNESS =====

// UNO R3 pins 9,10,11 are PWM digital
int LED_1  = 9;
int LED_2 = 10;
int LED_3 = 11;

// The lowest and highest levels ever allowed as PWM values
int MIN_LEVEL_ALLOWED = 0;
int MAX_LEVEL_ALLOWED = 255;


// the setup routine runs once when you press reset:
void setup() 
{
  // Analog input requires no setup

  // Analog output setup:
  // declare pins to be an output:
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);

/*  int initial_led_level = 128;
  analogWrite(LED_1, initial_led_level);
  analogWrite(LED_2, initial_led_level);
  analogWrite(LED_3, initial_led_level);*/
  set_led_levels(128);
  
  Serial.begin(9600);
  Serial.println(">>> START SETUP <<<  <<< <<< <<<");
  
  //Serial.print("@@@Analog input pin: "); Serial.println(ANALOG_PIN);
  Serial.print("  >>> ");
  Serial.print("Analog input pin: "); Serial.print(ANALOG_PIN, DEC);
  Serial.print("   LED Pins: "); 
    Serial.print(LED_1, DEC); Serial.print(" ");
    Serial.print(LED_2, DEC); Serial.print(" ");
    Serial.print(LED_3, DEC); Serial.print(" ");
    Serial.println("  <<<");
  ////  delay(10000);

  Serial.println(">>> END of SETUP <<<  <<< <<< <<<");
}

int convert_input_to_pwm_count(int raw_value)
{
  //Convert 0..1023 to 0..255
  return raw_value >> 2;
}

void set_led_levels(int pwm_level)
{
  Serial.print("SET LED LEVELS: pwm_level: "); Serial.print(pwm_level, DEC);
  if (pwm_level < MIN_LEVEL_ALLOWED) pwm_level = MIN_LEVEL_ALLOWED;
  if (pwm_level > MAX_LEVEL_ALLOWED) pwm_level = MAX_LEVEL_ALLOWED;
  Serial.print(" adj pwm_level: "); Serial.print(pwm_level, DEC);
  Serial.println();
  
  analogWrite(LED_1, pwm_level);
  analogWrite(LED_2, pwm_level);
  analogWrite(LED_3, pwm_level);
}

// the loop routine runs over and over again forever:
void loop() {
  
  // read the input on analog pin:
  int raw_value = analogRead(ANALOG_PIN);

  int diff = abs(raw_value - PREV_RAW);
  ////PREV_RAW = raw_value;

  ////Serial.print("diff="); Serial.print(diff, DEC); Serial.println();

  // If the difference between current and previous sensor values is small,
  // ignore the value and wait for a bigger difference.
  if (diff <= MIN_DIFF) {
    delay(0.001);
    return; 
  }
/*
  if (raw_value == ANALOG_PIN) {
    delay(0.001);
    return; 
  }*/
  PREV_RAW = raw_value;

  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  ////float voltage = raw_value * (5.0 / 1023.0);

  int pwm_value = convert_input_to_pwm_count(raw_value);

  // print out the value you read:
  Serial.print(" raw=");
  Serial.print(raw_value);
  Serial.print(" pwm_value=");
  Serial.println(pwm_value);

  set_led_levels(pwm_value);
  
  delay(33);
}
