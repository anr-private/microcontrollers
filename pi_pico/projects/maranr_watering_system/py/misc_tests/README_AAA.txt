MISC TESTS

These are for testing lib/ stuff, etc.
These are meant to be run directly in Thonny using RUN - not copied to the Pico.

main_Hello_World_ANR_fancy.py  - test for the lib_lcd1602_...py library (from pi_pico/examples/)

Test to see if mpremote run causes a soft reset on Pico
  mpremote run ZZ_set.py
  mpremote run ZZ_set.py
marker present: False means each run starts from a soft reset, so every 
test file gets a fresh interpreter. True means state survives between runs.
Got False: every 'run' gets a soft reset.

timing_flush_test.py
Tests how much latency doing a flush() on every log write() adds.
From Claude.
Running on Pico 2 W:
   flush each line: 10347 ms for 200 lines
   no flush:        270 ms for 200 lines
After adding flush every 10 lines:
  flush each line: 10430 ms for 200 lines
  no flush:        273 ms for 200 lines
  flush every 10:  1194 ms for 200 lines
Added more test:
  flush each line: 10506 ms for 200 lines
  no flush:        211 ms for 200 lines
  flush every  10:  1249 ms for 200 lines
  flush every  50:  379 ms for 200 lines
  flush every 100:  265 ms for 200 lines
###

