# TimeMgr.py

import micropython
import ntptime
import os
import platform
import sys
try:
    import time
except ModuleNotFoundError:
    import utime as time
try:
    import gc
    _ = gc.mem_free
except Exception as ex:
    print(f"utils.py  CANNOT IMPORT MICROPYTHON VERSION of 'gc' !!!!!")
    del gc
    import gc_FAKE as gc
    print(f"utils.py  USING FAKE VERSION OF 'gc'  !!!!!!!!!!!!!!!!!!!!!!!!!!!!")

from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib2.DataBoard import DataBoard


#TODO ADD table for daylight savings time changes

NTP_UPDATE_INTERVAL_SECS = 60 # 3600 (once/hour) how often we update @@@@@@@@@@@@@@@@@@@TODO

# offset between Unix and Micropython epochs (secs between 1970 and 2000)
UNIX_EPOCH_OFFSET = 946684800

VALIDATE = 890421


log = None
logrt = None
logi = None


class TimeMgr(ElemLoggerABC):
    
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = TimeMgr(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        TimeMgr._instance = None
        # Remove any messages - unit test only
        #ElemLogControl._clear_latest_messages()


    def __init__(self, validate=None):
        self.latest_ntp_update_secs = 0   # init: a long time ago
        self.number_of_ntp_updates = 0
        self.number_of_time_jumps = 0
        self.maximum_time_jump_secs = 0
        self._data_board = None
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    @staticmethod
    def get_time_unix_seconds(secs=None):
        if secs is None: secs = time.time()
        return secs + UNIX_EPOCH_OFFSET

    @staticmethod
    def get_local_time():  # for our TZ
        # Get UTC time from clock
        #### THIS RETURNS UTC  utc_time = time.localtime()
        # Example: Apply offset for Central TZ: UTC-6 hrs
        # TODO handle automatic switch to DAYLIGHT_TIME_OFFSET
        STD_TIME_OFFSET = -6 # hours
        DAYLIGHT_TIME_OFFSET = -5 # hours
        offset = DAYLIGHT_TIME_OFFSET * 3600 # seconds
        local_time = time.localtime(time.time() + offset)
        return local_time

    @staticmethod
    def get_formatted_local_time():
        now = TimeMgr.get_local_time()
        # Format the date as "YYYY-MM-DD" and time as "HH:MM:SS"
        date_str = "{}-{}-{}".format(now[0], now[1], now[2])
        time_str = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])
        return (date_str, time_str)

    @staticmethod
    def get_formatted_date_time_string():
        date_stg,time_stg = TimeMgr.get_formatted_local_time()
        return f"{date_stg} {time_stg}"


    def set_time_clock_from_ntp(self):
    
        # Time to call NTP website and update?
        now = time.time()
        elapsed = now - self.latest_ntp_update_secs
        log(f"TimeMgr@109  Time for NTP update?  elapsed time {elapsed} / {NTP_UPDATE_INTERVAL_SECS} secs")
        log(f"TimeMgr@110  ... now: {now}  latest-ntp-update-secs {self.latest_ntp_update_secs} ")
    
        if elapsed < NTP_UPDATE_INTERVAL_SECS:
            log(f"TimeMgr@113  Not time yet for update. elapsed < INTERVAL:  {elapsed} < {NTP_UPDATE_INTERVAL_SECS}")
            return
    
        logi(f"TimeMgr@116 TIME TO PERFORM NTP TIME UPDATE  {elapsed=} secs.  {NTP_UPDATE_INTERVAL_SECS=}")
    
        now_was = now
    
        try:
            ntptime.settime()
        except Exception as ex:
            logi(f"TimeMgr@123 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}")
            return False
    
        now = time.time()
        logi(f"TimeMgr@127 set_time_clock_from_ntp  Micropython epoch: {now} secs.  unix: {TimeMgr.get_time_unix_seconds(now)}")
        #print("Seconds since MicroPython epoch (2000):", micropython_timestamp)
        #print("Seconds since Unix epoch (1970):", unix_timestamp)
    
        self.latest_ntp_update_secs = now
        self.number_of_ntp_updates += 1
    
        ###log(f"TimeMgr@134  after update, elapsed is {now-self.latest_ntp_update_secs} ")
    
        # Did time jump by very much?
        jumped_secs = now - now_was
        logi(f"TimeMgr@138  TIME-JUMP-DELTA secs {jumped_secs}   prior-num-jumps: {self.number_of_time_jumps}  prior-max-jmp-secs: {self.maximum_time_jump_secs}")
        if abs(jumped_secs) > 10 and jumped_secs < 1700:  # at startup the jump is big - ignore it
            self.number_of_time_jumps += 1
            self.maximum_time_jump_secs = max(jumped_secs, self.maximum_time_jump_secs)
            logi(f"TimeMgr@142  ***************** TIME JUMPED!   {jumped_secs} secs  *************************")
            logi(f"TimeMgr@143  ***************** TIME JUMPED!   Number of jumps: {self.number_of_time_jumps}  *************************")
            logi(f"TimeMgr@144  ***************** TIME JUMPED:   Max jump: {self.maximum_time_jump_secs} secs")
    
        # Report our status
        if self._data_board is None: self._data_board = DataBoard.get_instance()
        self._data_board.post_time_mgr_status(
                        self.latest_ntp_update_secs,
                        self.number_of_ntp_updates,
                        self.number_of_time_jumps,
                        self.maximum_time_jump_secs)


        # verify the time
        current_time = time.localtime()
        
        # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
        # (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday is 0=Sun, etc
        logi(f"TimeMgr@161 TIME FROM NTP: {current_time} ") # as tuple
        year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
        weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
        logi(f"TimeMgr@164 date/time: {year}/{month}/{date}  {hour:02d}:{minute:02d}:{second:02d}  {weekday=} {weekday_stg=}  {yearday=}")
    

def main():
    pass

if __name__ == "__main__":
    main()

### end ###
