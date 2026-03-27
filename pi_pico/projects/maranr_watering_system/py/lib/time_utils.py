# time_utils.py

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


NTP_UPDATE_INTERVAL_SECS = 60 # how often we update @@@@@@@@@@@@@@@@@@@
LATEST_NTP_UPDATE_SECS = 0  # a long time ago
NUMBER_OF_NTP_UPDATES = 0
NUMBER_OF_TIME_JUMPS = 0

#TODO ADD table for daylight savings time changes

LOGI = None

# provide a logger
def set_time_utils_logger(log_and_print_method):
    global LOGI
    LOGI = log_and_print_method


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

def get_formatted_date_time_string():
    date_stg,time_stg = get_formatted_local_time()
    return f"{date_stg} {time_stg}"

def get_formatted_local_time():
    now = get_local_time()
    # Format the date as "YYYY-MM-DD" and time as "HH:MM:SS"
    date_str = "{}-{}-{}".format(now[0], now[1], now[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])
    return (date_str, time_str)



# offset between Unix and Micropython epochs (secs between 1970 and 2000)
UNIX_EPOCH_OFFSET = 946684800

def get_time_unix_seconds(secs=None):
    if secs is None: secs = time.time()
    return secs + UNIX_EPOCH_OFFSET


def set_time_clock_from_ntp():
    global LATEST_NTP_UPDATE_SECS
    global NUMBER_OF_NTP_UPDATES
    global NUMBER_OF_TIME_JUMPS

    LOGI(f"TimeUtils@71 set_time_clock_from_ntp @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # Time to call NTP website and update?
    now = time.time()
    elapsed = now - LATEST_NTP_UPDATE_SECS
    LOGI(f"TimeUtils@76  Time for NTP update?  elapsed time {elapsed} secs   {NTP_UPDATE_INTERVAL_SECS=}")
    LOGI(f"TimeUtils@77  ... now: {now}  LATEST_NTP_UPDATE_SECS {LATEST_NTP_UPDATE_SECS} ")

    if elapsed < NTP_UPDATE_INTERVAL_SECS:
        LOGI(f"TimeUtils@78  Not time yet for update. elapsed < INTERVAL:  {elapsed} < {NTP_UPDATE_INTERVAL_SECS}")
        return

    LOGI(f"TimeUtils@81 TIME TO PERFORM NTP TIME UPDATE  {elapsed=} secs.  {NTP_UPDATE_INTERVAL_SECS=}")

    now_was = now

    try:
        ntptime.settime()
    except Exception as ex:
        LOGI(f"TimeUtils@86 **ERROR** ntptime.settime() FAILED. ex={repr(ex)}  ex.str={str(ex)}")
        return False

    now = time.time()
    LOGI(f"TimeUtils@90 set_time_clock_from_ntp  Micropython epoch: {now} secs.  unix: {get_time_unix_seconds(now)}")
    #print("Seconds since MicroPython epoch (2000):", micropython_timestamp)
    #print("Seconds since Unix epoch (1970):", unix_timestamp)

    LATEST_NTP_UPDATE_SECS = now
    NUMBER_OF_NTP_UPDATES += 1

    LOGI(f"TimeUtils@97  after update, elaspsed is {now-LATEST_NTP_UPDATE_SECS} ")

    # Did time jump by very much?
    jumped_secs = now - now_was
    LOGI(f"TimeUtils@108  TIME-JUMP-DELTA secs {jumped_secs}")
    if abs(jumped_secs) > 10:
        NUMBER_OF_TIME_JUMPS += 1
        LOGI(f"TimeUtils@107  ***************** TIME JUMPED!   {jumped_secs} secs  *************************")
        LOGI(f"TimeUtils@107  ***************** TIME JUMPED!   {NUMBER_OF_TIME_JUMPS=}  *************************")
        

    # verify the time
    current_time = time.localtime()
    
    # Example output: (2024, 2, 16, 11, 4, 30, 3, 47) 
    # (year, month, mday, hour, minute, second, weekday, yearday)
    # weekday is 0=Sun, etc
    LOGI(f"TimeUtils@103 TIME FROM NTP: {current_time} ") # as tuple
    year, month, date, hour, minute, second, weekday, yearday = current_time  # unpack
    LOGI(f"TimeUtils@105 date/time: {year}/{month}/{date}  {hour:02d}:{minute:02d}:{second:02d}  ")
    weekday_stg = [ "sun", "mon", "tue", "wed", "thu", "fri", "sat"] [weekday]
    LOGI(f"TimeUtils@107   {weekday=}  {yearday=}   {weekday_stg=}")
    

def main():
    pass

if __name__ == "__main__":
    main()

### end ###
