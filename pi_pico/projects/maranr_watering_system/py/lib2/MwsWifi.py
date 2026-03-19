# mws_wifi.py
#
# handle connecting to Wifi

#@@@@@ FIXES FOR WIFI  @@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$
#Disable Power-Save Mode: By default, the Pico W uses aggressive power-saving, which can cause connection drops. Use wlan.config(pm = 0xa11140) to keep the radio active.
#Robust Reconnection Loop: Do not assume wlan.connect() works permanently. Implement a while not wlan.isconnected(): loop with time.sleep() to check status and re-initiate connection.
#Handle DHCP Timeouts: The Pico W might fail to get an IP quickly. Add a timeout to your connection script; if it doesn't connect within 10-20 seconds, deactivate (wlan.active(False)) and reactivate the interface before trying again.
#Place your network setup code in boot.py, which runs automatically on startup 
#  before main.py, as is standard practice for MicroPython devices. 
# Run machine.reset() to reboot

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

NTP_UPDATE_INTERVAL_SECS = 3600 # once an hour


class _State:

    # active _State
    state = None

    def __init__(self):
        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        self.restarts_counter = 0
        self.latest_ntp_update_secs = 0 # 'a long time ago'
        self.num_ntp_updates = 0

    def nullify(self):
        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        
    def __str__(self):
        ntp_elapsed = time.time() - self.latest_ntp_update_secs
        elapsed_stg = f"{ntp_elapsed}/{NTP_UPDATE_INTERVAL_SECS}"
        s = []
        s.append("state=%s" % str(self.state))
        s.append("wlan=%s" % str(self.wlan))
        s.append("sleepSecs=%s" % str(self.sleep_secs))
        s.append("retries=%s" % str(self.status_retries))
        s.append("restarts_counter=%s" % str(self.restarts_counter))
        s.append("latest_ntp_update_secs=%s" % str(self.latest_ntp_update_secs))
        s.append("ntp_elapsed_secs=%s" % str(elapsed_stg))
        s.append("num_ntp_updates=%s" % str(self.num_ntp_updates))
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
        self._port = 0
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"MwsWifi@87 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def wifi_task(self):
        print(f"nMwsWifi@94 TASK STARTED!")

        st = _State()

        # for allowing visbility
        MwsWifi.state = st

        states = {
            0:  self._state_zero,
            1:  self._state_init,
            2:  self._state_create_wlan_obj,
            3:  self._state_status_wait,
            4:  self._state_check_connected,
            }


        while 1:
            print(f"\nMwsWifi@108 STATE: {st}")

            state_callable = states.get(st.state, self._no_such_state)

            next_state = state_callable(st)

            # Zero means repeat the state
            if next_state == 0: next_state = st.state

            print(f"MwsWifi@117  next_state={next_state}")
            if next_state not in states:
                print(f"MwsWifi@119  No such state {next_state}  - RESTART!")
                self._nullify_connection_state(st)
                next_state = 1

            st.state = next_state

            if st.sleep_secs > 0:
                print(f"MwsWifi@126 task sleeping {st.sleep_secs} secs   {st}")
                await asyncio.sleep(st.sleep_secs)
                # set back to default
                st.sleep_secs = 1


    def _state_zero(self, st):
        print(f"MwsWifi@133  SHOULD NEVER ENTER STATE ZERO!  {st}")
        return 1

    def _state_init(self, st):
        print(f"MwsWifi@137  (RE) INITIALIZE   {st}")
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
        logi(f"MwsWifi@149   Connect to wifi: ssid='{ssid}'")
        ###print(f"MwsWifi@150   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
        st.wlan = wlan
        st.status_retries = 30
        st.sleep_secs = 5
        return 3

    def _state_status_wait(self, st):
        st.status_retries -= 1
        if st.status_retries <= 0:
            print(f"MwsWifi.148  STATUS RETRIES EXHAUSTED. Restart")
            return 1

        status = st.wlan.status()
        print(f"MwsWifi@164  wlan.status = {status} ")

        if status != 3:
            st.sleep_secs = 5
            # keep trying
            return 0

        # Got a good status. Move to the next state
        print(f"MwsWifi@172  Status-Wait GOT GOOD-CONNECTION STATUS  {st}")
        self._set_ipaddr_and_port(st.wlan)
        st.status_retries = 0
        st.sleep_secs = 1
        return 4

    def _state_check_connected(self, st):
        # See if still connected
        if not st.wlan.isconnected():
            print(f"MwsWifi@184 *** LOST OUR CONNECTION  ****  {st}")
            return 1

        print(f"MwsWifi@181 STILL CONNECTED  {self._ipaddr} {self._port}")

        self._wifi_set_time_from_ntp(st)

        st.sleep_secs = 3
        return 0


    def _no_such_state(self, st):
        print(f"MwsWifi@189 ILLEGAL STATE! {st}")
        ###$$$$ return 1
        raise RuntimeError(f"MwsWifi@191 ILLEGAL STATE {st}")
        sys.exit(1) #$$$$$$$$$$$$$$$$$$


    def _nullify_connection_state(self, st):
        print(f"MwsWifi@196  NULLIFY - STARTING OVER")
        self._ipaddr = None
        self._port = 0
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        wlan = st.wlan
        st.nullify()
        # Clean up if possible
        if wlan is not None:
            #@@@@@@@@@@@@@@@@$$$$$$$$$$$$ ADD try/except
            m = "MwsWifi@205 DISCONNECT the wlan object."
            print(m)
            logi(m)
            wlan.active(False)
            wlan.disconnect()


    def _set_ipaddr_and_port(self, wlan):
        info = wlan.ifconfig()
        self._ipaddr = info[0]
        self._port = OUR_PORT_NUMBER
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        print(f"MwsWifi@217  CONNECTED: IP={self._ipaddr} PORT={self._port} ")


    def _wifi_set_time_from_ntp(self, st):
        # See if it's time to update
        now = time.time()

        elapsed = now - st.latest_ntp_update_secs
        print(f"MwsWifi@237  NTP elapsed time {elapsed} secs   {NTP_UPDATE_INTERVAL_SECS=}")
        if elapsed < NTP_UPDATE_INTERVAL_SECS:
            return

        m = f"MwsWifi@241 TIME TO PERFORM NTP TIME UPDATE  {elapsed=} secs.  {st}"
        print(m)
        logi(m)

        try:
            ntptime.settime()
        except Exception as ex:
            m = f"MwsWifi@324 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}"
            logi(m)
            return False
    
        # verify the time
        current_time = utime.localtime()
    
        # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
        # (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday is 0=Sun, etc
        logi(f"MwsWifi@334 TIME FROM NTP: {current_time} ") # as tuple
        year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
        logi(f"MwsWifi@336 {year=}  {month=}  {date=}  {hour=}  {minute=}  {second=}  {weekday=}  {yearday=}  ")
        weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
        logi(f"MwsWifi@338   {weekday_stg=}")
    
        # successful update
        st.latest_ntp_update_secs = now
        st.num_ntp_updates += 1

        return True

