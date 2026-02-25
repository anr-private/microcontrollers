README_EasyLogger.txt
# Provides support for logging using a simple 'log(s:str)' function.
# It allows control logging on/off by making requests to the 
# logging module that is used together with this Abstract Base Class (ABC).
# You control how a class logs by requesting the logger to
# enable or disable logging. The request includes (1) the name
# of the class (str) and a flag (bool) with these values:
#    True   enable logging
#    False  disable (mute) logging
#    None   get the current logging status for the class
# This LoggerABC class allows a class to subclass it and
# so participate in logging control.
# The subclass ('user class') needs to include/implement a 
# few items; these are minimized to reduce clutter in the subclass.
#
# The control scheme uses a module-level variable to point to the 
# logging function 'log(s:str)'. The variable is normally named
# 'log'. It points to a function found in the logger module; 
# the function either performs logging or is a 'mute' logger,
# meaning it ignores requests to log (so 'disables' logging).
# The mute logger function just returns and does nothing else.
#
# The approach uses a base class ABC that has most of the code.
# The LoggerABC below is that base class.
# Most of the work is done by class-method's defined in LoggerABC.
# This allows controlling all instances of a user class as a group;
# the name of the user class is used when making requests to the
# logging module to enable/disable logging.
# This simplifies control: any and all instances of the user class
# respond to the enable/disable of logging as a group rather than
# individually instance by instance.
#
# To participate, a user subclass must do the following items;
# they are shown in the typical order in which they are found
# in the source file of the user class (MyClass, in this example):
#  # Items in file MyClass.py:
#    # import the ABC class
#       import LoggerABC
#    # Provide a module-global variable 'log' which is declared
#    # in the subclass module but before the subclass itself is declared.
#       log = None
#    # subclass the ABC
#       class MyClass(LoggerABC):
#          ...
#    # In MyClass.__init__, call set_logger(True) to enable logging.
#        def __init__(...)
#           self.set_logger(True)
#    # Provide 2 methods:
#      def _get_logger(self): global log; return log
#      def _set_logger(self, newlog): global log; log = newlog
# Then the subclass can do logging very simply:
#         log(f"some message {some_var}")
#
# NOTE that the subclass DOES NOT NEED TO IMPORT the 'logger' module;
# only LoggerABC does 'import logger'.
#
# Sidebar:
# The subclass has the option of not performing the 
# call to set_logger(True). Instead it can import the logger
# and set the module-level variable 'log' like this:
#     log = logger.dbg_dbg_
# NOTE THIS IS NOT RECOMMENDED as it exposes the logger.dbg_dbg_
# method, which is supposed to be used only by the base class.
