# run_pico_tests.py
#
# PC-side driver (CPython) for the tests that run on the Pico. Run it from the repo root:
#     python3 run_pico_tests.py [what ...]      (--help shows examples)
# Each "what" is a test file, a directory, or a package name (like lib1, meaning
# tests/shared/lib1 and tests/pico/lib1). No arguments: everything.
#
# For each shared test (tests/shared/**/test_*.py) it builds a throw-away script
# (build/_assembled_<package>_<name>) = the test source + tests/pico/pico_glue.py, and
# sends it with `mpremote run`. Nothing is copied to the Pico.
# Self-contained Pico tests (tests/pico/**/pico_test_*.py) are sent as they are.
# Prints one line per file, the whole output only for a file that did not pass.
# Test file names must be unique across the whole tests/ tree.
import argparse
import pathlib
import subprocess
import sys

TESTS = pathlib.Path("tests")
SHARED = TESTS / "shared"
PICO = TESTS / "pico"
BUILD = pathlib.Path("build")
TIMEOUT_SECONDS = 120


def is_shared_test(test_file: pathlib.Path) -> bool:
    """ Shared tests are named test_*.py; the self-contained Pico ones pico_test_*.py. """
    return test_file.name.startswith("test_")


def create_assembled_name(test_file: pathlib.Path) -> str:
    """ _assembled_lib1_test_file_utils.py for tests/shared/lib1/test_file_utils.py """
    try:
        parts = test_file.resolve().relative_to(SHARED.resolve()).parts
    except ValueError:
        parts = (test_file.name,)
    return "_assembled_" + "_".join(parts)


def assemble_script(test_file: pathlib.Path) -> pathlib.Path:
    # The glue goes AFTER the test source: tracebacks then show the test file's line numbers.
    BUILD.mkdir(exist_ok=True)
    glue = (PICO / "pico_glue.py").read_text()
    script = BUILD / create_assembled_name(test_file)
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


def find_tests_under(directory: pathlib.Path) -> list[pathlib.Path]:
    """ The shared and the Pico tests under `directory`, at any depth. """
    return sorted(directory.rglob("test_*.py")) + sorted(directory.rglob("pico_test_*.py"))


def find_test_files(args: list[str]) -> list[pathlib.Path]:
    """ No arguments: all tests. An argument is a file, a directory, or a package name. """
    if not args:
        return find_tests_under(SHARED) + find_tests_under(PICO)
    found: list[pathlib.Path] = []
    for arg in args:
        path = pathlib.Path(arg)
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            found += find_tests_under(path)
        elif (SHARED / arg).is_dir() or (PICO / arg).is_dir():
            for base in (SHARED / arg, PICO / arg):
                if base.is_dir():
                    found += find_tests_under(base)
        else:
            sys.exit("not a test file, directory or package: " + arg)
    return found


USAGE_EXAMPLES = """\
examples (run from the repo root):
  python3 run_pico_tests.py                                   all tests
  python3 run_pico_tests.py lib1                              one package
  python3 run_pico_tests.py lib1 weblib                       several packages
  python3 run_pico_tests.py tests/shared/lib1                 one directory
  python3 run_pico_tests.py tests/shared/lib1/test_file_utils.py   one file
"""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Pico tests on the board with `mpremote run`; "
                    "print one result line per test file.",
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("what", nargs="*", metavar="WHAT",
                        help="a test file, a directory, or a package name such as lib1 "
                             "(tests/shared/lib1 and tests/pico/lib1); default: all tests")
    return parser.parse_args()


def main() -> int:
    bad = 0
    test_files = find_test_files(parse_arguments().what)
    if not test_files:
        print("NO TEST FILES FOUND")
        return 1
    for test_file in test_files:
        output = run_script(assemble_script(test_file) if is_shared_test(test_file) else test_file)
        result = find_result_line(output)
        print("%-50s %s" % (str(test_file.relative_to(TESTS)) if TESTS in test_file.parents else str(test_file), result))
        if "PASSED" not in result:
            bad += 1
            print(output)
    print("ALL PASSED" if bad == 0 else "%d FILE(S) DID NOT PASS" % bad)
    return 1 if bad else 0


sys.exit(main())

###
