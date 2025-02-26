/*
  FadePwm

  This is based on the 'Fade' basic 01 examples 01 basic from Arduino Starter Kit
  modified to fade 3 LEDs up and then down, in sequence. Only 1 LED is 'active'
  at a time.

  The original example shows how to fade an LED on pin 9 using the analogWrite()
  function. 
  This one uses 3 LEDs, on UNO R3 pins 9,10,11.

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
int LED_1  = 9;
int LED_2 = 10;
int LED_3 = 11;

int ACTIVE_LED = -1;

////int led = LED_BUILTIN;     // PIN 13 -- does not typically have PWM capability

// how many points to fade the LED by
int FADE_AMOUNT = 5;    

// The lowest and highest levels ever allowed
int MIN_LEVEL_ALLOWED = 0;
int MAX_LEVEL_ALLOWED = 255;

// The max, min levels that we fade up and down to.
int MAX_LEVEL_1 = 64; // largest usable value is 255;
int MIN_LEVEL_1 = 0;
int MAX_LEVEL_2 = 128; // largest usable value is 255;
int MIN_LEVEL_2 = 0;
int MAX_LEVEL_3 = 255; // largest usable value is 255;
int MIN_LEVEL_3 = 0;
// LED is set to this level after it's been faded up and down
// This leaves enough signal for an oscope to trigger on  - if zero,
// there is no signal, just zero volts, so oscope cannot trigger.
int IDLE_LEVEL = 1;

// the setup routine runs once when you press reset:
void setup() {
  // declare pins to be an output:
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);
  
  Serial.begin(9600);
  Serial.print("  >>> LED Pins: "); 
    Serial.print(LED_1, DEC); Serial.print(" ");
    Serial.print(LED_2, DEC); Serial.print(" ");
    Serial.print(LED_3, DEC); Serial.print(" ");
    Serial.println("  <<<");
  Serial.println(">>> end of SETUP  <<<");
  ////delay(10000);
}

int get_min_level(int led)
{
  int min = MIN_LEVEL_1;
  if (led == LED_2) min = MIN_LEVEL_2;
  if (led == LED_3) min = MIN_LEVEL_3;
  if (min < MIN_LEVEL_ALLOWED) min = MIN_LEVEL_ALLOWED;
  return min;
}
int get_max_level(int led)
{
  int max = MAX_LEVEL_1;
  if (led == LED_2) max = MAX_LEVEL_2;
  if (led == LED_3) max = MAX_LEVEL_3;
  if (max > MAX_LEVEL_ALLOWED) max = MAX_LEVEL_ALLOWED;
  return max;
}


void fade_one_led(int led, int fade_amt)
{
  int max_level = get_max_level(led);
  int min_level = get_min_level(led);
  if (1) {
    Serial.print("Fade LED: "); Serial.print(led,DEC);
    Serial.print("  max="); Serial.print(max_level);
    Serial.print("  min="); Serial.print(min_level);    
    //Serial.print("  brightness: "); Serial.print(brightness, DEC);
    //Serial.println(" <<< bright!");
    Serial.println();
  }

  int level = 0;

  while (1) {
    level += fade_amt;
    if (level >= max_level) {
      Serial.print("  --- fadeup highestLevel="); Serial.print(level, DEC); Serial.print("  max="); Serial.print(max_level, DEC); Serial.println();
      break;
    }
    analogWrite(led, level);
    delay(30);  // slow down to make fading visible
  }
  /*
  for (level = 0; level <= max_level; level += fade_amt) {
    if (level > MAX_LEVEL_ALLOWED) level = MAX_LEVEL_ALLOWED;
    analogWrite(led, level);
    delay(30);  // slow down to make fading visible
  }*/
  
  if (level > MAX_LEVEL_ALLOWED) {
    Serial.print("  --- level>MAX_ALLOWED: level="); Serial.print(level, DEC); Serial.print("  maxAllowed="); Serial.print(MAX_LEVEL_ALLOWED, DEC); Serial.println();
    level = MAX_LEVEL_ALLOWED;
  }
  
  for ( ; level > min_level; level -= fade_amt) {
    analogWrite(led, level);
    delay(30);  // slow down to make fading visible
    analogWrite(led, 1);
  }
  
}

int get_next_led(int active_led)
{
  if (active_led == LED_1) return LED_2;
  if (ACTIVE_LED == LED_2) return LED_3;
  //return LED_3;
  return LED_1;
}

void loop()
{
  ACTIVE_LED = get_next_led(ACTIVE_LED);

  fade_one_led(ACTIVE_LED, FADE_AMOUNT);
  delay(500);


/*  if (ACTIVE_LED == LED_9) {
    ACTIVE_LED = LED_10;
  } else if (ACTIVE_LED == LED_10) {
    ACTIVE_LED = LED_11;
  } else {
    ACTIVE_LED = LED_9;
  }*/
  
}

// ### end ###
