# LEM review: unit tests

Nov 17, 2026 (updated Nov 25, 2026) · Zilot

All 21 LEM unit tests pass under CPython in a copy of the sideline tree. This review of the tests completes the review of the four LEM files, `lib1/`, and the tests. Short throwaway probes checked the main suspicions; items marked **(confirmed)** were seen to happen. None of the original files were changed.

## Problems in the tests (confirmed)

**P1. The `Z__` setters are never restored, so results depend on test order.**

- In `test_lem_log_file_table.py`:
    - `test_rotating_the_files()` sets `MAX_LOG_FILE_SIZE` to 1200.
    - `test_reduce_file_usage_to_below_low_watermark()` sets the low watermark.
    - `test_remove_logs_if_fspace_needed()` sets both watermarks.
- None of them put the old value back, although each `Z__` docstring says the caller will.
- **(confirmed)** Running `test_rotating_the_files` and then `test_log_one_line_call_many_times` fails with `16 == 104`. The full suite passes only because of the order the tests are written in.
- pytest runs every file in one process, so the changed values also carry into later test files.

**P2. `test_logging_after_closing()` passes even if logging after close is allowed.** The `try`/`except RuntimeError` has no `else: assert False`, so if `log_one_line()` doesn't raise, the test still passes.

**P3. `test_rotating_the_files()` would fail on the Pico. FIXED 2026-11-25.**

- The expected file sizes (1331, 1344, …) include the chatter lines that `LemLogFileTable` writes into each log, such as `OPENED NEW LOG <path>` and `CLOSING … <path>`.
- Those lines contain the full scratch path, which on CPython is `/tmp/MWS_tests_xxxxxxxx/logs/…`. `pico_glue`'s path will be a different length, so the sizes will differ.
- Editing any of that message text also breaks the test. `test_log_one_line_call_many_times()` has the same dependency with its `+ 4` lines of chatter.

**Fix:** confirmed on the Pico. `LemLogFileTable`'s log messages now always right-justify paths, in production and in tests alike, so line lengths match on both platforms. Some tests now check only the base filename (e.g. `mws_log.010`). `test_lem_log_file_table.py` gives the same file count and sizes on both platforms (content differs and isn't checked).

**P4. `assert oldest_idx is 0` in `test_find_the_oldest_extant_logfile()`.** **(confirmed)** CPython warns about `is` with an int literal; with warnings turned into errors, the file doesn't compile. `== 0` is what's meant.

**P5. The same test checks less than its comments say. FIXED 2026-11-18.** Under "Add new item[2]" it calls `_append_to_log_file_table(fname2, fsize2)`, so the table holds `file.2` twice, not `file.3`.

**Correction and fix:** the code was wrong, not the comment: `fname3`/`fsize3` were set but never used. The test is now fixed. Not yet confirmed: whether the off-by-one names further down (`fname3 = "file.4"`, `fname4 = "file.5"`, `fname5 = "file.6"`) were also renamed.

**K1. A failure inside `__enter__` breaks every later test.**

- In the `LemTestContext` class in `test_lem_log_control.py` and `test_lem_log_ABC.py`, `__enter__` first calls `configure_logger(None)`, then `Z_replace_log_file_table()`.
- If anything after `configure_logger()` raises, `__exit__` never runs, so the class attribute `LemLogControl._instance` stays set.
- **(confirmed)** Every later test then fails with `LEMLC$25 LOGGER IS ALREADY CONFIGURED!`, and one real failure turns into many.

**K2. `LemLogABC._enable_prt(True)` is never turned off.** `test_class_gets_registered()` turns on the module-level variable `PRT` in `LemLogABC.py` and leaves it on, so every later test in the process gets the extra print lines.

## Problems in the support code (confirmed)

**Z1. `ClassA.try_all_loggers()` never reaches `logi()`.** The method `try_all_loggers()` in `ClassA.py` (and `ClassB.py`) calls `logrt()`, which raises, before `logi()`. **(confirmed)** Only the `log` and `logrt` lines reach the fake.

**Z2. The `verbose` argument of `ZLemLogFileTable` does nothing.** In `ZLemLogFileTable.__init__`, `global V` is followed by `v = verbose`, which sets a local `v`, so `V` never changes.

**Z3. The fake's `get_lines_from_log_file()` doesn't match the real method.** **(confirmed)** With 10 lines, asking for more lines than exist gives different answers:

| Call | Fake | Real (`read_last_n_lines()`) |
| --- | --- | --- |
| `(12, 1)` | `['L9']` | `['L1']` |
| `(11, 3)` | `[]` | `['L1','L2','L3']` |

