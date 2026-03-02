# mws_wifi.py
#
# handle connecting to Wifi

#@@@@@ FIXES FOR WIFI
#Disable Power-Save Mode: By default, the Pico W uses aggressive power-saving, which can cause connection drops. Use wlan.config(pm = 0xa11140) to keep the radio active.
#Robust Reconnection Loop: Do not assume wlan.connect() works permanently. Implement a while not wlan.isconnected(): loop with time.sleep() to check status and re-initiate connection.
#Handle DHCP Timeouts: The Pico W might fail to get an IP quickly. Add a timeout to your connection script; if it doesn't connect within 10-20 seconds, deactivate (wlan.active(False)) and reactivate the interface before trying again.

import network
import utime
import ntptime

from details import SSID, PW
#from utils import *
import lib.utils as utils
from logger.LoggerABC import LoggerABC

log = None
log_name_ = "None"

logrt = None
logi = None

ssid = SSID
password = PW

class MwsWifi(LoggerABC):
    
    _instance = None

    @classmethod
    def _get_logger(cls): global log; return log
    @classmethod
    def _get_logger_name(cls): global log_name_; return log_name_
    @classmethod
    def _set_logger(cls, newlog, new_name):
        global log, log_name_; log = newlog; log_name_ = new_name
    @classmethod
    def _set_logger_rt(cls, newlog_rt):
        global logrt; logrt = newlog_rt
    @classmethod
    def _set_logger_important(cls, newlog_important):
        global logi; logi = newlog_important

    @classmethod
    def get_instance(cls):
        if MwsWifi._instance is None:
            MwsWifi._instance = MwsWifi(1234567)
        return MwsWifi._instance


    def __init__(self, do_not_call_directly):
        if do_not_call_directly != 1234567:
            raise RuntimeError("EasyLogger.init DO NOT CALL")
        super().__init__()
        self.init_logger()


    def connect_to_wifi(self, show_details=True):
        """ Connect to the WIFI WLAN.
        Return a wlan obj if successful else exception.
        """
        
        logi(f"MwsWifi@29 CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
        
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
        logi(f"MwsWifi@35   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
    
        max_wait = 30 # Timeout in seconds
        num_tries = 0
        while num_tries < max_wait:
            wlan_status = wlan.status()
            logi(f"MwsWifi@42 waiting...  wlan_status={wlan_status}")
            if wlan_status < 0 or wlan_status >= 3:
                break
            num_tries += 1
            logi(f"MwsWifi@46 Waiting for connection...   num_tries={num_tries}  max={max_wait}")
            utime.sleep(1)
        logi(f"MwsWifi@48 wlan.status() = {wlan.status()}")
        
        if wlan.status() != 3:
            wlan.disconnect() # ignored if not connected
            raise RuntimeError(f"Network connection failed. wlan.status={wlan_status}")
    
        if show_details:
            logi(f"Connected to wlan {ssid}")
            info = wlan.ifconfig()
            ip_addr = info[0]
            logi(f"  IP={ip_addr}")
            # typical output: INFO: ('192.168.1.49', '255.255.255.0', '192.168.1.1', '192.168.1.1')
            ###logi(f"  INFO: {info}")
        
        return wlan, ip_addr


    def wifi_set_time_from_ntp(self, wlan):
    
        try:
            ntptime.settime()
        except Exception as ex:
            m = f"MwsWifi@70 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}"
            logi(m)
            return False
    
        # verify the time
        current_time = utime.localtime()
    
        # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
        # (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday is 0=Sun, etc
        logi(f"MwsWifi@81 TIME FROM NTP: {current_time} ") # as tuple
        year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
        logi(f"MwsWifi@83 {year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
        weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
        logi(f"MwsWifi@85   {weekday_stg=}")
    
        return True

###
