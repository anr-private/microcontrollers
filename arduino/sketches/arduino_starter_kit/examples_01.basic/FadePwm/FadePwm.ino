/*
  FadePwm

  This is based on the 'Fade' basic 01 examples 01 basic from Arduino Starter Kit

  This example shows how to fade an LED on pin 9 using the analogWrite()
  function.

  The analogWrite() function uses PWM, so if you want to change the pin you're
  using, be sure to use another PWM capable pin. On most Arduino, the PWM pins
  are identified with a "~" sign, like ~3, ~5, ~6, ~9, ~10 and ~11.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Fade
  Circuit:  Uno R3 
    Pin-9   220-ohm  LED  gnd
    Pin-10  220-ohm  LED  gnd
    Pin-11  220-ohm  LED  gnd
  Pins 9,19,11 are Pwm capable.
 
*/

// UNO R3 pins 9,10,11 are PWM digital
int led9 = 9;
int led10 = 10;
int led11 = 11;

////int led = LED_BUILTIN;     // PIN 13 -- does not typically have PWM capability
int brightness = 0;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

// the setup routine runs once when you press reset:
void setup() {
  // declare pins to be an output:
  pinMode(led9, OUTPUT);
  pinMode(led10, OUTPUT);
  pinMode(led11, OUTPUT);
  Serial.begin(9600);
  Serial.print("  >>> LEDs: "); 
    Serial.print(led9, DEC); Serial.print(" ");
    Serial.print(led10, DEC); Serial.print(" ");
    Serial.print(led11, DEC); Serial.print(" ");
    Serial.println("  <<<");
  Serial.println(">>> end of SETUP  <<<");
  ////delay(10000);
}

// the loop routine runs over and over again forever:
void loop() {
  // set the brightness of pin 
  //Serial.println("brightness=" + brightness);

  Serial.print(brightness, DEC);
  Serial.println(" <<< bright!");
  
  analogWrite(led9, brightness);
  analogWrite(led10, brightness);
  analogWrite(led11, brightness);

  // change the brightness for next time through the loop:
  brightness = brightness + fadeAmount;

  // reverse the direction of the fading at the ends of the fade:
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }
  // wait for 30 milliseconds to see the dimming effect
  delay(30);

  if (brightness <=  0) {
     //delay(5000);
  }
  
}
