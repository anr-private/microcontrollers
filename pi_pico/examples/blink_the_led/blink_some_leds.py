# blink_some_leds.py
#
# Blink some leds in order 'chasing lights' style.
# Also blinks the built-in LED on Pico W and Pico2 W.
#
# Normally installed as 'main.py' so it boots when Pico is powered.
# Typical wiring:
#   GPIO pin ->  resistor  ->   (+ LED -)  -> GND
# Normally the + lead is the longer lead of the LED.
# Resistor is 470 or 1K
# Connect the LEDs - as many as desired; add them to the 'leds' tuple

import machine
import utime as time

# board physical pin 18 13 8 3 are GND

gpio10 = 10  # physical 14  
gpio11 = 11  # physical 15  
gpio12 = 12  # physical 16  
gpio13 = 13  # physical 17  
        #      physical 18  GND
gpio14 = 14  # physical 19  
gpio15 = 15  # physical 20  (lower left corner)
gpio16 = 16  # physical 21  (lower right corner)

led10 = machine.Pin(gpio10, machine.Pin.OUT)
led11 = machine.Pin(gpio11, machine.Pin.OUT)
led12 = machine.Pin(gpio12, machine.Pin.OUT)
led13 = machine.Pin(gpio13, machine.Pin.OUT)
led14 = machine.Pin(gpio14, machine.Pin.OUT)
led15 = machine.Pin(gpio15, machine.Pin.OUT)
led16 = machine.Pin(gpio16, machine.Pin.OUT)

builtin_led = machine.Pin("LED", machine.Pin.OUT)


leds = (led11, led12, led13, led14, led15, led16)


def turn_all_off(leds):
    for i in range(len(leds)):
        leds[i].value(0)


def blink_one_led(led):
    while True:
        print(f"Blink led {led}")
        led.value(1)
        time.sleep(1.75)
        led.value(0)
        time.sleep(0.25)

def blink_the_leds(leds):
    lednum = 0
    while True:
        if lednum == 0: builtin_led.toggle()

        led = leds[lednum]
        print(f" {lednum=} {led=} ")

        led.value(1)

        time.sleep(0.5)        

        led.value(0)

        lednum += 1
        if lednum >= len(leds): lednum = 0

def main():    

    print("turn all off")
    turn_all_off(leds)
    
    
    try:
    
        blink_the_leds(leds)
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        turn_all_off(leds)

#main()


blink_one_led(led16)

###