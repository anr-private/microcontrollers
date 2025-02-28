README_SKETCHES.txt

An index of the Arduino sketches

02.Digital
BlinkWithoutDelay     - loop runs continuously - no delay() calls - keeps track of time using millis() to blink an LED
Button  - button pin 2, LED pin 13 (internal LED)  push button to blink LED. Uses digitalRead(), digitalWrite()
          Uses pull-down to force pin 2 to LOW when btn not pushed. Btn forces pin 2 HIGH when pushed.
          - LED attached from pin 13 to ground through 220 ohm resistor
          - pushbutton  pin 2 and +5V
          - 10K resistor pin 2 to ground (pull-down)
Debounce  - btn pin 2, LED 13.  Uses millis() to delay to avoid button bounce.
DigitalInputPullup - btn pin 2, LED 13.  pinMode(INPUT_PULLUP): btn pin is LOW when pushed, HIGH if not.
                                         Vs pinMode(INPUT), which requires pull-down on the button.
                       - pushbutton pin 2 to ground
                       - built-in LED on pin 13
StateChangeDetection - btn pin 2, LED 13. Detect btn state change (edge detect).
toneKeyboard  - force-sense resistors (pressure); 8 ohm spkr pin 8. Uses tone() to play tone based on sensed pressure; analogRead()
toneMelody  - plays a melody 8 ohm spkr pin 8; uses tone(). Runs all in setup(); loop() does nothing.
toneMultiple - plays multiple tones, one tone to each of 3 spkrs (pins 6,7,8). Uses tone(),noTone(), delay()
tonePitchFollower - plays tone (spkr pin 8) based on analogRead() of photoresistor (light sensitive). 
                    Uses map() to convert input to tone freq.

 

### end ###

