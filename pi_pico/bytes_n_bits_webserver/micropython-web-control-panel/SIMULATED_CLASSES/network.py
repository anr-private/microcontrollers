# network.py
#
# This is a simulated version to allow the Pico code to run under Linux

STAT_IDLE = 0

STA_IF = 0

STAT_CONNECTING = 0


class WLAN:
    """ """
    def __init__(*args, **kwargs):
        """ """
        print(f"WLAN class init")

    def active(*args):
        return True

    def connect(*args):
        return True

    def status(*args):
        return True


### end ###

