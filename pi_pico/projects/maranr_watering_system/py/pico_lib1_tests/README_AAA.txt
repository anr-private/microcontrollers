This dir contains files for testing lib1/ contents:

 README_AAA.txt                   this readme

  # Test files
 read_last_n_lines.py             read_last_n_lines function fixed by Claude
 test_read_last_n_lines.py        test pgm - runs in CPython See below
 pico_test_read_last_n_lines.py   Pico version of test - see below

  # scripts used for interchanging files with the CPython Pico support
  #  in git/art/
 COMPARE_pico_lib1_tests.sh*      Compares this dir vs /tmp/PICO_LIB1_TESTS/
 DOWNLOAD_pico_lib1_tests.sh*
 UPLOAD_pico_lib1_tests.sh*

  # push the test files to the PICO
 PUSH_pico_lib1_tests_to_PICO.sh*
 PUSH_test_files_to_pico.sh_NOTUSEDYET*


=== CPYTHON VERSION OF THE TEST  ==================

It runs on Ubuntu / Python3 like this:
  python3 test_read_last_n_lines.py ./lib1_FAKE/read_last_n_lines.py 
OUTPUT:
 Next: reading a file that does not exist on purpose. The function should
 print ONE error line (FileNotFoundError) and return []. That is expected.
 FU read_last_n_lines  EX=FileNotFoundError(2, 'No such file or directory')
   errno=2
 (end of the expected error output)

 ./lib1_FAKE/read_last_n_lines.py: 10620 cases, 0 failures
 RESULT: PASSED - all cases correct


=== PICO VERSION OF THE TEST  ==================

To run it:
Push the test files to the PICO:
  ./PUSH_pico_lib1_tests_to_PICO
On the PICO:
  Thonny - connect
  Open pico_lib1_tests/ dir
  Open the desired test file:
    pico_test_read_last_n_lines  # tests read_last_n_lines.py
    ... or whichever ...
  Press RUN to run the test.
  Verify the output.


=== Test for Claude's version of read_last_n_lines()  ===

Expected output:
 MPY: soft reboot
 chunk size: 1
 chunk size: 3
 chunk size: 7
 chunk size: 100
 chunk size: 128
 Next: reading a file that does not exist, on purpose. The function should
 print ONE error line and return []. That is expected.
 FU read_last_n_lines  EX=OSError(2,)  errno=2
 (end of the expected error output)
 386 cases, 0 failures
 RESULT: PASSED - all cases correct


=== OLD INSTRUCTIONS for running tests - from Claude


Edit the import line near the top so mod is the module that holds
 read_last_n_lines. For your real code that is probably import file_utils as
 mod.
Make sure that module is on the Pico (in /lib or at the root).
Run it from your PC with mpremote run pico_test_read_last_n_lines.py. This sends the script to the Pico and shows its output in your terminal. The script itself doesn’t need to be copied to the board.
The output ends with RESULT: PASSED or RESULT: FAILED.

How it differs from the PC version:

It writes a small scratch file, _rlnl_test.txt, to the Pico’s flash and deletes
it at the end. A run does a few hundred small writes, so don’t 
loop it endlessly.
It runs about 390 cases instead of 10,000. You can raise RANDOM_CASES_PER_CHUNK
at the top for a longer run.
It changes the chunk size only if the module has _CHUNK_SIZE, which the cleaned
function does and your original doesn’t. If you test your original, it runs at
its fixed 100-byte chunk.
It prints the same expected FileNotFoundError note as the PC script.

:wrap=soft:
###