- The fake's negative start index wraps around. (R2 from the `lib1/` review asks which answer is right.)
- The fake also counts blank lines; the real function skips them by default.

**Z4. The fake lacks methods that `LemLogControl` passes through.** `get_current_log_fpath`, `get_current_log_fsize`, `get_logs_totals`, `get_log_table_item` and `get_status_lines` are missing, so calling any of those `LemLogControl` methods while the fake is installed raises `AttributeError`. No current test does that.

## C4 and C1 from the first review

**C4 (confirmed).** The probe:

1. Configure logging and create a `ClassA`.
2. Close logging, then configure again.
3. Call the old object's `to_log()`.

The line goes to the *old* fake, which raises `ZLLFT$21 LOGGING IS CLOSED…`. With the fake, at least the error is clear. With the real `LemLogFileTable`, the same situation gives the misleading "CANNOT CREATE LOGS SUBDIRECTORY". None of the current tests hits it, because each test creates fresh instances.

**C1 (confirmed). FIXED 2026-11-18.** A `LemLogABC` subclass whose `__repr__` uses an attribute set after `super().__init__()` gets `AttributeError` during registration.

**Fix:** in `LemLogControl.py`, `extract_simplified_classname()` now returns `type(obj_instance).__name__`; it was checked on the Pico. The method `register_user_class()` now logs only the class name, never `str()`/`repr()` of the half-built object. It still passes `obj_instance` to `_get_module_for_object()`. The note in `LemLogABC.py` now says to call `super().__init__()` before any `log()`/`logi()`/`logrt()` call. The duplicate registry store (C10) was also removed. mypy and the CPython tests pass.

## What the tests don't cover

These matter because they're the main promise of LEM:

- **Logged lines reaching the fake:** no test checks that a class's `log()` line actually lands in the fake. `test_get_lines_from_log_file()` calls `llc.log_one_line()` directly.
- **Effect of `enable_log(False)`:** no test checks that it stops `log()` lines while `logi()`/`logrt()` still log, or that `logrt()` raises.
- **`test_get_unmatched_override_classnames()`:** it can only ever pass, because nothing writes overrides (C5).
- **`test_class_gets_registered()`:** it reads `is_enabled()` but asserts nothing about it.
- **`LemLogFileTable` failure paths:** there are no tests for F1 (past 999), F2 (failed `open`), a failed mkdir, or calling `close_logging()` twice.

## Smaller items

- **Q1. Duplicated context manager:** `LemTestContext` is defined identically in `test_lem_log_control.py` and `test_lem_log_ABC.py`. `test_lem_log_file_table.py` has a different class with the same name. The first two could live in `ztest_logger_embed_module/`.
- **Q2. Second fake in `test_registry_trivial_case()`:** it installs a second fake, but the context already installed one. The comment "classes is a view object" is stale; it's a tuple.
- **Q3. Second table in three tests:** `test_remove_the_oldest_extant_logfile()`, `test_reduce_file_usage_to_below_low_watermark()` and `test_remove_logs_if_fspace_needed()` each assign a new `LemLogFileTable` to `llft` inside the `with`. The context still closes its own, unused table. That's harmless but confusing.
- **Q4. Leftovers in `test_lem_log_file_table.py`:** the helper `check_production_log_dir_unchanged()` is no longer used. `test_SKELETON_for_tests()` is an empty test that always passes.
- **M1. Header conventions:**
    - The line-1 names are wrong in `test_lem_log_control.py` (says `test_lem_control.py`) and `test_lem_log_ABC.py` (says `test_lem_logger_ABC.py`).
    - `junk_ctx_mgr.py` has no name line and no `###`.
- **M2. Line-marker headers** that `redo_line_markers` may not like:
    - `# # LINEMARKER=ZLLC` has a doubled `#`.
    - `LINEMARKER=ZLLFT$` has a trailing `$`.
    - The prefix `ZLLFT` is used by both `ZLemLogFileTable.py` and `test_lem_log_file_table.py`.
    - `ClassA.py`/`ClassB.py` contain `CLSA$$34`/`CLSB$$34`.
- **M3. Old files to tidy before the branch:**
    - `*.COPY`, `*.COPYCOPY` and `cpython_test_support.py_COPY` in `tests/shared/logger_embed_module/`.
    - Three old `logger_elem` copies in `tests/cpython/logger_elem/`.
    - Unused imports (`os`) in the test files and in `ZLemLogFileTable.py`.
- **M4. `unit_tests/logs/` is empty and read-only.** Probably deliberate, so any test that wrote to a relative `logs/` would fail loudly. Open question: is it?
