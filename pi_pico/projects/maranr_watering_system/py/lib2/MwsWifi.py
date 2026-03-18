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
from lib2.DataBoard import DataBoard
from details import SSID, PW
from logger_elem.ElemLoggerABC import ElemLoggerABC

# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None


ssid = SSID
password = PW

OUR_PORT_NUMBER = 8000

class _State:
    def __init__(self):
        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        self.restarts_counter = 0

    def nullify(self):
        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        
    def __str__(self):
        s = []
        s.append("state=%s" % str(self.state))
        s.append("wlan=%s" % str(self.wlan))
        s.append("sleepSecs=%s" % str(self.sleep_secs))
        s.append("retries=%s" % str(self.status_retries))
        s.append("restarts_counter=%s" % str(self.restarts_counter))

        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))



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
        #@@@@@$$$$$self.wlan = None
        self._dataBoard = DataBoard.get_instance()
        self._ipaddr = None
        self._port = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsWifi@82 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def wifi_task(self):
        print(f"nMwsWifi@89 TASK STARTED!")

        st = _State()

        states = {
            0:  self._state_zero,
            1:  self._state_init,
            2:  self._state_create_wlan_obj,
            3:  self._state_status_wait,
            4:  self._state_check_connected,
            }


        while 1:
            print(f"\nMwsWifi@103 STATE: {st}")

            state_callable = states.get(st.state, self._no_such_state)

            next_state = state_callable(st)

            # Zero means repeat the state
            if next_state == 0: next_state = st.state

            print(f"MwsWifi@114  next_state={next_state}")
            if next_state not in states:
                print(f"MwsWifi@116  No such state {next_state}  - RESTART!")
                self._nullify_connection_state(st)
                next_state = 1

            st.state = next_state

            if st.sleep_secs > 0:
                print(f"MwsWifi@123 task sleeping {st.sleep_secs} secs   {st}")
                await asyncio.sleep(st.sleep_secs)
                # set back to default
                st.sleep_secs = 1


    def _state_zero(self, st):
        print(f"MwsWifi@130  SHOULD NEVER ENTER STATE ZERO!  {st}")
        return 1

    def _state_init(self, st):
        print(f"MwsWifi@134  (RE) INITIALIZE   {st}")
        self._nullify_connection_state(st)
        st.restarts_counter += 1
        st.sleep_secs = 0
        return 2

    def _state_create_wlan_obj(self, st):
        #@@@@@self._nullify_connection_state(st)
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # Connect
        logi(f"MwsWifi@144   Connect to wifi: ssid='{ssid}'")
        ###print(f"MwsWifi@145   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
        st.wlan = wlan
        st.status_retries = 30
        return 3

    def _state_status_wait(self, st):
        st.status_retries -= 1
        if st.status_retries <= 0:
            print(f"MwsWifi.148  STATUS RETRIES EXHAUSTED. Restart")
            return 1

        status = st.wlan.status()
        print(f"MwsWifi@158  wlan.status = {status} ")

        if status != 3:
            # keep trying
            return 0

        # Got a good status. Move to the next state
        print(f"MwsWifi@165  Status-Wait GOT GOOD-CONNECTION STATUS  {st}")
        self._set_ipaddr_and_port(st.wlan)
        st.status_retries = 0
        return 4

    def _state_check_connected(self, st):
        # See if still connected
        if st.wlan.isconnected():
            print(f"MwsWifi@173 STILL CONNECTED  {self._ipaddr} {self._port}")
            st.sleep_secs = 3
            return 0
        print(f"MwsWifi@176 *** LOST OUR CONNECTION  ****  {st}")
        return 1


    def _no_such_state(self, st):
        print(f"MwsWifi@181 ILLEGAL STATE! {st}")
        ###$$$$ return 1
        raise RuntimeError(f"MwsWifi@183 ILLEGAL STATE {st}")
        sys.exit(1) #$$$$$$$$$$$$$$$$$$


    def _nullify_connection_state(self, st):
        print(f"MwsWifi@188  NULLIFY - STARTING OVER")
        self._ipaddr = None
        self._port = None
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        wlan = st.wlan
        st.nullify()
        # Clean up if possible
        if wlan is not None:
            #@@@@@@@@@@@@@@@@$$$$$$$$$$$$ ADD try/except
            wlan.active(False)
            wlan.disconnect()

    def _set_ipaddr_and_port(self, wlan):
        info = wlan.ifconfig()
        self._ipaddr = info[0]
        self._port = OUR_PORT_NUMBER
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        print(f"MwsWifi@203  CONNECTED: IP={self._ipaddr} PORT={self._port} ")


######################################################################
######################################################################
######################################################################

    def OLDSTUFF(self):

        CTR = 8
        while 1:
            if sleep_secs > 0:
                print(f"nMwsWifi@65 task sleeping {sleep_secs} secs")
                await asyncio.sleep(sleep_secs)
            sleep_secs = 1   # default

            print(f"MwsWifi@219   CTR is {CTR} _________________________________")
            if CTR < 0:
                if self.wlan is not None: 
                    self.wlan.active(False)
                    print(f"MwsWifi@223  _____________******************* SIMULATE DISCONNECT")
                else:
                    print(f"MwsWifi@225  _____________******************* CANNOT SIMULATE DISCONNECT")

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
                    print(f"nMwsWifi@92 Giving up on waiting for status==3 - start over")
                    self._nullify_connection_state()
                    continue

            # Check if we're still connected
            if not self.wlan.isconnected():
                print(f"MwsWifi@251 *** LOST OUR WIFI CONNECTION ***.   Start over.")
                self._nullify_connection_state()
                sleep_secs = 4
                continue

            print(f"nMwsWifi@110 wifi is connected ok")
            sleep_secs = 4 #$$$$$



######################################################################


    def ___OLD_connect_to_wifi(self, show_details=True):
        """ Connect to the WIFI WLAN.
        Return a wlan obj if successful else exception.
        """
        
        logi(f"MwsWifi@269 CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
        
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
        logi(f"MwsWifi@275   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
    
        max_wait = 30 # Timeout in seconds
        num_tries = 0
        while num_tries < max_wait:
            wlan_status = wlan.status()
            logi(f"MwsWifi@282 waiting...  wlan_status={wlan_status}")
            if wlan_status < 0 or wlan_status >= 3:
                break
            num_tries += 1
            logi(f"MwsWifi@286 Waiting for connection...   num_tries={num_tries}  max={max_wait}")
            utime.sleep(1)
        logi(f"MwsWifi@288 wlan.status() = {wlan.status()}")
        
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
            m = f"MwsWifi@310 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}"
            logi(m)
            return False
    
        # verify the time
        current_time = utime.localtime()
    
        # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
        # (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday is 0=Sun, etc
        logi(f"MwsWifi@320 TIME FROM NTP: {current_time} ") # as tuple
        year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
        logi(f"MwsWifi@322 {year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
        weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
        logi(f"MwsWifi@324   {weekday_stg=}")
    
        return True

###
