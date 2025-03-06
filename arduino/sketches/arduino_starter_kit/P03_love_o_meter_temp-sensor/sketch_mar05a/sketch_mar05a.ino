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

const bool DBG_GRV = false;
const bool DBG_TONL = false;


// === GLOBAL VARS  ==============

int raw_baseline = 0;

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
    //Serial.print("   i="); Serial.print(i); Serial.print("  pin="); Serial.print(pnum); Serial.println();
    pinMode(pnum, OUTPUT);
    digitalWrite(pnum, LOW);
  }

  //Serial.print("Begin sensing the baseline temp.  Curr rawValue="); Serial.println(analogRead(sensorPin));

//  while (1) {
    raw_baseline = setup__get_temp_baseline();
//break;//@@@@@@@
//  }
  Serial.print("Setup: rawBaseline="); Serial.println(raw_baseline);
  blink_leds();


  
  if (1) {
    Serial.println(">>> end of SETUP  <<<");
  }  
}

int setup__get_temp_baseline()
{

  const int num_raw_values = 6;
  int raw_values[num_raw_values]= {0};  // init the values

  setup__get_raw_values(raw_values, num_raw_values);

  dump_raw_values(raw_values, num_raw_values);

  // average raw
  int raw_sum = 0;
  for (int val_num=0; val_num < num_raw_values; val_num++) {
    raw_sum += raw_values[val_num];
  }
  int raw_avg = (raw_sum + num_raw_values -1) / num_raw_values;

  Serial.print("  get_temp_baseline:  num_raw_values="); Serial.print(num_raw_values);
  Serial.print("  total="); Serial.print(raw_sum); 
  Serial.print("  avg="); Serial.print(raw_avg);
  Serial.println();

  return raw_avg;
}

bool setup__get_raw_values(int raw_values[], int num_raw_values)
{
  Serial.println("@@@@ get raw values");
  
  int current_led = -999;
  for (int val_num=0; val_num < num_raw_values; val_num++) {
    
    current_led = turn_on_next_led(current_led);

    raw_values[val_num] = analogRead(sensorPin);

    if (DBG_GRV) {
      Serial.print("  @@GET_RAW_VALUES  rawVal["); Serial.print(val_num); Serial.print("]="); 
      Serial.print(raw_values[val_num]); Serial.println();
    }
    delay(700);    
  }
  Serial.println("@@@@ EXIT from get raw values");
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
  Serial.println("  ------------------------------");
}



void loop() {

  Serial.println(); Serial.println("LOOP begins Now -----");
  
  int raw_value = analogRead(sensorPin);

  int delta_raw = abs(raw_value - raw_baseline);

  show_leds_for_raw(delta_raw);

  float temp = raw_to_degrees_C(raw_value);
  
  Serial.print("  LOOP  rawValue="); Serial.print(raw_value);
  Serial.print("  baseline="); Serial.print(raw_baseline);
  Serial.print("  deltaRaw="); Serial.print(delta_raw);
  Serial.println();

  delay(4000);
  
}

// Turn on LEDs based on the difference between raw baseline
// and current value ie the raw_delta;
void show_leds_for_raw(int delta_raw)
{
  // Relative delta values for each pin
  int LED_THRESHOLD[NUM_PINS] = {0, 0, 9};
  
  for (int i=0; i < NUM_PINS; i++) {
    int thresh = LED_THRESHOLD[i];
    bool turn_on = (delta_raw >= thresh);
    if (1) {
      Serial.print("  show_leds_for_raw  raw="); Serial.print(delta_raw);
      Serial.print("  threshold for pin["); Serial.print(i); Serial.print("]="); Serial.print(thresh);
      Serial.print(". Turn on=");Serial.print(turn_on);
      Serial.println();
    }
    ///int pnum = PINS[i];
    turn_led_on_if(i, turn_on);
  }
}

// Convert raw value to volts, then to degrees Celsius
 //  DATASHEET info for TMP36
 //  Low voltage operation (Vcc range 2.7 V to 5.5 V)
 //  Calibrated directly in °C
 //  10 mV/°C scale factor (20 mV/°C on TMP37)
 //  ±2°C accuracy over temperature (typ)
 //  ±0.5°C linearity (typ)
 //  Stable with large capacitive loads
 //  Specified −40°C to +125°C, operation to +150°C
 //  Less than 50 µA quiescent current
 //  Shutdown current 0.5 µA max
 //  Low self-heating
 //  Qualified for automotive applications
float raw_to_degrees_C(int raw_value)
{
  // Sensor is being fed Vcc of 5v, so output is 0..5v
  // Sensor raw values are 0..1023  (10 bit)
  // Scale the 10 bit raw to 0..5v
  float volts = (raw_value / 1024.0) * 5.0;

  // Sensor is 10mV per deg C
  // Its low end is below 0 deg C, so need to subtract that bias
  float temp = (volts - 0.5) * 100;

  if (1) {
    Serial.print("  Cvt to temp:  raw="); Serial.print(raw_value);
    Serial.print("  volts="); Serial.print(volts);
    Serial.print("  temp="); Serial.print(temp); Serial.print(" degs C");
    Serial.println();
  }
  return temp;
}


// === LED functions  ==========================================

// Set all LEDs on or off
void set_all_leds(bool turn_on)
{
  for (int i=0; i < NUM_PINS; i++) {
    turn_led_on_if(i, turn_on);
    ////int pnum = PINS[i];
    ////if (turn_on) {
    ////  digitalWrite(i, HIGH);
    ////} else {
    ////  digitalWrite(i, LOW);
    ////}
  }
}

void blink_leds()
{
  for (int i=0; i < 3; i++) {
    set_all_leds(true);
    delay(250);
    set_all_leds(false);
    delay(200);
  }
}

void turn_led_on_if(int led_num, bool turn_on)
{
  if (turn_on) {
    turn_on_led(led_num);
  } else {
    turn_off_led(led_num);
  }
}

// Given LED number (relative number, 0..N-1) - not the actual Arduino pin#
void turn_on_led(int led_num)
{
    int pnum = PINS[led_num];
    digitalWrite(pnum, HIGH);
}
// Given LED number (relative number, 0..N-1) - not the actual Arduino pin#
void turn_off_led(int led_num)
{
    int pnum = PINS[led_num];
    digitalWrite(pnum, LOW);
}


// Turns off the current LED and turns on the next one
// Returns the new 'currently on' LED number 0..NUM_PINS-1
int  turn_on_next_led(int currently_on)
{
  if (DBG_TONL) { Serial.print(" @@TURNONNEXT  curr="); Serial.println(currently_on);}
  
  if (currently_on < 0 || currently_on >= NUM_PINS) {
      currently_on = 0;
  }
  // turn off current led
  if (DBG_TONL) { Serial.print(" @@TURNONNEXT OLD curr="); Serial.println(currently_on); }
  digitalWrite(PINS[currently_on], LOW);

  // next led is ...
  currently_on += 1;
  if (currently_on >= NUM_PINS) currently_on = 0;
  if (DBG_TONL) { Serial.print(" @@TURNONNEXT NEW curr="); Serial.println(currently_on); }

  // turn on the new one
  digitalWrite(PINS[currently_on], HIGH);

  return currently_on;
}

  
// ### end ###
