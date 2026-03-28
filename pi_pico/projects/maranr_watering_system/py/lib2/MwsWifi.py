# mws_wifi.py
#
# handle connecting to Wifi

#@@@@@ FIXES FOR WIFI  TODO  @@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$
#Disable Power-Save Mode: By default, the Pico W uses aggressive power-saving, which can cause connection drops. Use wlan.config(pm = 0xa11140) to keep the radio active.
#Robust Reconnection Loop: Do not assume wlan.connect() works permanently. Implement a while not wlan.isconnected(): loop with time.sleep() to check status and re-initiate connection.
#Handle DHCP Timeouts: The Pico W might fail to get an IP quickly. Add a timeout to your connection script; if it doesn't connect within 10-20 seconds, deactivate (wlan.active(False)) and reactivate the interface before trying again.
#Place your network setup code in boot.py, which runs automatically on startup 
#  before main.py, as is standard practice for MicroPython devices. 
# Run machine.reset() to reboot

import network
import asyncio
try:
    import time
except ModuleNotFoundError:
    import utime as time

from lib.utils import MWS_CONFIG
from lib2.DataBoard import DataBoard
from details import SSID, PW
from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib2.TimeMgr import TimeMgr


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
        self.restarts_counter = 0

        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        self.check_connected_ctr = 0

    def nullify(self):
        self.state = 1
        self.wlan = None
        self.sleep_secs = 1
        self.status_retries = 0
        self.check_connected_ctr = 0
        
    def __str__(self):
        s = []
        s.append("state=%s" % str(self.state))
        s.append("wlan=%s" % str(self.wlan))
        s.append("sleepSecs=%s" % str(self.sleep_secs))
        s.append("retries=%s" % str(self.status_retries))
        s.append("restarts_counter=%s" % str(self.restarts_counter))
        s.append("check_connected_ctr=%s" % str(self.check_connected_ctr))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


class MwsWifi(ElemLoggerABC):
    
    _instance = None


    @classmethod
    def get_instance(cls):
        if MwsWifi._instance is None:
            MwsWifi._instance = MwsWifi(1234567)
        return MwsWifi._instance


    @classmethod
    def get_ip_and_port(cls):
        obj = MwsWifi._instance
        if not obj._instance: return "IP-PORT-?!"
        if not obj._ipaddr: return "IP:PORT-unknown"
        return f"{obj._ipaddr}:{obj._port}"

    def __init__(self, do_not_call_directly):
        if do_not_call_directly != 1234567:
            raise RuntimeError("MwsWifi.init DO NOT CALL")
        #@@@@@$$$$$self.wlan = None
        self._dataBoard = DataBoard.get_instance()
        self._time_mgr = TimeMgr.get_instance()
        self._ipaddr = None
        self._port = 0
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    async def wifi_task(self):
        log(f"nMwsWifi@114 TASK STARTED!")

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
            log(f"\nMwsWifi@131 STATE: {st}")

            state_callable = states.get(st.state, self._no_such_state)

            next_state = state_callable(st)

            # Zero means repeat the state
            if next_state == 0: next_state = st.state

            log(f"MwsWifi@140  next_state={next_state}")
            if next_state not in states:
                log(f"MwsWifi@142  No such state {next_state}  - RESTART!")
                self._nullify_connection_state(st)
                next_state = 1

            st.state = next_state

            if st.sleep_secs > 0:
                log(f"MwsWifi@149 task sleeping {st.sleep_secs} secs   {st}")
                await asyncio.sleep(st.sleep_secs)
                # set back to default
                st.sleep_secs = 1


    def _state_zero(self, st):
        logi(f"MwsWifi@156  SHOULD NEVER ENTER STATE ZERO!  {st}")
        return 1

    def _state_init(self, st):
        logi(f"MwsWifi@160  (RE) INITIALIZE   {st}")
        self._nullify_connection_state(st)
        st.restarts_counter += 1
        st.sleep_secs = 0
        return 2

    def _state_create_wlan_obj(self, st):
        #@@@@@self._nullify_connection_state(st) TODO wtf?
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # Connect
        logi(f"MwsWifi@172   Connect to wifi: ssid='{ssid}'")
        wlan.connect(ssid, password)
        st.wlan = wlan
        st.status_retries = 30
        st.sleep_secs = 5
        return 3

    def _state_status_wait(self, st):
        st.status_retries -= 1
        if st.status_retries <= 0:
            log(f"MwsWifi.148  STATUS RETRIES EXHAUSTED. Restart")
            return 1

        status = st.wlan.status()
        log(f"MwsWifi@186  wlan.status = {status} ")

        if status != 3:
            st.sleep_secs = 5
            # keep trying
            return 0

        # Got a good status. Move to the next state
        logi(f"MwsWifi@194  Status-Wait GOT GOOD-CONNECTION STATUS  {st}")
        self._set_ipaddr_and_port(st.wlan)
        st.status_retries = 0
        st.sleep_secs = 1
        return 4

    def _state_check_connected(self, st):
        # See if still connected
        if not st.wlan.isconnected():
            logi(f"MwsWifi@203 *** LOST OUR CONNECTION  ****  {st}")
            return 1

        # Reduce the routine 'connected' mesg when logging is not enabled
        # on this class (ie when only logi() actually logs)
        m = f"MwsWifi@206 STILL CONNECTED  {self._ipaddr} {self._port}"
        st.check_connected_ctr += 1
        if st.check_connected_ctr >= 10:
            st.check_connected_ctr = 0
            logi(m)
        else:
            log(m)

        self._time_mgr.set_time_clock_from_ntp()

        st.sleep_secs = 10
        return 0


    def _no_such_state(self, st):
        logi(f"MwsWifi@215 ILLEGAL STATE! {st}")
        ###$$$$$$$ return 1  TODO fix this
        ###raise RuntimeError(f"MwsWifi@217 ILLEGAL STATE {st}")
        ###sys.exit(1) #$$$$$$$$$$$$$$$$$$


    def _nullify_connection_state(self, st):
        log(f"MwsWifi@222  NULLIFY - STARTING OVER")
        self._ipaddr = None
        self._port = 0
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        wlan = st.wlan
        st.nullify()
        # Clean up if possible
        if wlan is not None:
            #@@@@@@@@@@@@@@@@$$$$$$$$$$$$ ADD try/except TODO
            m = "MwsWifi@231 DISCONNECT the wlan object."
            logi(m)
            wlan.active(False)
            wlan.disconnect()


    def _set_ipaddr_and_port(self, wlan):
        info = wlan.ifconfig()
        self._ipaddr = info[0]
        self._port = OUR_PORT_NUMBER
        self._dataBoard.set_ip_and_port(self._ipaddr, self._port)
        logi(f"MwsWifi@242  CONNECTED: IP={self._ipaddr} PORT={self._port} ")



###
