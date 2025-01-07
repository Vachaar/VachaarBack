from time import time
from typing import Any, Dict
from unittest.case import TestCase
from unittest.runner import TextTestResult, TextTestRunner

from django.conf import settings
from django.test.runner import DiscoverRunner
from termcolor import colored


class TimedTextTestResult(TextTestResult):
    """
    Provides a custom test runner to track and display the execution time of test cases.
    The `TimedTextTestResult` class extends `TextTestResult` to:
    - Record execution times for each test case.
    - Display results with execution durations and statuses (e.g., "OK", "FAIL", "ERROR").
    - Summarize execution times, optionally sorted by duration.
    Usage:
    Use `TimedTextTestResult` as the `resultclass` in a custom `unittest.TextTestRunner`.
    """

    def __init__(
        self,
        *args: Any,
        sort_descending: bool = False,
        show_all: bool = True,
        **kwargs: Any,
    ) -> None:
        super(TimedTextTestResult, self).__init__(*args, **kwargs)
        self.sort_descending = sort_descending
        self.clocks: Dict[TestCase, float] = {}
        self.exec_times: Dict[TestCase, float] = {}
        self.showAll: bool = show_all
        self.dots: bool = True

    def startTest(self, test: TestCase) -> None:
        self.clocks[test] = time()
        super().startTest(test)

    def addSuccess(self, test: TestCase) -> None:
        self.exec_times[test] = time() - self.clocks[test]
        super(TextTestResult, self).addSuccess(test)
        self._handleResult(
            message=f"OK ({self.exec_times[test]:6f}s)",
            color="green",
            short=".",
        )

    def addError(self, test: TestCase, err: Any) -> None:
        super(TextTestResult, self).addError(test, err)
        self._handleResult(message="ERROR", color="red", short="E")

    def addFailure(self, test: TestCase, err: Any) -> None:
        super(TextTestResult, self).addFailure(test, err)
        self._handleResult(message="FAIL", color="red", short="F")

    def _handleResult(self, message: str, color: str, short: str) -> None:
        """
        Handles the consistent logic for displaying the result of a test case.
        Depending on `showAll` and `dots`, it prints the appropriate message.
        """
        if self.showAll:
            self.stream.writeln(colored(message, color))
        elif self.dots:
            self.stream.write(short)
            self.stream.flush()

    def stopTestRun(self) -> None:
        self.stream.writeln(f'\n{"-" * 26} EXECUTION TIMES {"-" * 26}')
        sorted_exec_times = sorted(
            self.exec_times.items(),
            key=lambda x: x[1],
            reverse=self.sort_descending,
        )
        for test, run_time in sorted_exec_times:
            self.stream.writeln(f"({run_time:6f}s) {str(test)}")


class TimedTextTestRunner(TextTestRunner):
    resultclass = TimedTextTestResult

    def __init__(
        self,
        *args: Any,
        sort_descending: bool = False,
        show_all: bool = False,
        **kwargs: Any,
    ) -> None:
        self.sort_descending = sort_descending
        self.showAll = show_all
        super().__init__(*args, **kwargs)

    def _makeResult(self):
        return self.resultclass(
            self.stream,
            self.descriptions,
            self.verbosity,
            sort_descending=self.sort_descending,
            show_all=self.showAll,
        )


class SimpleTimedTestRunner(DiscoverRunner):
    test_runner = TimedTextTestRunner

    def __init__(
        self,
        *args: Any,
        sort_descending: bool = False,
        show_all: bool = True,
        **kwargs: Any,
    ) -> None:
        self.sort_descending = sort_descending
        self.showAll = show_all
        super().__init__(*args, **kwargs)

    def get_test_runner_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_test_runner_kwargs()
        kwargs["sort_descending"] = getattr(
            settings, "TEST_RUNNER_SORT_DESCENDING", True
        )
        kwargs["show_all"] = getattr(settings, "TEST_RUNNER_SHOW_ALL", True)
        return kwargs
