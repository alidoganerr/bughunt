# Tests for run.py and harness.py. python3 -m unittest -v

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run  # noqa: E402

RUN_PY = os.path.join(HERE, "run.py")
TASKS_DIR = os.path.join(HERE, "tasks")
POSIX = os.name == "posix"

HEADER = "# filler: selfcheck wants buggy.py to have at least 8 lines\n" + "\n" * 5
BUGGY = HEADER + 'def add(a, b):\n    """Sum of a and b."""\n    return a - b\n'
FIXED = HEADER + 'def add(a, b):\n    """Sum of a and b."""\n    return a + b\n'
SPEC = "# Add\n\nWrite `add(a, b)`.\n\n## Example\n\n```python\n>>> add(2, 3)\n5\n```\n"
META = {"category": "demo", "difficulty": 1, "summary": "subtracts instead of adding"}
TEST = (
    "import unittest\n\nfrom solution import add\n\n\n"
    "class AddTest(unittest.TestCase):\n"
    "    def test_basic(self):\n        self.assertEqual(add(2, 3), 5)\n\n"
    "    def test_zero(self):\n        self.assertEqual(add(0, 0), 0)\n"
)


def cli(*args, **kwargs):
    return subprocess.run(
        [sys.executable, RUN_PY] + list(args),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=180, **kwargs
    )


def write(path, text, mode="w"):
    with open(path, mode) as handle:
        handle.write(text)


def make_task(tasks_dir, name="01-demo", buggy=BUGGY, fixed=FIXED, test=TEST, spec=SPEC, meta=META):
    path = os.path.join(tasks_dir, name)
    os.makedirs(path, exist_ok=True)
    write(os.path.join(path, "buggy.py"), buggy)
    write(os.path.join(path, "fixed.py"), fixed)
    write(os.path.join(path, "test_task.py"), test)
    write(os.path.join(path, "task.md"), spec)
    write(os.path.join(path, "meta.json"), json.dumps(meta))
    return path


def shipped_task(number):
    return run.resolve_task(run.discover_tasks(TASKS_DIR), str(number))


def shipped_source(number, which):
    with open(shipped_task(number).file(which), "rb") as handle:
        return handle.read()


def is_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    try:
        with open("/proc/%d/stat" % pid) as handle:
            return handle.read().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return True


