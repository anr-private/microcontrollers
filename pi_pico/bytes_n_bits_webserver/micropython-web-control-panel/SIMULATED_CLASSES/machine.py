# machine.py
#
# This is a simulated version to allow the Pico code to run under Linux
#

def time():
	return 0


class Pin:

    OUT = 0
    
    def __init__(*args, **kwargs):
        """ """
        print(f"Pin class init")


class ADC:
    
    def __init__(*args, **kwargs):
        """ """
        print(f"ADC class init")



### end ###

