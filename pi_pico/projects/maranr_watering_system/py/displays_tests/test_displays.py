# test_displays.py
#
# You can run this either of 2 ways.
# You can run it locally on the linux system by
# opening this file in Thonny and then running it.
# (That is the easiest way)
#
# Or you can copy the file to the Pico, go to the Pico's remote files/dirs
# window, double-click it (downloads it back into Thonny), and then run
# it in Thonny.
# NOTE that the /lib/utils.py must exist on the Pico in order for the import to work!

import asyncio
import sys

print(f"SYS.PATH {sys.path}")

import lib.utils as utils
from displays.MwsDisplays import MwsDisplays



async def test1():
    print("\n=== TEST 1  ============================")
    displays = MwsDisplays()

    ok = displays.locate_the_lcd()

    if not ok:
        m = f"@30 FAILED TO LOCATE the lcd!"
        print(m)

    displays_task = displays.start_the_task()

    print(f"@35  {displays_task=}")

    while 1:
        print("@38 sleeping.   displays_task.done={displays_task.done()}")
        await asyncio.sleep(1)


    print("=== end of TEST 1  ============================\n")

    

def main(*args):
    try:
        # Start the event loop and run the main server coroutine
        asyncio.run(test1())

    except KeyboardInterrupt:
        print("@52 interrupt from keyboard")

    finally:
        # Clean up the event loop (optional, but good practice)
        asyncio.new_event_loop()



if __name__ == "__main__":
    main(sys.argv[1:])




###