def leftover_temp_dirs():
    return sorted(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bughunt-"))


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name

    def candidate(self, source, name="cand.py"):
        path = os.path.join(self.tmp, name)
        if isinstance(source, bytes):
            write(path, source, "wb")
        else:
            write(path, source)
        return path


class ShippedTasksTest(unittest.TestCase):
    def test_selfcheck_passes(self):
        proc = cli("selfcheck")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("0 with violations", proc.stdout)

    def test_difficulty_spread(self):
        tasks = run.discover_tasks(TASKS_DIR)
        self.assertGreaterEqual(len(tasks), 28)
        levels = {}
        for task in tasks:
            level = task.meta()["difficulty"]
            levels[level] = levels.get(level, 0) + 1
        for level in (1, 2, 3):
            self.assertGreaterEqual(levels.get(level, 0), 5, levels)

    def test_task_folder_files(self):
        for task in run.discover_tasks(TASKS_DIR):
            self.assertEqual(sorted(os.listdir(task.path)), sorted(run.REQUIRED_FILES), task.name)

    def test_readme_table(self):
        with open(os.path.join(HERE, "README.md"), encoding="utf-8") as handle:
            readme = handle.read()
        rows = {}
        for match in re.finditer(r"^\| (\d+) \| ([a-z0-9-]+) \| ([a-z0-9-]+) \| ([123]) \|$", readme, re.M):
            rows[match.group(1)] = (match.group(2), match.group(3), int(match.group(4)))
        expected = {}
        for task in run.discover_tasks(TASKS_DIR):
            meta = task.meta()
            expected[task.id] = (task.slug, meta["category"], meta["difficulty"])
        self.assertEqual(rows, expected)

    def test_buggy_fails_fixed_passes(self):
        for task in run.discover_tasks(TASKS_DIR):
            with open(task.file("buggy.py"), "rb") as handle:
                buggy = run.run_tests(task, handle.read())
            with open(task.file("fixed.py"), "rb") as handle:
                fixed = run.run_tests(task, handle.read())
            self.assertEqual(buggy.status, "fail", task.name)
            self.assertGreater(buggy.passed, 0, task.name)
            self.assertEqual(fixed.status, "pass", task.name)


class ListShowTest(unittest.TestCase):
    def test_list(self):
        proc = cli("list")
        self.assertEqual(proc.returncode, 0)
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 2 + len(run.discover_tasks(TASKS_DIR)))
        self.assertIn("BUG CATEGORY", lines[0])
        self.assertNotIn("summary", proc.stdout.lower())

    def test_show_id_forms(self):
        outputs = {cli("show", ident).stdout for ident in ("1", "01", "01-moving-window-sums", "moving-window-sums")}
        self.assertEqual(len(outputs), 1)
        self.assertIn("moving_sums", outputs.pop())

    def test_spec_has_no_answer(self):
        for task in run.discover_tasks(TASKS_DIR):
            summary = task.meta()["summary"]
            with open(task.file("task.md"), encoding="utf-8") as handle:
                self.assertNotIn(summary, handle.read())

    def test_bad_ids(self):
        for ident in ("99", "nope", "../../etc/passwd", "01/../02", "9" * 5000, "", "  ", "-1", "1e3", "١"):
            proc = cli("show", ident)
            self.assertEqual(proc.returncode, 2, ident[:20])
            self.assertIn("error: unknown task id", proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertEqual(proc.stdout, "")

    def test_bad_args(self):
        for args in ([], ["frobnicate"], ["grade"], ["selfcheck", "--timeout", "abc"], ["selfcheck", "--repeat", "0"]):
            proc = cli(*args)
            self.assertEqual(proc.returncode, 2, args)
            self.assertNotIn("Traceback", proc.stderr)

    def test_missing_tasks_dir(self):
        proc = cli("--tasks-dir", os.path.join(tempfile.gettempdir(), "bughunt-does-not-exist"), "list")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("tasks directory not found", proc.stderr)


class GradeTest(TempDirCase):
    def test_grade_cli(self):
        for number in (1, 17, 33):
            task = shipped_task(number)
            good = cli("grade", str(number), task.file("fixed.py"))
            self.assertEqual(good.returncode, 0, good.stdout)
            self.assertIn("PASS", good.stdout)
            bad = cli("grade", task.id, task.file("buggy.py"))
            self.assertEqual(bad.returncode, 1, bad.stdout)
            self.assertIn("FAIL", bad.stdout)
            self.assertIn("failing tests:", bad.stdout)
            self.assertIn("test_", bad.stdout)

    def test_failing_names(self):
        task = shipped_task(1)
        outcome = run.run_tests(task, shipped_source(1, "buggy.py"))
        names = {name for name, status, _ in outcome.failing}
        self.assertIn("MovingSumsTest.test_basic", names)
        self.assertNotIn("MovingSumsTest.test_empty_input", names)

    def test_infinite_loop(self):
        task = shipped_task(1)
        started = time.monotonic()
        outcome = run.run_tests(task, b"while True:\n    pass\n", timeout=2)
        self.assertEqual(outcome.status, "timeout")
        self.assertFalse(outcome.ok)
        self.assertLess(time.monotonic() - started, 8)

    def test_sleep_timeout(self):
        outcome = run.run_tests(shipped_task(1), b"import time\ntime.sleep(60)\n", timeout=2)
        self.assertEqual(outcome.status, "timeout")

    def test_hang_in_test(self):
        source = b"def moving_sums(values, k):\n    while True:\n        pass\n"
        self.assertEqual(run.run_tests(shipped_task(1), source, timeout=2).status, "timeout")

    def test_endless_print(self):
        source = b"while True:\n    print('x' * 1000)\n"
        started = time.monotonic()
        outcome = run.run_tests(shipped_task(1), source, timeout=2)
        self.assertEqual(outcome.status, "timeout")
        self.assertLessEqual(len(outcome.output), run.OUTPUT_CAP)
        self.assertTrue(outcome.truncated)
        self.assertLess(time.monotonic() - started, 8)

    def test_large_output_still_passes(self):
        flood = b"import sys\nfor _ in range(30):\n    sys.stdout.write('x' * 1000000)\n    sys.stderr.write('y' * 1000000)\n"
        outcome = run.run_tests(shipped_task(1), flood + shipped_source(1, "fixed.py"))
        self.assertEqual(outcome.status, "pass")
        self.assertLessEqual(len(outcome.output), run.OUTPUT_CAP)
        self.assertTrue(outcome.truncated)

    @unittest.skipUnless(POSIX, "process groups are POSIX only")
    def test_children_killed(self):
        pid_file = os.path.join(self.tmp, "child.pid")
        prelude = (
            "import subprocess, sys\n"
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
            "open(%r, 'w').write(str(child.pid))\n" % pid_file
        ).encode()
        started = time.monotonic()
        outcome = run.run_tests(shipped_task(1), prelude + shipped_source(1, "fixed.py"), timeout=5)
        self.assertEqual(outcome.status, "pass")
        self.assertLess(time.monotonic() - started, 4)
        with open(pid_file) as handle:
            pid = int(handle.read())
        deadline = time.monotonic() + 3
        while is_alive(pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertFalse(is_alive(pid), "the candidate's child process was left running")

    @unittest.skipUnless(POSIX, "process groups are POSIX only")
    def test_child_holding_pipe_after_timeout(self):
        source = (
            b"import subprocess, sys\n"
            b"subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
            b"while True:\n    pass\n"
        )
        started = time.monotonic()
        outcome = run.run_tests(shipped_task(1), source, timeout=2)
        self.assertEqual(outcome.status, "timeout")
        self.assertLess(time.monotonic() - started, 8)

    @unittest.skipUnless(POSIX, "needs POSIX sessions")
    def test_escaped_grandchild_holding_pipe(self):
        pid_file = os.path.join(self.tmp, "escaped.pid")
        prelude = (
            "import subprocess, sys\n"
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'],"
            " start_new_session=True)\n"
            "open(%r, 'w').write(str(child.pid))\n" % pid_file
        ).encode()

        def reap():
            try:
                with open(pid_file) as handle:
                    os.kill(int(handle.read()), 9)
            except (OSError, ValueError):
                pass

        self.addCleanup(reap)
        started = time.monotonic()
        outcome = run.run_tests(shipped_task(1), prelude + shipped_source(1, "fixed.py"), timeout=5)
        self.assertEqual(outcome.status, "pass")
        self.assertLess(time.monotonic() - started, 6)

    def test_syntax_error(self):
        outcome = run.run_tests(shipped_task(1), b"def moving_sums(values, k)\n    return []\n")
        self.assertEqual(outcome.status, "error")
        self.assertIn("SyntaxError", outcome.detail)
        proc = cli("grade", "1", self.candidate("def f(:\n"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("ERROR", proc.stdout)
        self.assertNotIn("Traceback", proc.stdout + proc.stderr)

    def test_missing_function(self):
        outcome = run.run_tests(shipped_task(1), b"x = 1\n")
        self.assertEqual(outcome.status, "error")
        self.assertIn("moving_sums", outcome.detail)

    def test_odd_source_bytes(self):
        for source in (b"\xff\xfe\x00garbage", b"x = 1\x00\n", b"", b"# only a comment\n"):
            outcome = run.run_tests(shipped_task(1), source)
            self.assertFalse(outcome.ok, source)
            self.assertIn(outcome.status, ("error", "crash"), source)

    def test_sys_exit_on_import(self):
        outcome = run.run_tests(shipped_task(1), b"import sys\nsys.exit(0)\n")
        self.assertEqual(outcome.status, "error")
        self.assertFalse(outcome.ok)

    def test_sys_exit_in_function(self):
        source = b"import sys\n\ndef moving_sums(values, k):\n    sys.exit(0)\n"
        outcome = run.run_tests(shipped_task(1), source)
        self.assertEqual(outcome.status, "fail")
        self.assertEqual(outcome.passed, 0)

    def test_os_exit(self):
        outcome = run.run_tests(shipped_task(1), b"import os\nos._exit(0)\n")
        self.assertEqual(outcome.status, "crash")
        self.assertFalse(outcome.ok)

    def test_killed_by_signal(self):
        outcome = run.run_tests(shipped_task(1), b"import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n"
                                if POSIX else b"import os\nos._exit(3)\n")
        self.assertEqual(outcome.status, "crash")

    def test_infinite_recursion(self):
        source = b"def moving_sums(values, k):\n    return moving_sums(values, k)\n"
        outcome = run.run_tests(shipped_task(1), source)
        self.assertEqual(outcome.status, "fail")
        self.assertEqual(outcome.passed, 0)

    def test_non_daemon_thread(self):
        source = b"import threading, time\nthreading.Thread(target=time.sleep, args=(60,)).start()\n"
        source += shipped_source(1, "fixed.py")
        started = time.monotonic()
        outcome = run.run_tests(shipped_task(1), source, timeout=5)
        self.assertEqual(outcome.status, "pass")
        self.assertLess(time.monotonic() - started, 4)

    def test_fake_pass_by_printing(self):
        source = b"print('{\"tests\": [{\"name\": \"x\", \"status\": \"pass\"}]}')\nimport os\nos._exit(0)\n"
        self.assertFalse(run.run_tests(shipped_task(1), source).ok)

    def test_terminal_escapes(self):
        source = b"print('\\x1b[31mRED\\x1b]0;title\\x07')\nraise SystemExit\n"
        proc = cli("grade", "1", self.candidate(source), "-v")
        self.assertNotIn("\x1b", proc.stdout)
        self.assertNotIn("\x07", proc.stdout)
        self.assertEqual(run.clean("a\x1b[0mb\nc"), "a?[0mb c")

    def test_non_ascii_output(self):
        source = "print('café 日本 \U0001F600')\n".encode() + shipped_source(1, "fixed.py")
        env = dict(os.environ, PYTHONIOENCODING="ascii")
        proc = subprocess.run(
            [sys.executable, RUN_PY, "grade", "1", self.candidate(source), "-v"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn(b"Traceback", proc.stderr)

    def test_temp_dirs_removed(self):
        before = leftover_temp_dirs()
        source = b"open('junk.txt', 'w').write('x' * 1000)\n" + shipped_source(1, "fixed.py")
        self.assertTrue(run.run_tests(shipped_task(1), source).ok)
        run.run_tests(shipped_task(1), b"while True:\n    pass\n", timeout=1)
        self.assertEqual(leftover_temp_dirs(), before)

    def test_env_not_passed(self):
        os.environ["BUGHUNT_SECRET_FOR_TEST"] = "hunter2"
        self.addCleanup(os.environ.pop, "BUGHUNT_SECRET_FOR_TEST", None)
        source = (
            b"import os\n"
            b"assert 'BUGHUNT_SECRET_FOR_TEST' not in os.environ\n"
        ) + shipped_source(1, "fixed.py")
        self.assertTrue(run.run_tests(shipped_task(1), source).ok)

    @unittest.skipUnless(sys.platform.startswith("linux"), "memory limit is checked on Linux only")
    def test_memory_bomb(self):
        source = b"x = bytearray(10 ** 11)\n" + shipped_source(1, "fixed.py")
        outcome = run.run_tests(shipped_task(1), source, timeout=5)
        self.assertFalse(outcome.ok)

    def test_stdin_empty(self):
        source = b"import sys\nassert sys.stdin.read() == ''\n" + shipped_source(1, "fixed.py")
        self.assertTrue(run.run_tests(shipped_task(1), source, timeout=5).ok)

    def test_fake_stdlib_in_cwd(self):
        for name in ("unittest.py", "json.py", "doctest.py", "importlib.py"):
            write(os.path.join(self.tmp, name), "print('HIJACKED')\nraise SystemExit(7)\n")
        proc = cli("grade", "1", shipped_task(1).file("fixed.py"), "-v", cwd=self.tmp)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertNotIn("HIJACKED", proc.stdout + proc.stderr)

    def test_file_errors(self):
        missing = cli("grade", "1", os.path.join(self.tmp, "nope.py"))
        self.assertEqual(missing.returncode, 2)
        self.assertIn("no such file", missing.stderr)
        directory = cli("grade", "1", self.tmp)
        self.assertEqual(directory.returncode, 2)
        self.assertIn("is a directory", directory.stderr)
        big = self.candidate(b"#" * (run.MAX_SOURCE_BYTES + 1), "big.py")
        too_large = cli("grade", "1", big)
        self.assertEqual(too_large.returncode, 2)
        self.assertIn("too large", too_large.stderr)
        for proc in (missing, directory, too_large):
            self.assertNotIn("Traceback", proc.stderr)

    def test_grade_unknown_task(self):
        path = self.candidate("x = 1\n")
        for ident in ("99", "../01", "/etc/passwd"):
            proc = cli("grade", ident, path)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("unknown task id", proc.stderr)

    def test_resolve_task_odd_ids(self):
        tasks = run.discover_tasks(TASKS_DIR)
        for ident in ("\x00", "../", "01\n02", "0" * 100, "٣"):
            with self.assertRaises(run.RunnerError):
                run.resolve_task(tasks, ident)
        self.assertEqual(run.resolve_task(tasks, " 7 ").number, 7)


class GradeDirTest(TempDirCase):
    def test_mixed_directory(self):
        solutions = os.path.join(self.tmp, "solutions")
        os.mkdir(solutions)
        write(os.path.join(solutions, "01.py"), shipped_source(1, "fixed.py").decode(), "w")
        write(os.path.join(solutions, "02-mutable-default-tags.py"), shipped_source(2, "buggy.py").decode(), "w")
        write(os.path.join(solutions, "04.py"), "while True:\n    pass\n", "w")
        write(os.path.join(solutions, "05.py"), shipped_source(5, "fixed.py").decode(), "w")
        write(os.path.join(solutions, "05-fee-rounding.py"), shipped_source(5, "fixed.py").decode(), "w")
        write(os.path.join(solutions, "notes.txt"), "hello", "w")
        write(os.path.join(solutions, "unrelated.py"), "x = 1\n", "w")
        os.mkdir(os.path.join(solutions, "06.py"))
        if POSIX:
            os.symlink(shipped_task(3).file("fixed.py"), os.path.join(solutions, "03.py"))
        proc = cli("grade-dir", solutions, "--timeout", "2")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rows = {line.split()[0]: line for line in proc.stdout.splitlines() if re.match(r"^\d\d ", line)}
        self.assertIn("PASS", rows["01"])
        self.assertIn("FAIL", rows["02"])
        self.assertIn("TIMEOUT", rows["04"])
        self.assertIn("AMBIGUOUS", rows["05"])
        self.assertIn("MISSING", rows["06"])
        self.assertIn("MISSING", rows["03"])
        self.assertIn("Score: 1/%d tasks solved" % len(run.discover_tasks(TASKS_DIR)), proc.stdout)
        self.assertIn("notes.txt", proc.stdout)
        self.assertIn("unrelated.py", proc.stdout)
        self.assertNotIn("Traceback", proc.stdout + proc.stderr)

    def test_empty_directory(self):
        proc = cli("grade-dir", self.tmp)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Score: 0/", proc.stdout)

    def test_bad_directory(self):
        for path in (os.path.join(self.tmp, "nope"), os.path.join(self.tmp, "file.txt")):
            write(os.path.join(self.tmp, "file.txt"), "x")
            proc = cli("grade-dir", path)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not a directory", proc.stderr)

    def test_oversized_file(self):
        write(os.path.join(self.tmp, "01.py"), "#" * (run.MAX_SOURCE_BYTES + 1))
        proc = cli("grade-dir", self.tmp)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("too large", proc.stdout)

    def test_escapes_in_file_names(self):
        write(os.path.join(self.tmp, "x\x1b[31m.py"), "x = 1\n")
        write(os.path.join(self.tmp, "01\x07.py"), "x = 1\n")
        proc = cli("grade-dir", self.tmp)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("\x1b", proc.stdout)
        self.assertNotIn("\x07", proc.stdout)

    def test_many_stray_files(self):
        for n in range(30):
            write(os.path.join(self.tmp, "stray%d.txt" % n), "x")
        proc = cli("grade-dir", self.tmp)
        self.assertIn("ignored 30 entries", proc.stdout)
        self.assertIn("and 10 more", proc.stdout)


class SelfcheckTest(TempDirCase):
    def check(self, **overrides):
        tasks_dir = os.path.join(self.tmp, "tasks")
        make_task(tasks_dir, **overrides)
        rows = run.selfcheck(run.discover_tasks(tasks_dir), timeout=3)
        return rows[0]

    def test_good_task(self):
        row = self.check()
        self.assertEqual(row.violations, [])
        self.assertEqual(row.example, "ok")

    def test_broken_fixed(self):
        row = self.check(fixed=BUGGY)
        self.assertTrue(any("fixed.py does not pass" in v for v in row.violations), row.violations)

    def test_broken_fixed_cli(self):
        tasks_dir = os.path.join(self.tmp, "tasks")
        make_task(tasks_dir, fixed=BUGGY)
        proc = cli("--tasks-dir", tasks_dir, "selfcheck", "--timeout", "5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("VIOLATION", proc.stdout)
        self.assertIn("1 with violations", proc.stdout)

    def test_fixed_crashes(self):
        row = self.check(fixed=HEADER + "raise RuntimeError('boom')\n")
        self.assertTrue(any("fixed.py" in v for v in row.violations), row.violations)

    def test_buggy_passes_everything(self):
        weak = TEST.replace("    def test_basic(self):\n        self.assertEqual(add(2, 3), 5)\n\n", "")
        row = self.check(test=weak)
        self.assertTrue(any("passes every test" in v for v in row.violations), row.violations)

    def test_buggy_fails_everything(self):
        strict = TEST.replace("    def test_zero(self):\n        self.assertEqual(add(0, 0), 0)\n", "")
        row = self.check(test=strict)
        self.assertTrue(any("fails every test" in v or "must pass" in v for v in row.violations), row.violations)

    def test_buggy_hangs(self):
        row = self.check(buggy=HEADER + "while True:\n    pass\n")
        self.assertTrue(any("buggy.py cannot be tested" in v for v in row.violations), row.violations)

    def test_missing_file(self):
        tasks_dir = os.path.join(self.tmp, "tasks")
        path = make_task(tasks_dir)
        os.remove(os.path.join(path, "fixed.py"))
        row = run.selfcheck(run.discover_tasks(tasks_dir), timeout=5)[0]
        self.assertTrue(any("missing file" in v for v in row.violations), row.violations)

    def test_bad_meta(self):
        for meta in ({"category": "x", "difficulty": 4, "summary": "s"},
                     {"category": "", "difficulty": 1, "summary": "s"},
                     {"category": "x", "difficulty": True, "summary": "s"},
                     {"category": "x", "difficulty": 1}):
            row = self.check(meta=meta)
            self.assertTrue(any("must be" in v for v in row.violations), (meta, row.violations))

    def test_example_passes_on_buggy(self):
        spec = SPEC.replace(">>> add(2, 3)\n5", ">>> add(0, 0)\n0")
        row = self.check(spec=spec)
        self.assertTrue(any("does not show the failure" in v for v in row.violations), row.violations)

    def test_example_fails_on_fixed(self):
        row = self.check(spec=SPEC.replace("\n5\n", "\n6\n"))
        self.assertTrue(any("example fails on fixed.py" in v for v in row.violations), row.violations)

    def test_no_example(self):
        row = self.check(spec="# Add\n\nNo example here.\n")
        self.assertTrue(any("example" in v for v in row.violations), row.violations)

    def test_buggy_too_short(self):
        row = self.check(buggy="def add(a, b):\n    return a - b\n")
        self.assertTrue(any("lines" in v for v in row.violations), row.violations)

    def test_identical_buggy_and_fixed(self):
        row = self.check(fixed=BUGGY)
        self.assertTrue(any("identical" in v for v in row.violations), row.violations)

    def test_nondeterministic_tests(self):
        for extra in ("import time\n\n\ndef nap():\n    time.sleep(0)\n",
                      "import datetime\n\n\ndef today():\n    return datetime.datetime.now()\n",
                      "import random\n\n\ndef roll():\n    return random.random()\n"):
            row = self.check(test=TEST + "\n\n" + extra)
            self.assertTrue(any("deterministic" in v or "random" in v for v in row.violations), (extra, row.violations))

    def test_repeat_finds_flaky_tests(self):
        flaky = TEST + (
            "\n\nclass Flaky(unittest.TestCase):\n"
            "    def test_hash_order(self):\n"
            "        self.assertEqual(list({'alpha', 'beta', 'gamma', 'delta'})[0], 'alpha')\n"
        )
        tasks_dir = os.path.join(self.tmp, "tasks")
        make_task(tasks_dir, test=flaky)
        task = run.discover_tasks(tasks_dir)[0]
        found = False
        for _ in range(4):
            row = run.check_task(task, timeout=5, repeat=6)
            if any("not deterministic" in v for v in row.violations):
                found = True
                break
        self.assertTrue(found, "hash-order dependence was never detected")

    def test_duplicate_numbers(self):
        tasks_dir = os.path.join(self.tmp, "tasks")
        make_task(tasks_dir, name="01-a")
        make_task(tasks_dir, name="01-b")
        proc = cli("--tasks-dir", tasks_dir, "list")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("share the number", proc.stderr)


class HelperTest(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(run.clean("ok"), "ok")
        self.assertEqual(run.clean("a\tb\nc"), "a b c")
        self.assertEqual(run.clean("\x00\x1b"), "??")
        self.assertEqual(len(run.clean("x" * 1000)), 300)
        self.assertTrue(run.clean("x" * 1000).endswith("..."))

    def test_format_table(self):
        text = run.format_table(["A", "BB"], [["1", "2"], ["333", "4"]])
        self.assertEqual(text.splitlines()[0], "A    BB")
        self.assertEqual(text.splitlines()[-1], "333  4")


if __name__ == "__main__":
    unittest.main()
