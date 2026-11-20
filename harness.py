# Runs inside the child process. run.py starts it as
#   python -I -B harness.py tests|examples WORKDIR RESULT [TASK_MD]
# Results go to the RESULT file, never stdout, so the candidate can't fake
# one by printing.

import json
import os
import sys
import unittest

MAX_MESSAGE = 300


def apply_limits():
    try:
        import resource
    except ImportError:
        return
    limits = [
        ("RLIMIT_CPU", 15),
        ("RLIMIT_CORE", 0),
        ("RLIMIT_FSIZE", 8 * 1024 * 1024),
        ("RLIMIT_AS", 2 * 1024 * 1024 * 1024),
    ]
    for name, value in limits:
        try:
            limit = getattr(resource, name)
            soft, hard = resource.getrlimit(limit)
            if hard != resource.RLIM_INFINITY and hard < value:
                value = hard
            resource.setrlimit(limit, (value, hard))
        except (AttributeError, ValueError, OSError):
            pass  # best effort


def short(text):
    text = " ".join(str(text).split())
    if len(text) > MAX_MESSAGE:
        text = text[: MAX_MESSAGE - 3] + "..."
    return text


def describe(exc_type, exc_value):
    try:
        lines = str(exc_value).splitlines()
    except BaseException:  # candidate exceptions can have a broken __str__
        lines = []
    return short("%s: %s" % (exc_type.__name__, lines[0] if lines else ""))


class Recorder(unittest.TestResult):
    # one status per test: pass, fail, error or skip

    def __init__(self):
        super().__init__()
        self.results = {}

    @staticmethod
    def _name(test):
        parts = test.id().split(".")
        return ".".join(parts[1:]) if len(parts) > 1 else parts[0]

    def _put(self, test, status, message=""):
        name = self._name(test)
        old = self.results.get(name)
        if old is not None and old[0] in ("fail", "error") and status == "pass":
            return
        self.results[name] = (status, message)

    def startTest(self, test):
        super().startTest(test)
        self.results.setdefault(self._name(test), ("pass", ""))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._put(test, "fail", describe(err[0], err[1]))

    def addError(self, test, err):
        super().addError(test, err)
        self._put(test, "error", describe(err[0], err[1]))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._put(test, "skip", short(reason))

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self._put(test, "fail", "unexpected success")

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            status = "fail" if issubclass(err[0], test.failureException) else "error"
            self._put(test, status, "%s: %s" % (subtest, describe(err[0], err[1])))


def run_tests():
    import importlib

    module = importlib.import_module("test_task")
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    if suite.countTestCases() == 0:
        return {"load_error": "no tests found in test_task.py"}
    recorder = Recorder()
    suite.run(recorder)
    tests = [
        {"name": name, "status": status, "message": message}
        for name, (status, message) in recorder.results.items()
    ]
    return {"tests": tests}


def run_examples(task_md):
    import doctest
    import importlib
    import re

    with open(task_md, encoding="utf-8") as handle:
        text = handle.read()
    blocks = re.findall(r"```python\n(.*?)```", text, re.S)
    source = "\n".join(block for block in blocks if ">>>" in block)
    solution = importlib.import_module("solution")
    namespace = {k: v for k, v in vars(solution).items() if not k.startswith("__")}
    test = doctest.DocTestParser().get_doctest(source, namespace, "task.md", task_md, 0)
    report = []
    runner = doctest.DocTestRunner(verbose=False)
    outcome = runner.run(test, out=report.append, clear_globs=False)
    first = short(report[0]) if report else ""
    return {"attempted": outcome.attempted, "failed": outcome.failed, "message": first}


def load_error(exc_type, exc_value):
    message = describe(exc_type, exc_value)
    if issubclass(exc_type, SyntaxError):
        line = getattr(exc_value, "lineno", None)
        if line:
            message += " (line %s)" % line
    return {"load_error": message}


def main(argv):
    if len(argv) < 4:
        return 2
    mode, workdir, result_path = argv[1], argv[2], argv[3]
    apply_limits()
    sys.path.insert(0, workdir)
    try:
        if mode == "tests":
            result = run_tests()
        else:
            result = run_examples(argv[4])
    except BaseException as exc:  # includes SystemExit from the candidate
        result = load_error(type(exc), exc)
    try:
        with open(result_path, "w", encoding="utf-8") as handle:
            json.dump(result, handle)
    except BaseException:
        pass
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except BaseException:
        pass
    # skip atexit handlers and non-daemon threads the candidate may have left
    os._exit(0)


if __name__ == "__main__":
    main(sys.argv)
