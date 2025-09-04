# async_printing_test.py

import uasyncio
import utime

async def prt(who, secs, start_time):
    while True:
        now = utime.time()
        print(f"This is {who}  {now-start_time}") 
        await uasyncio.sleep_ms(secs*1000)
        
async def main():
    start_time = utime.time()
    uasyncio.create_task(prt("A", 3, start_time))
    uasyncio.create_task(prt("B", 4, start_time))
    
    target_end_time = start_time + 24
    
    curr_secs = start_time
    
    while True:
        while True:
            now = utime.time()
            if now > curr_secs:
                break
            await uasyncio.sleep_ms(200)
            
            
        curr_secs = utime.time()
        
        print(f"MAIN: {curr_secs-start_time}")
        if curr_secs >= target_end_time:
            break
    
    ###await uasyncio.sleep_ms(24_000)
    end_time = utime.time()
    elapsed_time = end_time - start_time
    print(f"MAIN:  elapsed time: {elapsed_time} secs.")
    
# Running on a generic board
###from machine import Pin
###uasyncio.run(main(Pin(1), Pin(2)))
uasyncio.run(main())

### end ###

