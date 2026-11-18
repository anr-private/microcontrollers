# REQS_apply_action_to_files.md

# apply_action_to_files: Requirements

Status: requirements draft 7 (2026-11-17). No open questions. Matches `apply_action_to_files` VERSION 2026-11-17_1945.

## 1. Purpose

`apply_action_to_files` is a development tool. It finds files under the directories named on its command line, filters them through a fixed chain of simple, data-driven filters, and runs a command on each file that survives. The first use is to run `redo_line_markers` on the `*.py` files of the MWS tree.

## 2. Environment and conventions

- Runs on Linux under Python 3.12 (Ubuntu 24.04). Standard library only.
- Lives at `~/bin/apply_action_to_files`, with no `.py` extension. (`~/bin/apply_action_to_files` is a symlink into the user's Linux-config Git repo; this has no effect on the program.)
- Follows the user's code conventions:
  - The first line is a comment with the file's own name.
  - The file ends with a blank line, a line holding `###`, and a trailing newline.
  - Function and method names are verb + object; variable names are descriptive.
  - Print lines carry line markers with the prefix `AATF` (e.g. `AATF$123`), maintained by `redo_line_markers`.

## 3. Command line

Typical use, from a one-line Bash script such as `maranr_watering_system/run_renumbering.sh`:

```
apply_action_to_files -c redo_line_markers -g '*.py' py/ py2/
```

| Option | Meaning |
|---|---|
| `-c COMMAND` | The command to run on each surviving file. Required. Split like a Bash command line (Python `shlex.split`), so quoted parts stay together: `-c 'the_cmd -opt "opt value"'` runs `the_cmd -opt "opt value" FILE_PATH`. The file path is always added as the last argument. |
| `-g GLOB` | Filename glob that selects the candidate files, e.g. `'*.py'`. Given once. Required. |
| `-n`, `--dry-run` | Report only: show what would be run or skipped, and run nothing. |
| `--stop-on-error` | Stop at the first file whose command fails. Without it, the program keeps going and lists the failures at the end. |
| `--version` | Print `VERSION <value of the VERSION constant>` as the first output line (printed before the command line is checked), then carry on exactly as without it. The other options and the roots are still required: `--version` alone prints the version, then the usage message, and exits with status 2. |
| `--verbose` | Also print the report lines that are hidden by default: one `SKIP LINK` line per symlink skipped, and one `SKIP NOMATCH` line per file that does not match `-g`. |
| `ROOT ...` | One or more root directories, after the options. Relative paths are taken from the current directory. At least one is required. |

Running (not dry-run) is the default.

## 4. Startup checks (hard errors, nothing is run)

- A root that does not exist, or is not a directory, is a hard error naming that root.
- The first word of `-c` must be found on `PATH` (`shutil.which`). If not, hard error. This check is also made in dry-run mode.
- Every regex in the regex-exclude list must compile. A bad pattern is a hard error naming the pattern.
- `-c` that cannot be split (e.g. an unclosed quote) is a hard error.

## 5. Processing chain

Each stage is a separate, simple function. Stages run in this fixed order; each takes the output of the one before it.

### Stage 1: Walk the roots, applying the directory-exclude rules

- Walk each root and all of its subdirectories.
- **Directory-exclude rules** are glob patterns (`fnmatch.fnmatchcase`, case-sensitive), each tested against **one directory name** at a time, e.g. `.*_venv` matches `.mws_venv`. A trailing `/` is not used.
- Only directories **below** a root are tested. A root itself is never tested, and neither are the parent directories above it: a root named on the command line is always walked, even if its own name matches a rule.
- A directory that matches a rule is not entered at all (it is pruned). The report shows one line for it, not one line per file inside it.
- Starting list:

```
.*_venv
.git
__pycache__
.pytest_cache
.mypy_cache
*COPY*
*IGNORE*
*NOT_USED*
*NOTUSED*
DEPRECATED*
primitives        (MWS specific, as are the rest)
build
*ARCHIVE*
*_FAKE
*_FAKES
OLD
```

- Symlinks, to directories **or** to files, are not followed and not processed. Each one gets a `SKIP LINK` report line only with `--verbose`; the summary always shows how many were skipped.
- Overlapping roots (e.g. `py/` and `py/lib1/`): each file is kept once, by its real path, and a note says which roots overlap.

### Stage 2: Select candidates with `-g`

- Keep only files whose **filename** (not the directory path) matches the `-g` glob, case-sensitive.
- A file that does not match `-g` gets a `SKIP NOMATCH` report line only with `--verbose` (e.g. to spot a `foo.PY`); the summary always shows how many there were.

### Stage 3: Filename glob excludes

- A list of glob patterns, case-sensitive (`fnmatch.fnmatchcase`), each tested against the **filename only**. Similar to `.gitignore` patterns for file names.
- Starting list:

```
*OLD.py
*DEPRECATED.py
*NOTUSED*.py
*NOT_USED*.py
*JUNK*.py
*junk*.py
*IGNORE.py
*IGNORED.py
*SAVE.py
*COPY*.py
*IGNORE*.py
```

- `*COPY*.py` also catches names ending in `COPY.py` (the `*` can match nothing).
- Within a stage, rules are tried in list order and the first match is the one reported and counted.

### Stage 4: Filename regex excludes

- A short list of Python regular expressions, each tested against the **filename only** with `re.search`. That means a pattern matches anywhere in the name unless it uses `^` (start) or `$` (end). Any Python `re` syntax is allowed.
- Kept separate from Stage 3 and kept as simple as possible. Anything a glob can do goes in Stage 3 instead.
- Case-insensitive matching needs no extra feature: a regex that starts with `(?i)` ignores case. (Globs in Stages 1 to 3 are always case-sensitive.)
- Starting list:

```
_V\d+\.py$
```

(excludes names ending in `_V1.py`, `_V2.py`, `_V10.py`, ...)

### Stage 5: Apply the action

- For each surviving file, in sorted path order, call `do_it_to_this_path(file_path: str) -> bool`.
- The default `do_it_to_this_path` runs the `-c` command with the file path added as the last argument, without a shell, so paths with spaces are safe. It returns `True` if the command's exit status is 0, `False` otherwise (including when the command cannot be started).
- `do_it_to_this_path` is the one interception point. For a custom action, a throw-away copy of the program replaces only this function with a hand-written one. It never needs to know about dry-run: in dry-run mode it is simply not called.

## 6. Filter data

- The three rule lists (directory excludes, filename glob excludes, filename regex excludes) are plain, flat Python tuples of strings near the top of the program.
- One set of rules for every repo the program is used on (decided for now; per-repo rules may come later).
- Adding a rule means adding a line to a tuple, never changing control flow.
- The roots are **not** in the program; they are on the command line only.

## 7. Output and report

The same report lines are printed in both run mode and dry-run mode. Paths are shown relative to the current directory and sorted, so two reports can be compared with `diff`.

- One line per file or pruned directory, showing:
  - `RUN` (or `WOULD RUN` in dry-run), or `SKIP`;
  - for `SKIP`: the stage and the exact rule that caught it, e.g. `SKIP DIR py/.mws_venv [dir rule: .*_venv]`, `SKIP py/lib1/x_OLD.py [glob: *OLD.py]`, `SKIP py/lib1/x_V2.py [regex: _V\d+\.py$]`, and with `--verbose` only, `SKIP LINK py/lib1/foo.py [symlink]` and `SKIP NOMATCH py/lib1/notes.txt [-g: *.py]`.
- In run mode, the `RUN` line is printed (and stdout flushed) just before the command runs, so it acts as a header for that command's own output, which appears in place right after it. The command's stdout and stderr both go straight through.
- A failed command gets a line naming the file and its exit status.
- Summary at the end:
  - counts: files run, files skipped, symlinks skipped, files not matching `-g`, failures;
  - count of hits for each rule;
  - **rules that matched nothing**, listed per stage (catches a mistyped pattern). Note: a rule can also show as unmatched because an earlier stage already removed every file it would have caught;
  - the list of failed paths, if any.

## 8. Errors and exit status

- Without `--stop-on-error`: keep going after a failed command; list all failures in the summary.
- With `--stop-on-error`: stop after the first failed command; print the summary for what was done so far.
- Exit status: `0` if every command succeeded (or dry-run finished), `1` if any command failed, `2` for usage and startup errors (bad options, missing root, command not on `PATH`, bad regex). `2` for usage errors is what Python's `argparse` uses.

## 9. Notes

- Unlike `rg`, this program does not read `.gitignore`. Anything gitignored is skipped only if a rule here says so.

## 10. Implementation decisions (approved)

1. Line 1 is the shebang `#!/usr/bin/env python3` (needed to run from `~/bin`); line 2 is the filename comment; the header comment also holds the line-marker declaration `# LINEMARKER=AATF`.
2. Report lines (`RUN` / `WOULD RUN` / `SKIP ...`) and the summary carry no line markers, so dry-run reports from before and after a rule change can be compared with `diff`. Only NOTE, ERROR, FAILED and exit-status lines carry `AATF$nnn` markers.
3. `do_it_to_this_path(file_path: str) -> bool` gets the command from `_command_words`, a module-level variable set once by `main()`. A hand-written replacement can ignore it.
4. A root that is itself a symlink is walked (roots are never tested). Symlinks below a root are skipped as in Stage 1.
5. ERROR lines go to stderr; everything else goes to stdout. To save a run's output to a file with each command's error messages in place, use `2>&1`.
6. The module-level constant `VERSION` (a string such as `"2026-11-17_1129"`) sits just below the module docstring, so the docstring stays the file's first statement. Update it whenever the program changes.
