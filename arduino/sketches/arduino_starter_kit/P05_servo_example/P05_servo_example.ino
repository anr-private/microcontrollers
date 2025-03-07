// project 05  from Arduino starter kit:
// "Mood Cue"  uses servo motor to position a pointer showing
// what mood someone is in.
// CIRCUIT:
//  Potentiometer: used 10k
//     ends go to +5 and gnd; center goes to Arduino analog pin A0
//     100uf electrolytic in parallel with ends of the pot
//      (i.e., +5 and gnd - across the pot on the breadboard)
//  Servo:
//    Red to +5.  Black to gnd.  White (or yellow) to Arduino pin 6 (a PWM capable pin)

// Load the 'Servo' library using library mgr.
// Then include:
#include <Servo.h>


// Input from the center wiper of the pot
const int input_pin = A0;

// Output to a PWM pin
const int motor_pin = 6;

// motor object
const Servo servo_obj;

// detect change in input value
int prev_inp_val = -9999;


void setup() 
{
  servo_obj.attach(motor_pin);

  Serial.begin(9600);
  if (1) {
    Serial.print(">>> SETUP   inputPin="); Serial.print(input_pin);
    Serial.print(">>> SETUP   motorPin="); Serial.print(motor_pin);
    Serial.println("  <<<");
  }

  if (1) {
    Serial.println(">>> end of SETUP  <<<");
  }  
}

void loop() 
{
  if (0) {
    Serial.println("+++ LOOP begins +++");
  }

  // 0..1023
  const int inp_val = analogRead(input_pin);

  if (0) {
    Serial.print("  LOOP inputVal="); Serial.print(inp_val); Serial.println();
  }

  const int angle = map(inp_val, 0, 1023, 0, 179);

  // show some of the data - but not all, there is some jitter in the input vals
  if (abs(inp_val - prev_inp_val) > 1) {
    Serial.print("  LOOP inputVal="); Serial.print(inp_val); 
    Serial.print("  motorAngle="); Serial.print(angle);
    Serial.println();
    prev_inp_val = inp_val;
  }

  servo_obj.write(angle);

  delay(15);
}
