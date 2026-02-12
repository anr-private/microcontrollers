# async_printing_test.py
# Runs tasks that just print and sleep
# Main watches the clock and tries to print once a second,
#  checking 5 times a second (every 200 msecs) to see if
#  clock has ticked to the next second.

import uasyncio
import utime

TOTAL_RUN_TIME_SECS = 28

async def prt(who, secs, start_time):
    while True:
        now = utime.time()
        print(f"This is {who}  {now-start_time}") 
        await uasyncio.sleep_ms(secs*1000)
        
async def main():
    start_time = utime.time()
    uasyncio.create_task(prt("A-3", 3, start_time))
    uasyncio.create_task(prt("B-4", 4, start_time))
    uasyncio.create_task(prt("C-5", 5, start_time))
    uasyncio.create_task(prt("D-7", 7, start_time))
    
    target_end_time = start_time + TOTAL_RUN_TIME_SECS
    
    curr_secs = start_time
    
    while True:
        # Wait for the clock to tick to the next second
        ticks_waited = 0
        while True:
            now = utime.time()
            if now > curr_secs:
                break
            ticks_waited += 1
            await uasyncio.sleep_ms(200)
            
            
        curr_secs = utime.time()
        
        print(f"MAIN: Elapsed: {curr_secs-start_time}  Remains: {target_end_time-curr_secs}   ({ticks_waited=}) ")
        
        if curr_secs >= target_end_time:
            break
    
    ###await uasyncio.sleep_ms(24_000)
    end_time = utime.time()
    elapsed_time = end_time - start_time
    print(f"MAIN:  elapsed time: {elapsed_time} secs.")
    
# Running on a generic board
###from machine import Pin
###uasyncio.run(main(Pin(1), Pin(2)))
try:
    uasyncio.run(main())
except KeyboardInterrupt:
    print(f"=== Interrupted by USER control-C")

### end ###

