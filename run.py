#!/usr/bin/env python3
# bughunt runner. This executes candidate code: read the warning in README.md.

import argparse
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TASKS_DIR = os.path.join(ROOT, "tasks")
HARNESS = os.path.join(ROOT, "harness.py")

DEFAULT_TIMEOUT = 10.0
MAX_TIMEOUT = 120.0
OUTPUT_CAP = 64 * 1024
RESULT_CAP = 1024 * 1024
MAX_SOURCE_BYTES = 1024 * 1024
MAX_ID_LENGTH = 64  # newer Pythons refuse int() on very long digit strings

NAME_RE = re.compile(r"^([0-9]{2,6})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
REQUIRED_FILES = ("task.md", "buggy.py", "fixed.py", "test_task.py", "meta.json")
BUGGY_LINES = (8, 40)

# selfcheck rejects test files that match any of these
TEST_LINT = [
    (r"\bsleep\s*\(", "sleeps"),
    (r"\bdatetime\.(now|utcnow|today)\b|\bdate\.today\b|\btime\.(time|localtime|gmtime)\b",
     "reads the clock"),
    (r"\bos\.environ\b|\bgetenv\b|\bimport locale\b|\bsetlocale\b", "reads environment or locale"),
    (r"\bopen\s*\(|\bos\.listdir\b|\bglob\b|\bpathlib\b|\btempfile\b", "touches the file system"),
    (r"\bsocket\b|\burllib\b|\bhttp\.client\b", "uses the network"),
]


class RunnerError(Exception):
    pass


def clean(text, limit=300):
    # for anything the candidate controls: one line, no control characters
    out = []
    for ch in str(text):
        if ch in "\n\r\t":
            out.append(" ")
        elif ch.isprintable():
            out.append(ch)
        else:
            out.append("?")
    text = "".join(out)
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def format_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    lines = []
    for row in [headers] + [["-" * w for w in widths]] + rows:
        lines.append("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip())
    return "\n".join(lines)


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class Task:
    def __init__(self, name, path):
        match = NAME_RE.match(name)
        self.name = name
        self.id = match.group(1)
        self.number = int(self.id)
        self.slug = match.group(2)
        self.path = path

    def file(self, filename):
        return os.path.join(self.path, filename)

    def meta(self):
        try:
            data = json.loads(read_text(self.file("meta.json")))
        except (OSError, ValueError) as exc:
            raise RunnerError("%s: cannot read meta.json (%s)" % (self.name, exc))
        problems = meta_problems(data)
        if problems:
            raise RunnerError("%s: meta.json: %s" % (self.name, "; ".join(problems)))
        return data


def meta_problems(data):
    if not isinstance(data, dict):
        return ["must be a JSON object"]
    problems = []
    category = data.get("category")
    if not isinstance(category, str) or not category.strip():
        problems.append("category must be a non-empty string")
    difficulty = data.get("difficulty")
    if type(difficulty) is not int or difficulty not in (1, 2, 3):
        problems.append("difficulty must be 1, 2 or 3")
    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        problems.append("summary must be a non-empty string")
    return problems


def discover_tasks(tasks_dir):
    if not os.path.isdir(tasks_dir):
        raise RunnerError("tasks directory not found: %s" % tasks_dir)
    tasks = []
    for name in sorted(os.listdir(tasks_dir)):
        path = os.path.join(tasks_dir, name)
        if NAME_RE.match(name) and os.path.isdir(path) and not os.path.islink(path):
            tasks.append(Task(name, path))
    seen = {}
    for task in tasks:
        if task.number in seen:
            raise RunnerError(
                "two tasks share the number %s: %s and %s" % (task.id, seen[task.number], task.name)
            )
        seen[task.number] = task.name
    tasks.sort(key=lambda t: t.number)
    return tasks


def resolve_task(tasks, ident):
    # '7', '07', '07-slug' or 'slug'. Only compared with task names, never used as a path.
    ident = ident.strip()
    hits = []
    if ident.isascii() and ident.isdigit():
        if len(ident) <= MAX_ID_LENGTH:
            hits = [t for t in tasks if t.number == int(ident)]
    else:
        hits = [t for t in tasks if t.name == ident] or [t for t in tasks if t.slug == ident]
    if not hits:
        raise RunnerError("unknown task id %r (run `python3 run.py list`)" % ident[:MAX_ID_LENGTH])
    if len(hits) > 1:
        raise RunnerError("task id %r is ambiguous" % ident)
    return hits[0]


def _child_env():
    # fixed non-UTC zone so local-time bugs fail the same way on every machine
    env = {"TZ": "Asia/Kolkata"}
    for key in ("PATH", "SYSTEMROOT"):
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def _wait_for_exit(proc, timeout):
    # Returns (exited, can_kill_group). With waitid(WNOWAIT) the child stays
    # unreaped, so its pgid can't be reused before we kill what's left in it.
    if not (hasattr(os, "waitid") and hasattr(os, "WNOWAIT") and hasattr(os, "P_PID")):
        # No waitid (macOS): the child is already reaped here, but its group
        # id stays taken while any process it left behind is alive, so
        # killing the group still only hits those leftovers.
        try:
            proc.wait(timeout=timeout)
            return True, True
        except subprocess.TimeoutExpired:
            return False, True
    deadline = time.monotonic() + timeout
    delay = 0.001
    while True:
        try:
            info = os.waitid(os.P_PID, proc.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        except ChildProcessError:
            return True, False
        if info is not None:
            return True, True
        if time.monotonic() >= deadline:
            return False, True
        time.sleep(delay)
        delay = min(delay * 2, 0.02)


def _kill(proc, group):
    if group and os.name == "posix":
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        proc.kill()
    except OSError:
        pass


def run_capped(cmd, cwd, timeout):
    # own session, so the whole process group can be killed afterwards
    kwargs = {}
    if os.name == "posix":
        kwargs["start_new_session"] = True
    started = time.monotonic()
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=_child_env(),
        bufsize=0,
        **kwargs
    )
    captured = {"data": bytearray(), "total": 0}

    def pump():
        try:
            while True:
                chunk = proc.stdout.read(65536)
                if not chunk:
                    return
                captured["total"] += len(chunk)
                room = OUTPUT_CAP - len(captured["data"])
                if room > 0:
                    captured["data"] += chunk[:room]
        except (OSError, ValueError):
            return
        finally:
            try:
                proc.stdout.close()
            except OSError:
                pass

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()
    try:
        exited, group_ok = _wait_for_exit(proc, timeout)
        if not exited:
            _kill(proc, True)
        elif group_ok:
            _kill(proc, True)  # stragglers started by the candidate
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _kill(proc, True)
    except BaseException:
        _kill(proc, True)
        raise
    finally:
        reader.join(timeout=2)
    return {
        "timed_out": not exited,
        "returncode": proc.returncode,
        "output": bytes(captured["data"]),
        "truncated": captured["total"] > len(captured["data"]),
        "seconds": time.monotonic() - started,
    }


def _read_result(path):
    try:
        if os.path.getsize(path) > RESULT_CAP:
            return None
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def execute(mode, source_bytes, task, timeout):
    root = tempfile.mkdtemp(prefix="bughunt-")
    try:
        work = os.path.join(root, "work")
        os.mkdir(work)
        with open(os.path.join(work, "solution.py"), "wb") as handle:
            handle.write(source_bytes)
        shutil.copyfile(task.file("test_task.py"), os.path.join(work, "test_task.py"))
        result_path = os.path.join(root, "result.json")
        cmd = [sys.executable, "-I", "-B", HARNESS, mode, work, result_path]
        if mode == "examples":
            cmd.append(task.file("task.md"))
        run = run_capped(cmd, work, timeout)
        run["result"] = _read_result(result_path)
        return run
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _how_it_ended(run):
    code = run["returncode"]
    if code is None:
        return "no exit status"
    if code < 0:
        return "killed by signal %d" % -code
    return "exit status %d" % code


class Outcome:
    def __init__(self, status, tests=(), detail="", output="", truncated=False, seconds=0.0):
        self.status = status  # pass, fail, error, timeout or crash
        self.tests = list(tests)  # (name, status, message)
        self.detail = detail
        self.output = output
        self.truncated = truncated
        self.seconds = seconds

    @property
    def passed(self):
        return sum(1 for t in self.tests if t[1] == "pass")

    @property
    def total(self):
        return len(self.tests)

    @property
    def failing(self):
        return [t for t in self.tests if t[1] != "pass"]

    @property
    def ok(self):
        return self.status == "pass"

    def signature(self):
        return (self.status, tuple((t[0], t[1]) for t in self.tests))


def _outcome_from_run(run, timeout):
    output = run["output"].decode("utf-8", "replace")
    common = dict(output=output, truncated=run["truncated"], seconds=run["seconds"])
    if run["timed_out"]:
        return Outcome("timeout", detail="no result after %g s; the process was killed" % timeout, **common)
    result = run["result"]
    if result is None:
        return Outcome(
            "crash",
            detail="the test process ended (%s) without reporting results" % _how_it_ended(run),
            **common
        )
    if "load_error" in result:
        return Outcome("error", detail="could not load: %s" % clean(result["load_error"]), **common)
    raw = result.get("tests")
    tests = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get("status") in ("pass", "fail", "error", "skip"):
                tests.append((clean(item.get("name", "?"), 120), item["status"], clean(item.get("message", ""))))
    if not tests:
        return Outcome("crash", detail="the result file was empty or malformed", **common)
    status = "pass" if all(t[1] == "pass" for t in tests) else "fail"
    return Outcome(status, tests=tests, **common)


def run_tests(task, source_bytes, timeout=DEFAULT_TIMEOUT):
    return _outcome_from_run(execute("tests", source_bytes, task, timeout), timeout)


def run_examples(task, source_bytes, timeout=DEFAULT_TIMEOUT):
    # -> (status, attempted, failed, detail) for the >>> examples in task.md
    run = execute("examples", source_bytes, task, timeout)
    if run["timed_out"]:
        return "timeout", 0, 0, "examples timed out"
    result = run["result"]
    if result is None:
        return "crash", 0, 0, "examples ended (%s) without a result" % _how_it_ended(run)
    if "load_error" in result:
        return "error", 0, 0, "could not load: %s" % clean(result["load_error"])
    try:
        return "done", int(result["attempted"]), int(result["failed"]), clean(result.get("message", ""))
    except (KeyError, TypeError, ValueError):
        return "crash", 0, 0, "malformed examples result"


def load_source(path, label=None):
    shown = label or path
    if os.path.isdir(path):
        raise RunnerError("%s is a directory, not a file" % shown)
    if not os.path.exists(path):
        raise RunnerError("no such file: %s" % shown)
    try:
        if not stat.S_ISREG(os.stat(path).st_mode):  # a FIFO would block the read
            raise RunnerError("%s is not a regular file" % shown)
        with open(path, "rb") as handle:
            data = handle.read(MAX_SOURCE_BYTES + 1)
    except OSError as exc:
        raise RunnerError("cannot read %s: %s" % (shown, exc.strerror or exc))
    if len(data) > MAX_SOURCE_BYTES:
        raise RunnerError("%s is too large (the limit is %d bytes)" % (shown, MAX_SOURCE_BYTES))
    return data


class CheckRow:
    def __init__(self, task):
        self.task = task
        self.category = "?"
        self.difficulty = "?"
        self.buggy = None
        self.fixed = None
        self.example = "-"
        self.violations = []

    @property
    def ok(self):
        return not self.violations


def _count(outcome):
    if outcome is None:
        return "-"
    if outcome.tests:
        return "%dP/%dF" % (outcome.passed, outcome.total - outcome.passed)
    return outcome.status


def _repeat_outcomes(task, source, timeout, repeat):
    first = run_tests(task, source, timeout)
    unstable = False
    for _ in range(repeat - 1):
        again = run_tests(task, source, timeout)
        if again.signature() != first.signature():
            unstable = True
    return first, unstable


def check_task(task, timeout=DEFAULT_TIMEOUT, repeat=1):
    row = CheckRow(task)
    bad = row.violations.append
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(task.file(f))]
    if missing:
        bad("missing file(s): %s" % ", ".join(missing))
        return row
    try:
        meta = task.meta()
        row.category, row.difficulty = meta["category"], str(meta["difficulty"])
    except RunnerError as exc:
        bad(str(exc).split(": ", 1)[-1])
    try:
        buggy = load_source(task.file("buggy.py"))
        fixed = load_source(task.file("fixed.py"))
        test_source = read_text(task.file("test_task.py"))
        spec = read_text(task.file("task.md"))
    except (RunnerError, OSError, UnicodeDecodeError) as exc:
        bad("cannot read task files: %s" % exc)
        return row

    lines = len(buggy.decode("utf-8", "replace").splitlines())
    if not BUGGY_LINES[0] <= lines <= BUGGY_LINES[1]:
        bad("buggy.py has %d lines (expected %d to %d)" % ((lines,) + BUGGY_LINES))
    if buggy == fixed:
        bad("buggy.py and fixed.py are identical")
    if "from solution import" not in test_source:
        bad("test_task.py does not import from solution")
    for pattern, what in TEST_LINT:
        if re.search(pattern, test_source):
            bad("test_task.py %s (tests must be deterministic)" % what)
    if re.search(r"\brandom\b", test_source) and not re.search(r"\bseed\s*\(|Random\s*\(\s*[0-9A-Za-z_]", test_source):
        bad("test_task.py uses random without a fixed seed")

    row.buggy, unstable_b = _repeat_outcomes(task, buggy, timeout, repeat)
    row.fixed, unstable_f = _repeat_outcomes(task, fixed, timeout, repeat)
    if unstable_b or unstable_f:
        bad("test results differ between repeated runs (not deterministic)")

    b, f = row.buggy, row.fixed
    if f.status != "pass":
        why = "; ".join("%s (%s)" % (t[0], t[2]) for t in f.failing[:3]) or f.detail
        bad("fixed.py does not pass all tests: %s" % why)
    if b.status in ("timeout", "crash", "error"):
        bad("buggy.py cannot be tested (%s): %s" % (b.status, b.detail))
    elif b.status == "pass":
        bad("buggy.py passes every test, so the tests do not detect the bug")
    elif b.passed == 0:
        bad("buggy.py fails every test; at least one test must pass on it")
    if b.tests and f.tests and b.total != f.total:
        bad("buggy and fixed ran a different number of tests")

    ex_fixed = run_examples(task, fixed, timeout)
    ex_buggy = run_examples(task, buggy, timeout)
    if ex_fixed[0] != "done" or ex_fixed[1] < 1:
        bad("task.md needs a runnable '>>>' example that fixed.py reproduces (%s)" % ex_fixed[3])
        row.example = "bad"
    elif ex_fixed[2] != 0:
        bad("task.md example fails on fixed.py: %s" % ex_fixed[3])
        row.example = "bad"
    elif ex_buggy[0] == "done" and ex_buggy[2] == 0:
        bad("task.md example passes on buggy.py, so it does not show the failure")
        row.example = "weak"
    else:
        row.example = "ok"
    return row


def selfcheck(tasks, timeout=DEFAULT_TIMEOUT, repeat=1):
    return [check_task(task, timeout, repeat) for task in tasks]


def cmd_list(args, tasks):
    rows = []
    for task in tasks:
        try:
            meta = task.meta()
            rows.append([task.id, task.slug, meta["category"], str(meta["difficulty"])])
        except RunnerError:
            rows.append([task.id, task.slug, "?", "?"])
    print(format_table(["ID", "TASK", "BUG CATEGORY", "DIFFICULTY"], rows))
    return 0


def cmd_show(args, tasks):
    task = resolve_task(tasks, args.id)
    try:
        text = read_text(task.file("task.md"))
    except (OSError, UnicodeDecodeError) as exc:
        raise RunnerError("cannot read task.md for %s: %s" % (task.name, exc))
    print(text.rstrip("\n"))
    return 0


def cmd_selfcheck(args, tasks):
    if not tasks:
        raise RunnerError("no tasks found")
    rows = selfcheck(tasks, args.timeout, args.repeat)
    table = []
    for row in rows:
        table.append([
            row.task.id, row.task.slug, row.category, row.difficulty,
            _count(row.buggy), _count(row.fixed), row.example,
            "ok" if row.ok else "VIOLATION",
        ])
    print(format_table(
        ["ID", "TASK", "CATEGORY", "D", "BUGGY", "FIXED", "EXAMPLE", "STATUS"], table
    ))
    bad = [r for r in rows if not r.ok]
    if bad:
        print()
        for row in bad:
            for problem in row.violations:
                print("%s: %s" % (row.task.name, problem))
    print()
    print("%d task(s) checked, %d with violations" % (len(rows), len(bad)))
    return 1 if bad else 0


def describe_outcome(outcome):
    if outcome.status == "pass":
        return "PASS (%d/%d tests passed)" % (outcome.passed, outcome.total)
    if outcome.status == "fail":
        return "FAIL (%d/%d tests passed)" % (outcome.passed, outcome.total)
    return "%s (%s)" % (outcome.status.upper(), outcome.detail)


def cmd_grade(args, tasks):
    task = resolve_task(tasks, args.id)
    source = load_source(args.file)
    outcome = run_tests(task, source, args.timeout)
    print("%s: %s" % (task.name, describe_outcome(outcome)))
    if outcome.status == "fail":
        print("failing tests:")
        for name, status, message in outcome.failing:
            print("  - %s [%s]%s" % (name, status, ": " + message if message else ""))
    if args.verbose and outcome.output:
        print("captured output%s:" % (" (truncated)" if outcome.truncated else ""))
        print(clean(outcome.output, 2000))
    elif outcome.truncated:
        print("note: the candidate printed a lot of output; only the first %d bytes were kept" % OUTPUT_CAP)
    return 0 if outcome.ok else 1


def cmd_grade_dir(args, tasks):
    directory = args.dir
    if not os.path.isdir(directory):
        raise RunnerError("not a directory: %s" % directory)
    try:
        entries = sorted(os.listdir(directory))
    except OSError as exc:
        raise RunnerError("cannot read %s: %s" % (directory, exc.strerror or exc))
    files = {}
    ignored = []
    for entry in entries:
        path = os.path.join(directory, entry)
        stem, ext = os.path.splitext(entry)
        if ext != ".py" or os.path.isdir(path):
            ignored.append((entry, "not a .py file"))
            continue
        if os.path.islink(path):
            ignored.append((entry, "symbolic link"))
            continue
        try:
            task = resolve_task(tasks, stem)
        except RunnerError:
            ignored.append((entry, "no matching task"))
            continue
        files.setdefault(task.number, []).append(entry)

    rows = []
    solved = 0
    for task in tasks:
        names = files.get(task.number, [])
        if not names:
            rows.append([task.id, task.slug, "-", "MISSING", "-"])
            continue
        if len(names) > 1:
            rows.append([task.id, task.slug, ", ".join(clean(n, 40) for n in names),
                         "AMBIGUOUS", "several files for one task; none was run"])
            continue
        shown = clean(names[0], 40)
        try:
            source = load_source(os.path.join(directory, names[0]), label=shown)
        except RunnerError as exc:
            rows.append([task.id, task.slug, shown, "ERROR", str(exc)])
            continue
        outcome = run_tests(task, source, args.timeout)
        if outcome.ok:
            solved += 1
        if outcome.tests:
            detail = "%d/%d tests" % (outcome.passed, outcome.total)
        else:
            detail = clean(outcome.detail, 80)
        rows.append([task.id, task.slug, shown, outcome.status.upper(), detail])

    print(format_table(["ID", "TASK", "FILE", "RESULT", "DETAIL"], rows))
    if ignored:
        print()
        print("ignored %d entr%s:" % (len(ignored), "y" if len(ignored) == 1 else "ies"))
        for name, why in ignored[:20]:
            print("  %s (%s)" % (clean(name, 60), why))
        if len(ignored) > 20:
            print("  ... and %d more" % (len(ignored) - 20))
    print()
    print("Score: %d/%d tasks solved" % (solved, len(tasks)))
    return 0


def _timeout(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("not a number: %r" % text)
    if not 0 < value <= MAX_TIMEOUT:
        raise argparse.ArgumentTypeError("must be above 0 and at most %g" % MAX_TIMEOUT)
    return value


def _repeat(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("not an integer: %r" % text)
    if not 1 <= value <= 20:
        raise argparse.ArgumentTypeError("must be between 1 and 20")
    return value


def build_parser():
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Grade bughunt solutions, or check the task set itself.",
    )
    parser.add_argument("--tasks-dir", metavar="DIR", default=DEFAULT_TASKS_DIR,
                        help="where the NN-slug task folders are (default: ./tasks)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    p = sub.add_parser("list", help="list all tasks")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="print the specification of one task")
    p.add_argument("id", help="task number (7 or 07) or name (07-late-binding-limits)")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("selfcheck", help="check every task (buggy fails some tests, fixed passes all)")
    p.add_argument("--timeout", type=_timeout, default=DEFAULT_TIMEOUT, help="seconds per run (default 10)")
    p.add_argument("--repeat", type=_repeat, default=1,
                   help="run each test file N times, flag results that change")
    p.set_defaults(func=cmd_selfcheck)

    p = sub.add_parser("grade", help="grade one solution file against one task")
    p.add_argument("id")
    p.add_argument("file", help="solution file")
    p.add_argument("--timeout", type=_timeout, default=DEFAULT_TIMEOUT, help="seconds (default 10)")
    p.add_argument("-v", "--verbose", action="store_true", help="show what the solution printed")
    p.set_defaults(func=cmd_grade)

    p = sub.add_parser("grade-dir", help="grade a folder of solutions (07.py, 07-slug.py)")
    p.add_argument("dir")
    p.add_argument("--timeout", type=_timeout, default=DEFAULT_TIMEOUT, help="seconds per task (default 10)")
    p.set_defaults(func=cmd_grade_dir)
    return parser


def main(argv=None):
    # don't die on an ascii-only terminal
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2
    try:
        tasks = discover_tasks(os.path.abspath(args.tasks_dir))
        return args.func(args, tasks)
    except RunnerError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except BrokenPipeError:  # e.g. `run.py list | head`
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 1
    except Exception as exc:
        print("internal error: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
