import mock
from optparse import OptionParser

from nose_connection_report import ConnectionReportPlugin

from StringIO import StringIO
import unittest


class TestConnectionReportPlugin(unittest.TestCase):
    @mock.patch("nose_connection_report.SubprocessTestProxy")
    def test_prepares_proxy_with_self(self, mock_proxy_class):
        test = mock.MagicMock()
        plugin = ConnectionReportPlugin()

        prepared = plugin.prepareTestCase(test)

        mock_proxy_class.assert_called_with(plugin, test)

        self.assertEqual(mock_proxy_class.return_value, prepared)

    def test_reports_connections_made(self):
        output = StringIO()

        test1 = mock.MagicMock()
        test2 = mock.MagicMock()

        test1.id.return_value = "Test1"
        test2.id.return_value = "Test2"

        plugin = ConnectionReportPlugin()

        plugin.add_test_connections(
            test1,
            [
                {
                    "host": "127.0.0.1",
                    "port": 1234
                },
                {
                    "host": "127.0.0.1",
                    "port": 4321
                }
            ]
        )

        plugin.add_test_connections(
            test2,
            [
                {
                    "host": "127.0.0.1",
                    "port": 8080
                }
            ]
        )

        plugin.report(output)

        self.assertEqual(
            """Test1
    127.0.0.1:1234
    127.0.0.1:4321
Test2
    127.0.0.1:8080
""",
            output.getvalue())

    def test_resets_itself_in_begin(self):
        output = StringIO()

        test1 = mock.MagicMock()
        test2 = mock.MagicMock()

        test1.id.return_value = "Test1"
        test2.id.return_value = "Test2"

        plugin = ConnectionReportPlugin()

        plugin.begin()

        plugin.add_test_connections(test1, [{
            "host": "127.0.0.1",
            "port": 1234
        }])

        plugin.begin()

        plugin.add_test_connections(test2, [{
            "host": "127.0.0.1",
            "port": 1234
        }])

        plugin.report(output)

        self.assertEqual(
            """Test2
    127.0.0.1:1234
""",
            output.getvalue())

    def test_tests_without_connections_are_not_reported(self):
        output = StringIO()

        test1 = mock.MagicMock()
        test2 = mock.MagicMock()

        test1.id.return_value = "Test1"
        test2.id.return_value = "Test2"

        plugin = ConnectionReportPlugin()

        plugin.begin()

        plugin.add_test_connections(test1, [{
            "host": "127.0.0.1",
            "port": 1234
        }])

        plugin.add_test_connections(test2, [])

        plugin.report(output)

        self.assertEqual(
            """Test1
    127.0.0.1:1234
""",
            output.getvalue())

    def test_doesnt_filter_anything_without_ignores(self):
        output = StringIO()

        test1 = mock.MagicMock()
        test2 = mock.MagicMock()

        test1.id.return_value = "Test1"
        test2.id.return_value = "Test2"

        parser = OptionParser()

        plugin = ConnectionReportPlugin()

        plugin.options(parser, {})

        options, _ = parser.parse_args([
            "--with-connection-report"
        ])

        plugin.configure(options, None)

        plugin.begin()

        plugin.add_test_connections(
            test1,
            [
                {
                    "host": "127.0.0.1",
                    "port": 1234
                }
            ]
        )

        plugin.add_test_connections(
            test2,
            [
                {
                    "host": "127.0.0.1",
                    "port": 4321
                }
            ]
        )

        plugin.report(output)

        self.assertEqual(
            """Test1
    127.0.0.1:1234
Test2
    127.0.0.1:4321
""",
            output.getvalue())

    def test_requested_connections_are_filtered_out(self):
        output = StringIO()

        test1 = mock.MagicMock()
        test2 = mock.MagicMock()

        test1.id.return_value = "Test1"
        test2.id.return_value = "Test2"

        parser = OptionParser()

        plugin = ConnectionReportPlugin()

        plugin.options(parser, {})

        options, _ = parser.parse_args([
            "--with-connection-report",
            "--connection-report-ignore",
            "127.0.0.1:8080",
            "--connection-report-ignore",
            "127.0.0.1:8000"
        ])

        plugin.configure(options, None)

        plugin.begin()

        plugin.add_test_connections(
            test1,
            [
                {
                    "host": "127.0.0.1",
                    "port": 1234
                },
                {
                    "host": "127.0.0.1",
                    "port": 8000
                }
            ]
        )

        plugin.add_test_connections(
            test2,
            [
                {
                    "host": "127.0.0.1",
                    "port": 8080
                },
                {
                    "host": "127.0.0.1",
                    "port": 4321
                }
            ]
        )

        plugin.report(output)

        self.assertEqual(
            """Test1
    127.0.0.1:1234
Test2
    127.0.0.1:4321
""",
            output.getvalue())