######################################################################
######################################################################
######################################################################

    def OLDSTUFF(self):

        CTR = 8
        while 1:
            if sleep_secs > 0:
                print(f"nMwsWifi@229 task sleeping {sleep_secs} secs")
                await asyncio.sleep(sleep_secs)
            sleep_secs = 1   # default

            print(f"MwsWifi@233   CTR is {CTR} _________________________________")
            if CTR < 0:
                if self.wlan is not None: 
                    self.wlan.active(False)
                    print(f"MwsWifi@237  _____________******************* SIMULATE DISCONNECT")
                else:
                    print(f"MwsWifi@239  _____________******************* CANNOT SIMULATE DISCONNECT")

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
                    print(f"nMwsWifi@259 Giving up on waiting for status==3 - start over")
                    self._nullify_connection_state()
                    continue

            # Check if we're still connected
            if not self.wlan.isconnected():
                print(f"MwsWifi@265 *** LOST OUR WIFI CONNECTION ***.   Start over.")
                self._nullify_connection_state()
                sleep_secs = 4
                continue

            print(f"nMwsWifi@270 wifi is connected ok")
            sleep_secs = 4 #$$$$$



######################################################################


    def ___OLD_connect_to_wifi(self, show_details=True):
        """ Connect to the WIFI WLAN.
        Return a wlan obj if successful else exception.
        """
        
        logi(f"MwsWifi@283 CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
        
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
        logi(f"MwsWifi@289   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
    
        max_wait = 30 # Timeout in seconds
        num_tries = 0
        while num_tries < max_wait:
            wlan_status = wlan.status()
            logi(f"MwsWifi@296 waiting...  wlan_status={wlan_status}")
            if wlan_status < 0 or wlan_status >= 3:
                break
            num_tries += 1
            logi(f"MwsWifi@300 Waiting for connection...   num_tries={num_tries}  max={max_wait}")
            utime.sleep(1)
        logi(f"MwsWifi@302 wlan.status() = {wlan.status()}")
        
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



###
