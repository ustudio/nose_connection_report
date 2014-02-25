5Running tests in a subprocess
=============================

The plugin runs each test in a separate process.

XXX This doctest doesn't actually test that separate processes are
used!


    >>> import os.path, sys

    >>> import nose.plugins

    >>> import nose_connection_report

    >>> directory_with_tests = os.path.join(os.path.dirname(__file__),
    ...                                     "test-support")
    >>> plugins = [nose_connection_report.ConnectionReportPlugin(),
    ...            nose_connection_report.ProcessIsolationReporterPlugin()]


Successful run:

    >>> nose.plugins.plugintest.run(
    ...     argv=["nosetests", "-v", "--with-connection-report",
    ...           os.path.join(directory_with_tests, "passing")],
    ...     plugins=plugins)
    ...     # doctest: +REPORT_NDIFF
    passing_tests.passing_test_1 ... ok
    passing_tests.passing_test_2 ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK


Connection report:

    >>> nose.plugins.plugintest.run(
    ...     argv=["nosetests", "-v", "--with-connection-report",
    ...           os.path.join(directory_with_tests, "connecting")],
    ...     plugins=plugins)
    ...     # doctest: +REPORT_NDIFF
    connecting_tests.connecting_test_1 ... ok
    connecting_tests.connecting_test_2 ... ok
    <BLANKLINE>
    connecting_tests.connecting_test_1
        127.0.0.1:8080
    connecting_tests.connecting_test_2
        127.0.0.1:8080
        127.0.0.1:8000
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK


Failing run:

    >>> py = os.path.join(directory_with_tests, "failing", "failing_tests.py")
    >>> testname = py + ":failing_test"
    >>> nose.plugins.plugintest.run(
    ...     argv=["nosetests", "-v", "--with-connection-report",
    ...           testname],
    ...     plugins=plugins)
    ...     # doctest: +REPORT_NDIFF
    failing_tests.failing_test ... FAIL
    <BLANKLINE>
    ======================================================================
    FAIL: failing_tests.failing_test
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (failures=1)


Erroring run:

    >>> py = os.path.join(directory_with_tests, "failing", "failing_tests.py")
    >>> testname = py + ":erroring_test"
    >>> nose.plugins.plugintest.run(
    ...     argv=["nosetests", "-v", "--with-connection-report",
    ...           testname],
    ...     plugins=plugins)
    ...     # doctest: +REPORT_NDIFF
    failing_tests.erroring_test ... ERROR
    <BLANKLINE>
    ======================================================================
    ERROR: failing_tests.erroring_test
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Exception
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (errors=1)


Multiple failing tests:

    >>> nose.plugins.plugintest.run(
    ...     argv=["nosetests", "-v", "--with-connection-report",
    ...           os.path.join(directory_with_tests, "failing")],
    ...     plugins=plugins)
    ...     # doctest: +REPORT_NDIFF
    failing_tests.erroring_test ... ERROR
    failing_tests.failing_test ... FAIL
    <BLANKLINE>
    ======================================================================
    ERROR: failing_tests.erroring_test
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Exception
    <BLANKLINE>
    ======================================================================
    FAIL: failing_tests.failing_test
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    FAILED (errors=1, failures=1)
