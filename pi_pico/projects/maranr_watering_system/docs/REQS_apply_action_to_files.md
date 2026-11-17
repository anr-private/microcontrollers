# REQS_apply_action_to_files.md

# apply_action_to_files: Requirements

Status: requirements draft 2 (2026-11-16). Items marked **OPEN** still need a decision.

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
- Only directories **below** a root are tested. Parent directories above a root are never tested.
- A directory that matches a rule is not entered at all (it is pruned). The report shows one line for it, not one line per file inside it.
- Symlinks, to directories **or** to files, are not followed and not processed. Each is reported as skipped.
- Overlapping roots (e.g. `py/` and `py/lib1/`): each file is kept once, by its real path, and a note says which roots overlap.

### Stage 2: Select candidates with `-g`

- Keep only files whose **filename** (not the directory path) matches the `-g` glob, case-sensitive.
- Files that do not match `-g` are not reported individually (they were never candidates).

### Stage 3: Filename glob excludes

- A list of glob patterns, case-sensitive (`fnmatch.fnmatchcase`), each tested against the **filename only**. Similar to `.gitignore` patterns for file names.
- Starting list:

```
*OLD.py
*DEPRECATED.py
*NOTUSED.py
*NOT_USED.py
*JUNK*.py
*junk*.py
*IGNORE.py
*IGNORED.py
*SAVE.py
```

### Stage 4: Filename regex excludes

- A short list of Python regular expressions, each tested against the **filename only** with `re.search`. That means a pattern matches anywhere in the name unless it uses `^` (start) or `$` (end). Any Python `re` syntax is allowed.
- Kept separate from Stage 3 and kept as simple as possible. Anything a glob can do goes in Stage 3 instead.
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
- Adding a rule means adding a line to a tuple, never changing control flow.
- The roots are **not** in the program; they are on the command line only.

## 7. Output and report

The same report lines are printed in both run mode and dry-run mode. Paths are shown relative to the current directory and sorted, so two reports can be compared with `diff`.

- One line per file or pruned directory, showing:
  - `RUN` (or `WOULD RUN` in dry-run), or `SKIP`;
  - for `SKIP`: the stage and the exact rule that caught it, e.g. `SKIP DIR py/.mws_venv [dir rule: .*_venv]`, `SKIP py/lib1/x_OLD.py [glob: *OLD.py]`, `SKIP py/lib1/x_V2.py [regex: _V\d+\.py$]`, `SKIP LINK py/lib1/foo.py [symlink]`.
- In run mode, the `RUN` line is printed (and stdout flushed) just before the command runs, so it acts as a header for that command's own output, which appears in place right after it. The command's stdout and stderr both go straight through.
- A failed command gets a line naming the file and its exit status.
- Summary at the end:
  - counts: files run, files skipped, failures;
  - count of hits for each rule;
  - **rules that matched nothing**, listed per stage (catches a mistyped pattern). Note: a rule can also show as unmatched because an earlier stage already removed every file it would have caught;
  - the list of failed paths, if any.

## 8. Errors and exit status

- Without `--stop-on-error`: keep going after a failed command; list all failures in the summary.
- With `--stop-on-error`: stop after the first failed command; print the summary for what was done so far.
- Exit status: `0` if every command succeeded (or dry-run finished), `1` if any command failed, `2` for usage and startup errors (bad options, missing root, command not on `PATH`, bad regex). `2` for usage errors is what Python's `argparse` uses.

## 9. Open questions

1. **OPEN — where the rule tuples live.** The program lives in `~/bin` and can be used on any repo, but the rule tuples (Section 6) are inside it, so every repo gets the same rules. Fine for now, or should a repo be able to supply its own rules later?
2. **OPEN — is a root itself tested by the directory rules?** Proposal: no. A root given on the command line is always walked, even if its own name matches a rule (e.g. `apply_action_to_files ... .mws_venv/` would be walked).
3. **OPEN — initial directory rules.** Proposal: `.*_venv`, `.git`, `__pycache__`. Note: unlike `rg`, this program does not read `.gitignore`, so anything gitignored (e.g. `*COPY*`, `*IGNORE*` scratch files and dirs) is only skipped if a rule here says so. Add `*COPY*` and `*IGNORE*` as directory rules too?
4. **OPEN — case-insensitive matching.** Globs stay case-sensitive. If ever needed, a regex in Stage 4 can be made case-insensitive by starting it with `(?i)`; no new feature is needed for that.
5. **OPEN — symlink skip lines.** Proposal: reported like other skips (`SKIP LINK ...`). Or should they be silent?
