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
        plugin = mock.MagicMock()

        test = mock.MagicMock()
        test.address.return_value = ("foo.py", "tests", "TestFoo.test_something")

        base_command = os.path.abspath(sys.argv[0])
        cwd = os.getcwd()

        mock_popen = mock_popen_class.return_value
        mock_popen.stdout.read.return_value = ""

        proxy = SubprocessTestProxy(plugin, test)

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

    @mock.patch("subprocess.Popen")
    def test_parses_strace_output_when_done(self, mock_popen_class):
        mock_popen = mock_popen_class.return_value
        mock_popen.stdout.read.return_value = ''

        plugin = mock.MagicMock()

        test = mock.MagicMock()
        test.address.return_value = ("foo.py", "tests", "TestFoo.test_something")

        proxy = SubprocessTestProxy(plugin, test)

        # This is a goofy way to test this, but I don't feel like
        # pulling apart the existing IPC parsing from the Popen calls
        with mock.patch.object(proxy, "parse_strace") as mock_parse_strace:
            proxy(None)

            mock_parse_strace.assert_called_with(mock_popen.stderr)

    def test_parses_strace_for_connect_calls(self):
        strace_output = """connect(3, {sa_family=AF_FILE, path="/var/run/nscd/socket"}, 110) = -1 ENOENT (No such file or directory)
connect(3, {sa_family=AF_INET, sin_port=htons(8080), sin_addr=inet_addr("127.0.0.1")}, 16) = -1 ECONNREFUSED (Connection refused)
connect(3, {sa_family=AF_INET, sin_port=htons(8000), sin_addr=inet_addr("127.0.0.1")}, 16) = -1 ECONNREFUSED (Connection refused)
"""

        plugin = mock.MagicMock()
        test = mock.MagicMock()

        proxy = SubprocessTestProxy(plugin, test)

        proxy.parse_strace(strace_output.split("\n"))

        plugin.add_test_connections.assert_called_with(
            test,
            [
                {
                    "host": "127.0.0.1",
                    "port": 8080,
                },
                {
                    "host": "127.0.0.1",
                    "port": 8000
                }
            ]
        )
