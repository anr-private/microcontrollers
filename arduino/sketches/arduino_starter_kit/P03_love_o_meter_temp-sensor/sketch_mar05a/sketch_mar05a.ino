// project 03  from Arduino starter kit:
// Love-o-meter   
// Uses TMP36 temperature sensor
//
// CIRCUIT:
//  TMP36 sensor connected to +5, gnd, and analog pin A0.
//   Pins are (holding the TMP36 with flat side toward you):
//     left: plus (+5v)    center=sensor output (volts)   right=gnd (0 v)
//  LEDs are connected to gnd on cathode lead (short lead)
//      and anode (long lead) connected to 220 ohm resisor;
//      other side of resistor is connected to digital pin (see below for pin numbers)
//      (or the LED and resistor can be swapped, as long as cathode is toward gnd
//       and anode is toward digital pin)
// 
// OPERATION
// Runs in 2 phases (as usual): setup and loop.
// SETUP:
// Setup samples the temp sensor repeatedly, until the sensor stabilizes.
// I.e., the temperature sensed stabilizes.
// When stabilized, setup ends.
// During setup, the 3 LEDs are lighted in sequence to show setup 
// is active.
// When setup ends, all 3 LEDs are blinked simultaneously.
// LOOP:
// The temp is sensed and its value is used to turn the LEDs on.
// The warmer the sensor reports, the more LEDs are lit.

// Analog pin - connected to TMP36 
const int sensorPin = A0;

// Digital pins 9,10,11 are PWM-capable, but we are not using that herein
const int PIN_1 = 9;
const int PIN_2 = 10;
const int PIN_3 = 11;

const int PINS[] = {PIN_1, PIN_2, PIN_3};
// sizeof() is always 'number of bytes'
const int NUM_PINS = sizeof(PINS) / sizeof(int);

float baselineTemp = 20.0;

void setup() {
  Serial.begin(9600);
  if (1) {
    Serial.print(">>> SETUP   sensorPin="); Serial.print(sensorPin);
    Serial.print("  baselineTemp="); Serial.print(baselineTemp);
    Serial.print("  num-pins="); Serial.print(NUM_PINS);
    Serial.println("  <<<");
  }
  for (int i=0; i < NUM_PINS; i++) {
    int pnum = PINS[i];
    Serial.print("  @@@ i="); Serial.print(i); Serial.print("  pin="); Serial.print(pnum); Serial.println();
    pinMode(pnum, OUTPUT);
    digitalWrite(pnum, LOW);
  }

  Serial.println("Begin sensing the baseline temp.  Curr rawValue="); Serial.println(analogRead(sensorPin));

  while (1) {
    setup__get_temp_baseline();
break;//@@@@@@@
  }

  
  if (1) {
    Serial.println(">>> end of SETUP  <<<");
  }  
}

int setup__get_temp_baseline()
{

  const int num_raw_values = 10;
  int raw_values[num_raw_values]= {0};  // init the values

  setup__get_raw_values(raw_values, num_raw_values);

  dump_raw_values(raw_values, num_raw_values);
}

bool setup__get_raw_values(int raw_values[], int num_raw_values)
{
  int current_led = -999;
  for (int val_num=0; val_num < num_raw_values; val_num++) {
    
    current_led = turn_on_next_led(current_led);

    raw_values[val_num] = analogRead(sensorPin);

    if (1) {
      Serial.print("  @@ loop  rawVal["); Serial.print(val_num); Serial.print("]="); 
      Serial.print(raw_values[val_num]); Serial.println();
    }
    delay(1000);    
  }
  return false;
}

void dump_raw_values(int raw_values[], int num_raw_values)
{
  Serial.println("--- RAW VALUES  ---");
  for (int vn=0; vn < num_raw_values; vn++) {
    Serial.print("  raw["); Serial.print(vn); Serial.print("]=");
    Serial.print(raw_values[vn]);
    Serial.println();
  }
}



void loop() {

  int rawVal = analogRead(sensorPin);
  
  Serial.print("  @@ loop  rawVal="); Serial.print(rawVal); Serial.println();

  delay(3000);
  
}

// Turns off the current LED and turns on the next one
// Returns the new 'currently on' LED number 0..NUM_PINS-1
int  turn_on_next_led(int currently_on)
{
  Serial.print(" @@TURNONNEXT  curr="); Serial.println(currently_on);
  if (currently_on < 0 || currently_on >= NUM_PINS) {
      currently_on = 0;
  }
  // turn off current led
  Serial.print(" @@TURNONNEXT OLD curr="); Serial.println(currently_on);
  digitalWrite(PINS[currently_on], LOW);

  // next led is ...
  currently_on += 1;
  if (currently_on >= NUM_PINS) currently_on = 0;
  Serial.print(" @@TURNONNEXT NEW curr="); Serial.println(currently_on);

  // turn on the new one
  digitalWrite(PINS[currently_on], HIGH);

  return currently_on;
}

  
// ### end ###
