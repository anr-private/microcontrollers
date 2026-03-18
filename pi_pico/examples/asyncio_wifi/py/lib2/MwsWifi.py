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
import asyncio
try:
    import utime as time
except Exception:
    import time

from lib.utils import MWS_CONFIG
from details import SSID, PW
from logger_elem.ElemLoggerABC import ElemLoggerABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


ssid = SSID
password = PW

OUR_PORT_NUMBER = 8000


class MwsWifi(ElemLoggerABC):
    
    _instance = None


    @classmethod
    def get_instance(cls):
        if MwsWifi._instance is None:
            MwsWifi._instance = MwsWifi(1234567)
        return MwsWifi._instance


    def __init__(self, do_not_call_directly):
        if do_not_call_directly != 1234567:
            raise RuntimeError("MwsWifi.init DO NOT CALL")
        self.wlan = None
        self._ipaddr = None
        self._port = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsWifi@47 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def wifi_task(self):
        print(f"WIFI@61 TASK STARTED!")

        sleep_secs = 0
        status_retries = 999
        CTR = 8
        while 1:
            if sleep_secs > 0:
                print(f"WIFI@65 task sleeping {sleep_secs} secs")
                await asyncio.sleep(sleep_secs)
            sleep_secs = 1   # default

            print(f"MwsWifi@77   CTR is {CTR} _________________________________")
            if CTR < 0:
                if self.wlan is not None: 
                    self.wlan.active(False)
                    print(f"MwsWifi@79  _____________******************* SIMULATE DISCONNECT")
                else:
                    print(f"MwsWifi@79  _____________******************* CANNOT SIMULATE DISCONNECT")

                CTR = 8
            CTR -= 1

            if self.wlan is None:
                self._create_wlan_obj()
                status_retries = 30
                continue

            if status_retries > 0:
                if self.wlan.status() == 3:
                    # Got a good status - done waiting.
                    status_retries = 0
                    self._set_ipaddr_and_port()
                    continue
                # Give up?
                status_retries -=1
                if status_retries <= 0:
                    status_retries = 0
                    print(f"WIFI@92 Giving up on waiting for status==3 - start over")
                    self._nullify_connection_state()
                    continue

            # Check if we're still connected
            if not self.wlan.isconnected():
                print(f"MwsWifi@106 *** LOST OUR WIFI CONNECTION ***.   Start over.")
                self._nullify_connection_state()
                sleep_secs = 4
                continue

            print(f"WIFI@110 wifi is connected ok")
            sleep_secs = 4 #$$$$$


    def _create_wlan_obj(self):
        self._nullify_connection_state()
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # Connect
        logi(f"MwsWifi@87   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
        self.wlan = wlan 

    def _nullify_connection_state(self):
        self._ipaddr = None
        self._port = None
        wlan = self.wlan
        self.wlan = None
        # Clean up if possible
        if wlan is not None:
            #@@@@@@@@@@@@@@@@$$$$$$$$$$$$ ADD try/except
            wlan.active(False)
            wlan.disconnect()

    def _set_ipaddr_and_port(self):
        info = self.wlan.ifconfig()
        self._ipaddr = info[0]
        self._port = OUR_PORT_NUMBER
        print(f"MwsWifi@73  CONNECTED: IP={self._ipaddr} PORT={self._port} ")

######################################################################


    def ___OLD_connect_to_wifi(self, show_details=True):
        """ Connect to the WIFI WLAN.
        Return a wlan obj if successful else exception.
        """
        
        logi(f"MwsWifi@58 CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
        
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
        logi(f"MwsWifi@64   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
    
        max_wait = 30 # Timeout in seconds
        num_tries = 0
        while num_tries < max_wait:
            wlan_status = wlan.status()
            logi(f"MwsWifi@71 waiting...  wlan_status={wlan_status}")
            if wlan_status < 0 or wlan_status >= 3:
                break
            num_tries += 1
            logi(f"MwsWifi@75 Waiting for connection...   num_tries={num_tries}  max={max_wait}")
            utime.sleep(1)
        logi(f"MwsWifi@77 wlan.status() = {wlan.status()}")
        
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


    def ___OLD__wifi_set_time_from_ntp(self, wlan):
    
        try:
            ntptime.settime()
        except Exception as ex:
            m = f"MwsWifi@99 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}"
            logi(m)
            return False
    
        # verify the time
        current_time = utime.localtime()
    
        # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
        # (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday is 0=Sun, etc
        logi(f"MwsWifi@109 TIME FROM NTP: {current_time} ") # as tuple
        year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
        logi(f"MwsWifi@111 {year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
        weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
        logi(f"MwsWifi@113   {weekday_stg=}")
    
        return True

###
