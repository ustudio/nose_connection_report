import mock
import os
import os.path

from nose_connection_report import SubprocessTestProxy

import subprocess
import sys
import unittest


class TestSubprocessTestProxy(unittest.TestCase):
    @mock.patch("subprocess.Popen")
    def test_calls_test_inside_strace(self, mock_popen_class):
        test = mock.MagicMock()
        test.address.return_value = ("foo.py", "tests", "TestFoo.test_something")

        base_command = os.path.abspath(sys.argv[0])
        cwd = os.getcwd()

        mock_popen = mock_popen_class.return_value
        mock_popen.stdout.read.return_value = ""

        proxy = SubprocessTestProxy(test)

        proxy(None)

        mock_popen_class.assert_called_with(
            [
                "strace",
                "-e", "trace=connect",
                base_command,
                "--with-process-isolation-reporter",
                "foo.py:TestFoo.test_something"
            ],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
