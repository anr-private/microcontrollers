# run_pico_tests.py
#
# Runs tests on the PICO.
# Usage:
#     python3 run_pico_tests.py [test_file ...]
# For each shared test (tests/shared/test_*.py) it builds a throw-away script
# (build/_assembled_<name>) = the test source + tests/pico/pico_glue.py, and sends
# it with `mpremote run`. Nothing is copied to the Pico.
# Self-contained Pico tests (tests/pico/pico_test_*.py) are sent as they are.
# Prints one line per file, the whole output only for a file that did not pass.
import pathlib
import subprocess
import sys

TESTS = pathlib.Path("tests")
BUILD = pathlib.Path("build")
TIMEOUT_SECONDS = 120


def assemble_script(test_file: pathlib.Path) -> pathlib.Path:
    # The glue goes AFTER the test source: tracebacks then show the test file's line numbers.
    BUILD.mkdir(exist_ok=True)
    glue = (TESTS / "pico" / "pico_glue.py").read_text()
    script = BUILD / ("_assembled_" + test_file.name)
    script.write_text(test_file.read_text() + "\n\n" + glue)
    return script


def run_script(script: pathlib.Path) -> str:
    try:
        done = subprocess.run(["mpremote", "run", str(script)],
                              capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return "TIMED OUT after %d seconds" % TIMEOUT_SECONDS
    return done.stdout + done.stderr


def find_result_line(output: str) -> str:
    for line in output.splitlines():
        if "RESULT:" in line:
            return line.strip()
    return "NO RESULT LINE (crashed, timed out, or not a test script?)"


def find_test_files(args: list[str]) -> list[pathlib.Path]:
    if args:
        return [pathlib.Path(a) for a in args]
    return sorted(TESTS.glob("shared/test_*.py")) + sorted(TESTS.glob("pico/pico_test_*.py"))


def main() -> int:
    bad = 0
    for test_file in find_test_files(sys.argv[1:]):
        shared = test_file.parent.name == "shared"
        output = run_script(assemble_script(test_file) if shared else test_file)
        result = find_result_line(output)
        print("%-40s %s" % (test_file.name, result))
        if "PASSED" not in result:
            bad += 1
            print(output)
    print("ALL PASSED" if bad == 0 else "%d FILE(S) DID NOT PASS" % bad)
    return 1 if bad else 0


sys.exit(main())

###
