# format_specifiers.py

"""
 {var:[fill][align][width]}
 
 fill  char used for padding; space is default
 width minimum total width
 align < ^ > =  (see below)
 
d, i: Signed integer decimal.
o: Signed octal value.
x, X: Signed hexadecimal (lowercase/uppercase).
e, E: Floating-point exponential format (lowercase/uppercase 'e').
f, F: Floating-point decimal format.
g, G: General floating-point format (uses f or e as appropriate).
c: Single character (accepts integer or single character string).
r: String as per calling repr().
s: String as per calling str().
%: A literal percentage character.
b: Binary format.

Fill and Alignment:
    <: Left align.
    >: Right align.
    ^: Center align.
    =: Pad after the sign.
Sign:
    +: Always show sign (+ or -).
    -: Show sign for negative numbers only.
    (space): Space for positive numbers, minus for negative.
Width: A minimum field width as an integer.
Precision: A . followed by an integer for the number of digits after the
  decimal point (for floats) or maximum field size (for strings).
Thousands Separator: The , option is accepted in MicroPython,
  even with non-decimal radixes, although this may not be CPython-compatible in some cases.
Alternate Form: The # specifier adds the appropriate prefix for
  binary (0b), octal (0o), or hexadecimal (0x) output. 
"""

def basic_examples():
    print(f"\n=== BASIC EXAMPLES  =================================")
    ii = 123
    jj = -531
    ff = 135.79
    ss = "A STRING!"
    
    print(f" width 10 default just: '{ii:10}'    {{ii:10}} ")
    print(f" width 10 left justif:  '{ii:<10}'   {{ii:<10}} ")
    print(f" width 10 centered:     '{ii:^10}'   {{ii:^10}} ")
    print(f" width 10 right-justif: '{ii:>10}'   {{ii:>10}} ")
    print(f" width 10 right-justif: '{ii:=10}'   {{ii:=10}} No sign, so equals has no effect.")
    print()
    print(f" width 10 default just: '{jj:10}'    {{jj:10}} ")
    print(f" width 10 left justif:  '{jj:<10}'   {{jj:<10}} ")
    print(f" width 10 centered:     '{jj:^10}'   {{jj:^10}} ")
    print(f" width 10 right-justif: '{jj:>10}'   {{jj:>10}} ")
    print(f" width 10 right-justif: '{jj:=10}'   {{jj:=10}} NOTE sign is at far left due to '='.")
    print()
    print(f" width 10 right-just:   '{jj:@>10}'  {{jj:@>10}}   NOTE jj:_10 fails; you need the '>' or similar")
    print(f" width 10 right-just:   '{jj:.>10}'  {{jj:.>10}}")
    print(f" width 10 right-just::  '{jj:->10}'  {{jj:->10}}   NOTE obscures the '-' sign of the value")
    print(f" width 10 left justif:  '{jj:-<10}'  {{jj:-<10}} ")
    print(f" width 10 left justif:  '{jj:_<10}'  {{jj:_<10}} ")
    print(f" width 10 centered:     '{jj:^10}'   {{jj:^10}} ")
    print(f" width 10 centered:     '{jj:+^10}'  {{jj:+^10}}   NOTE rather odd; hard to see the '-' of the value.")
    print(f" width 10 centered:     '{jj: ^10}'  {{jj: ^10}}   NOTE explicit ' ' as the fill char.")
    print(f" width 10 right-justif: '{jj:>10}'   {{jj:>10}} ")
    print(f" width 10 right-justif: '{jj:=10}'   {{jj:=10}} ")
    print(f" width 10 right-justif: '{jj:-=10}'  {{jj:-=10}}   NOTE obscures the '-' of the value")
    
def variable_spec_examples():
    print(f"\n=== VARIABLE SPEC EXAMPLES  =================================")
    ii = 123
    jj = -531
    ff = 135.79
    ss = "A STRING!"
    
    spec = "^10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = "+^10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = " 10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = "<10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = ">10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = "=10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   ")
    spec = "+=10"
    print(f" width 10 centered:     '{jj:{spec}}'   {{jj:{{spec}}  spec='{spec}'   NOTE: odd!")
    
    
def main():
    basic_examples()
    variable_spec_examples()
    
if  __name__ == "__main__":
    main()
###

