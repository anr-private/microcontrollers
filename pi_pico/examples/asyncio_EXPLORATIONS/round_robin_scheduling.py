# round_robin_scheduling.py
#
# Demonstrate that asyncio does round robin, giving every task a chance

import asyncio

TASK_1_CTR = 0
TASK_2_CTR = 0


async def task_1():
    global TASK_1_CTR
    TASK_1_CTR = 0
    while 1:
        TASK_1_CTR += 1
        if TASK_1_CTR % 500 == 0:
            print(f"@10 task_1  ctr={TASK_1_CTR}")
        await asyncio.sleep(0)

async def task_2():
    global TASK_2_CTR
    TASK_2_CTR = 0
    while 1:
        TASK_2_CTR += 1
        if TASK_2_CTR % 500 == 0:
            print(f"@10 task_2  ctr={TASK_2_CTR}")
        await asyncio.sleep(0)


async def main():
    ctr_task = asyncio.create_task(task_1())
    ctr_task = asyncio.create_task(task_2())

    ctr = 0
    while ctr < 30:
        ctr += 1
        print(f"@29 MAIN:  idling, ctr={ctr}")
        await asyncio.sleep(1)
    print("@30 MAIN is COMPLETED")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("@53    KEYBOARD interrupt")
finally:
    print("@35   <<<  Create a new event loop, as cleanup >>>")
    asyncio.new_event_loop()

print(f"@47 AFTER RUNNING:  {TASK_1_CTR=}  {TASK_2_CTR=}")

delta = TASK_1_CTR - TASK_2_CTR
print(f"@52   counter delta is {delta}")
# Did the tasks each get some time to run?
# Or did one task hog the processor?
if delta > 50:
    print(f"@54 ****************** Counter-DELTA is TOO BIG!!! **********************")

###
