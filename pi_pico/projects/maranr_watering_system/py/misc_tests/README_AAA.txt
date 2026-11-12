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

###

