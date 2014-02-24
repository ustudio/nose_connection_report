import mock

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

        plugin.add_test_connections(test1, [])

        plugin.begin()

        plugin.add_test_connections(test2, [])

        plugin.report(output)

        self.assertEqual("Test2\n", output.getvalue())
