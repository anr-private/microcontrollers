/*
  ReadAnalogVoltage

  Based on 01.Basic example
  
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/ReadAnalogVoltage

  Circuit:  UNO R3
    10K pot
    Low end = gnd
    High end = 5v
    Wiper = Analog pin A0
*/

int ANALOG_PIN = A0;

// If the current and prev differ by this much (or less), ignore the value
int MIN_DIFF = 4;

// previous raw value from analog pin input
int PREV_RAW = -1;

// the setup routine runs once when you press reset:
void setup() {
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
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
  float voltage = raw_value * (5.0 / 1023.0);

  // print out the value you read:
  Serial.print(" raw=");
  Serial.print(raw_value);
  Serial.print(" V=");
  Serial.println(voltage);

  delay(333);
}
