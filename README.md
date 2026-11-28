# bughunt

36 small Python debugging exercises. Each has one bug of the kind that is easy to miss when reading code, plus a script that grades fixes and checks that the tasks themselves are sound.

Every task is a short module (8 to 40 lines) with one bug, a spec, the fixed version and a unittest file. Most of the tests pass on the buggy code. Only the standard library is used; Python 3.9+.

## Usage

```
python3 run.py list
python3 run.py show 06                    # the spec
cp tasks/06-late-binding-limits/buggy.py my_06.py
# ...fix my_06.py...
python3 run.py grade 06 my_06.py
python3 run.py grade-dir solutions/       # 07.py, 7.py or 07-slug.py per task
python3 run.py selfcheck                  # check all shipped tasks
```

Ids can be `6`, `06`, `06-late-binding-limits` or just `late-binding-limits`.

Your file gets copied in as `solution.py` next to the task's tests, so the name doesn't matter. `grade` exits 0 on pass, 1 on fail, 2 if you got the arguments wrong. `grade-dir` prints a table and a score, skips files it can't match to a task, and won't run anything if there are two files for the same task.

## Layout

```
tasks/NN-slug/
    task.md        spec, with a >>> example that fails on buggy.py
    buggy.py
    fixed.py
    test_task.py   imports from solution
    meta.json      category, difficulty (1-3), summary of the bug
```

`meta.json` is the answer key. If you give these to someone, give them `task.md` and `buggy.py` only.

## How grading works

The solution and the test file go into a temp dir and run in a separate `python -I -B` process (`harness.py`). The harness writes results to a JSON file rather than stdout, so printing a fake result doesn't do anything. The temp dir is deleted afterwards.

Default time limit is 10s (`--timeout`, max 120); on timeout the whole process group is killed. Only the first 64 KiB of output is kept. On POSIX the child also gets rlimits (15s CPU, 2 GiB memory, 8 MiB file size), an empty stdin and an environment with only `PATH` and a fixed `TZ`. Syntax errors, `sys.exit()`, `os._exit()`, crashes and hangs all count as failures and are reported as ERROR, CRASH or TIMEOUT.

`selfcheck` goes through every task and fails if any of these don't hold:

- all five files exist and `meta.json` is valid
- `buggy.py` is 8 to 40 lines and differs from `fixed.py`
- `buggy.py` passes at least one test and fails at least one
- `fixed.py` passes all of them
- the `>>>` example in `task.md` passes on `fixed.py` and fails on `buggy.py`
- `test_task.py` doesn't sleep, read the clock/env/files, use the network or unseeded `random`

`--repeat N` runs everything N times to catch flaky tests.

## Tasks

10 easy, 20 medium, 6 hard.

| ID | Task | Bug category | Difficulty |
|----|------|--------------|------------|
| 01 | moving-window-sums | off-by-one | 1 |
| 02 | mutable-default-tags | mutable-default-argument | 1 |
| 03 | mean-int-division | integer-division | 1 |
| 04 | float-total-equality | float-comparison | 1 |
| 05 | fee-rounding | rounding | 2 |
| 06 | late-binding-limits | late-binding-closure | 2 |
| 07 | shallow-copy-grid | shallow-copy | 2 |
| 08 | remove-while-iterating | mutation-during-iteration | 2 |
| 09 | exhausted-iterator-scale | exhausted-iterator | 2 |
| 10 | precedence-checkout | operator-precedence | 1 |
| 11 | identity-vs-equality | identity-vs-equality | 2 |
| 12 | casefold-names | unicode-casefold | 2 |
| 13 | combining-marks-length | unicode-combining-marks | 3 |
| 14 | stable-priority-sort | sort-stability | 2 |
| 15 | version-sort-key | sort-key | 1 |
| 16 | naive-aware-seconds | naive-vs-aware-datetime | 2 |
| 17 | falsy-config-default | falsy-default | 1 |
| 18 | setdefault-shared-list | setdefault-shared-default | 2 |
| 19 | bare-except-json | bare-except | 2 |
| 20 | early-return-validation | early-return | 2 |
| 21 | shadowed-format | shadowed-builtin | 2 |
| 22 | lower-bound-search | binary-search-bounds | 2 |
| 23 | wrap-add-int32 | integer-wraparound | 3 |
| 24 | nesting-depth | recursion-base-case | 2 |
| 25 | greedy-bold-tags | regex-greedy | 1 |
| 26 | id-anchor-newline | regex-anchor | 3 |
| 27 | pagination-has-next | pagination | 2 |
| 28 | csv-embedded-newline | csv-parsing | 3 |
| 29 | path-absolute-join | path-join | 2 |
| 30 | fsum-balance | float-summation | 2 |
| 31 | lru-cache-stale | lru-cache-mutable-state | 3 |
| 32 | truncate-utf8 | bytes-vs-str | 2 |
| 33 | add-months | month-arithmetic | 3 |
| 34 | header-split-colon | string-split | 1 |
| 35 | defaultdict-lookup | defaultdict-side-effect | 2 |
| 36 | remove-prefix-lstrip | str-strip-misuse | 1 |

Difficulty 1: you can see it if you read carefully. 3: you need to know some language or library detail, or it only shows up at the edges.

## Don't grade untrusted code on your own machine

The limits above are there for infinite loops and runaway output. They are not a sandbox. A solution can still read your files, open sockets, spawn processes that escape the group, or write a fake result file. If you are grading code from people you don't know, do it in a throwaway container or VM with no network and no credentials.

## Tests

```
python3 -m unittest -v
```

This tests the runner (`test_run.py`), not the tasks. Takes about a minute.

MIT licensed.
